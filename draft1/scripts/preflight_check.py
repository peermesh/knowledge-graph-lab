#!/usr/bin/env python3
"""
Knowledge Graph Lab - Pre-Flight Launch Validation Script

This script validates that all components are ready for intern onboarding.
Run before Monday launch to ensure 85%+ setup success rate.

Usage:
    python scripts/preflight_check.py [--fix] [--verbose]
    
Returns:
    Exit code 0: All checks pass - READY FOR LAUNCH
    Exit code 1: Critical issues found - DO NOT LAUNCH
    Exit code 2: Warnings found - LAUNCH WITH CAUTION
"""

import os
import sys
import subprocess
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

@dataclass
class CheckResult:
    name: str
    status: str  # 'PASS', 'FAIL', 'WARN'
    message: str
    details: List[str] = field(default_factory=list)
    fix_suggestion: Optional[str] = None

class PreFlightValidator:
    def __init__(self, project_root: Path, verbose: bool = False, auto_fix: bool = False):
        self.project_root = project_root
        self.verbose = verbose
        self.auto_fix = auto_fix
        self.results: List[CheckResult] = []
    
    def log(self, message: str, force: bool = False):
        """Log message if verbose mode or force is True"""
        if self.verbose or force:
            print(f"[LOG] {message}")
    
    def check_file_exists(self, file_path: Path, name: str, critical: bool = True) -> CheckResult:
        """Check if a required file exists"""
        if file_path.exists():
            return CheckResult(
                name=name,
                status='PASS',
                message=f"File exists: {file_path}"
            )
        else:
            status = 'FAIL' if critical else 'WARN'
            return CheckResult(
                name=name,
                status=status,
                message=f"Missing file: {file_path}",
                fix_suggestion=f"Create missing file: {file_path}"
            )
    
    def check_directory_structure(self) -> List[CheckResult]:
        """Validate expected directory structure"""
        results = []
        
        # Critical directories
        critical_dirs = [
            "modules",
            "shared", 
            "mock-data",
            "docs",
            "scripts"
        ]
        
        for dir_name in critical_dirs:
            dir_path = self.project_root / dir_name
            results.append(self.check_file_exists(dir_path, f"Directory: {dir_name}", critical=True))
        
        # Module-specific directories
        modules = [
            "modules/module-1-ingestion",
            "modules/module-2-knowledge-graph", 
            "modules/module-3-reasoning",
            "modules/module-4-frontend"
        ]
        
        for module in modules:
            module_path = self.project_root / module
            results.append(self.check_file_exists(module_path, f"Module: {module}", critical=True))
            
            # Check for module source directories
            src_path = module_path / "src"
            results.append(self.check_file_exists(src_path, f"Module src: {module}/src", critical=True))
        
        return results
    
    def check_configuration_files(self) -> List[CheckResult]:
        """Validate configuration files exist and are properly formatted"""
        results = []
        
        # Critical configuration files
        config_files = [
            (".env.example", True),
            ("docker-compose.yml", True), 
            ("SETUP.md", True),
            ("shared/database/schema.sql", True),
            ("shared/nginx/nginx.conf", False)
        ]
        
        for file_path, critical in config_files:
            full_path = self.project_root / file_path
            results.append(self.check_file_exists(full_path, f"Config: {file_path}", critical=critical))
        
        # Check .env.example format
        env_example = self.project_root / ".env.example"
        if env_example.exists():
            try:
                content = env_example.read_text()
                required_vars = [
                    "DATABASE_URL",
                    "REDIS_URL", 
                    "QDRANT_URL",
                    "OPENAI_API_KEY",
                    "ANTHROPIC_API_KEY"
                ]
                
                missing_vars = []
                for var in required_vars:
                    if var not in content:
                        missing_vars.append(var)
                
                if missing_vars:
                    results.append(CheckResult(
                        name="ENV vars validation",
                        status='WARN',
                        message=f"Missing environment variables in .env.example",
                        details=missing_vars,
                        fix_suggestion=f"Add missing variables: {', '.join(missing_vars)}"
                    ))
                else:
                    results.append(CheckResult(
                        name="ENV vars validation", 
                        status='PASS',
                        message="All required environment variables documented"
                    ))
            except Exception as e:
                results.append(CheckResult(
                    name="ENV file parsing",
                    status='FAIL',
                    message=f"Cannot parse .env.example: {e}",
                    fix_suggestion="Check .env.example file format"
                ))
        
        return results
    
    def check_docker_configuration(self) -> List[CheckResult]:
        """Validate Docker configuration"""
        results = []
        
        # Check docker-compose.yml exists and is valid
        compose_file = self.project_root / "docker-compose.yml"
        if compose_file.exists():
            try:
                import yaml
                with open(compose_file) as f:
                    compose_config = yaml.safe_load(f)
                
                # Check required services
                required_services = [
                    "postgres",
                    "redis", 
                    "qdrant",
                    "ingestion-service",
                    "knowledge-graph-service",
                    "reasoning-service",
                    "frontend"
                ]
                
                services = compose_config.get('services', {})
                missing_services = []
                
                for service in required_services:
                    if service not in services:
                        missing_services.append(service)
                
                if missing_services:
                    results.append(CheckResult(
                        name="Docker services",
                        status='FAIL',
                        message="Missing required Docker services",
                        details=missing_services,
                        fix_suggestion=f"Add missing services to docker-compose.yml: {', '.join(missing_services)}"
                    ))
                else:
                    results.append(CheckResult(
                        name="Docker services",
                        status='PASS', 
                        message="All required Docker services defined"
                    ))
                
                # Check for health checks
                services_without_healthcheck = []
                for service_name, service_config in services.items():
                    if service_name not in ['frontend'] and 'healthcheck' not in service_config:
                        services_without_healthcheck.append(service_name)
                
                if services_without_healthcheck:
                    results.append(CheckResult(
                        name="Docker health checks",
                        status='WARN',
                        message="Services missing health checks",
                        details=services_without_healthcheck,
                        fix_suggestion="Add health check configurations for better reliability"
                    ))
                else:
                    results.append(CheckResult(
                        name="Docker health checks",
                        status='PASS',
                        message="Health checks configured"
                    ))
                    
            except ImportError:
                results.append(CheckResult(
                    name="Docker config validation",
                    status='WARN',
                    message="Cannot validate docker-compose.yml - PyYAML not installed",
                    fix_suggestion="Install PyYAML: pip install pyyaml"
                ))
            except Exception as e:
                results.append(CheckResult(
                    name="Docker config validation",
                    status='FAIL',
                    message=f"Invalid docker-compose.yml: {e}",
                    fix_suggestion="Fix docker-compose.yml syntax errors"
                ))
        
        return results
    
    def check_module_dependencies(self) -> List[CheckResult]:
        """Check that all module dependency files exist and are valid"""
        results = []
        
        # Python modules
        python_modules = [
            "modules/module-1-ingestion",
            "modules/module-2-knowledge-graph",
            "modules/module-3-reasoning"
        ]
        
        for module in python_modules:
            req_file = self.project_root / module / "requirements.txt"
            results.append(self.check_file_exists(req_file, f"Requirements: {module}", critical=True))
            
            # Validate requirements.txt format
            if req_file.exists():
                try:
                    content = req_file.read_text()
                    lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                    
                    if len(lines) == 0:
                        results.append(CheckResult(
                            name=f"Requirements content: {module}",
                            status='WARN',
                            message=f"Empty requirements.txt in {module}",
                            fix_suggestion="Add required Python packages to requirements.txt"
                        ))
                    else:
                        results.append(CheckResult(
                            name=f"Requirements content: {module}",
                            status='PASS',
                            message=f"Requirements file has {len(lines)} dependencies"
                        ))
                except Exception as e:
                    results.append(CheckResult(
                        name=f"Requirements parsing: {module}",
                        status='FAIL',
                        message=f"Cannot parse requirements.txt: {e}",
                        fix_suggestion="Check requirements.txt file format"
                    ))
        
        # Node.js module
        package_json = self.project_root / "modules/module-4-frontend/package.json"
        results.append(self.check_file_exists(package_json, "Frontend package.json", critical=True))
        
        if package_json.exists():
            try:
                with open(package_json) as f:
                    package_config = json.load(f)
                
                # Check for required scripts
                scripts = package_config.get('scripts', {})
                required_scripts = ['dev', 'build', 'start']
                missing_scripts = [script for script in required_scripts if script not in scripts]
                
                if missing_scripts:
                    results.append(CheckResult(
                        name="Frontend scripts",
                        status='WARN',
                        message="Missing package.json scripts",
                        details=missing_scripts,
                        fix_suggestion=f"Add missing scripts: {', '.join(missing_scripts)}"
                    ))
                else:
                    results.append(CheckResult(
                        name="Frontend scripts",
                        status='PASS',
                        message="All required npm scripts present"
                    ))
                    
                # Check for Next.js dependency
                deps = {**package_config.get('dependencies', {}), **package_config.get('devDependencies', {})}
                if 'next' not in deps:
                    results.append(CheckResult(
                        name="Next.js dependency",
                        status='FAIL',
                        message="Next.js not found in dependencies",
                        fix_suggestion="Add Next.js: npm install next react react-dom"
                    ))
                else:
                    results.append(CheckResult(
                        name="Next.js dependency",
                        status='PASS',
                        message=f"Next.js version: {deps['next']}"
                    ))
                    
            except Exception as e:
                results.append(CheckResult(
                    name="Frontend package.json parsing",
                    status='FAIL',
                    message=f"Cannot parse package.json: {e}",
                    fix_suggestion="Check package.json file format"
                ))
        
        return results
    
    def check_system_prerequisites(self) -> List[CheckResult]:
        """Check system-level prerequisites"""
        results = []
        
        # Check Python version
        try:
            python_version = subprocess.check_output([
                sys.executable, '--version'
            ], text=True).strip()
            
            # Parse version
            version_str = python_version.split()[1]
            major, minor = map(int, version_str.split('.')[:2])
            
            if major == 3 and minor >= 11:
                results.append(CheckResult(
                    name="Python version",
                    status='PASS',
                    message=f"Python {version_str} (>= 3.11 required)"
                ))
            else:
                results.append(CheckResult(
                    name="Python version",
                    status='FAIL',
                    message=f"Python {version_str} is too old (3.11+ required)",
                    fix_suggestion="Install Python 3.11+: brew install python@3.11"
                ))
        except Exception as e:
            results.append(CheckResult(
                name="Python availability",
                status='FAIL',
                message=f"Cannot check Python version: {e}",
                fix_suggestion="Install Python 3.11+"
            ))
        
        # Check Docker
        try:
            docker_version = subprocess.check_output([
                'docker', '--version'
            ], text=True).strip()
            results.append(CheckResult(
                name="Docker availability",
                status='PASS',
                message=docker_version
            ))
            
            # Check if Docker daemon is running
            try:
                subprocess.check_output(['docker', 'info'], stderr=subprocess.DEVNULL)
                results.append(CheckResult(
                    name="Docker daemon",
                    status='PASS',
                    message="Docker daemon is running"
                ))
            except subprocess.CalledProcessError:
                results.append(CheckResult(
                    name="Docker daemon",
                    status='FAIL',
                    message="Docker daemon is not running",
                    fix_suggestion="Start Docker Desktop application"
                ))
                
        except FileNotFoundError:
            results.append(CheckResult(
                name="Docker availability",
                status='FAIL',
                message="Docker not installed",
                fix_suggestion="Install Docker Desktop from https://docker.com"
            ))
        except Exception as e:
            results.append(CheckResult(
                name="Docker availability",
                status='FAIL',
                message=f"Docker check failed: {e}",
                fix_suggestion="Check Docker installation"
            ))
        
        # Check Node.js (for frontend)
        try:
            node_version = subprocess.check_output(['node', '--version'], text=True).strip()
            version_num = int(node_version.lstrip('v').split('.')[0])
            
            if version_num >= 20:
                results.append(CheckResult(
                    name="Node.js version",
                    status='PASS',
                    message=f"Node.js {node_version} (>= v20 required)"
                ))
            else:
                results.append(CheckResult(
                    name="Node.js version",
                    status='FAIL',
                    message=f"Node.js {node_version} is too old (v20+ required)",
                    fix_suggestion="Install Node.js 20+: brew install node@20"
                ))
        except FileNotFoundError:
            results.append(CheckResult(
                name="Node.js availability",
                status='FAIL',
                message="Node.js not installed",
                fix_suggestion="Install Node.js 20+: brew install node@20"
            ))
        except Exception as e:
            results.append(CheckResult(
                name="Node.js availability",
                status='WARN',
                message=f"Cannot check Node.js version: {e}",
                fix_suggestion="Verify Node.js installation"
            ))
        
        return results
    
    def check_setup_instructions(self) -> List[CheckResult]:
        """Validate SETUP.md instructions against actual file structure"""
        results = []
        
        setup_file = self.project_root / "SETUP.md"
        if not setup_file.exists():
            results.append(CheckResult(
                name="SETUP.md exists",
                status='FAIL',
                message="SETUP.md file missing",
                fix_suggestion="Create SETUP.md with setup instructions"
            ))
            return results
        
        try:
            setup_content = setup_file.read_text()
            
            # Check for key sections
            required_sections = [
                "System Requirements",
                "Step-by-Step Setup", 
                "Troubleshooting",
                "Success Confirmation"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in setup_content:
                    missing_sections.append(section)
            
            if missing_sections:
                results.append(CheckResult(
                    name="SETUP.md completeness",
                    status='WARN',
                    message="Missing setup guide sections",
                    details=missing_sections,
                    fix_suggestion=f"Add missing sections: {', '.join(missing_sections)}"
                ))
            else:
                results.append(CheckResult(
                    name="SETUP.md completeness",
                    status='PASS',
                    message="All required setup sections present"
                ))
            
            # Check for command accuracy (sample some critical commands)
            if "docker-compose up -d" in setup_content:
                results.append(CheckResult(
                    name="Docker commands in setup",
                    status='PASS',
                    message="Docker commands documented"
                ))
            else:
                results.append(CheckResult(
                    name="Docker commands in setup",
                    status='WARN',
                    message="Docker startup commands missing from setup guide",
                    fix_suggestion="Add 'docker-compose up -d' to setup instructions"
                ))
            
        except Exception as e:
            results.append(CheckResult(
                name="SETUP.md parsing",
                status='FAIL',
                message=f"Cannot parse SETUP.md: {e}",
                fix_suggestion="Check SETUP.md file format"
            ))
        
        return results
    
    def check_port_availability(self) -> List[CheckResult]:
        """Check if required ports are available"""
        results = []
        
        required_ports = {
            5432: "PostgreSQL",
            6379: "Redis", 
            6333: "Qdrant",
            8001: "Ingestion Service",
            8002: "Knowledge Graph Service",
            8003: "Reasoning Service", 
            3000: "Frontend",
            8000: "API Gateway"
        }
        
        for port, service in required_ports.items():
            try:
                import socket
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(('localhost', port))
                    
                    if result == 0:
                        # Port is occupied
                        results.append(CheckResult(
                            name=f"Port {port} availability",
                            status='WARN',
                            message=f"Port {port} ({service}) is already in use",
                            fix_suggestion=f"Stop service using port {port} or use docker-compose down"
                        ))
                    else:
                        # Port is available
                        results.append(CheckResult(
                            name=f"Port {port} availability",
                            status='PASS',
                            message=f"Port {port} ({service}) is available"
                        ))
            except Exception as e:
                results.append(CheckResult(
                    name=f"Port {port} check",
                    status='WARN',
                    message=f"Cannot check port {port}: {e}",
                    fix_suggestion="Manual port verification needed"
                ))
        
        return results
    
    def run_all_checks(self) -> Tuple[int, List[CheckResult]]:
        """Run all validation checks and return exit code"""
        
        print("🚀 Knowledge Graph Lab - Pre-Flight Validation")
        print("=" * 50)
        
        # Run all check categories
        check_categories = [
            ("Directory Structure", self.check_directory_structure),
            ("Configuration Files", self.check_configuration_files), 
            ("Docker Configuration", self.check_docker_configuration),
            ("Module Dependencies", self.check_module_dependencies),
            ("System Prerequisites", self.check_system_prerequisites),
            ("Setup Instructions", self.check_setup_instructions),
            ("Port Availability", self.check_port_availability)
        ]
        
        all_results = []
        for category_name, check_function in check_categories:
            print(f"\n📋 Checking: {category_name}")
            category_results = check_function()
            all_results.extend(category_results)
            
            # Print results for this category
            for result in category_results:
                icon = "✅" if result.status == 'PASS' else "⚠️" if result.status == 'WARN' else "❌"
                print(f"   {icon} {result.name}: {result.message}")
                
                if result.details and self.verbose:
                    for detail in result.details:
                        print(f"      → {detail}")
                
                if result.fix_suggestion and result.status != 'PASS':
                    print(f"      💡 Fix: {result.fix_suggestion}")
        
        # Summary
        total = len(all_results)
        passed = len([r for r in all_results if r.status == 'PASS'])
        warnings = len([r for r in all_results if r.status == 'WARN'])
        failures = len([r for r in all_results if r.status == 'FAIL'])
        
        print(f"\n📊 VALIDATION SUMMARY")
        print("=" * 50)
        print(f"Total Checks:    {total}")
        print(f"✅ Passed:       {passed}")
        print(f"⚠️  Warnings:     {warnings}")
        print(f"❌ Failures:     {failures}")
        print(f"Success Rate:    {(passed/total)*100:.1f}%")
        
        # Determine exit code and launch readiness
        if failures > 0:
            print(f"\n🚨 LAUNCH STATUS: NOT READY")
            print(f"Critical issues must be fixed before intern onboarding.")
            print(f"Fix {failures} failure(s) then re-run validation.")
            exit_code = 1
        elif warnings > 0:
            print(f"\n⚠️  LAUNCH STATUS: CAUTION ADVISED")
            print(f"Launch possible but {warnings} warning(s) may impact intern experience.")
            print(f"Consider fixing warnings for smoother onboarding.")
            exit_code = 2
        else:
            print(f"\n🎉 LAUNCH STATUS: READY")
            print(f"All checks passed! Repository is ready for intern onboarding.")
            exit_code = 0
        
        # Action items
        failed_items = [r for r in all_results if r.status == 'FAIL']
        warning_items = [r for r in all_results if r.status == 'WARN']
        
        if failed_items:
            print(f"\n🔧 CRITICAL FIXES NEEDED:")
            for item in failed_items[:5]:  # Show top 5
                print(f"   • {item.name}: {item.fix_suggestion or item.message}")
            if len(failed_items) > 5:
                print(f"   • ... and {len(failed_items) - 5} more")
        
        if warning_items and exit_code != 1:
            print(f"\n💡 RECOMMENDED IMPROVEMENTS:")
            for item in warning_items[:3]:  # Show top 3
                print(f"   • {item.name}: {item.fix_suggestion or item.message}")
            if len(warning_items) > 3:
                print(f"   • ... and {len(warning_items) - 3} more")
        
        return exit_code, all_results

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Knowledge Graph Lab Pre-Flight Validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit Codes:
  0 - All checks passed, ready for launch
  1 - Critical failures, do not launch
  2 - Warnings present, launch with caution
        """
    )
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose output')
    parser.add_argument('--fix', action='store_true',
                       help='Attempt to auto-fix issues (future feature)')
    
    args = parser.parse_args()
    
    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    if not (project_root / "docker-compose.yml").exists():
        print(f"❌ Error: Not a Knowledge Graph Lab repository")
        print(f"   Expected docker-compose.yml in {project_root}")
        sys.exit(1)
    
    # Run validation
    validator = PreFlightValidator(
        project_root=project_root,
        verbose=args.verbose,
        auto_fix=args.fix
    )
    
    exit_code, results = validator.run_all_checks()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()