#!/usr/bin/env python3
"""
System Health Check Script for Knowledge Graph Lab
Validates that all services are running and responding correctly.
"""

import asyncio
import aiohttp
import docker
import sys
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json
import os

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class HealthCheckResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []
        self.warnings_list = []
        self.service_status = {}
    
    def pass_check(self, service: str, message: str):
        print(f"{Colors.GREEN}✅ {service}: {message}{Colors.END}")
        self.passed += 1
        self.service_status[service] = "healthy"
    
    def fail_check(self, service: str, message: str):
        print(f"{Colors.RED}❌ {service}: {message}{Colors.END}")
        self.failed += 1
        self.errors.append(f"{service}: {message}")
        self.service_status[service] = "unhealthy"
    
    def warn_check(self, service: str, message: str):
        print(f"{Colors.YELLOW}⚠️  {service}: {message}{Colors.END}")
        self.warnings += 1
        self.warnings_list.append(f"{service}: {message}")
        self.service_status[service] = "warning"
    
    def info(self, message: str):
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

async def check_docker_services(result: HealthCheckResult):
    """Check Docker services are running."""
    print(f"\n{Colors.BOLD}🐳 DOCKER SERVICES CHECK{Colors.END}")
    
    try:
        client = docker.from_env()
        
        expected_services = {
            "postgres": {"port": 5432, "health_check": None},
            "redis": {"port": 6379, "health_check": None},
            "qdrant": {"port": 6333, "health_check": "http://localhost:6333/"}
        }
        
        # Get all containers
        containers = client.containers.list(all=True)
        container_map = {c.name: c for c in containers}
        
        for service_name, config in expected_services.items():
            # Look for container with service name in it
            container = None
            for name, cont in container_map.items():
                if service_name in name.lower():
                    container = cont
                    break
            
            if container:
                if container.status == "running":
                    result.pass_check(service_name, f"Container running ({container.name})")
                else:
                    result.fail_check(service_name, f"Container not running: {container.status}")
            else:
                result.fail_check(service_name, "Container not found")
                
    except docker.errors.DockerException as e:
        result.fail_check("Docker", f"Docker daemon not accessible: {e}")
    except Exception as e:
        result.fail_check("Docker", f"Unexpected error: {e}")

async def check_service_ports(result: HealthCheckResult):
    """Check that services are responding on expected ports."""
    print(f"\n{Colors.BOLD}🔌 SERVICE PORT CONNECTIVITY{Colors.END}")
    
    services = {
        "PostgreSQL": ("localhost", 5432),
        "Redis": ("localhost", 6379),
        "Qdrant": ("localhost", 6333)
    }
    
    for service_name, (host, port) in services.items():
        try:
            # Try to connect to the port
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5 second timeout
            result_code = sock.connect_ex((host, port))
            sock.close()
            
            if result_code == 0:
                result.pass_check(service_name, f"Port {port} is open and accepting connections")
            else:
                result.fail_check(service_name, f"Port {port} is not accessible")
                
        except Exception as e:
            result.fail_check(service_name, f"Error checking port {port}: {e}")

async def check_http_services(result: HealthCheckResult):
    """Check HTTP-based services."""
    print(f"\n{Colors.BOLD}🌐 HTTP SERVICES CHECK{Colors.END}")
    
    http_services = {
        "Qdrant Vector DB": "http://localhost:6333/",
        "MailHog (Dev Email)": "http://localhost:8025/"
    }
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        for service_name, url in http_services.items():
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        result.pass_check(service_name, f"HTTP service responding (200 OK)")
                    else:
                        result.warn_check(service_name, f"HTTP service responding but status {response.status}")
                        
            except aiohttp.ClientConnectorError:
                result.fail_check(service_name, f"Cannot connect to {url}")
            except asyncio.TimeoutError:
                result.fail_check(service_name, f"Timeout connecting to {url}")
            except Exception as e:
                result.fail_check(service_name, f"Error: {e}")

async def check_api_endpoints(result: HealthCheckResult):
    """Check module API endpoints if they exist."""
    print(f"\n{Colors.BOLD}🚀 MODULE API ENDPOINTS{Colors.END}")
    
    # Enhanced module endpoints with additional paths to test
    module_endpoints = {
        "Module 1 Ingestion": {
            "health": "http://localhost:8001/health",
            "api_paths": ["http://localhost:8001/api/ingest", "http://localhost:8001/api/sources"]
        },
        "Module 2 Knowledge Graph": {
            "health": "http://localhost:8002/health",
            "api_paths": ["http://localhost:8002/api/graph/nodes", "http://localhost:8002/api/graph/relationships"]
        },
        "Module 3 Reasoning": {
            "health": "http://localhost:8003/health",
            "api_paths": ["http://localhost:8003/api/reasoning/query", "http://localhost:8003/api/reasoning/inference"]
        },
        "Module 4 Frontend": {
            "health": "http://localhost:3000/health",
            "api_paths": ["http://localhost:3000/api/status", "http://localhost:3000/api/data"]
        }
    }
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        for module_name, endpoints in module_endpoints.items():
            # First check health endpoint
            try:
                async with session.get(endpoints["health"]) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            status = data.get("status", "ok")
                            result.pass_check(module_name, f"Health endpoint OK (status: {status})")
                        except:
                            result.pass_check(module_name, f"Health endpoint OK (status: {response.status})")
                    else:
                        result.warn_check(module_name, f"Health endpoint status {response.status}")
                        
            except aiohttp.ClientConnectorError:
                result.warn_check(module_name, "Module not running (expected during setup)")
                continue  # Skip API path tests if module isn't running
            except asyncio.TimeoutError:
                result.warn_check(module_name, "Health check timeout (may be starting up)")
                continue
            except Exception as e:
                result.warn_check(module_name, f"Health check failed: {e}")
                continue
            
            # Test API endpoints connectivity (using HEAD to avoid side effects)
            api_reachable = 0
            total_apis = len(endpoints["api_paths"])
            
            for api_path in endpoints["api_paths"]:
                try:
                    async with session.head(api_path, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        if response.status in [200, 404, 405]:  # 405 = Method Not Allowed is OK for HEAD
                            api_reachable += 1
                except:
                    pass  # API not ready, that's expected
            
            if api_reachable == total_apis:
                result.pass_check(f"{module_name} APIs", f"All {total_apis} API endpoints reachable")
            elif api_reachable > 0:
                result.warn_check(f"{module_name} APIs", f"{api_reachable}/{total_apis} API endpoints reachable")
            else:
                result.warn_check(f"{module_name} APIs", "API endpoints not ready (expected during setup)")

def check_environment_setup(result: HealthCheckResult):
    """Check local environment setup."""
    print(f"\n{Colors.BOLD}🛠️  ENVIRONMENT SETUP CHECK{Colors.END}")
    
    # Check Python version
    try:
        python_version = sys.version_info
        if python_version >= (3, 11):
            result.pass_check("Python", f"Version {python_version.major}.{python_version.minor}.{python_version.micro} (✓ 3.11+)")
        else:
            result.fail_check("Python", f"Version {python_version.major}.{python_version.minor}.{python_version.micro} (need 3.11+)")
    except Exception as e:
        result.fail_check("Python", f"Error checking version: {e}")
    
    # Check Node.js if available
    try:
        node_result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if node_result.returncode == 0:
            version = node_result.stdout.strip()
            major_version = int(version.split('.')[0].replace('v', ''))
            if major_version >= 20:
                result.pass_check("Node.js", f"{version} (✓ 20+)")
            else:
                result.warn_check("Node.js", f"{version} (recommend 20+)")
        else:
            result.warn_check("Node.js", "Not found (needed for Module 4)")
    except Exception as e:
        result.warn_check("Node.js", f"Error checking: {e}")
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        result.pass_check("Virtual Environment", "Active Python virtual environment detected")
    else:
        result.warn_check("Virtual Environment", "No virtual environment detected (recommended)")
    
    # Check critical environment variables
    env_vars = {
        "DATABASE_URL": False,
        "OPENAI_API_KEY": False,
        "ANTHROPIC_API_KEY": False
    }
    
    for var, required in env_vars.items():
        if os.getenv(var):
            value = os.getenv(var)
            # Mask secrets for display
            if "key" in var.lower():
                display_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "set"
            else:
                display_value = value
            result.pass_check("Environment", f"{var}={display_value}")
        elif required:
            result.fail_check("Environment", f"Missing required variable: {var}")
        else:
            result.warn_check("Environment", f"Optional variable not set: {var}")

def check_file_permissions(result: HealthCheckResult):
    """Check file permissions for scripts."""
    print(f"\n{Colors.BOLD}📁 FILE PERMISSIONS CHECK{Colors.END}")
    
    project_root = Path(__file__).parent.parent
    
    executable_files = [
        "scripts/validate_repository.py",
        "scripts/health_check.py"
    ]
    
    for file_path in executable_files:
        full_path = project_root / file_path
        if full_path.exists():
            if os.access(full_path, os.X_OK):
                result.pass_check("Permissions", f"{file_path} is executable")
            else:
                result.warn_check("Permissions", f"{file_path} not executable (run: chmod +x {file_path})")
        else:
            result.warn_check("Permissions", f"{file_path} not found")

def check_database_connectivity(result: HealthCheckResult):
    """Check database connectivity with actual queries."""
    print(f"\n{Colors.BOLD}🗄️  DATABASE CONNECTIVITY{Colors.END}")
    
    try:
        import psycopg2
        
        # Try to connect to PostgreSQL
        conn_params = {
            "host": "localhost",
            "port": 5432,
            "database": "postgres",  # Default database
            "user": "postgres",
            "password": "postgres"
        }
        
        try:
            conn = psycopg2.connect(**conn_params)
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            result.pass_check("PostgreSQL", f"Connected successfully - {version[:50]}...")
            cursor.close()
            conn.close()
        except psycopg2.OperationalError as e:
            result.fail_check("PostgreSQL", f"Connection failed: {e}")
        
    except ImportError:
        result.warn_check("PostgreSQL", "psycopg2 not installed (pip install psycopg2-binary)")
    
    try:
        import redis
        
        # Try to connect to Redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        info = r.info()
        result.pass_check("Redis", f"Connected successfully - version {info.get('redis_version')}")
        
    except ImportError:
        result.warn_check("Redis", "redis package not installed (pip install redis)")
    except redis.ConnectionError as e:
        result.fail_check("Redis", f"Connection failed: {e}")

def print_health_summary(result: HealthCheckResult):
    """Print health check summary."""
    print(f"\n{Colors.BOLD}🏥 HEALTH CHECK SUMMARY{Colors.END}")
    print(f"{'='*60}")
    
    total_checks = result.passed + result.failed + result.warnings
    
    print(f"{Colors.GREEN}✅ Healthy: {result.passed}{Colors.END}")
    print(f"{Colors.RED}❌ Unhealthy: {result.failed}{Colors.END}")
    print(f"{Colors.YELLOW}⚠️  Warnings: {result.warnings}{Colors.END}")
    print(f"Total Checks: {total_checks}")
    
    # Service status overview
    if result.service_status:
        print(f"\n{Colors.BOLD}Service Status Overview:{Colors.END}")
        for service, status in result.service_status.items():
            color = Colors.GREEN if status == "healthy" else Colors.RED if status == "unhealthy" else Colors.YELLOW
            print(f"  {color}• {service}: {status}{Colors.END}")
    
    # Overall assessment
    if result.failed == 0:
        if result.warnings <= 2:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 EXCELLENT! System is ready for development.{Colors.END}")
            return 0
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}✅ GOOD! System is functional with some improvements needed.{Colors.END}")
            return 0
    elif result.failed <= 2:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  PARTIAL! Some services need attention but development can proceed.{Colors.END}")
        return 1
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}🚨 CRITICAL ISSUES! Address failed checks before development.{Colors.END}")
        
        if result.errors:
            print(f"\n{Colors.RED}Critical Issues:{Colors.END}")
            for error in result.errors[:5]:  # Show first 5 errors
                print(f"  • {error}")
            if len(result.errors) > 5:
                print(f"  ... and {len(result.errors) - 5} more issues")
        
        return 2

async def main():
    """Main health check function."""
    print(f"{Colors.BOLD}{Colors.BLUE}🔍 Knowledge Graph Lab System Health Check{Colors.END}")
    print(f"Checking all services and dependencies...\n")
    
    result = HealthCheckResult()
    
    # Run all health checks
    await check_docker_services(result)
    await check_service_ports(result)
    await check_http_services(result)
    await check_api_endpoints(result)
    check_environment_setup(result)
    check_file_permissions(result)
    check_database_connectivity(result)
    
    # Additional comprehensive checks
    result.info("Running additional test infrastructure checks...")
    
    # Check if our new test scripts exist and are executable
    test_scripts = [
        "scripts/test_module_communication.py",
        "scripts/seed_data.py", 
        "scripts/validate_environment.py",
        "shared/db/test_connection.py",
        "shared/db/init_db.py"
    ]
    
    for script in test_scripts:
        script_path = Path(script)
        if script_path.exists():
            if os.access(script_path, os.X_OK):
                result.pass_check("Test Infrastructure", f"{script} ready")
            else:
                result.warn_check("Test Infrastructure", f"{script} not executable (chmod +x {script})")
        else:
            result.fail_check("Test Infrastructure", f"Missing: {script}")
    
    # Quick test of database connection if available
    try:
        import psycopg2
        test_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'kgl_database', 
            'user': 'kgl_user',
            'password': 'kgl_password'
        }
        
        conn = psycopg2.connect(**test_config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        result.pass_check("Database Integration", "PostgreSQL connection successful")
    except Exception as e:
        result.warn_check("Database Integration", f"PostgreSQL test failed: {str(e)[:50]}")
    
    # Test Redis connection if available
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        result.pass_check("Cache Integration", "Redis connection successful")
    except Exception as e:
        result.warn_check("Cache Integration", f"Redis test failed: {str(e)[:50]}")
        
    # Test Qdrant connection if available
    try:
        import requests
        response = requests.get("http://localhost:6333/health", timeout=5)
        if response.status_code == 200:
            result.pass_check("Vector DB Integration", "Qdrant connection successful")
        else:
            result.warn_check("Vector DB Integration", f"Qdrant returned status {response.status_code}")
    except Exception as e:
        result.warn_check("Vector DB Integration", f"Qdrant test failed: {str(e)[:50]}")
    
    # Print summary and exit with appropriate code
    exit_code = print_health_summary(result)
    
    # Save results for automation
    health_report = {
        "timestamp": time.time(),
        "passed": result.passed,
        "failed": result.failed,
        "warnings": result.warnings,
        "service_status": result.service_status,
        "overall_status": "healthy" if exit_code == 0 else "degraded" if exit_code == 1 else "critical"
    }
    
    # Save to file for monitoring
    try:
        with open("health_check_results.json", "w") as f:
            json.dump(health_report, f, indent=2)
        result.info("Health check results saved to health_check_results.json")
    except Exception as e:
        result.warn_check("Logging", f"Could not save results: {e}")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    asyncio.run(main())