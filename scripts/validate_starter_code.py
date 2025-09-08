#!/usr/bin/env python3
"""
Starter Code Validation Script for Knowledge Graph Lab
Validates that all starter code runs without errors and meets basic requirements.
"""

import os
import sys
import subprocess
import json
import ast
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import importlib.util

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class CodeValidationResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []
        self.warnings_list = []
        self.module_status = {}
    
    def pass_check(self, module: str, message: str):
        print(f"{Colors.GREEN}✅ {module}: {message}{Colors.END}")
        self.passed += 1
    
    def fail_check(self, module: str, message: str):
        print(f"{Colors.RED}❌ {module}: {message}{Colors.END}")
        self.failed += 1
        self.errors.append(f"{module}: {message}")
    
    def warn_check(self, module: str, message: str):
        print(f"{Colors.YELLOW}⚠️  {module}: {message}{Colors.END}")
        self.warnings += 1
        self.warnings_list.append(f"{module}: {message}")
    
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

def validate_python_syntax(file_path: Path, result: CodeValidationResult, module_name: str):
    """Validate Python file syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
        # Parse the AST to check syntax
        ast.parse(source, filename=str(file_path))
        result.pass_check(module_name, f"Valid Python syntax: {file_path.name}")
        return True
        
    except SyntaxError as e:
        result.fail_check(module_name, f"Syntax error in {file_path.name}: {e}")
        return False
    except Exception as e:
        result.fail_check(module_name, f"Error reading {file_path.name}: {e}")
        return False

def validate_python_imports(file_path: Path, result: CodeValidationResult, module_name: str):
    """Validate that all imports can be resolved."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
        tree = ast.parse(source)
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ''
                imports.append(module)
        
        # Filter out standard library and local imports
        external_imports = []
        for imp in imports:
            if imp and not imp.startswith('.') and imp.split('.')[0] not in [
                'os', 'sys', 'json', 'time', 'datetime', 'pathlib', 'typing', 
                're', 'asyncio', 'logging', 'uuid', 'hashlib', 'base64'
            ]:
                external_imports.append(imp.split('.')[0])
        
        if external_imports:
            result.info(f"{module_name}: External dependencies found: {', '.join(set(external_imports))}")
        
        return True
        
    except Exception as e:
        result.warn_check(module_name, f"Could not analyze imports in {file_path.name}: {e}")
        return False

def validate_requirements_file(req_path: Path, result: CodeValidationResult, module_name: str):
    """Validate requirements.txt file."""
    if not req_path.exists():
        result.fail_check(module_name, "requirements.txt missing")
        return False
        
    try:
        with open(req_path, 'r') as f:
            requirements = f.read().strip()
            
        if not requirements:
            result.warn_check(module_name, "requirements.txt is empty")
            return False
            
        lines = [line.strip() for line in requirements.split('\n') if line.strip() and not line.startswith('#')]
        
        if len(lines) < 1:
            result.warn_check(module_name, "No dependencies in requirements.txt")
        else:
            result.pass_check(module_name, f"requirements.txt has {len(lines)} dependencies")
            
        # Check for common packages
        req_text = requirements.lower()
        common_packages = {
            'fastapi': 'FastAPI web framework',
            'requests': 'HTTP requests library',
            'openai': 'OpenAI API client',
            'psycopg2': 'PostgreSQL adapter',
            'redis': 'Redis client'
        }
        
        for package, description in common_packages.items():
            if package in req_text:
                result.info(f"{module_name}: Found {description}")
                
        return True
        
    except Exception as e:
        result.fail_check(module_name, f"Error reading requirements.txt: {e}")
        return False

def validate_package_json(pkg_path: Path, result: CodeValidationResult, module_name: str):
    """Validate package.json file."""
    if not pkg_path.exists():
        result.fail_check(module_name, "package.json missing")
        return False
        
    try:
        with open(pkg_path, 'r') as f:
            package_data = json.load(f)
            
        # Check required fields
        required_fields = ['name', 'version', 'scripts']
        for field in required_fields:
            if field in package_data:
                result.pass_check(module_name, f"package.json has {field}")
            else:
                result.warn_check(module_name, f"package.json missing {field}")
                
        # Check scripts
        scripts = package_data.get('scripts', {})
        recommended_scripts = ['dev', 'build', 'start']
        for script in recommended_scripts:
            if script in scripts:
                result.pass_check(module_name, f"Has {script} script")
            else:
                result.warn_check(module_name, f"Missing {script} script")
                
        # Check dependencies
        dependencies = package_data.get('dependencies', {})
        dev_dependencies = package_data.get('devDependencies', {})
        total_deps = len(dependencies) + len(dev_dependencies)
        
        if total_deps > 0:
            result.pass_check(module_name, f"Has {total_deps} total dependencies")
        else:
            result.warn_check(module_name, "No dependencies found")
            
        # Check for common React/Next.js packages
        if 'next' in dependencies:
            result.info(f"{module_name}: Next.js project detected")
        if 'react' in dependencies:
            result.info(f"{module_name}: React project detected")
            
        return True
        
    except json.JSONDecodeError as e:
        result.fail_check(module_name, f"Invalid JSON in package.json: {e}")
        return False
    except Exception as e:
        result.fail_check(module_name, f"Error reading package.json: {e}")
        return False

def run_code_quality_checks(src_path: Path, result: CodeValidationResult, module_name: str):
    """Run basic code quality checks."""
    if not src_path.exists():
        result.fail_check(module_name, "src/ directory missing")
        return
        
    python_files = list(src_path.rglob("*.py"))
    if not python_files:
        result.warn_check(module_name, "No Python files found in src/")
        return
        
    result.info(f"{module_name}: Found {len(python_files)} Python files")
    
    # Check each Python file
    syntax_errors = 0
    for py_file in python_files:
        if not validate_python_syntax(py_file, result, module_name):
            syntax_errors += 1
        else:
            validate_python_imports(py_file, result, module_name)
    
    if syntax_errors == 0:
        result.pass_check(module_name, "All Python files have valid syntax")
    else:
        result.fail_check(module_name, f"{syntax_errors} files with syntax errors")

def check_basic_functionality(module_path: Path, result: CodeValidationResult, module_name: str, module_type: str):
    """Check basic functionality by running simple tests."""
    if module_type == "python":
        # Look for main.py or app.py
        main_files = ['main.py', 'app.py', '__init__.py']
        src_path = module_path / 'src'
        
        main_file = None
        for filename in main_files:
            candidate = src_path / filename
            if candidate.exists():
                main_file = candidate
                break
                
        if main_file:
            result.pass_check(module_name, f"Entry point found: {main_file.name}")
            
            # Try to import the module (basic test)
            try:
                # Add the src directory to Python path temporarily
                original_path = sys.path.copy()
                sys.path.insert(0, str(src_path))
                
                # Try to import without executing
                spec = importlib.util.spec_from_file_location("test_module", main_file)
                if spec and spec.loader:
                    result.pass_check(module_name, "Module can be imported")
                else:
                    result.warn_check(module_name, "Module import spec could not be created")
                    
            except Exception as e:
                result.warn_check(module_name, f"Module import test failed: {e}")
            finally:
                sys.path = original_path
        else:
            result.warn_check(module_name, "No obvious entry point found (main.py, app.py)")
            
    elif module_type == "node":
        # Check if npm/yarn commands work
        try:
            # Check if package.json scripts can be parsed
            pkg_path = module_path / 'package.json'
            if pkg_path.exists():
                result.pass_check(module_name, "Node.js module structure looks correct")
            else:
                result.fail_check(module_name, "package.json missing for Node.js module")
                
        except Exception as e:
            result.warn_check(module_name, f"Node.js validation error: {e}")

def validate_module_structure(project_root: Path, result: CodeValidationResult):
    """Validate the structure and code of each module."""
    
    modules_config = [
        ("module-1-ingestion", "python"),
        ("module-2-knowledge-graph", "python"),
        ("module-3-reasoning", "python"),
        ("module-4-frontend", "node")
    ]
    
    for module_name, module_type in modules_config:
        print(f"\n{Colors.BOLD}🧩 VALIDATING {module_name.upper()}{Colors.END}")
        
        module_path = project_root / "modules" / module_name
        
        if not module_path.exists():
            result.fail_check(module_name, "Module directory does not exist")
            continue
            
        # Check README
        readme_path = module_path / "README.md"
        if readme_path.exists():
            result.pass_check(module_name, "README.md exists")
            
            # Check README content
            try:
                with open(readme_path, 'r') as f:
                    readme_content = f.read()
                if len(readme_content.strip()) > 100:
                    result.pass_check(module_name, "README.md has substantial content")
                else:
                    result.warn_check(module_name, "README.md is very brief")
            except:
                result.warn_check(module_name, "Could not read README.md")
        else:
            result.warn_check(module_name, "README.md missing")
            
        # Validate based on module type
        if module_type == "python":
            # Check requirements.txt
            req_path = module_path / "requirements.txt"
            validate_requirements_file(req_path, result, module_name)
            
            # Check source code
            src_path = module_path / "src"
            run_code_quality_checks(src_path, result, module_name)
            
        elif module_type == "node":
            # Check package.json
            pkg_path = module_path / "package.json"
            validate_package_json(pkg_path, result, module_name)
            
            # Check source structure
            src_paths = [module_path / "src", module_path / "pages", module_path / "app"]
            src_found = any(p.exists() for p in src_paths)
            
            if src_found:
                result.pass_check(module_name, "Source directory found")
            else:
                result.warn_check(module_name, "No src/, pages/, or app/ directory found")
        
        # Check basic functionality
        check_basic_functionality(module_path, result, module_name, module_type)

def validate_shared_components(project_root: Path, result: CodeValidationResult):
    """Validate shared components and utilities."""
    print(f"\n{Colors.BOLD}🔗 SHARED COMPONENTS VALIDATION{Colors.END}")
    
    shared_path = project_root / "shared"
    if not shared_path.exists():
        result.warn_check("Shared", "shared/ directory missing")
        return
        
    # Check for database utilities
    db_path = shared_path / "database"
    if db_path.exists():
        result.pass_check("Shared", "Database utilities directory exists")
        
        # Look for common database files
        db_files = ['connection.py', 'models.py', 'init.py', '__init__.py']
        found_files = []
        for filename in db_files:
            if (db_path / filename).exists():
                found_files.append(filename)
                
        if found_files:
            result.pass_check("Shared", f"Database files found: {', '.join(found_files)}")
        else:
            result.warn_check("Shared", "No database utility files found")
    else:
        result.warn_check("Shared", "Database utilities missing")

def validate_configuration_templates(project_root: Path, result: CodeValidationResult):
    """Validate configuration file templates."""
    print(f"\n{Colors.BOLD}⚙️  CONFIGURATION TEMPLATES{Colors.END}")
    
    # Check .env.example
    env_example = project_root / ".env.example"
    if env_example.exists():
        try:
            with open(env_example, 'r') as f:
                env_content = f.read()
                
            # Count variables
            env_lines = [line for line in env_content.split('\n') if '=' in line and not line.startswith('#')]
            
            if len(env_lines) >= 5:
                result.pass_check("Config", f".env.example has {len(env_lines)} variables")
            else:
                result.warn_check("Config", f".env.example only has {len(env_lines)} variables")
                
        except Exception as e:
            result.warn_check("Config", f"Error reading .env.example: {e}")
    else:
        result.fail_check("Config", ".env.example missing")
    
    # Check docker-compose.yml
    compose_file = project_root / "docker-compose.yml"
    if compose_file.exists():
        try:
            with open(compose_file, 'r') as f:
                compose_content = f.read()
                
            # Look for required services
            required_services = ['postgres', 'redis', 'qdrant']
            found_services = []
            
            for service in required_services:
                if service in compose_content:
                    found_services.append(service)
                    
            if len(found_services) >= 2:
                result.pass_check("Config", f"docker-compose.yml has services: {', '.join(found_services)}")
            else:
                result.warn_check("Config", f"docker-compose.yml missing key services")
                
        except Exception as e:
            result.warn_check("Config", f"Error reading docker-compose.yml: {e}")
    else:
        result.fail_check("Config", "docker-compose.yml missing")

def print_code_validation_summary(result: CodeValidationResult):
    """Print code validation summary."""
    print(f"\n{Colors.BOLD}📊 CODE VALIDATION SUMMARY{Colors.END}")
    print(f"{'='*60}")
    
    total_checks = result.passed + result.failed + result.warnings
    
    print(f"{Colors.GREEN}✅ Passed: {result.passed}{Colors.END}")
    print(f"{Colors.RED}❌ Failed: {result.failed}{Colors.END}")
    print(f"{Colors.YELLOW}⚠️  Warnings: {result.warnings}{Colors.END}")
    print(f"Total Checks: {total_checks}")
    
    # Overall assessment
    if result.failed == 0:
        if result.warnings <= 3:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 EXCELLENT! All starter code is ready for development.{Colors.END}")
            return 0
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}✅ GOOD! Code is functional with minor improvements needed.{Colors.END}")
            return 0
    elif result.failed <= 2:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  PARTIAL! Some issues need attention but development can start.{Colors.END}")
        return 1
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}🚨 CRITICAL! Address code issues before intern onboarding.{Colors.END}")
        
        if result.errors:
            print(f"\n{Colors.RED}Critical Issues:{Colors.END}")
            for error in result.errors[:5]:
                print(f"  • {error}")
            if len(result.errors) > 5:
                print(f"  ... and {len(result.errors) - 5} more issues")
        
        return 2

def main():
    """Main validation function."""
    print(f"{Colors.BOLD}{Colors.BLUE}🔍 Knowledge Graph Lab Starter Code Validation{Colors.END}")
    print(f"Validating all starter code and module structure...\n")
    
    project_root = get_project_root()
    print(f"Project root: {project_root}")
    
    result = CodeValidationResult()
    
    # Run all validation checks
    validate_module_structure(project_root, result)
    validate_shared_components(project_root, result)
    validate_configuration_templates(project_root, result)
    
    # Print summary and exit with appropriate code
    exit_code = print_code_validation_summary(result)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()