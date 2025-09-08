#!/usr/bin/env python3
"""
Database Connection Test Script for Knowledge Graph Lab
Tests connectivity to all database services (PostgreSQL, Redis, Qdrant).
"""

import psycopg2
import redis
import requests
import sys
import time
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, Tuple, Optional

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class DatabaseConnectionTester:
    def __init__(self):
        self.results = {'passed': 0, 'failed': 0, 'warnings': 0}
        self.setup_logging()
        
        # Database configurations
        self.postgres_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'kgl_database',
            'user': 'kgl_user',
            'password': 'kgl_password'
        }
        
        self.redis_config = {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }
        
        self.qdrant_config = {
            'host': 'localhost',
            'port': 6333
        }

    def setup_logging(self):
        """Setup logging to file and console."""
        log_dir = Path('../logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'db_connection_test_{timestamp}.log'
        
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

    def test_postgres_connection(self) -> Tuple[bool, Dict]:
        """Test PostgreSQL database connection and basic operations."""
        self.print_status("Testing PostgreSQL connection...", 'info')
        
        connection_info = {
            'connected': False,
            'version': None,
            'database': None,
            'tables_count': 0,
            'response_time': None
        }
        
        try:
            start_time = time.time()
            
            # Test connection
            conn = psycopg2.connect(**self.postgres_config)
            cursor = conn.cursor()
            
            # Test basic query
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            connection_info['version'] = version.split(' ')[1]  # Extract version number
            
            # Get database info
            cursor.execute("SELECT current_database();")
            connection_info['database'] = cursor.fetchone()[0]
            
            # Count tables
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            connection_info['tables_count'] = cursor.fetchone()[0]
            
            # Test write operation
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS connection_test (
                    id SERIAL PRIMARY KEY,
                    test_time TIMESTAMP DEFAULT NOW()
                );
            """)
            
            cursor.execute("INSERT INTO connection_test (test_time) VALUES (NOW());")
            
            # Test read operation
            cursor.execute("SELECT COUNT(*) FROM connection_test;")
            test_records = cursor.fetchone()[0]
            
            # Cleanup
            cursor.execute("DROP TABLE IF EXISTS connection_test;")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            connection_info['connected'] = True
            connection_info['response_time'] = round((time.time() - start_time) * 1000, 2)
            
            self.print_status(f"✓ PostgreSQL connection successful", 'success')
            self.print_status(f"  Version: {connection_info['version']}", 'info')
            self.print_status(f"  Database: {connection_info['database']}", 'info')
            self.print_status(f"  Tables: {connection_info['tables_count']}", 'info')
            self.print_status(f"  Response time: {connection_info['response_time']}ms", 'info')
            self.print_status(f"  Read/Write test: {test_records} records handled", 'info')
            
            self.results['passed'] += 1
            return True, connection_info
            
        except psycopg2.OperationalError as e:
            error_msg = str(e).strip()
            self.print_status(f"✗ PostgreSQL connection failed: {error_msg}", 'error')
            if "could not connect" in error_msg.lower():
                self.print_status("  → Check if PostgreSQL service is running", 'warning')
                self.print_status("  → Try: docker-compose up postgres", 'warning')
            self.results['failed'] += 1
            return False, connection_info
            
        except psycopg2.Error as e:
            self.print_status(f"✗ PostgreSQL error: {str(e)}", 'error')
            self.results['failed'] += 1
            return False, connection_info
            
        except Exception as e:
            self.print_status(f"✗ Unexpected PostgreSQL error: {str(e)}", 'error')
            self.results['failed'] += 1
            return False, connection_info

    def test_redis_connection(self) -> Tuple[bool, Dict]:
        """Test Redis connection and basic operations."""
        self.print_status("Testing Redis connection...", 'info')
        
        connection_info = {
            'connected': False,
            'version': None,
            'memory_used': None,
            'response_time': None
        }
        
        try:
            start_time = time.time()
            
            # Test connection
            r = redis.Redis(**self.redis_config)
            
            # Test ping
            r.ping()
            
            # Get server info
            info = r.info()
            connection_info['version'] = info['redis_version']
            connection_info['memory_used'] = f"{info['used_memory_human']}"
            
            # Test basic operations
            test_key = 'connection_test'
            test_value = f'test_{int(time.time())}'
            
            # Write test
            r.set(test_key, test_value, ex=60)  # Expire in 60 seconds
            
            # Read test
            retrieved_value = r.get(test_key).decode('utf-8')
            
            if retrieved_value != test_value:
                raise Exception("Read/write test failed")
            
            # Test list operations
            list_key = 'connection_test_list'
            r.lpush(list_key, 'item1', 'item2', 'item3')
            list_length = r.llen(list_key)
            
            # Cleanup
            r.delete(test_key, list_key)
            
            connection_info['connected'] = True
            connection_info['response_time'] = round((time.time() - start_time) * 1000, 2)
            
            self.print_status(f"✓ Redis connection successful", 'success')
            self.print_status(f"  Version: {connection_info['version']}", 'info')
            self.print_status(f"  Memory used: {connection_info['memory_used']}", 'info')
            self.print_status(f"  Response time: {connection_info['response_time']}ms", 'info')
            self.print_status(f"  Read/Write test: successful", 'info')
            self.print_status(f"  List operations: {list_length} items handled", 'info')
            
            self.results['passed'] += 1
            return True, connection_info
            
        except redis.ConnectionError as e:
            self.print_status(f"✗ Redis connection failed: {str(e)}", 'error')
            self.print_status("  → Check if Redis service is running", 'warning')
            self.print_status("  → Try: docker-compose up redis", 'warning')
            self.results['failed'] += 1
            return False, connection_info
            
        except redis.RedisError as e:
            self.print_status(f"✗ Redis error: {str(e)}", 'error')
            self.results['failed'] += 1
            return False, connection_info
            
        except Exception as e:
            self.print_status(f"✗ Unexpected Redis error: {str(e)}", 'error')
            self.results['failed'] += 1
            return False, connection_info

    def test_qdrant_connection(self) -> Tuple[bool, Dict]:
        """Test Qdrant vector database connection and basic operations."""
        self.print_status("Testing Qdrant connection...", 'info')
        
        connection_info = {
            'connected': False,
            'version': None,
            'collections_count': 0,
            'response_time': None
        }
        
        try:
            start_time = time.time()
            
            qdrant_url = f"http://{self.qdrant_config['host']}:{self.qdrant_config['port']}"
            
            # Test health endpoint
            health_response = requests.get(f"{qdrant_url}/health", timeout=10)
            if health_response.status_code != 200:
                raise Exception(f"Health check failed with status {health_response.status_code}")
            
            # Get version info (if available)
            try:
                metrics_response = requests.get(f"{qdrant_url}/metrics", timeout=5)
                if metrics_response.status_code == 200:
                    # Parse version from metrics (basic approach)
                    connection_info['version'] = "Available"
            except:
                connection_info['version'] = "Unknown"
            
            # List collections
            collections_response = requests.get(f"{qdrant_url}/collections", timeout=10)
            if collections_response.status_code == 200:
                collections = collections_response.json()
                connection_info['collections_count'] = len(collections.get('result', {}).get('collections', []))
            
            # Test collection operations
            test_collection = 'connection_test'
            
            # Create test collection
            collection_config = {
                "vectors": {
                    "size": 4,  # Small vector for test
                    "distance": "Cosine"
                }
            }
            
            create_response = requests.put(
                f"{qdrant_url}/collections/{test_collection}",
                json=collection_config,
                timeout=10
            )
            
            if create_response.status_code not in [200, 409]:  # 409 = already exists
                raise Exception(f"Failed to create test collection: {create_response.status_code}")
            
            # Test vector upsert
            test_point = {
                "points": [{
                    "id": 1,
                    "vector": [0.1, 0.2, 0.3, 0.4],
                    "payload": {"test": "connection_test"}
                }]
            }
            
            upsert_response = requests.put(
                f"{qdrant_url}/collections/{test_collection}/points",
                json=test_point,
                timeout=10
            )
            
            if upsert_response.status_code != 200:
                raise Exception(f"Failed to upsert test vector: {upsert_response.status_code}")
            
            # Test search
            search_query = {
                "vector": [0.1, 0.2, 0.3, 0.4],
                "top": 1
            }
            
            search_response = requests.post(
                f"{qdrant_url}/collections/{test_collection}/points/search",
                json=search_query,
                timeout=10
            )
            
            if search_response.status_code != 200:
                raise Exception(f"Search test failed: {search_response.status_code}")
            
            search_results = search_response.json()
            if not search_results.get('result'):
                raise Exception("Search returned no results")
            
            # Cleanup - delete test collection
            delete_response = requests.delete(f"{qdrant_url}/collections/{test_collection}", timeout=10)
            # Don't fail if cleanup fails
            
            connection_info['connected'] = True
            connection_info['response_time'] = round((time.time() - start_time) * 1000, 2)
            
            self.print_status(f"✓ Qdrant connection successful", 'success')
            self.print_status(f"  Version: {connection_info['version']}", 'info')
            self.print_status(f"  Collections: {connection_info['collections_count']}", 'info')
            self.print_status(f"  Response time: {connection_info['response_time']}ms", 'info')
            self.print_status(f"  Vector operations: successful", 'info')
            
            self.results['passed'] += 1
            return True, connection_info
            
        except requests.ConnectionError as e:
            self.print_status(f"✗ Qdrant connection failed: {str(e)}", 'error')
            self.print_status("  → Check if Qdrant service is running", 'warning')
            self.print_status("  → Try: docker-compose up qdrant", 'warning')
            self.results['failed'] += 1
            return False, connection_info
            
        except requests.RequestException as e:
            self.print_status(f"✗ Qdrant request error: {str(e)}", 'error')
            self.results['failed'] += 1
            return False, connection_info
            
        except Exception as e:
            self.print_status(f"✗ Unexpected Qdrant error: {str(e)}", 'error')
            self.results['failed'] += 1
            return False, connection_info

    def run_all_tests(self) -> bool:
        """Run all database connection tests."""
        self.print_status(f"{Colors.BOLD}Starting Database Connection Tests{Colors.END}", 'info')
        
        all_results = {}
        
        # Test PostgreSQL
        postgres_success, postgres_info = self.test_postgres_connection()
        all_results['postgres'] = postgres_info
        
        # Test Redis
        redis_success, redis_info = self.test_redis_connection()
        all_results['redis'] = redis_info
        
        # Test Qdrant
        qdrant_success, qdrant_info = self.test_qdrant_connection()
        all_results['qdrant'] = qdrant_info
        
        return all([postgres_success, redis_success, qdrant_success])

    def print_summary(self):
        """Print test results summary."""
        total = self.results['passed'] + self.results['failed']
        
        print(f"\n{Colors.BOLD}=== Database Connection Test Summary ==={Colors.END}")
        print(f"Total tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.results['passed']}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.results['failed']}{Colors.END}")
        
        if self.results['failed'] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All database connections successful!{Colors.END}")
            print(f"\n{Colors.BLUE}Next steps:{Colors.END}")
            print(f"  • Run 'python scripts/seed_data.py' to populate databases")
            print(f"  • Run 'python shared/db/init_db.py' to initialize schemas")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Some database connections failed.{Colors.END}")
            print(f"\n{Colors.YELLOW}Troubleshooting:{Colors.END}")
            print(f"  • Ensure Docker services are running: docker-compose up -d")
            print(f"  • Check service logs: docker-compose logs <service-name>")
            print(f"  • Verify port availability: netstat -tulpn | grep <port>")

def main():
    """Main test function."""
    tester = DatabaseConnectionTester()
    
    try:
        success = tester.run_all_tests()
        tester.print_summary()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        tester.print_status("\nTest interrupted by user", 'warning')
        return 1
    except Exception as e:
        tester.print_status(f"Unexpected error: {str(e)}", 'error')
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)