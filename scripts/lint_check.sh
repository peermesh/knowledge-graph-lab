#!/bin/bash

##
# Local Code Quality & Linting Script
# 
# This script runs all code quality checks locally before pushing to GitHub.
# It mirrors the GitHub Actions workflow for consistent results.
#
# Usage:
#   ./scripts/lint_check.sh            # Run all checks
#   ./scripts/lint_check.sh python     # Run only Python checks
#   ./scripts/lint_check.sh javascript # Run only JavaScript checks
#   ./scripts/lint_check.sh --fix       # Run checks and auto-fix where possible
#
# Author: Knowledge Graph Lab Quality Framework
# Created: 2025-09-08
##

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
WARNINGS=0

# Configuration
AUTO_FIX=false
CHECK_TYPE="all"
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --fix)
      AUTO_FIX=true
      shift
      ;;
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    python|javascript|markdown|docker|security|tests)
      CHECK_TYPE="$1"
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [OPTIONS] [CHECK_TYPE]"
      echo ""
      echo "Options:"
      echo "  --fix        Auto-fix issues where possible"
      echo "  --verbose    Show detailed output"
      echo "  --help       Show this help message"
      echo ""
      echo "Check types:"
      echo "  python       Python code linting and formatting"
      echo "  javascript   JavaScript/TypeScript linting and formatting"
      echo "  markdown     Markdown documentation linting"
      echo "  docker       Dockerfile linting"
      echo "  security     Security vulnerability scanning"
      echo "  tests        Test template validation"
      echo "  all          Run all checks (default)"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    ((PASSED_CHECKS++))
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    ((WARNINGS++))
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

run_check() {
    local check_name="$1"
    local command="$2"
    local fix_command="${3:-}"
    
    ((TOTAL_CHECKS++))
    
    log_info "Running $check_name..."
    
    if $VERBOSE; then
        echo "Command: $command"
    fi
    
    if eval "$command"; then
        log_success "$check_name passed"
        return 0
    else
        if [[ $AUTO_FIX == true && -n "$fix_command" ]]; then
            log_info "Attempting to auto-fix $check_name..."
            if eval "$fix_command"; then
                log_warning "$check_name issues auto-fixed"
                return 0
            else
                log_error "$check_name failed and could not be auto-fixed"
                return 1
            fi
        else
            log_error "$check_name failed"
            return 1
        fi
    fi
}

# Check if required tools are installed
check_dependencies() {
    local missing_deps=()
    
    if [[ $CHECK_TYPE == "all" || $CHECK_TYPE == "python" ]]; then
        command -v python3 >/dev/null || missing_deps+=("python3")
        command -v pip >/dev/null || missing_deps+=("pip")
    fi
    
    if [[ $CHECK_TYPE == "all" || $CHECK_TYPE == "javascript" ]]; then
        if [[ -d "modules/module-4-frontend" ]]; then
            command -v node >/dev/null || missing_deps+=("node")
            command -v npm >/dev/null || missing_deps+=("npm")
        fi
    fi
    
    if [[ $CHECK_TYPE == "all" || $CHECK_TYPE == "docker" ]]; then
        command -v docker >/dev/null || missing_deps+=("docker")
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies and try again"
        exit 1
    fi
}

# Python linting checks
run_python_checks() {
    log_info "🐍 Running Python code quality checks..."
    
    # Check if Python modules exist
    local python_modules=(
        "modules/module-1-ingestion"
        "modules/module-2-knowledge-graph"
        "modules/module-3-reasoning"
    )
    
    local has_python_code=false
    for module in "${python_modules[@]}"; do
        if [[ -d "$module" ]] && find "$module" -name "*.py" | head -1 | grep -q .; then
            has_python_code=true
            break
        fi
    done
    
    if ! $has_python_code; then
        log_info "No Python code found, skipping Python checks"
        return 0
    fi
    
    # Install Python linting tools if not available
    if ! command -v flake8 >/dev/null || ! command -v black >/dev/null || ! command -v isort >/dev/null; then
        log_info "Installing Python linting tools..."
        pip install --quiet flake8 black isort mypy bandit pytest || {
            log_error "Failed to install Python linting tools"
            return 1
        }
    fi
    
    # Find all Python files in modules
    local python_files=$(find modules/ -name "*.py" 2>/dev/null || true)
    
    if [[ -z "$python_files" ]]; then
        log_info "No Python files found in modules/"
        return 0
    fi
    
    # Flake8 linting
    run_check "Python syntax and style (flake8)" \
        "flake8 modules/ --count --select=E9,F63,F7,F82 --show-source --statistics && flake8 modules/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics" \
        ""
    
    # Black formatting
    run_check "Python code formatting (black)" \
        "black --check --diff modules/" \
        "black modules/"
    
    # isort import sorting
    run_check "Python import sorting (isort)" \
        "isort --check-only --diff modules/" \
        "isort modules/"
    
    # MyPy type checking (warning only)
    if command -v mypy >/dev/null; then
        if mypy modules/ --ignore-missing-imports --no-strict-optional 2>/dev/null; then
            log_success "Python type checking (mypy) passed"
            ((PASSED_CHECKS++))
        else
            log_warning "Python type checking (mypy) issues found (non-blocking)"
            ((WARNINGS++))
        fi
        ((TOTAL_CHECKS++))
    fi
}

# JavaScript linting checks
run_javascript_checks() {
    log_info "🟨 Running JavaScript/TypeScript code quality checks..."
    
    local frontend_dir="modules/module-4-frontend"
    
    if [[ ! -d "$frontend_dir" ]]; then
        log_info "No frontend module found, skipping JavaScript checks"
        return 0
    fi
    
    cd "$frontend_dir"
    
    # Install dependencies if node_modules doesn't exist
    if [[ ! -d "node_modules" ]]; then
        log_info "Installing Node.js dependencies..."
        npm install --silent || {
            log_error "Failed to install Node.js dependencies"
            cd - >/dev/null
            return 1
        }
    fi
    
    # Install linting tools if not in package.json
    if ! npm list eslint >/dev/null 2>&1; then
        log_info "Installing JavaScript linting tools..."
        npm install --save-dev --silent eslint prettier @typescript-eslint/eslint-plugin @typescript-eslint/parser || {
            log_error "Failed to install JavaScript linting tools"
            cd - >/dev/null
            return 1
        }
    fi
    
    # ESLint
    run_check "JavaScript/TypeScript linting (ESLint)" \
        "npx eslint . --ext .js,.jsx,.ts,.tsx --max-warnings 0" \
        "npx eslint . --ext .js,.jsx,.ts,.tsx --fix"
    
    # Prettier formatting
    run_check "JavaScript/TypeScript formatting (Prettier)" \
        "npx prettier --check ." \
        "npx prettier --write ."
    
    # TypeScript type checking (if tsconfig.json exists)
    if [[ -f "tsconfig.json" ]]; then
        if npx tsc --noEmit 2>/dev/null; then
            log_success "TypeScript type checking passed"
            ((PASSED_CHECKS++))
        else
            log_warning "TypeScript type checking issues found (non-blocking)"
            ((WARNINGS++))
        fi
        ((TOTAL_CHECKS++))
    fi
    
    cd - >/dev/null
}

# Markdown linting checks
run_markdown_checks() {
    log_info "📝 Running Markdown documentation checks..."
    
    # Check if there are any markdown files
    local md_files=$(find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" 2>/dev/null || true)
    
    if [[ -z "$md_files" ]]; then
        log_info "No Markdown files found, skipping Markdown checks"
        return 0
    fi
    
    # Install markdownlint if not available
    if ! command -v markdownlint >/dev/null; then
        if command -v npm >/dev/null; then
            log_info "Installing markdownlint..."
            npm install -g markdownlint-cli --silent || {
                log_warning "Could not install markdownlint, skipping Markdown checks"
                return 0
            }
        else
            log_warning "npm not available, skipping Markdown checks"
            return 0
        fi
    fi
    
    # Run markdownlint
    run_check "Markdown linting (markdownlint)" \
        "markdownlint *.md modules/**/*.md docs/**/*.md || true" \
        ""
}

# Docker linting checks
run_docker_checks() {
    log_info "🐳 Running Docker linting checks..."
    
    # Find Dockerfiles
    local dockerfiles=$(find modules/ -name "Dockerfile" 2>/dev/null || true)
    
    if [[ -z "$dockerfiles" ]]; then
        log_info "No Dockerfiles found, skipping Docker checks"
        return 0
    fi
    
    # Check if hadolint is available via Docker
    if command -v docker >/dev/null; then
        for dockerfile in $dockerfiles; do
            run_check "Docker linting ($dockerfile)" \
                "docker run --rm -i hadolint/hadolint < $dockerfile" \
                ""
        done
    else
        log_warning "Docker not available, skipping Docker linting"
    fi
}

# Security scanning
run_security_checks() {
    log_info "🔒 Running security vulnerability checks..."
    
    # Python security with Bandit
    local python_files=$(find modules/ -name "*.py" 2>/dev/null || true)
    
    if [[ -n "$python_files" ]]; then
        if ! command -v bandit >/dev/null; then
            log_info "Installing Bandit for Python security scanning..."
            pip install --quiet bandit || {
                log_warning "Failed to install Bandit, skipping Python security checks"
                return 0
            }
        fi
        
        if bandit -r modules/ -f txt 2>/dev/null; then
            log_success "Python security scan (Bandit) passed"
            ((PASSED_CHECKS++))
        else
            log_warning "Python security issues found (review recommended)"
            ((WARNINGS++))
        fi
        ((TOTAL_CHECKS++))
    fi
    
    # JavaScript security (if package.json exists)
    if [[ -f "modules/module-4-frontend/package.json" ]]; then
        cd "modules/module-4-frontend"
        
        if npm audit --audit-level=high 2>/dev/null; then
            log_success "JavaScript security audit passed"
            ((PASSED_CHECKS++))
        else
            log_warning "JavaScript security vulnerabilities found"
            if $AUTO_FIX; then
                log_info "Attempting to fix JavaScript security issues..."
                npm audit fix || log_warning "Could not auto-fix all security issues"
            fi
            ((WARNINGS++))
        fi
        ((TOTAL_CHECKS++))
        
        cd - >/dev/null
    fi
}

# Test template validation
run_test_validation() {
    log_info "🧪 Running test template validation..."
    
    local test_templates=(
        "modules/module-1-ingestion/tests/test_template.py"
        "modules/module-2-knowledge-graph/tests/test_template.py"
        "modules/module-3-reasoning/tests/test_template.py"
        "modules/module-4-frontend/tests/test_template.js"
    )
    
    for template in "${test_templates[@]}"; do
        if [[ -f "$template" ]]; then
            case "$template" in
                *.py)
                    run_check "Python test template syntax ($template)" \
                        "python3 -m py_compile $template" \
                        ""
                    ;;
                *.js)
                    run_check "JavaScript test template syntax ($template)" \
                        "node -c $template" \
                        ""
                    ;;
            esac
        fi
    done
}

# Main execution
main() {
    log_info "🚀 Starting Knowledge Graph Lab code quality checks..."
    echo "Check type: $CHECK_TYPE"
    echo "Auto-fix: $AUTO_FIX"
    echo "Verbose: $VERBOSE"
    echo ""
    
    check_dependencies
    
    # Run checks based on type
    case $CHECK_TYPE in
        python)
            run_python_checks
            ;;
        javascript)
            run_javascript_checks
            ;;
        markdown)
            run_markdown_checks
            ;;
        docker)
            run_docker_checks
            ;;
        security)
            run_security_checks
            ;;
        tests)
            run_test_validation
            ;;
        all)
            run_python_checks
            run_javascript_checks
            run_markdown_checks
            run_docker_checks
            run_security_checks
            run_test_validation
            ;;
    esac
    
    # Summary report
    echo ""
    log_info "📊 Code Quality Summary:"
    echo "  Total checks: $TOTAL_CHECKS"
    echo "  Passed: $PASSED_CHECKS"
    echo "  Warnings: $WARNINGS"
    echo "  Failed: $((TOTAL_CHECKS - PASSED_CHECKS - WARNINGS))"
    echo ""
    
    if [[ $PASSED_CHECKS -eq $TOTAL_CHECKS ]]; then
        log_success "All code quality checks passed! 🎉"
        exit 0
    elif [[ $((PASSED_CHECKS + WARNINGS)) -eq $TOTAL_CHECKS ]]; then
        log_warning "All checks completed with some warnings. Review recommended."
        exit 0
    else
        log_error "Some code quality checks failed. Please fix issues before pushing."
        exit 1
    fi
}

# Run main function
main "$@"