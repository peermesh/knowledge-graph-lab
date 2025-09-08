#!/usr/bin/env python3
"""
Environment Validation Script for Knowledge Graph Lab
Pre-flight system checks to ensure environment is ready for development.
"""

import asyncio
import aiohttp
import docker
import subprocess
import sys
import os
import shutil
import time
import json
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple, Any

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class EnvironmentValidator:
    def __init__(self):
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'errors': [],
            'system_info': {}
        }
        self.setup_logging()
        
        # Required software and versions
        self.requirements = {
            'docker': {'min_version': '20.0.0', 'command': ['docker', '--version']},
            'docker-compose': {'min_version': '1.29.0', 'command': ['docker-compose', '--version']},
            'python': {'min_version': '3.8.0', 'command': ['python3', '--version']},
            'node': {'min_version': '16.0.0', 'command': ['node', '--version']},
            'npm': {'min_version': '8.0.0', 'command': ['npm', '--version']}
        }
        
        # Required ports for services
        self.required_ports = [3000, 5432, 6333, 6379, 8001, 8002, 8003]
        
        # Required directories and files
        self.required_paths = [
            'modules/',
            'shared/',
            'scripts/',
            'mock-data/',
            'docker-compose.yml',
            '.env.example',
            'shared/database/schema.sql'
        ]

    def setup_logging(self):
        """Setup logging to file and console."""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'environment_validation_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def print_status(self, message: str, status: str = 'info'):
        """Print colored status messages."""
        color_map = {
            'info': Colors.BLUE,
            'success': Colors.GREEN,
            'warning': Colors.YELLOW,
            'error': Colors.RED
        }
        color = color_map.get(status, Colors.BLUE)
        print(f"{color}{message}{Colors.END}")
        self.logger.info(message)

    def run_command(self, command: List[str]) -> Tuple[bool, str, str]:
        """Run a shell command and return success, stdout, stderr."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except FileNotFoundError:
            return False, "", f"Command not found: {' '.join(command)}"
        except Exception as e:
            return False, "", str(e)

    def parse_version(self, version_string: str, software_name: str) -> Optional[str]:
        """Extract version number from version string."""
        import re
        
        # Common version patterns
        patterns = [
            r'(\d+\.\d+\.\d+)',  # x.y.z
            r'v(\d+\.\d+\.\d+)',  # vx.y.z
            r'(\d+\.\d+)',  # x.y
        ]
        
        for pattern in patterns:
            match = re.search(pattern, version_string)
            if match:
                return match.group(1)
        
        return None

    def compare_versions(self, current: str, required: str) -> bool:
        """Compare version strings (simple numeric comparison)."""
        try:
            current_parts = [int(x) for x in current.split('.')]
            required_parts = [int(x) for x in required.split('.')]
            
            # Pad shorter version with zeros
            max_len = max(len(current_parts), len(required_parts))
            current_parts += [0] * (max_len - len(current_parts))
            required_parts += [0] * (max_len - len(required_parts))
            
            return current_parts >= required_parts
        except:
            return False

    def validate_software_requirements(self) -> bool:
        """Validate required software and versions."""
        self.print_status("Validating software requirements...", 'info')
        
        all_passed = True
        
        for software, config in self.requirements.items():
            success, stdout, stderr = self.run_command(config['command'])
            
            if not success:
                self.print_status(f"✗ {software} not found or not working", 'error')
                self.results['failed'] += 1
                self.results['errors'].append(f"{software} not available: {stderr}")
                all_passed = False
                continue
            
            # Extract version
            version = self.parse_version(stdout, software)
            if not version:
                self.print_status(f"⚠ {software} found but version unclear: {stdout[:50]}", 'warning')
                self.results['warnings'] += 1
                continue
            
            # Check version requirement
            if self.compare_versions(version, config['min_version']):
                self.print_status(f"✓ {software} {version} (>= {config['min_version']})", 'success')
                self.results['passed'] += 1
            else:
                self.print_status(f"✗ {software} {version} < {config['min_version']} (required)", 'error')
                self.results['failed'] += 1
                self.results['errors'].append(f"{software} version {version} too old (need >= {config['min_version']})")
                all_passed = False
            
            # Store version info
            self.results['system_info'][software] = version
        
        return all_passed

    def check_port_availability(self) -> bool:
        """Check if required ports are available."""
        self.print_status("Checking port availability...", 'info')
        
        all_available = True
        
        for port in self.required_ports:
            # Check if port is in use
            success, stdout, stderr = self.run_command(['lsof', '-i', f':{port}'])
            
            if success and stdout:
                # Port is in use
                self.print_status(f"⚠ Port {port} is already in use", 'warning')
                self.print_status(f"  Process: {stdout.split()[1] if stdout.split() else 'unknown'}", 'info')
                self.results['warnings'] += 1
            else:
                # Port is available
                self.print_status(f"✓ Port {port} available", 'success')
                self.results['passed'] += 1
        
        return all_available

    def validate_project_structure(self) -> bool:
        """Validate required directories and files exist."""
        self.print_status("Validating project structure...", 'info')
        
        all_found = True
        
        for path_str in self.required_paths:
            path = Path(path_str)
            
            if path.exists():
                if path.is_dir():
                    file_count = len(list(path.rglob('*')))
                    self.print_status(f"✓ Directory {path_str} exists ({file_count} files)", 'success')
                else:
                    size = path.stat().st_size
                    self.print_status(f"✓ File {path_str} exists ({size} bytes)", 'success')
                self.results['passed'] += 1
            else:
                self.print_status(f"✗ Missing: {path_str}", 'error')
                self.results['failed'] += 1
                self.results['errors'].append(f"Missing required path: {path_str}")
                all_found = False
        
        return all_found

    def validate_docker_setup(self) -> bool:
        """Validate Docker setup and services."""
        self.print_status("Validating Docker setup...", 'info')
        
        try:
            # Test Docker connection
            client = docker.from_env()
            
            # Check if Docker daemon is running
            client.ping()
            self.print_status("✓ Docker daemon is running", 'success')
            self.results['passed'] += 1
            
            # Check docker-compose.yml
            if not Path('docker-compose.yml').exists():
                self.print_status("✗ docker-compose.yml not found", 'error')
                self.results['failed'] += 1
                return False
            
            # Validate docker-compose configuration
            success, stdout, stderr = self.run_command(['docker-compose', 'config'])
            if success:
                self.print_status("✓ docker-compose.yml is valid", 'success')
                self.results['passed'] += 1
            else:
                self.print_status(f"✗ docker-compose.yml has errors: {stderr}", 'error')
                self.results['failed'] += 1
                self.results['errors'].append(f"Docker compose config error: {stderr}")
                return False
            
            # Check for existing containers
            containers = client.containers.list(all=True)
            kgl_containers = [c for c in containers if 'kgl' in c.name or 'knowledge-graph-lab' in c.name]
            
            if kgl_containers:
                self.print_status(f"⚠ Found {len(kgl_containers)} existing KGL containers", 'warning')
                for container in kgl_containers:
                    self.print_status(f"  • {container.name} ({container.status})", 'info')
                self.results['warnings'] += 1
            else:
                self.print_status("✓ No conflicting containers found", 'success')
                self.results['passed'] += 1
            
            return True
            
        except docker.errors.DockerException as e:
            self.print_status(f"✗ Docker error: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"Docker error: {str(e)}")
            return False
        except Exception as e:
            self.print_status(f"✗ Docker validation error: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"Docker validation error: {str(e)}")
            return False

    def check_python_dependencies(self) -> bool:
        """Check Python dependencies and virtual environment."""
        self.print_status("Checking Python environment...", 'info')
        
        # Check if we're in a virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.print_status("✓ Running in virtual environment", 'success')
            self.results['passed'] += 1
        else:
            self.print_status("⚠ Not running in virtual environment", 'warning')
            self.results['warnings'] += 1
        
        # Check important Python packages
        important_packages = ['aiohttp', 'psycopg2', 'redis', 'docker']
        
        for package in important_packages:
            try:
                __import__(package)
                self.print_status(f"✓ Python package '{package}' available", 'success')
                self.results['passed'] += 1
            except ImportError:
                self.print_status(f"⚠ Python package '{package}' not available", 'warning')
                self.results['warnings'] += 1
        
        return True

    def check_environment_variables(self) -> bool:
        """Check environment variables and configuration."""
        self.print_status("Checking environment configuration...", 'info')
        
        # Check for .env file
        if Path('.env').exists():
            self.print_status("✓ .env file exists", 'success')
            self.results['passed'] += 1
        else:
            if Path('.env.example').exists():
                self.print_status("⚠ .env file missing, but .env.example exists", 'warning')
                self.print_status("  → Copy .env.example to .env and configure", 'info')
                self.results['warnings'] += 1
            else:
                self.print_status("✗ No environment configuration found", 'error')
                self.results['failed'] += 1
                return False
        
        # Check important environment variables
        important_vars = ['NODE_ENV', 'DATABASE_URL', 'REDIS_URL']
        
        for var in important_vars:
            if os.getenv(var):
                self.print_status(f"✓ Environment variable {var} is set", 'success')
                self.results['passed'] += 1
            else:
                self.print_status(f"⚠ Environment variable {var} not set", 'warning')
                self.results['warnings'] += 1
        
        return True

    def check_disk_space(self) -> bool:
        """Check available disk space."""
        self.print_status("Checking disk space...", 'info')
        
        try:
            # Get current directory disk usage
            total, used, free = shutil.disk_usage('.')
            
            free_gb = free // (1024**3)
            total_gb = total // (1024**3)
            
            self.print_status(f"Disk space: {free_gb}GB free of {total_gb}GB total", 'info')
            
            if free_gb > 10:  # At least 10GB free
                self.print_status("✓ Sufficient disk space available", 'success')
                self.results['passed'] += 1
            elif free_gb > 5:  # 5-10GB
                self.print_status("⚠ Limited disk space (5-10GB free)", 'warning')
                self.results['warnings'] += 1
            else:  # Less than 5GB
                self.print_status("✗ Low disk space (<5GB free)", 'error')
                self.results['failed'] += 1
                self.results['errors'].append("Insufficient disk space")
                return False
            
            return True
            
        except Exception as e:
            self.print_status(f"⚠ Could not check disk space: {str(e)}", 'warning')
            self.results['warnings'] += 1
            return True

    def run_all_validations(self) -> bool:
        """Run all environment validations."""
        self.print_status(f"{Colors.BOLD}Starting Environment Validation{Colors.END}", 'info')
        
        validation_results = []
        
        # Run all validation checks
        validation_results.append(self.validate_software_requirements())
        validation_results.append(self.check_port_availability())
        validation_results.append(self.validate_project_structure())
        validation_results.append(self.validate_docker_setup())
        validation_results.append(self.check_python_dependencies())
        validation_results.append(self.check_environment_variables())
        validation_results.append(self.check_disk_space())
        
        return all(validation_results)

    def print_summary(self):
        """Print validation results summary."""
        total_checks = self.results['passed'] + self.results['failed'] + self.results['warnings']
        
        print(f"\n{Colors.BOLD}=== Environment Validation Summary ==={Colors.END}")
        print(f"Total checks: {total_checks}")
        print(f"{Colors.GREEN}Passed: {self.results['passed']}{Colors.END}")
        print(f"{Colors.YELLOW}Warnings: {self.results['warnings']}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.results['failed']}{Colors.END}")
        
        if self.results['system_info']:
            print(f"\n{Colors.BLUE}System Information:{Colors.END}")
            for software, version in self.results['system_info'].items():
                print(f"  • {software}: {version}")
        
        if self.results['errors']:
            print(f"\n{Colors.RED}Critical Issues:{Colors.END}")
            for error in self.results['errors']:
                print(f"  • {error}")
        
        if self.results['failed'] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Environment validation passed!{Colors.END}")
            print(f"\n{Colors.BLUE}Ready to proceed:{Colors.END}")
            print(f"  • Run 'docker-compose up -d' to start services")
            print(f"  • Run 'python shared/db/init_db.py' to initialize database")
            print(f"  • Run 'python scripts/health_check.py' to verify system")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Environment validation failed.{Colors.END}")
            print(f"\n{Colors.YELLOW}Required actions:{Colors.END}")
            print(f"  • Fix critical issues listed above")
            print(f"  • Install missing software or update versions")
            print(f"  • Resolve port conflicts if any")

def main():
    """Main validation function."""
    validator = EnvironmentValidator()
    
    try:
        success = validator.run_all_validations()
        validator.print_summary()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        validator.print_status("\nValidation interrupted by user", 'warning')
        return 1
    except Exception as e:
        validator.print_status(f"Unexpected error: {str(e)}", 'error')
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)