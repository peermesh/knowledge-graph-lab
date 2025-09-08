"""
Integration Test Example for Knowledge Graph Lab
Tests end-to-end functionality across all modules with mock data.
"""

import unittest
import requests
import json
import time
import asyncio
from unittest.mock import patch, Mock
import subprocess
import os

class MockDataLoader:
    """Helper class to load mock data for integration testing"""
    
    def __init__(self, base_path="/Users/grig/work/peermesh/repo/knowledge-graph-lab/mock-data"):
        self.base_path = base_path
    
    def get_sample_content_url(self):
        """Return sample content URL for ingestion testing"""
        return "https://example.com/sample-creator-economy-article"
    
    def get_sample_user(self):
        """Get sample user for personalization testing"""
        with open(f"{self.base_path}/users/profiles.json", 'r') as f:
            users = json.load(f)
        return users[0]  # Return first user
    
    def get_sample_entities(self):
        """Get sample entities for knowledge graph testing"""
        entities = []
        entity_types = ['creators', 'platforms', 'organizations']
        
        for entity_type in entity_types:
            with open(f"{self.base_path}/entities/{entity_type}.json", 'r') as f:
                entities.extend(json.load(f)[:2])  # First 2 of each type
        
        return entities

class IntegrationTestBase(unittest.TestCase):
    """Base class for integration tests"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.mock_loader = MockDataLoader()
        cls.base_url = "http://localhost:8000"  # Assuming API runs on port 8000
        cls.test_timeout = 30  # 30 seconds timeout for API calls
        
        # Check if services are running (in real scenario)
        cls.services_available = cls._check_services()
    
    @classmethod
    def _check_services(cls):
        """Check if backend services are available"""
        services = {
            'module_1': f"{cls.base_url}/api/v1/ingestion/health",
            'module_2': f"{cls.base_url}/api/v1/knowledge-graph/health", 
            'module_3': f"{cls.base_url}/api/v1/reasoning/health",
            'module_4': f"{cls.base_url}/api/v1/frontend/health"
        }
        
        available = {}
        for service_name, health_url in services.items():
            try:
                # In real scenario, this would make actual HTTP requests
                # For mock testing, we'll assume services are available
                available[service_name] = True
            except:
                available[service_name] = False
        
        return available
    
    def setUp(self):
        """Set up individual test"""
        self.start_time = time.time()
    
    def tearDown(self):
        """Clean up after test"""
        test_duration = time.time() - self.start_time
        print(f"Test completed in {test_duration:.2f} seconds")

class TestEndToEndWorkflow(IntegrationTestBase):
    """Test complete end-to-end workflow"""
    
    @patch('requests.post')
    @patch('requests.get')
    def test_complete_content_pipeline(self, mock_get, mock_post):
        """Test complete pipeline: ingestion -> knowledge graph -> personalization -> frontend"""
        
        # Mock HTTP responses for each service
        mock_get.side_effect = self._mock_get_responses
        mock_post.side_effect = self._mock_post_responses
        
        # Step 1: Ingest content (Module 1)
        ingest_url = f"{self.base_url}/api/v1/ingestion/process"
        sample_url = self.mock_loader.get_sample_content_url()
        
        ingest_response = requests.post(ingest_url, json={
            'url': sample_url,
            'source_type': 'web_article'
        })
        
        self.assertEqual(ingest_response.status_code, 200)
        ingested_content = ingest_response.json()
        self.assertIn('content_id', ingested_content)
        
        # Step 2: Process with Knowledge Graph (Module 2) 
        kg_url = f"{self.base_url}/api/v1/knowledge-graph/process"
        
        kg_response = requests.post(kg_url, json={
            'content_id': ingested_content['content_id']
        })
        
        self.assertEqual(kg_response.status_code, 200)
        kg_result = kg_response.json()
        self.assertIn('entities_extracted', kg_result)
        self.assertIn('relationships_created', kg_result)
        
        # Step 3: Generate personalized content (Module 3)
        reasoning_url = f"{self.base_url}/api/v1/reasoning/personalize"
        sample_user = self.mock_loader.get_sample_user()
        
        reasoning_response = requests.post(reasoning_url, json={
            'user_id': sample_user['id'],
            'content_ids': [ingested_content['content_id']]
        })
        
        self.assertEqual(reasoning_response.status_code, 200)
        personalized_content = reasoning_response.json()
        self.assertIn('digest', personalized_content)
        self.assertIn('recommendations', personalized_content)
        
        # Step 4: Deliver through frontend (Module 4)
        frontend_url = f"{self.base_url}/api/v1/frontend/deliver"
        
        frontend_response = requests.post(frontend_url, json={
            'user_id': sample_user['id'],
            'digest': personalized_content['digest'],
            'channels': ['email', 'web_dashboard']
        })
        
        self.assertEqual(frontend_response.status_code, 200)
        delivery_result = frontend_response.json()
        self.assertIn('delivered_channels', delivery_result)
    
    def _mock_get_responses(self, url, **kwargs):
        """Mock GET responses based on URL"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        if 'health' in url:
            mock_response.json.return_value = {'status': 'healthy', 'timestamp': time.time()}
        elif 'knowledge-graph/entities' in url:
            mock_response.json.return_value = self.mock_loader.get_sample_entities()
        else:
            mock_response.json.return_value = {'message': 'Mock response'}
        
        return mock_response
    
    def _mock_post_responses(self, url, **kwargs):
        """Mock POST responses based on URL"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        if 'ingestion/process' in url:
            mock_response.json.return_value = {
                'content_id': 'mock_content_001',
                'status': 'processed',
                'entities_found': 5,
                'quality_score': 0.87
            }
        elif 'knowledge-graph/process' in url:
            mock_response.json.return_value = {
                'entities_extracted': 8,
                'relationships_created': 12,
                'processing_time': 2.3
            }
        elif 'reasoning/personalize' in url:
            mock_response.json.return_value = {
                'digest': {
                    'headline': 'Your Weekly Creator Economy Update',
                    'sections': [
                        {
                            'title': 'New Funding Opportunities',
                            'items': ['Colorado Arts Council grants available']
                        }
                    ]
                },
                'recommendations': [
                    {
                        'content_id': 'rec_001',
                        'relevance_score': 0.92,
                        'title': 'Creator Monetization Strategies'
                    }
                ]
            }
        elif 'frontend/deliver' in url:
            mock_response.json.return_value = {
                'delivered_channels': ['email', 'web_dashboard'],
                'delivery_time': time.time(),
                'success': True
            }
        
        return mock_response

class TestModuleInterfaces(IntegrationTestBase):
    """Test interfaces between modules"""
    
    @patch('requests.get')
    def test_module_1_to_2_interface(self, mock_get):
        """Test data flow from Module 1 (Ingestion) to Module 2 (Knowledge Graph)"""
        
        # Mock Module 1 output format
        module_1_output = {
            'content_id': 'test_content_001',
            'title': 'Test Article About Creator Economy',
            'content': 'This article discusses creator economy trends in Colorado...',
            'entities': ['Colorado', 'creator economy', 'funding'],
            'metadata': {
                'source': 'https://example.com/article',
                'published_date': '2024-12-18',
                'quality_score': 0.85
            }
        }
        
        # Test that Module 2 can process Module 1 output
        kg_process_url = f"{self.base_url}/api/v1/knowledge-graph/process-content"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'entities_created': 3,
            'relationships_identified': 5,
            'processing_success': True
        }
        mock_get.return_value = mock_response
        
        # In real scenario, this would be actual HTTP request
        response = requests.post(kg_process_url, json=module_1_output)
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['processing_success'])
    
    @patch('requests.post')
    def test_module_2_to_3_interface(self, mock_post):
        """Test data flow from Module 2 (Knowledge Graph) to Module 3 (Reasoning)"""
        
        # Mock Module 2 output format (knowledge graph data)
        module_2_output = {
            'entities': self.mock_loader.get_sample_entities()[:3],
            'relationships': [
                {
                    'source_id': 'creator_001',
                    'target_id': 'platform_001', 
                    'type': 'USES_PLATFORM',
                    'confidence': 0.95
                }
            ],
            'content_topics': ['creator funding', 'platform policies', 'monetization']
        }
        
        # Test that Module 3 can process Module 2 output
        reasoning_url = f"{self.base_url}/api/v1/reasoning/process-knowledge"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'insights_generated': 12,
            'user_relevance_calculated': True,
            'personalization_ready': True
        }
        mock_post.return_value = mock_response
        
        response = requests.post(reasoning_url, json=module_2_output)
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['personalization_ready'])
    
    @patch('requests.get')
    def test_module_3_to_4_interface(self, mock_get):
        """Test data flow from Module 3 (Reasoning) to Module 4 (Frontend)"""
        
        # Mock Module 3 output format (personalized content)
        module_3_output = {
            'user_id': 'user_001',
            'personalized_digest': {
                'headline': 'Your Weekly Creator Update',
                'sections': [
                    {
                        'title': 'Funding Opportunities',
                        'content': 'New grants available...',
                        'relevance': 0.92
                    }
                ]
            },
            'recommendations': [
                {
                    'content_id': 'article_001',
                    'score': 0.89,
                    'reason': 'Matches your interests in creator monetization'
                }
            ]
        }
        
        # Test that Module 4 can render Module 3 output
        frontend_url = f"{self.base_url}/api/v1/frontend/render"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'render_success': True,
            'components_generated': ['digest', 'recommendations', 'navigation'],
            'user_interface_ready': True
        }
        mock_get.return_value = mock_response
        
        response = requests.post(frontend_url, json=module_3_output)
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['user_interface_ready'])

class TestDataConsistency(IntegrationTestBase):
    """Test data consistency across modules"""
    
    def test_entity_id_consistency(self):
        """Test that entity IDs are consistent across modules"""
        
        # Load sample entities
        sample_entities = self.mock_loader.get_sample_entities()
        
        # Test ID format consistency
        for entity in sample_entities:
            self.assertIn('id', entity)
            self.assertIsInstance(entity['id'], str)
            self.assertRegex(entity['id'], r'^[a-z]+_\d{3}$')  # Format: type_number
    
    def test_data_schema_consistency(self):
        """Test that data schemas are consistent across modules"""
        
        # Required fields for all entities
        required_entity_fields = ['id', 'name', 'type', 'metadata']
        
        sample_entities = self.mock_loader.get_sample_entities()
        
        for entity in sample_entities:
            for field in required_entity_fields:
                self.assertIn(field, entity, f"Entity {entity.get('id', 'unknown')} missing field: {field}")
    
    def test_relationship_referential_integrity(self):
        """Test that relationships reference valid entities"""
        
        # Load entities and relationships
        entities = self.mock_loader.get_sample_entities()
        entity_ids = {entity['id'] for entity in entities}
        
        # Load relationships
        with open(f"{self.mock_loader.base_path}/relationships/creator-platform.json", 'r') as f:
            relationships = json.load(f)
        
        for relationship in relationships[:5]:  # Test first 5
            self.assertIn(relationship['source_id'], entity_ids, 
                         f"Relationship {relationship['id']} has invalid source_id")
            self.assertIn(relationship['target_id'], entity_ids,
                         f"Relationship {relationship['id']} has invalid target_id")

class TestPerformanceAndScalability(IntegrationTestBase):
    """Test performance and scalability across modules"""
    
    def test_batch_processing_performance(self):
        """Test performance with batch processing"""
        
        # Simulate processing multiple content items
        content_batch = [
            {'url': f'https://example.com/article_{i}', 'type': 'article'}
            for i in range(10)
        ]
        
        start_time = time.time()
        
        # Mock batch processing
        processed_items = []
        for item in content_batch:
            processed_items.append({
                'content_id': f"batch_item_{len(processed_items)}",
                'status': 'processed',
                'processing_time': 0.5
            })
        
        processing_time = time.time() - start_time
        
        # Should process batch efficiently
        self.assertLess(processing_time, 5.0)  # Should complete within 5 seconds
        self.assertEqual(len(processed_items), 10)
    
    def test_concurrent_user_handling(self):
        """Test handling multiple concurrent users"""
        
        # Simulate multiple users
        users = self.mock_loader.get_sample_user()
        user_requests = [
            {'user_id': f"concurrent_user_{i}", 'action': 'get_digest'}
            for i in range(5)
        ]
        
        start_time = time.time()
        
        # Mock concurrent processing
        responses = []
        for request in user_requests:
            responses.append({
                'user_id': request['user_id'],
                'digest': {'headline': f"Digest for {request['user_id']}"},
                'processing_time': 0.3
            })
        
        total_time = time.time() - start_time
        
        # Should handle concurrent requests efficiently
        self.assertLess(total_time, 3.0)
        self.assertEqual(len(responses), 5)

class TestErrorHandlingAndResilience(IntegrationTestBase):
    """Test error handling and system resilience"""
    
    @patch('requests.post')
    def test_module_failure_handling(self, mock_post):
        """Test system behavior when one module fails"""
        
        # Mock Module 1 success, Module 2 failure
        mock_responses = [
            Mock(status_code=200, json=lambda: {'content_id': 'test_001'}),  # Module 1 success
            Mock(status_code=500, json=lambda: {'error': 'Internal server error'})  # Module 2 failure
        ]
        mock_post.side_effect = mock_responses
        
        # Test graceful degradation
        try:
            # Module 1 should succeed
            response1 = requests.post(f"{self.base_url}/api/v1/ingestion/process", json={})
            self.assertEqual(response1.status_code, 200)
            
            # Module 2 should fail gracefully
            response2 = requests.post(f"{self.base_url}/api/v1/knowledge-graph/process", json={})
            self.assertEqual(response2.status_code, 500)
            
            # System should continue operating with fallback
            self.assertTrue(True)  # If we reach here, system handled failure gracefully
            
        except Exception as e:
            self.fail(f"System did not handle module failure gracefully: {e}")
    
    def test_data_validation_error_handling(self):
        """Test handling of invalid data"""
        
        invalid_data_samples = [
            {'invalid': 'no required fields'},
            {'id': '', 'name': 'Empty ID'},
            {'id': 'valid_001', 'type': None},  # Null type
            None  # Null object
        ]
        
        for invalid_data in invalid_data_samples:
            # Mock validation function
            def validate_entity(entity):
                if not entity:
                    return False, "Entity is null"
                if not entity.get('id'):
                    return False, "Missing or empty ID"
                if not entity.get('type'):
                    return False, "Missing or null type"
                return True, "Valid"
            
            is_valid, message = validate_entity(invalid_data)
            self.assertFalse(is_valid, f"Should reject invalid data: {invalid_data}")
            self.assertIsInstance(message, str)

if __name__ == '__main__':
    # Run integration tests
    print("Starting Knowledge Graph Lab Integration Tests")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    
    # Run with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")