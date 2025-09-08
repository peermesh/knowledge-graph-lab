#!/usr/bin/env python3
"""
Database Initialization Script for Knowledge Graph Lab
Initializes database tables and schema from SQL files.
"""

import psycopg2
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

class DatabaseInitializer:
    def __init__(self):
        self.results = {'executed': 0, 'failed': 0, 'errors': []}
        self.setup_logging()
        
        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'kgl_database',
            'user': 'kgl_user',
            'password': 'kgl_password'
        }
        
        # SQL files to execute in order
        self.sql_files = [
            '../database/schema.sql',  # Basic schema
            '../database/full-schema.sql'  # Extended schema if exists
        ]

    def setup_logging(self):
        """Setup logging to file and console."""
        log_dir = Path('../logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'db_init_{timestamp}.log'
        
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

    def test_connection(self) -> bool:
        """Test database connection before initialization."""
        self.print_status("Testing database connection...", 'info')
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            self.print_status(f"✓ Database connection successful", 'success')
            self.print_status(f"  PostgreSQL version: {version.split(' ')[1]}", 'info')
            
            return True
            
        except psycopg2.Error as e:
            self.print_status(f"✗ Database connection failed: {str(e)}", 'error')
            self.print_status("  → Check if PostgreSQL service is running", 'warning')
            self.print_status("  → Try: docker-compose up postgres", 'warning')
            return False

    def get_existing_tables(self, cursor) -> List[str]:
        """Get list of existing tables."""
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        return [row[0] for row in cursor.fetchall()]

    def execute_sql_file(self, cursor, sql_file_path: Path) -> bool:
        """Execute SQL statements from a file."""
        if not sql_file_path.exists():
            self.print_status(f"SQL file not found: {sql_file_path}", 'warning')
            return False
        
        try:
            self.print_status(f"Executing {sql_file_path.name}...", 'info')
            
            with open(sql_file_path, 'r') as f:
                sql_content = f.read()
            
            # Split SQL content into individual statements
            # Remove comments and empty lines
            statements = []
            current_statement = []
            
            for line in sql_content.split('\n'):
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('--'):
                    continue
                
                current_statement.append(line)
                
                # Check if statement ends with semicolon
                if line.endswith(';'):
                    statement = ' '.join(current_statement)
                    if statement.strip():
                        statements.append(statement)
                    current_statement = []
            
            # Execute each statement
            executed_count = 0
            for statement in statements:
                try:
                    cursor.execute(statement)
                    executed_count += 1
                except psycopg2.Error as e:
                    # Log error but continue with other statements
                    error_msg = str(e).strip()
                    if "already exists" in error_msg.lower():
                        self.print_status(f"  ⚠ Skipped existing object: {error_msg.split('\"')[1] if '\"' in error_msg else 'unknown'}", 'warning')
                    else:
                        self.print_status(f"  ✗ Statement error: {error_msg}", 'error')
                        self.results['errors'].append(f"{sql_file_path.name}: {error_msg}")
            
            self.print_status(f"✓ Executed {executed_count} statements from {sql_file_path.name}", 'success')
            self.results['executed'] += executed_count
            
            return True
            
        except Exception as e:
            self.print_status(f"✗ Error reading {sql_file_path.name}: {str(e)}", 'error')
            self.results['failed'] += 1
            self.results['errors'].append(f"File read error: {str(e)}")
            return False

    def create_indexes(self, cursor) -> bool:
        """Create additional indexes for performance."""
        self.print_status("Creating performance indexes...", 'info')
        
        indexes = [
            {
                'name': 'idx_documents_created_at',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at DESC);'
            },
            {
                'name': 'idx_entities_name_gin',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_entities_name_gin ON entities USING gin(name gin_trgm_ops);'
            },
            {
                'name': 'idx_entities_type',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);'
            },
            {
                'name': 'idx_relationships_source',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_entity_id);'
            },
            {
                'name': 'idx_relationships_target',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_entity_id);'
            },
            {
                'name': 'idx_users_email',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);'
            },
            {
                'name': 'idx_api_keys_hash',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(key_hash);'
            }
        ]
        
        created_count = 0
        for index in indexes:
            try:
                cursor.execute(index['sql'])
                created_count += 1
                self.print_status(f"  ✓ Created index: {index['name']}", 'success')
            except psycopg2.Error as e:
                error_msg = str(e).strip()
                if "already exists" in error_msg.lower():
                    self.print_status(f"  ⚠ Index already exists: {index['name']}", 'warning')
                else:
                    self.print_status(f"  ✗ Failed to create index {index['name']}: {error_msg}", 'error')
        
        self.print_status(f"✓ Created {created_count} new indexes", 'success')
        return True

    def create_default_data(self, cursor) -> bool:
        """Create default data for system operation."""
        self.print_status("Creating default system data...", 'info')
        
        try:
            # Create default admin user
            cursor.execute("""
                INSERT INTO users (email, name, role, preferences)
                VALUES ('admin@kgl.local', 'System Administrator', 'admin', '{"theme": "light"}')
                ON CONFLICT (email) DO NOTHING
            """)
            
            # Create default system API key (hashed)
            cursor.execute("""
                INSERT INTO api_keys (key_hash, user_id, name, permissions)
                VALUES (
                    'system_key_hash_placeholder', 
                    (SELECT id FROM users WHERE email = 'admin@kgl.local'),
                    'System Key',
                    '["read", "write", "admin"]'
                )
                ON CONFLICT (key_hash) DO NOTHING
            """)
            
            # Insert system settings if table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'system_settings'
                )
            """)
            
            if cursor.fetchone()[0]:
                cursor.execute("""
                    INSERT INTO system_settings (key, value, description)
                    VALUES 
                        ('system.version', '1.0.0', 'System version'),
                        ('system.environment', 'development', 'Environment type'),
                        ('features.module1_enabled', 'true', 'Enable Module 1'),
                        ('features.module2_enabled', 'true', 'Enable Module 2'),
                        ('features.module3_enabled', 'true', 'Enable Module 3'),
                        ('features.module4_enabled', 'true', 'Enable Module 4')
                    ON CONFLICT (key) DO NOTHING
                """)
                self.print_status("  ✓ Created system settings", 'success')
            
            self.print_status("✓ Created default system data", 'success')
            return True
            
        except psycopg2.Error as e:
            self.print_status(f"  ⚠ Default data creation error: {str(e)}", 'warning')
            return False

    def run_initialization(self) -> bool:
        """Run complete database initialization."""
        self.print_status(f"{Colors.BOLD}Starting Database Initialization{Colors.END}", 'info')
        
        # Test connection first
        if not self.test_connection():
            return False
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get initial table count
            initial_tables = self.get_existing_tables(cursor)
            self.print_status(f"Initial tables found: {len(initial_tables)}", 'info')
            
            if initial_tables:
                self.print_status(f"  Existing tables: {', '.join(initial_tables)}", 'info')
            
            # Execute SQL files
            success_count = 0
            total_files = 0
            
            for sql_file_name in self.sql_files:
                sql_file_path = Path(__file__).parent / sql_file_name
                total_files += 1
                
                if self.execute_sql_file(cursor, sql_file_path):
                    success_count += 1
            
            # Create indexes
            self.create_indexes(cursor)
            
            # Create default data
            self.create_default_data(cursor)
            
            # Commit all changes
            conn.commit()
            
            # Get final table count
            final_tables = self.get_existing_tables(cursor)
            new_tables = set(final_tables) - set(initial_tables)
            
            self.print_status(f"Final tables: {len(final_tables)}", 'info')
            if new_tables:
                self.print_status(f"New tables created: {', '.join(sorted(new_tables))}", 'success')
            
            cursor.close()
            conn.close()
            
            return success_count > 0
            
        except psycopg2.Error as e:
            self.print_status(f"Database initialization error: {str(e)}", 'error')
            return False
        except Exception as e:
            self.print_status(f"Unexpected error: {str(e)}", 'error')
            return False

    def print_summary(self):
        """Print initialization results summary."""
        print(f"\n{Colors.BOLD}=== Database Initialization Summary ==={Colors.END}")
        print(f"SQL statements executed: {self.results['executed']}")
        print(f"{Colors.RED}Failed operations: {self.results['failed']}{Colors.END}")
        
        if self.results['errors']:
            print(f"\n{Colors.YELLOW}Warnings/Errors:{Colors.END}")
            for error in self.results['errors']:
                print(f"  • {error}")
        
        if self.results['failed'] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Database initialization completed successfully!{Colors.END}")
            print(f"\n{Colors.BLUE}Next steps:{Colors.END}")
            print(f"  • Run 'python shared/db/test_connection.py' to verify connections")
            print(f"  • Run 'python scripts/seed_data.py' to populate with sample data")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Some initialization operations failed.{Colors.END}")

def main():
    """Main initialization function."""
    initializer = DatabaseInitializer()
    
    try:
        success = initializer.run_initialization()
        initializer.print_summary()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        initializer.print_status("\nInitialization interrupted by user", 'warning')
        return 1
    except Exception as e:
        initializer.print_status(f"Unexpected error: {str(e)}", 'error')
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)