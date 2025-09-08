#!/usr/bin/env python3
"""
Mock Data Insertion Script for Knowledge Graph Lab
Loads all mock data from JSON files and inserts into database.
"""

import json
import mysql.connector
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
import argparse
import logging

class MockDataInserter:
    """Insert mock data into Knowledge Graph Lab database"""
    
    def __init__(self, connection_config: Dict[str, str], mock_data_path: str):
        self.connection_config = connection_config
        self.mock_data_path = mock_data_path
        self.connection = None
        self.cursor = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """Connect to the database"""
        try:
            self.connection = mysql.connector.connect(**self.connection_config)
            self.cursor = self.connection.cursor(dictionary=True)
            self.logger.info("Successfully connected to database")
        except mysql.connector.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            sys.exit(1)
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.logger.info("Disconnected from database")
    
    def load_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded {len(data)} items from {file_path}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to load {file_path}: {e}")
            return []
    
    def clear_existing_data(self):
        """Clear existing mock data (optional)"""
        self.logger.info("Clearing existing data...")
        
        # Order matters due to foreign key constraints
        tables_to_clear = [
            'content_recommendations',
            'user_digests',
            'user_interests',
            'user_interactions',
            'content_entities',
            'entity_embeddings',
            'research_queue',
            'knowledge_gaps',
            'processing_jobs',
            'engagement_metrics',
            'system_metrics',
            'relationships',
            'content',
            'kgl_users',
            'entities',
            'ingestion_sources'
        ]
        
        try:
            # Disable foreign key checks temporarily
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            for table in tables_to_clear:
                self.cursor.execute(f"DELETE FROM {table} WHERE id LIKE '%mock%' OR id LIKE 'test_%' OR id REGEXP '^[a-z]+_[0-9]+$'")
                affected = self.cursor.rowcount
                if affected > 0:
                    self.logger.info(f"Cleared {affected} rows from {table}")
            
            # Re-enable foreign key checks
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.connection.commit()
            
        except mysql.connector.Error as e:
            self.logger.error(f"Failed to clear existing data: {e}")
            self.connection.rollback()
    
    def insert_entities(self):
        """Insert entities from mock data"""
        self.logger.info("Inserting entities...")
        
        entity_types = ['creators', 'platforms', 'organizations', 'grants', 'policies']
        total_inserted = 0
        
        for entity_type in entity_types:
            file_path = os.path.join(self.mock_data_path, 'entities', f'{entity_type}.json')
            entities = self.load_json_file(file_path)
            
            if not entities:
                continue
            
            insert_query = """
                INSERT INTO entities (id, name, type, metadata, created_at)
                VALUES (%(id)s, %(name)s, %(type)s, %(metadata)s, %(created_at)s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                metadata = VALUES(metadata),
                updated_at = CURRENT_TIMESTAMP
            """
            
            for entity in entities:
                try:
                    data = {
                        'id': entity['id'],
                        'name': entity['name'],
                        'type': entity['type'],
                        'metadata': json.dumps(entity['metadata']),
                        'created_at': datetime.now()
                    }
                    
                    self.cursor.execute(insert_query, data)
                    total_inserted += 1
                    
                except mysql.connector.Error as e:
                    self.logger.error(f"Failed to insert entity {entity['id']}: {e}")
        
        self.connection.commit()
        self.logger.info(f"Inserted {total_inserted} entities")
    
    def insert_relationships(self):
        """Insert relationships from mock data"""
        self.logger.info("Inserting relationships...")
        
        relationship_files = ['creator-platform.json', 'org-support.json', 'policy-impact.json']
        total_inserted = 0
        
        insert_query = """
            INSERT INTO relationships (id, source_id, target_id, relationship_type, metadata, confidence, created_at)
            VALUES (%(id)s, %(source_id)s, %(target_id)s, %(relationship_type)s, %(metadata)s, %(confidence)s, %(created_at)s)
            ON DUPLICATE KEY UPDATE
            metadata = VALUES(metadata),
            confidence = VALUES(confidence),
            updated_at = CURRENT_TIMESTAMP
        """
        
        for rel_file in relationship_files:
            file_path = os.path.join(self.mock_data_path, 'relationships', rel_file)
            relationships = self.load_json_file(file_path)
            
            if not relationships:
                continue
            
            for rel in relationships:
                try:
                    data = {
                        'id': rel['id'],
                        'source_id': rel['source_id'],
                        'target_id': rel['target_id'],
                        'relationship_type': rel['type'],
                        'metadata': json.dumps(rel['metadata']),
                        'confidence': rel['metadata'].get('confidence', 1.0),
                        'created_at': datetime.now()
                    }
                    
                    self.cursor.execute(insert_query, data)
                    total_inserted += 1
                    
                except mysql.connector.Error as e:
                    self.logger.error(f"Failed to insert relationship {rel['id']}: {e}")
        
        self.connection.commit()
        self.logger.info(f"Inserted {total_inserted} relationships")
    
    def insert_content(self):
        """Insert content from mock data"""
        self.logger.info("Inserting content...")
        
        content_types = ['articles', 'news', 'social-posts']
        total_inserted = 0
        
        insert_query = """
            INSERT INTO content (id, title, content_type, content_text, metadata, source_url, published_date, ingested_at, quality_score)
            VALUES (%(id)s, %(title)s, %(content_type)s, %(content_text)s, %(metadata)s, %(source_url)s, %(published_date)s, %(ingested_at)s, %(quality_score)s)
            ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            content_text = VALUES(content_text),
            metadata = VALUES(metadata)
        """
        
        for content_type in content_types:
            file_path = os.path.join(self.mock_data_path, 'content', f'{content_type}.json')
            content_items = self.load_json_file(file_path)
            
            if not content_items:
                continue
            
            for item in content_items:
                try:
                    # Extract content text based on type
                    if content_type == 'social-posts':
                        content_text = item.get('content', '')
                        published_date = item['metadata'].get('posted_date')
                    else:
                        content_text = item['metadata'].get('abstract', item['metadata'].get('summary', ''))
                        published_date = item['metadata'].get('published_date')
                    
                    # Parse published date
                    if published_date:
                        if 'T' in published_date:
                            published_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                        else:
                            published_date = datetime.strptime(published_date, '%Y-%m-%d')
                    
                    data = {
                        'id': item['id'],
                        'title': item.get('title', ''),
                        'content_type': content_type.replace('-', '_'),
                        'content_text': content_text,
                        'metadata': json.dumps(item['metadata']),
                        'source_url': item['metadata'].get('url', item['metadata'].get('source')),
                        'published_date': published_date,
                        'ingested_at': datetime.now(),
                        'quality_score': item['metadata'].get('quality_score', 0.8)
                    }
                    
                    self.cursor.execute(insert_query, data)
                    total_inserted += 1
                    
                except (mysql.connector.Error, ValueError) as e:
                    self.logger.error(f"Failed to insert content {item['id']}: {e}")
        
        self.connection.commit()
        self.logger.info(f"Inserted {total_inserted} content items")
    
    def insert_users(self):
        """Insert users from mock data"""
        self.logger.info("Inserting users...")
        
        file_path = os.path.join(self.mock_data_path, 'users', 'profiles.json')
        users = self.load_json_file(file_path)
        
        if not users:
            return
        
        insert_query = """
            INSERT INTO kgl_users (id, name, email, user_type, metadata, preferences, created_at, last_active)
            VALUES (%(id)s, %(name)s, %(email)s, %(user_type)s, %(metadata)s, %(preferences)s, %(created_at)s, %(last_active)s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            metadata = VALUES(metadata),
            preferences = VALUES(preferences),
            updated_at = CURRENT_TIMESTAMP
        """
        
        total_inserted = 0
        for user in users:
            try:
                data = {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['metadata']['email'],
                    'user_type': user['type'],
                    'metadata': json.dumps(user['metadata']),
                    'preferences': json.dumps(user['metadata'].get('content_preferences', {})),
                    'created_at': datetime.now(),
                    'last_active': datetime.now() - timedelta(days=1)
                }
                
                self.cursor.execute(insert_query, data)
                total_inserted += 1
                
            except mysql.connector.Error as e:
                self.logger.error(f"Failed to insert user {user['id']}: {e}")
        
        self.connection.commit()
        self.logger.info(f"Inserted {total_inserted} users")
    
    def insert_user_interactions(self):
        """Insert user interactions from mock data"""
        self.logger.info("Inserting user interactions...")
        
        file_path = os.path.join(self.mock_data_path, 'users', 'interactions.json')
        interactions = self.load_json_file(file_path)
        
        if not interactions:
            return
        
        insert_query = """
            INSERT INTO user_interactions (id, user_id, interaction_type, target_type, target_id, metadata, created_at)
            VALUES (%(id)s, %(user_id)s, %(interaction_type)s, %(target_type)s, %(target_id)s, %(metadata)s, %(created_at)s)
            ON DUPLICATE KEY UPDATE
            metadata = VALUES(metadata)
        """
        
        total_inserted = 0
        for interaction in interactions:
            try:
                # Determine target type and id
                target_type = None
                target_id = None
                
                if interaction['type'] in ['content_consumption']:
                    target_type = 'content'
                    target_id = interaction['metadata'].get('content_id')
                elif interaction['type'] in ['grant_application']:
                    target_type = 'entity'
                    target_id = interaction['metadata'].get('grant_id')
                
                data = {
                    'id': interaction['id'],
                    'user_id': interaction['user_id'],
                    'interaction_type': interaction['type'],
                    'target_type': target_type,
                    'target_id': target_id,
                    'metadata': json.dumps(interaction['metadata']),
                    'created_at': datetime.fromisoformat(interaction['metadata']['timestamp'].replace('Z', '+00:00'))
                }
                
                self.cursor.execute(insert_query, data)
                total_inserted += 1
                
            except mysql.connector.Error as e:
                self.logger.error(f"Failed to insert interaction {interaction['id']}: {e}")
        
        self.connection.commit()
        self.logger.info(f"Inserted {total_inserted} user interactions")
    
    def insert_sample_recommendations(self):
        """Insert sample content recommendations"""
        self.logger.info("Generating sample content recommendations...")
        
        # Get sample users and content
        self.cursor.execute("SELECT id FROM kgl_users LIMIT 5")
        users = [row['id'] for row in self.cursor.fetchall()]
        
        self.cursor.execute("SELECT id FROM content LIMIT 10")
        content_items = [row['id'] for row in self.cursor.fetchall()]
        
        if not users or not content_items:
            self.logger.warning("No users or content found for recommendations")
            return
        
        insert_query = """
            INSERT INTO content_recommendations (id, user_id, content_id, recommendation_score, reasoning, recommendation_type, created_at)
            VALUES (%(id)s, %(user_id)s, %(content_id)s, %(recommendation_score)s, %(reasoning)s, %(recommendation_type)s, %(created_at)s)
            ON DUPLICATE KEY UPDATE recommendation_score = VALUES(recommendation_score)
        """
        
        total_inserted = 0
        rec_id = 1
        
        for user_id in users:
            for i, content_id in enumerate(content_items[:3]):  # 3 recommendations per user
                try:
                    data = {
                        'id': f'rec_{rec_id:03d}',
                        'user_id': user_id,
                        'content_id': content_id,
                        'recommendation_score': 0.7 + (i * 0.1),  # Varied scores
                        'reasoning': f'Recommended based on user interests and content relevance',
                        'recommendation_type': 'personalized',
                        'created_at': datetime.now()
                    }
                    
                    self.cursor.execute(insert_query, data)
                    total_inserted += 1
                    rec_id += 1
                    
                except mysql.connector.Error as e:
                    self.logger.error(f"Failed to insert recommendation: {e}")
        
        self.connection.commit()
        self.logger.info(f"Inserted {total_inserted} sample recommendations")
    
    def run_full_insertion(self, clear_existing: bool = False):
        """Run complete mock data insertion"""
        self.logger.info("Starting mock data insertion...")
        start_time = datetime.now()
        
        try:
            self.connect()
            
            if clear_existing:
                self.clear_existing_data()
            
            # Insert data in dependency order
            self.insert_entities()
            self.insert_relationships()
            self.insert_content()
            self.insert_users()
            self.insert_user_interactions()
            self.insert_sample_recommendations()
            
            # Insert some sample system metrics
            self.insert_sample_metrics()
            
            duration = datetime.now() - start_time
            self.logger.info(f"Mock data insertion completed in {duration.total_seconds():.2f} seconds")
            
        except Exception as e:
            self.logger.error(f"Mock data insertion failed: {e}")
            if self.connection:
                self.connection.rollback()
            raise
        finally:
            self.disconnect()
    
    def insert_sample_metrics(self):
        """Insert sample system metrics"""
        self.logger.info("Inserting sample system metrics...")
        
        insert_query = """
            INSERT INTO system_metrics (id, metric_name, metric_value, metric_unit, component, recorded_at)
            VALUES (%(id)s, %(metric_name)s, %(metric_value)s, %(metric_unit)s, %(component)s, %(recorded_at)s)
        """
        
        metrics = [
            {'id': 'metric_mock_001', 'name': 'mock_data_entities_count', 'value': 100, 'unit': 'count', 'component': 'database'},
            {'id': 'metric_mock_002', 'name': 'mock_data_relationships_count', 'value': 50, 'unit': 'count', 'component': 'database'},
            {'id': 'metric_mock_003', 'name': 'mock_data_content_count', 'value': 35, 'unit': 'count', 'component': 'database'},
            {'id': 'metric_mock_004', 'name': 'mock_data_users_count', 'value': 10, 'unit': 'count', 'component': 'database'},
        ]
        
        for metric in metrics:
            try:
                data = {
                    'id': metric['id'],
                    'metric_name': metric['name'],
                    'metric_value': metric['value'],
                    'metric_unit': metric['unit'],
                    'component': metric['component'],
                    'recorded_at': datetime.now()
                }
                
                self.cursor.execute(insert_query, data)
                
            except mysql.connector.Error as e:
                self.logger.error(f"Failed to insert metric {metric['id']}: {e}")
        
        self.connection.commit()
        self.logger.info(f"Inserted {len(metrics)} sample metrics")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Insert mock data into Knowledge Graph Lab database')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', type=int, default=3306, help='Database port')
    parser.add_argument('--database', default='kgl', help='Database name')
    parser.add_argument('--username', default='kgl_user', help='Database username')
    parser.add_argument('--password', required=True, help='Database password')
    parser.add_argument('--mock-data-path', 
                       default='/Users/grig/work/peermesh/repo/knowledge-graph-lab/mock-data',
                       help='Path to mock data directory')
    parser.add_argument('--clear-existing', action='store_true',
                       help='Clear existing mock data before insertion')
    
    args = parser.parse_args()
    
    # Database connection configuration
    connection_config = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'user': args.username,
        'password': args.password,
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    # Verify mock data path exists
    if not os.path.exists(args.mock_data_path):
        print(f"Error: Mock data path does not exist: {args.mock_data_path}")
        sys.exit(1)
    
    # Create inserter and run
    inserter = MockDataInserter(connection_config, args.mock_data_path)
    
    try:
        inserter.run_full_insertion(clear_existing=args.clear_existing)
        print("✅ Mock data insertion completed successfully!")
        
        # Print summary
        inserter.connect()
        
        # Count inserted records
        tables = ['entities', 'relationships', 'content', 'kgl_users', 'user_interactions']
        print("\n📊 Insertion Summary:")
        print("-" * 40)
        
        for table in tables:
            inserter.cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = inserter.cursor.fetchone()['count']
            print(f"{table:20}: {count:6} records")
        
        inserter.disconnect()
        
    except Exception as e:
        print(f"❌ Mock data insertion failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()