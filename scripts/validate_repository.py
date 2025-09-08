#!/usr/bin/env python3
"""
Repository Structure Validation Script for Knowledge Graph Lab
Validates that all required files and directories are present for intern onboarding.
"""

import os
import sys
from pathlib import Path
import json
import re
from typing import List, Dict, Tuple, Optional

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ValidationResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []
        self.warnings_list = []
    
    def pass_check(self, message: str):
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
        self.passed += 1
    
    def fail_check(self, message: str):
        print(f"{Colors.RED}❌ {message}{Colors.END}")
        self.failed += 1
        self.errors.append(message)
    
    def warn_check(self, message: str):
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
        self.warnings += 1
        self.warnings_list.append(message)
    
    def info(self, message: str):
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def get_project_root() -> Path:
    """Find the project root directory."""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / ".git").exists() or (current / "README.md").exists():
            return current
        current = current.parent
    return Path.cwd()

def validate_directory_structure(project_root: Path, result: ValidationResult):
    """Validate the basic directory structure."""
    print(f"\n{Colors.BOLD}🏗️  DIRECTORY STRUCTURE VALIDATION{Colors.END}")
    
    required_dirs = [
        "modules",
        "modules/module-1-ingestion", 
        "modules/module-2-knowledge-graph",
        "modules/module-3-reasoning",
        "modules/module-4-frontend",
        "shared",
        "shared/database",
        "mock-data",
        "docs",
        "docs/ai",
        "scripts",
        ".git"
    ]
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists() and full_path.is_dir():
            result.pass_check(f"Directory exists: {dir_path}/")
        else:
            result.fail_check(f"Missing required directory: {dir_path}/")

def validate_root_files(project_root: Path, result: ValidationResult):
    """Validate required files in project root."""
    print(f"\n{Colors.BOLD}📄 ROOT FILES VALIDATION{Colors.END}")
    
    required_files = [
        ("README.md", True),
        ("SETUP.md", True),
        ("CONTRIBUTING.md", False),
        ("LICENSE", False),
        ("INDEX.md", False),
        ("CLAUDE.md", False),
        (".gitignore", True),
        ("docker-compose.yml", True),
        (".env.example", True)
    ]
    
    for file_name, is_critical in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            result.pass_check(f"File exists: {file_name}")
            
            # Validate file content for critical files
            if is_critical and file_path.stat().st_size == 0:
                result.warn_check(f"File is empty: {file_name}")
                
        elif is_critical:
            result.fail_check(f"Missing critical file: {file_name}")
        else:
            result.warn_check(f"Recommended file missing: {file_name}")

def validate_module_structure(project_root: Path, result: ValidationResult):
    """Validate each module's internal structure."""
    print(f"\n{Colors.BOLD}🧩 MODULE STRUCTURE VALIDATION{Colors.END}")
    
    modules = [
        ("module-1-ingestion", "Python", ["src/", "requirements.txt", "README.md"]),
        ("module-2-knowledge-graph", "Python", ["src/", "requirements.txt", "README.md"]),
        ("module-3-reasoning", "Python", ["src/", "requirements.txt", "README.md"]),
        ("module-4-frontend", "Node.js", ["src/", "package.json", "README.md"])
    ]
    
    for module_name, tech_stack, required_items in modules:
        module_path = project_root / "modules" / module_name
        result.info(f"Validating {module_name} ({tech_stack})")
        
        if not module_path.exists():
            result.fail_check(f"Module directory missing: {module_name}")
            continue
            
        for item in required_items:
            item_path = module_path / item
            if item_path.exists():
                result.pass_check(f"{module_name}: {item}")
            else:
                result.fail_check(f"{module_name}: Missing {item}")

def validate_documentation(project_root: Path, result: ValidationResult):
    """Validate documentation completeness."""
    print(f"\n{Colors.BOLD}📚 DOCUMENTATION VALIDATION{Colors.END}")
    
    # Check SETUP.md content
    setup_file = project_root / "SETUP.md"
    if setup_file.exists():
        content = setup_file.read_text()
        
        required_sections = [
            "System Requirements",
            "Step-by-Step Setup", 
            "Troubleshooting",
            "docker-compose up",
            "requirements.txt"
        ]
        
        for section in required_sections:
            if section in content:
                result.pass_check(f"SETUP.md contains: {section}")
            else:
                result.warn_check(f"SETUP.md may be missing: {section}")
                
        # Check length (should be comprehensive)
        lines = len(content.split('\n'))
        if lines > 200:
            result.pass_check(f"SETUP.md is comprehensive ({lines} lines)")
        else:
            result.warn_check(f"SETUP.md may be too brief ({lines} lines)")
    
    # Check for AI documentation organization
    ai_docs_path = project_root / "docs" / "ai"
    if ai_docs_path.exists():
        ai_files = list(ai_docs_path.glob("*.md"))
        result.pass_check(f"AI documentation directory exists ({len(ai_files)} files)")
        
        # Check naming convention
        valid_names = 0
        for file_path in ai_files:
            if re.match(r'\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\w+-.*\.md', file_path.name):
                valid_names += 1
                
        if valid_names > 0:
            result.pass_check(f"AI files follow naming convention ({valid_names}/{len(ai_files)})")
        else:
            result.warn_check("AI documentation files don't follow naming convention")

def validate_configuration_files(project_root: Path, result: ValidationResult):
    """Validate configuration file templates."""
    print(f"\n{Colors.BOLD}⚙️  CONFIGURATION VALIDATION{Colors.END}")
    
    # Check .env.example
    env_example = project_root / ".env.example"
    if env_example.exists():
        content = env_example.read_text()
        
        required_vars = [
            "DATABASE_URL",
            "VECTOR_DB_URL", 
            "OPENAI_API_KEY",
            "REDIS_URL",
            "DEBUG"
        ]
        
        for var in required_vars:
            if var in content:
                result.pass_check(f".env.example contains: {var}")
            else:
                result.warn_check(f".env.example missing: {var}")
    
    # Check docker-compose.yml
    docker_compose = project_root / "docker-compose.yml"
    if docker_compose.exists():
        content = docker_compose.read_text()
        
        required_services = [
            "postgres",
            "redis", 
            "qdrant"
        ]
        
        for service in required_services:
            if service in content:
                result.pass_check(f"docker-compose.yml contains: {service}")
            else:
                result.fail_check(f"docker-compose.yml missing: {service}")
    else:
        result.fail_check("docker-compose.yml is missing (critical for setup)")

def validate_mock_data(project_root: Path, result: ValidationResult):
    """Validate mock data for development."""
    print(f"\n{Colors.BOLD}📊 MOCK DATA VALIDATION{Colors.END}")
    
    mock_data_path = project_root / "mock-data"
    if not mock_data_path.exists():
        result.fail_check("Mock data directory missing")
        return
        
    # Look for data files
    data_files = list(mock_data_path.rglob("*.json")) + list(mock_data_path.rglob("*.csv"))
    
    if len(data_files) > 0:
        result.pass_check(f"Mock data files found ({len(data_files)} files)")
        
        # Validate JSON files
        valid_json = 0
        for json_file in mock_data_path.rglob("*.json"):
            try:
                with open(json_file) as f:
                    json.load(f)
                valid_json += 1
            except json.JSONDecodeError:
                result.warn_check(f"Invalid JSON file: {json_file.name}")
                
        if valid_json > 0:
            result.pass_check(f"Valid JSON files ({valid_json})")
    else:
        result.warn_check("No mock data files found (recommended for development)")

def validate_git_setup(project_root: Path, result: ValidationResult):
    """Validate git repository setup."""
    print(f"\n{Colors.BOLD}📝 GIT REPOSITORY VALIDATION{Colors.END}")
    
    # Check .gitignore
    gitignore = project_root / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text()
        
        important_entries = [
            ".env",
            "node_modules",
            "__pycache__",
            ".venv"
        ]
        
        for entry in important_entries:
            if entry in content:
                result.pass_check(f".gitignore excludes: {entry}")
            else:
                result.warn_check(f".gitignore should exclude: {entry}")
    else:
        result.fail_check(".gitignore missing (critical for security)")

def validate_scripts_directory(project_root: Path, result: ValidationResult):
    """Validate utility scripts."""
    print(f"\n{Colors.BOLD}🔧 SCRIPTS VALIDATION{Colors.END}")
    
    scripts_path = project_root / "scripts"
    if scripts_path.exists():
        script_files = list(scripts_path.glob("*.py")) + list(scripts_path.glob("*.sh"))
        result.pass_check(f"Scripts directory exists ({len(script_files)} files)")
        
        recommended_scripts = [
            "validate_repository.py",
            "health_check.py",
            "setup_database.py"
        ]
        
        for script in recommended_scripts:
            if (scripts_path / script).exists():
                result.pass_check(f"Script exists: {script}")
            else:
                result.warn_check(f"Recommended script missing: {script}")
    else:
        result.warn_check("Scripts directory missing (recommended for automation)")

def print_summary(result: ValidationResult):
    """Print validation summary."""
    print(f"\n{Colors.BOLD}📋 VALIDATION SUMMARY{Colors.END}")
    print(f"{'='*50}")
    
    total_checks = result.passed + result.failed + result.warnings
    
    print(f"{Colors.GREEN}✅ Passed: {result.passed}{Colors.END}")
    print(f"{Colors.RED}❌ Failed: {result.failed}{Colors.END}")
    print(f"{Colors.YELLOW}⚠️  Warnings: {result.warnings}{Colors.END}")
    print(f"Total Checks: {total_checks}")
    
    if result.failed == 0:
        if result.warnings == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 PERFECT! Repository is ready for intern onboarding.{Colors.END}")
            return 0
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}✅ GOOD! Repository is ready with minor improvements needed.{Colors.END}")
            return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}🚨 ISSUES FOUND! Address failed checks before launch.{Colors.END}")
        
        if result.errors:
            print(f"\n{Colors.RED}Critical Issues:{Colors.END}")
            for error in result.errors:
                print(f"  • {error}")
        
        return 1

def main():
    """Main validation function."""
    print(f"{Colors.BOLD}{Colors.BLUE}🔍 Knowledge Graph Lab Repository Validation{Colors.END}")
    print(f"Validating repository structure and readiness for intern onboarding...\n")
    
    project_root = get_project_root()
    print(f"Project root: {project_root}")
    
    result = ValidationResult()
    
    # Run all validation checks
    validate_directory_structure(project_root, result)
    validate_root_files(project_root, result)
    validate_module_structure(project_root, result)
    validate_documentation(project_root, result)
    validate_configuration_files(project_root, result)
    validate_mock_data(project_root, result)
    validate_git_setup(project_root, result)
    validate_scripts_directory(project_root, result)
    
    # Print summary and exit with appropriate code
    exit_code = print_summary(result)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()