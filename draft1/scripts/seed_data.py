#!/usr/bin/env python3
"""
Database Seeding Script for Knowledge Graph Lab
Loads sample data into databases for testing and development.
"""

import asyncio
import psycopg2
import redis
import requests
import json
import sys
import time
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Optional, Any
import os

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class DataSeeder:
    def __init__(self):
        self.results = {'seeded': 0, 'failed': 0, 'errors': []}
        self.setup_logging()
        
        # Database configurations
        self.db_config = {
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
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'seed_data_{timestamp}.log'
        
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

    def load_mock_data_files(self) -> Dict[str, Any]:
        """Load mock data from files."""
        mock_data = {}
        mock_data_dir = Path('mock-data')
        
        if not mock_data_dir.exists():
            self.print_status("Mock data directory not found, using built-in sample data", 'warning')
            return self.get_builtin_sample_data()
        
        try:
            # Load documents
            documents_file = mock_data_dir / 'documents.json'
            if documents_file.exists():
                with open(documents_file, 'r') as f:
                    mock_data['documents'] = json.load(f)
            
            # Load entities
            entities_file = mock_data_dir / 'entities.json'
            if entities_file.exists():
                with open(entities_file, 'r') as f:
                    mock_data['entities'] = json.load(f)
            
            # Load relationships
            relationships_file = mock_data_dir / 'relationships.json'
            if relationships_file.exists():
                with open(relationships_file, 'r') as f:
                    mock_data['relationships'] = json.load(f)
            
            if not mock_data:
                self.print_status("No mock data files found, using built-in sample data", 'warning')
                return self.get_builtin_sample_data()
                
            self.print_status(f"Loaded mock data from {len(mock_data)} files", 'success')
            return mock_data
            
        except Exception as e:
            self.print_status(f"Error loading mock data files: {str(e)}", 'error')
            return self.get_builtin_sample_data()

    def get_builtin_sample_data(self) -> Dict[str, Any]:
        """Get built-in sample data for testing."""
        return {
            'documents': [
                {
                    'id': 1,
                    'title': 'Sample Research Paper',
                    'content': 'This is a sample research paper about artificial intelligence and machine learning.',
                    'source': 'sample_source',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'id': 2,
                    'title': 'Knowledge Graph Fundamentals',
                    'content': 'Knowledge graphs represent information as a network of entities and relationships.',
                    'source': 'educational_source',
                    'created_at': datetime.now().isoformat()
                }
            ],
            'entities': [
                {
                    'id': 1,
                    'name': 'Artificial Intelligence',
                    'type': 'concept',
                    'properties': {'field': 'computer_science', 'category': 'technology'}
                },
                {
                    'id': 2,
                    'name': 'Machine Learning',
                    'type': 'concept',
                    'properties': {'field': 'computer_science', 'parent': 'artificial_intelligence'}
                },
                {
                    'id': 3,
                    'name': 'Knowledge Graph',
                    'type': 'concept',
                    'properties': {'field': 'data_science', 'category': 'data_structure'}
                }
            ],
            'relationships': [
                {
                    'id': 1,
                    'source_entity_id': 1,
                    'target_entity_id': 2,
                    'relationship_type': 'includes',
                    'properties': {'strength': 0.9}
                },
                {
                    'id': 2,
                    'source_entity_id': 3,
                    'target_entity_id': 1,
                    'relationship_type': 'related_to',
                    'properties': {'strength': 0.7}
                }
            ]
        }

    def seed_postgres(self, mock_data: Dict[str, Any]) -> bool:
        """Seed PostgreSQL database with sample data."""
        self.print_status("Seeding PostgreSQL database...", 'info')
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check if tables exist
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            if not tables:
                self.print_status("No tables found. Run database initialization first.", 'warning')
                return False
            
            # Seed documents if table exists
            if 'documents' in tables and 'documents' in mock_data:
                cursor.execute("DELETE FROM documents WHERE source LIKE 'sample_%' OR source = 'educational_source'")
                
                for doc in mock_data['documents']:
                    cursor.execute("""
                        INSERT INTO documents (title, content, source, created_at)
                        VALUES (%(title)s, %(content)s, %(source)s, %(created_at)s)
                        ON CONFLICT (title) DO NOTHING
                    """, doc)
                
                self.print_status(f"✓ Seeded {len(mock_data['documents'])} documents", 'success')
                self.results['seeded'] += len(mock_data['documents'])
            
            # Seed entities if table exists
            if 'entities' in tables and 'entities' in mock_data:
                cursor.execute("DELETE FROM entities WHERE properties->>'category' IN ('technology', 'data_structure')")
                
                for entity in mock_data['entities']:
                    cursor.execute("""
                        INSERT INTO entities (name, type, properties)
                        VALUES (%(name)s, %(type)s, %(properties)s)
                        ON CONFLICT (name, type) DO NOTHING
                    """, entity)
                
                self.print_status(f"✓ Seeded {len(mock_data['entities'])} entities", 'success')
                self.results['seeded'] += len(mock_data['entities'])
            
            # Seed relationships if table exists
            if 'relationships' in tables and 'relationships' in mock_data:
                cursor.execute("DELETE FROM relationships WHERE id IN (1, 2)")  # Remove sample data
                
                for rel in mock_data['relationships']:
                    cursor.execute("""
                        INSERT INTO relationships (source_entity_id, target_entity_id, relationship_type, properties)
                        VALUES (%(source_entity_id)s, %(target_entity_id)s, %(relationship_type)s, %(properties)s)
                        ON CONFLICT DO NOTHING
                    """, rel)
                
                self.print_status(f"✓ Seeded {len(mock_data['relationships'])} relationships", 'success')
                self.results['seeded'] += len(mock_data['relationships'])
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except psycopg2.Error as e:
            self.print_status(f"PostgreSQL seeding error: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"PostgreSQL: {str(e)}")
            return False
        except Exception as e:
            self.print_status(f"Unexpected PostgreSQL error: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"PostgreSQL unexpected: {str(e)}")
            return False

    def seed_redis(self, mock_data: Dict[str, Any]) -> bool:
        """Seed Redis with sample cache data."""
        self.print_status("Seeding Redis cache...", 'info')
        
        try:
            r = redis.Redis(**self.redis_config)
            
            # Test connection
            r.ping()
            
            # Clear existing sample data
            pattern_keys = r.keys('sample:*')
            if pattern_keys:
                r.delete(*pattern_keys)
            
            # Seed cache entries
            cache_data = {
                'sample:config': {'version': '1.0', 'environment': 'development'},
                'sample:stats': {'documents_processed': 100, 'entities_extracted': 250},
                'sample:session:user1': {'user_id': 1, 'last_active': datetime.now().isoformat()}
            }
            
            for key, value in cache_data.items():
                r.setex(key, 3600, json.dumps(value))  # Expire in 1 hour
            
            # Set some simple counters
            r.set('sample:counter:visits', 42)
            r.set('sample:counter:queries', 158)
            
            self.print_status(f"✓ Seeded {len(cache_data) + 2} Redis entries", 'success')
            self.results['seeded'] += len(cache_data) + 2
            
            return True
            
        except redis.ConnectionError as e:
            self.print_status(f"Redis connection error: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"Redis connection: {str(e)}")
            return False
        except Exception as e:
            self.print_status(f"Redis seeding error: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"Redis: {str(e)}")
            return False

    def seed_qdrant(self, mock_data: Dict[str, Any]) -> bool:
        """Seed Qdrant vector database with sample vectors."""
        self.print_status("Seeding Qdrant vector database...", 'info')
        
        try:
            qdrant_url = f"http://{self.qdrant_config['host']}:{self.qdrant_config['port']}"
            
            # Test connection
            health_response = requests.get(f"{qdrant_url}/health", timeout=10)
            if health_response.status_code != 200:
                raise Exception(f"Qdrant health check failed: {health_response.status_code}")
            
            collection_name = "sample_vectors"
            
            # Create collection if it doesn't exist
            collection_config = {
                "vectors": {
                    "size": 384,  # Standard embedding dimension
                    "distance": "Cosine"
                }
            }
            
            create_response = requests.put(
                f"{qdrant_url}/collections/{collection_name}",
                json=collection_config,
                timeout=10
            )
            
            if create_response.status_code not in [200, 409]:  # 409 = already exists
                raise Exception(f"Failed to create collection: {create_response.status_code}")
            
            # Sample vectors (384-dimensional for sentence transformers)
            import random
            sample_vectors = []
            
            for i, doc in enumerate(mock_data.get('documents', [])):
                vector = [random.uniform(-1, 1) for _ in range(384)]  # Random vector for demo
                sample_vectors.append({
                    "id": i + 1,
                    "vector": vector,
                    "payload": {
                        "title": doc['title'],
                        "content": doc['content'][:200],  # Truncate for demo
                        "source": doc['source']
                    }
                })
            
            if sample_vectors:
                upsert_response = requests.put(
                    f"{qdrant_url}/collections/{collection_name}/points",
                    json={"points": sample_vectors},
                    timeout=10
                )
                
                if upsert_response.status_code == 200:
                    self.print_status(f"✓ Seeded {len(sample_vectors)} vectors in Qdrant", 'success')
                    self.results['seeded'] += len(sample_vectors)
                    return True
                else:
                    raise Exception(f"Failed to upsert vectors: {upsert_response.status_code}")
            else:
                self.print_status("No document vectors to seed", 'warning')
                return True
            
        except requests.RequestException as e:
            self.print_status(f"Qdrant connection error: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"Qdrant connection: {str(e)}")
            return False
        except Exception as e:
            self.print_status(f"Qdrant seeding error: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"Qdrant: {str(e)}")
            return False

    def run_seeding(self) -> bool:
        """Run all database seeding operations."""
        self.print_status(f"{Colors.BOLD}Starting Database Seeding{Colors.END}", 'info')
        
        # Load mock data
        mock_data = self.load_mock_data_files()
        if not mock_data:
            self.print_status("No data to seed", 'error')
            return False
        
        success_count = 0
        total_operations = 3
        
        # Seed each database
        if self.seed_postgres(mock_data):
            success_count += 1
        
        if self.seed_redis(mock_data):
            success_count += 1
        
        if self.seed_qdrant(mock_data):
            success_count += 1
        
        return success_count == total_operations

    def print_summary(self):
        """Print seeding results summary."""
        print(f"\n{Colors.BOLD}=== Database Seeding Summary ==={Colors.END}")
        print(f"Records seeded: {self.results['seeded']}")
        print(f"{Colors.RED}Failed operations: {self.results['failed']}{Colors.END}")
        
        if self.results['errors']:
            print(f"\n{Colors.RED}Errors encountered:{Colors.END}")
            for error in self.results['errors']:
                print(f"  • {error}")
        
        if self.results['failed'] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Database seeding completed successfully!{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Some seeding operations failed. Check logs for details.{Colors.END}")

def main():
    """Main seeding function."""
    seeder = DataSeeder()
    
    try:
        success = seeder.run_seeding()
        seeder.print_summary()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        seeder.print_status("\nSeeding interrupted by user", 'warning')
        return 1
    except Exception as e:
        seeder.print_status(f"Unexpected error: {str(e)}", 'error')
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)