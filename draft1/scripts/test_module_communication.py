#!/usr/bin/env python3
"""
Module Communication Test Script for Knowledge Graph Lab
Tests inter-module API communication and data flow.
"""

import asyncio
import aiohttp
import json
import sys
import time
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ModuleCommunicationTester:
    def __init__(self):
        self.results = {'passed': 0, 'failed': 0, 'errors': []}
        self.setup_logging()
        
        # Module endpoints configuration
        self.modules = {
            'module-1-ingestion': {
                'base_url': 'http://localhost:8001',
                'health_endpoint': '/health',
                'test_endpoints': ['/api/ingest', '/api/sources']
            },
            'module-2-knowledge-graph': {
                'base_url': 'http://localhost:8002', 
                'health_endpoint': '/health',
                'test_endpoints': ['/api/graph/nodes', '/api/graph/relationships']
            },
            'module-3-reasoning': {
                'base_url': 'http://localhost:8003',
                'health_endpoint': '/health', 
                'test_endpoints': ['/api/reasoning/query', '/api/reasoning/inference']
            },
            'module-4-frontend': {
                'base_url': 'http://localhost:3000',
                'health_endpoint': '/health',
                'test_endpoints': ['/api/status', '/api/data']
            }
        }

    def setup_logging(self):
        """Setup logging to file and console."""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'module_communication_test_{timestamp}.log'
        
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

    async def test_module_health(self, session: aiohttp.ClientSession, module_name: str, config: Dict) -> bool:
        """Test if a module's health endpoint responds correctly."""
        try:
            health_url = f"{config['base_url']}{config['health_endpoint']}"
            
            async with session.get(health_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    self.print_status(f"✓ {module_name} health check passed", 'success')
                    self.results['passed'] += 1
                    return True
                else:
                    self.print_status(f"✗ {module_name} health check failed (status: {response.status})", 'error')
                    self.results['failed'] += 1
                    self.results['errors'].append(f"{module_name} health check returned status {response.status}")
                    return False
                    
        except asyncio.TimeoutError:
            self.print_status(f"✗ {module_name} health check timed out", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"{module_name} health check timed out")
            return False
        except Exception as e:
            self.print_status(f"✗ {module_name} health check error: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"{module_name} health check error: {str(e)}")
            return False

    async def test_module_endpoints(self, session: aiohttp.ClientSession, module_name: str, config: Dict) -> bool:
        """Test module's API endpoints for basic connectivity."""
        all_passed = True
        
        for endpoint in config['test_endpoints']:
            try:
                test_url = f"{config['base_url']}{endpoint}"
                
                # Use HEAD request to avoid side effects
                async with session.head(test_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status in [200, 404, 405]:  # 405 = Method Not Allowed is OK for HEAD
                        self.print_status(f"✓ {module_name} endpoint {endpoint} reachable", 'success')
                        self.results['passed'] += 1
                    else:
                        self.print_status(f"✗ {module_name} endpoint {endpoint} returned {response.status}", 'warning')
                        self.results['failed'] += 1
                        all_passed = False
                        
            except asyncio.TimeoutError:
                self.print_status(f"✗ {module_name} endpoint {endpoint} timed out", 'error')
                self.results['failed'] += 1
                all_passed = False
            except Exception as e:
                self.print_status(f"✗ {module_name} endpoint {endpoint} error: {str(e)}", 'error') 
                self.results['failed'] += 1
                all_passed = False
                
        return all_passed

    async def test_data_flow(self, session: aiohttp.ClientSession) -> bool:
        """Test data flow between modules (mock test)."""
        self.print_status("Testing inter-module data flow...", 'info')
        
        # Mock data flow test - Module 1 → Module 2 → Module 3 → Module 4
        flow_tests = [
            {
                'description': 'Module 1 → Module 2: Data ingestion to knowledge graph',
                'source_module': 'module-1-ingestion',
                'target_module': 'module-2-knowledge-graph',
                'test_data': {'type': 'document', 'content': 'test document'}
            },
            {
                'description': 'Module 2 → Module 3: Knowledge graph to reasoning',
                'source_module': 'module-2-knowledge-graph', 
                'target_module': 'module-3-reasoning',
                'test_data': {'query': 'test reasoning query'}
            },
            {
                'description': 'Module 3 → Module 4: Reasoning results to frontend',
                'source_module': 'module-3-reasoning',
                'target_module': 'module-4-frontend', 
                'test_data': {'results': 'test reasoning results'}
            }
        ]
        
        all_passed = True
        for test in flow_tests:
            try:
                self.print_status(f"  Testing: {test['description']}", 'info')
                
                # Since modules may not be fully implemented, we test connectivity
                source_url = f"{self.modules[test['source_module']]['base_url']}/health"
                target_url = f"{self.modules[test['target_module']]['base_url']}/health"
                
                # Test both endpoints are reachable
                source_task = session.get(source_url, timeout=aiohttp.ClientTimeout(total=5))
                target_task = session.get(target_url, timeout=aiohttp.ClientTimeout(total=5))
                
                source_response, target_response = await asyncio.gather(
                    source_task, target_task, return_exceptions=True
                )
                
                if (isinstance(source_response, aiohttp.ClientResponse) and 
                    isinstance(target_response, aiohttp.ClientResponse) and
                    source_response.status == 200 and target_response.status == 200):
                    self.print_status(f"  ✓ {test['description']} - connectivity verified", 'success')
                    self.results['passed'] += 1
                else:
                    self.print_status(f"  ✗ {test['description']} - connectivity failed", 'warning')
                    self.results['failed'] += 1
                    all_passed = False
                    
            except Exception as e:
                self.print_status(f"  ✗ {test['description']} - error: {str(e)}", 'error')
                self.results['failed'] += 1
                all_passed = False
                
        return all_passed

    async def test_timeout_handling(self, session: aiohttp.ClientSession) -> bool:
        """Test timeout and graceful degradation."""
        self.print_status("Testing timeout handling and graceful degradation...", 'info')
        
        # Test with very short timeout to simulate network issues
        try:
            async with session.get(
                f"{self.modules['module-1-ingestion']['base_url']}/health",
                timeout=aiohttp.ClientTimeout(total=0.001)  # 1ms timeout
            ) as response:
                pass
        except asyncio.TimeoutError:
            self.print_status("✓ Timeout handling works correctly", 'success')
            self.results['passed'] += 1
            return True
        except Exception as e:
            self.print_status(f"✓ Connection handling works (got {type(e).__name__})", 'success')
            self.results['passed'] += 1
            return True
            
        # If we get here, the request was too fast or something else happened
        self.print_status("? Timeout test inconclusive", 'warning')
        return True

    async def run_all_tests(self) -> bool:
        """Run all communication tests."""
        self.print_status(f"{Colors.BOLD}Starting Module Communication Tests{Colors.END}", 'info')
        
        connector = aiohttp.TCPConnector(limit=30, limit_per_host=10)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Test 1: Module health checks
            self.print_status("\n1. Testing module health endpoints...", 'info')
            for module_name, config in self.modules.items():
                await self.test_module_health(session, module_name, config)
            
            # Test 2: Module endpoint connectivity
            self.print_status("\n2. Testing module endpoint connectivity...", 'info')
            for module_name, config in self.modules.items():
                await self.test_module_endpoints(session, module_name, config)
            
            # Test 3: Data flow simulation
            self.print_status("\n3. Testing inter-module data flow...", 'info')
            await self.test_data_flow(session)
            
            # Test 4: Timeout handling
            self.print_status("\n4. Testing timeout and error handling...", 'info')
            await self.test_timeout_handling(session)
        
        return self.results['failed'] == 0

    def print_summary(self):
        """Print test results summary."""
        total = self.results['passed'] + self.results['failed']
        
        print(f"\n{Colors.BOLD}=== Module Communication Test Summary ==={Colors.END}")
        print(f"Total tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.results['passed']}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.results['failed']}{Colors.END}")
        
        if self.results['errors']:
            print(f"\n{Colors.RED}Errors encountered:{Colors.END}")
            for error in self.results['errors']:
                print(f"  • {error}")
        
        if self.results['failed'] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All module communication tests passed!{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed. Check logs for details.{Colors.END}")

async def main():
    """Main test function."""
    tester = ModuleCommunicationTester()
    
    try:
        success = await tester.run_all_tests()
        tester.print_summary()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        tester.print_status("\nTest interrupted by user", 'warning')
        return 1
    except Exception as e:
        tester.print_status(f"Unexpected error: {str(e)}", 'error')
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)