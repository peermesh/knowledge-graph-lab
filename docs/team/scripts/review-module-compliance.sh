#!/bin/bash
#
# Module Compliance Review Script
# Purpose: Automated checks for Standalone Module Requirements compliance
# Reference: docs/modules/shared/standalone-modules/README.md
#
# Usage: ./review-module-compliance.sh [module_path]
#        ./review-module-compliance.sh all  # Review all modules
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Log functions
log_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

log_section() {
    echo ""
    echo -e "${BLUE}== $1 ==${NC}"
}

log_pass() {
    echo -e "  ${GREEN}✓${NC} $1"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

log_fail() {
    echo -e "  ${RED}✗${NC} $1"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

log_warn() {
    echo -e "  ${YELLOW}⚠${NC} $1"
}

log_info() {
    echo -e "  ${BLUE}ℹ${NC} $1"
}

# Check if module directory exists
check_module_exists() {
    local module_path=$1
    if [ ! -d "$module_path" ]; then
        echo -e "${RED}Error: Module directory not found: $module_path${NC}"
        exit 1
    fi
}

# Phase 1: Structural Review
check_file_structure() {
    local module_path=$1
    log_section "Phase 1: Structural Review"

    # Required files
    if [ -f "$module_path/Dockerfile" ]; then
        log_pass "Dockerfile exists"
    else
        log_fail "Dockerfile missing"
    fi

    # Dependencies file (Python or Node.js)
    if [ -f "$module_path/requirements.txt" ] || [ -f "$module_path/package.json" ]; then
        log_pass "Dependencies file exists (requirements.txt or package.json)"
    else
        log_fail "Dependencies file missing (requirements.txt or package.json)"
    fi

    # README
    if [ -f "$module_path/README.md" ]; then
        log_pass "README.md exists"
    else
        log_fail "README.md missing"
    fi

    # Source code structure
    if [ -d "$module_path/src" ] || [ -d "$module_path/app" ] || [ -f "$module_path/main.py" ]; then
        log_pass "Source code structure exists"
    else
        log_warn "No standard source code structure found (src/, app/, or main.py)"
    fi

    # Forbidden files check
    local forbidden_found=0
    if [ -d "$module_path/node_modules" ]; then
        log_fail "Forbidden directory found: node_modules (should be in .gitignore)"
        forbidden_found=1
    fi
    if [ -d "$module_path/__pycache__" ]; then
        log_fail "Forbidden directory found: __pycache__ (should be in .gitignore)"
        forbidden_found=1
    fi
    if [ -f "$module_path/.env" ]; then
        log_fail "Forbidden file found: .env (should be in .gitignore)"
        forbidden_found=1
    fi
    if [ $forbidden_found -eq 0 ]; then
        log_pass "No forbidden files found"
    fi
}

# Check Dockerfile compliance
check_dockerfile() {
    local module_path=$1
    log_section "Dockerfile Compliance"

    if [ ! -f "$module_path/Dockerfile" ]; then
        log_fail "Dockerfile not found - skipping Dockerfile checks"
        return
    fi

    # Check for base image
    if grep -q "^FROM python:3\.1[1-9]" "$module_path/Dockerfile" || \
       grep -q "^FROM node:1[8-9]" "$module_path/Dockerfile" || \
       grep -q "^FROM node:2[0-9]" "$module_path/Dockerfile"; then
        log_pass "Uses correct base image (Python 3.11+ or Node.js 18+)"
    else
        log_warn "Base image may not meet requirements (Python 3.11+ or Node.js 18+)"
    fi

    # Check for EXPOSE
    if grep -q "^EXPOSE" "$module_path/Dockerfile"; then
        local port=$(grep "^EXPOSE" "$module_path/Dockerfile" | awk '{print $2}' | head -1)
        log_pass "Exposes port: $port"
    else
        log_fail "No EXPOSE statement found"
    fi

    # Check for ENV usage
    if grep -q "^ENV" "$module_path/Dockerfile"; then
        log_pass "Uses environment variables"
    else
        log_warn "No environment variables defined in Dockerfile"
    fi

    # Basic syntax check
    if docker build -f "$module_path/Dockerfile" -t test-build --dry-run "$module_path" 2>/dev/null; then
        log_pass "Dockerfile syntax is valid"
    else
        log_warn "Dockerfile syntax check failed (requires Docker)"
    fi
}

# Check API compliance
check_api_compliance() {
    local module_path=$1
    log_section "API Standards Compliance"

    # Look for /api/v1 base path in code
    if grep -r "\/api\/v1" "$module_path" --include="*.py" --include="*.js" --include="*.ts" >/dev/null 2>&1; then
        log_pass "Uses /api/v1 base path"
    else
        log_fail "No /api/v1 base path found in code"
    fi

    # Look for health endpoint
    if grep -r "\/health" "$module_path" --include="*.py" --include="*.js" --include="*.ts" >/dev/null 2>&1; then
        log_pass "Health endpoint implemented"
    else
        log_fail "No /health endpoint found"
    fi

    # Look for OpenAPI spec
    if grep -r "openapi" "$module_path" --include="*.py" --include="*.js" --include="*.ts" >/dev/null 2>&1 || \
       [ -f "$module_path/openapi.json" ] || [ -f "$module_path/openapi.yaml" ]; then
        log_pass "OpenAPI documentation exists"
    else
        log_fail "No OpenAPI documentation found"
    fi
}

# Check database integration
check_database() {
    local module_path=$1
    log_section "Database Standards"

    # Check for PostgreSQL connection
    if grep -r "postgresql\|psycopg\|pg_pool" "$module_path" --include="*.py" --include="*.js" --include="*.ts" >/dev/null 2>&1; then
        log_pass "PostgreSQL connection configured"
    else
        log_warn "No PostgreSQL connection found"
    fi

    # Check for migrations
    if [ -d "$module_path/migrations" ] || [ -d "$module_path/alembic" ] || [ -d "$module_path/db/migrations" ]; then
        log_pass "Migration system exists"
    else
        log_warn "No migration system found"
    fi

    # Check for models
    if grep -r "class.*Model\|models\." "$module_path" --include="*.py" >/dev/null 2>&1 || \
       grep -r "Schema\|model" "$module_path" --include="*.ts" >/dev/null 2>&1; then
        log_pass "Database models defined"
    else
        log_warn "No database models found"
    fi
}

# Check authentication integration
check_authentication() {
    local module_path=$1
    log_section "Authentication Integration"

    # Check for JWT
    if grep -r "jwt\|JWT\|token" "$module_path" --include="*.py" --include="*.js" --include="*.ts" >/dev/null 2>&1; then
        log_pass "JWT token handling exists"
    else
        log_warn "No JWT token handling found"
    fi

    # Check for auth endpoints (for backend module)
    if grep -r "\/auth\|\/login\|\/register" "$module_path" --include="*.py" --include="*.js" --include="*.ts" >/dev/null 2>&1; then
        log_pass "Authentication endpoints exist"
    else
        log_warn "No authentication endpoints found (OK if not Backend module)"
    fi
}

# Check logging
check_logging() {
    local module_path=$1
    log_section "Observability - Logging"

    # Check for structured logging
    if grep -r "logging\|logger\|log" "$module_path" --include="*.py" --include="*.js" --include="*.ts" >/dev/null 2>&1; then
        log_pass "Logging implemented"
    else
        log_fail "No logging implementation found"
    fi

    # Check for JSON logging
    if grep -r "json.*log\|structlog\|winston" "$module_path" --include="*.py" --include="*.js" --include="*.ts" >/dev/null 2>&1; then
        log_pass "Structured/JSON logging configured"
    else
        log_warn "No structured/JSON logging found"
    fi
}

# Check testing
check_testing() {
    local module_path=$1
    log_section "Code Quality & Testing"

    # Check for test files
    if [ -d "$module_path/tests" ] || [ -d "$module_path/test" ] || \
       find "$module_path" -name "*test*.py" -o -name "*test*.js" -o -name "*test*.ts" 2>/dev/null | grep -q .; then
        log_pass "Test files exist"
    else
        log_fail "No test files found"
    fi

    # Check for test framework
    if grep -r "pytest\|unittest\|jest\|vitest" "$module_path" --include="*.py" --include="*.json" >/dev/null 2>&1; then
        log_pass "Test framework configured"
    else
        log_warn "No test framework found"
    fi
}

# Generate summary report
generate_summary() {
    local module_name=$1
    echo ""
    log_header "REVIEW SUMMARY: $module_name"
    echo ""
    echo "Total Checks: $TOTAL_CHECKS"
    echo -e "${GREEN}Passed: $PASSED_CHECKS${NC}"
    echo -e "${RED}Failed: $FAILED_CHECKS${NC}"
    echo ""

    if [ $FAILED_CHECKS -eq 0 ]; then
        echo -e "${GREEN}✓ All checks passed!${NC}"
        return 0
    else
        local pass_rate=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
        echo -e "${YELLOW}⚠ Compliance: $pass_rate%${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Review failed checks above"
        echo "2. Refer to: docs/modules/shared/standalone-modules/README.md"
        echo "3. Document gaps in module-specific gap analysis"
        return 1
    fi
}

# Review a single module
review_module() {
    local module_path=$1
    local module_name=$(basename "$module_path")

    # Reset counters
    TOTAL_CHECKS=0
    PASSED_CHECKS=0
    FAILED_CHECKS=0

    log_header "REVIEWING MODULE: $module_name"
    log_info "Path: $module_path"
    echo ""

    check_module_exists "$module_path"
    check_file_structure "$module_path"
    check_dockerfile "$module_path"
    check_api_compliance "$module_path"
    check_database "$module_path"
    check_authentication "$module_path"
    check_logging "$module_path"
    check_testing "$module_path"

    generate_summary "$module_name"
}

# Review all modules
review_all_modules() {
    local base_path="modules/standalone"
    local modules=("backend" "frontend" "ai" "publishing")
    local failed_modules=()

    for module in "${modules[@]}"; do
        local module_path="$base_path/$module"
        if [ -d "$module_path" ]; then
            review_module "$module_path"
            if [ $FAILED_CHECKS -gt 0 ]; then
                failed_modules+=("$module")
            fi
            echo ""
            echo ""
        else
            echo -e "${RED}Module not found: $module_path${NC}"
        fi
    done

    # Overall summary
    log_header "OVERALL SUMMARY"
    echo ""
    echo "Reviewed ${#modules[@]} modules"
    if [ ${#failed_modules[@]} -eq 0 ]; then
        echo -e "${GREEN}✓ All modules passed compliance checks${NC}"
    else
        echo -e "${YELLOW}⚠ Modules with issues: ${failed_modules[*]}${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Review individual module reports above"
        echo "2. Document gaps in .dev/ai/reports/"
        echo "3. Generate developer task lists"
    fi
}

# Main script
main() {
    if [ $# -eq 0 ]; then
        echo "Usage: $0 [module_path|all]"
        echo ""
        echo "Examples:"
        echo "  $0 modules/standalone/backend"
        echo "  $0 all"
        exit 1
    fi

    if [ "$1" = "all" ]; then
        review_all_modules
    else
        review_module "$1"
    fi
}

main "$@"
