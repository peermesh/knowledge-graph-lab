#!/usr/bin/env python3
"""
Health Check Script for Knowledge Graph Lab
Monitors all modules and services with mock data integration.
"""

import json
import time
import requests
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import argparse

class HealthChecker:
    """Comprehensive health checker for all KGL modules"""
    
    def __init__(self, base_url: str = "http://localhost:8000", mock_mode: bool = True):
        self.base_url = base_url
        self.mock_mode = mock_mode
        self.mock_data_path = "/Users/grig/work/peermesh/repo/knowledge-graph-lab/mock-data"
        self.health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'unknown',
            'modules': {},
            'data_integrity': {},
            'performance_metrics': {}
        }
    
    def run_full_health_check(self) -> Dict:
        """Run comprehensive health check on all components"""
        print("🔍 Starting Knowledge Graph Lab Health Check...")
        print("=" * 60)
        
        # Check each module
        self.check_module_1_ingestion()
        self.check_module_2_knowledge_graph()
        self.check_module_3_reasoning()
        self.check_module_4_frontend()
        
        # Check data integrity
        self.check_mock_data_integrity()
        
        # Check system performance
        self.check_system_performance()
        
        # Calculate overall status
        self.calculate_overall_status()
        
        return self.health_report
    
    def check_module_1_ingestion(self):
        """Check Module 1: Ingestion & Adapters"""
        print("📥 Checking Module 1: Ingestion & Adapters")
        
        module_health = {
            'status': 'unknown',
            'services': {},
            'last_check': datetime.now().isoformat()
        }
        
        if self.mock_mode:
            # Mock health checks
            module_health['services'] = {
                'web_scraper': self._mock_service_check('web_scraper', 0.95),
                'url_validator': self._mock_service_check('url_validator', 0.98),
                'content_normalizer': self._mock_service_check('content_normalizer', 0.92),
                'deduplicator': self._mock_service_check('deduplicator', 0.89),
                'quality_filter': self._mock_service_check('quality_filter', 0.94)
            }
        else:
            # Real service checks
            endpoints = [
                ('web_scraper', f"{self.base_url}/api/v1/ingestion/scraper/health"),
                ('url_validator', f"{self.base_url}/api/v1/ingestion/validator/health"),
                ('content_normalizer', f"{self.base_url}/api/v1/ingestion/normalizer/health"),
                ('deduplicator', f"{self.base_url}/api/v1/ingestion/dedup/health"),
                ('quality_filter', f"{self.base_url}/api/v1/ingestion/quality/health")
            ]
            
            for service_name, endpoint in endpoints:
                module_health['services'][service_name] = self._check_service_endpoint(endpoint)
        
        # Test ingestion pipeline with mock data
        pipeline_test = self._test_ingestion_pipeline()
        module_health['pipeline_test'] = pipeline_test
        
        # Determine module status
        service_statuses = [service['healthy'] for service in module_health['services'].values()]
        module_health['status'] = 'healthy' if all(service_statuses) and pipeline_test['success'] else 'degraded'
        
        self.health_report['modules']['module_1_ingestion'] = module_health
        print(f"   Status: {module_health['status'].upper()}")
    
    def check_module_2_knowledge_graph(self):
        """Check Module 2: Knowledge Graph & AI Research"""
        print("🧠 Checking Module 2: Knowledge Graph & AI Research")
        
        module_health = {
            'status': 'unknown',
            'services': {},
            'last_check': datetime.now().isoformat()
        }
        
        if self.mock_mode:
            module_health['services'] = {
                'graph_builder': self._mock_service_check('graph_builder', 0.96),
                'entity_extractor': self._mock_service_check('entity_extractor', 0.91),
                'relationship_mapper': self._mock_service_check('relationship_mapper', 0.88),
                'search_engine': self._mock_service_check('search_engine', 0.97),
                'research_queue': self._mock_service_check('research_queue', 0.93),
                'gap_detector': self._mock_service_check('gap_detector', 0.85)
            }
        else:
            endpoints = [
                ('graph_builder', f"{self.base_url}/api/v1/kg/builder/health"),
                ('entity_extractor', f"{self.base_url}/api/v1/kg/extractor/health"),
                ('relationship_mapper', f"{self.base_url}/api/v1/kg/relations/health"),
                ('search_engine', f"{self.base_url}/api/v1/kg/search/health"),
                ('research_queue', f"{self.base_url}/api/v1/kg/research/health"),
                ('gap_detector', f"{self.base_url}/api/v1/kg/gaps/health")
            ]
            
            for service_name, endpoint in endpoints:
                module_health['services'][service_name] = self._check_service_endpoint(endpoint)
        
        # Test knowledge graph operations
        kg_test = self._test_knowledge_graph_operations()
        module_health['kg_test'] = kg_test
        
        service_statuses = [service['healthy'] for service in module_health['services'].values()]
        module_health['status'] = 'healthy' if all(service_statuses) and kg_test['success'] else 'degraded'
        
        self.health_report['modules']['module_2_knowledge_graph'] = module_health
        print(f"   Status: {module_health['status'].upper()}")
    
    def check_module_3_reasoning(self):
        """Check Module 3: Reasoning & Content Synthesis"""
        print("🤖 Checking Module 3: Reasoning & Content Synthesis")
        
        module_health = {
            'status': 'unknown',
            'services': {},
            'last_check': datetime.now().isoformat()
        }
        
        if self.mock_mode:
            module_health['services'] = {
                'user_profiler': self._mock_service_check('user_profiler', 0.94),
                'content_personalizer': self._mock_service_check('content_personalizer', 0.90),
                'digest_generator': self._mock_service_check('digest_generator', 0.92),
                'recommender': self._mock_service_check('recommender', 0.87),
                'reasoning_engine': self._mock_service_check('reasoning_engine', 0.89),
                'content_formatter': self._mock_service_check('content_formatter', 0.96)
            }
        else:
            endpoints = [
                ('user_profiler', f"{self.base_url}/api/v1/reasoning/profiler/health"),
                ('content_personalizer', f"{self.base_url}/api/v1/reasoning/personalizer/health"),
                ('digest_generator', f"{self.base_url}/api/v1/reasoning/digest/health"),
                ('recommender', f"{self.base_url}/api/v1/reasoning/recommender/health"),
                ('reasoning_engine', f"{self.base_url}/api/v1/reasoning/engine/health"),
                ('content_formatter', f"{self.base_url}/api/v1/reasoning/formatter/health")
            ]
            
            for service_name, endpoint in endpoints:
                module_health['services'][service_name] = self._check_service_endpoint(endpoint)
        
        # Test reasoning pipeline
        reasoning_test = self._test_reasoning_pipeline()
        module_health['reasoning_test'] = reasoning_test
        
        service_statuses = [service['healthy'] for service in module_health['services'].values()]
        module_health['status'] = 'healthy' if all(service_statuses) and reasoning_test['success'] else 'degraded'
        
        self.health_report['modules']['module_3_reasoning'] = module_health
        print(f"   Status: {module_health['status'].upper()}")
    
    def check_module_4_frontend(self):
        """Check Module 4: Frontend & User Experience"""
        print("🖥️  Checking Module 4: Frontend & User Experience")
        
        module_health = {
            'status': 'unknown',
            'services': {},
            'last_check': datetime.now().isoformat()
        }
        
        if self.mock_mode:
            module_health['services'] = {
                'web_server': self._mock_service_check('web_server', 0.98),
                'api_gateway': self._mock_service_check('api_gateway', 0.95),
                'user_interface': self._mock_service_check('user_interface', 0.92),
                'dashboard': self._mock_service_check('dashboard', 0.89),
                'notification_service': self._mock_service_check('notification_service', 0.91),
                'publishing_service': self._mock_service_check('publishing_service', 0.87)
            }
        else:
            endpoints = [
                ('web_server', f"{self.base_url}/health"),
                ('api_gateway', f"{self.base_url}/api/health"),
                ('user_interface', f"{self.base_url}/api/v1/frontend/ui/health"),
                ('dashboard', f"{self.base_url}/api/v1/frontend/dashboard/health"),
                ('notification_service', f"{self.base_url}/api/v1/frontend/notifications/health"),
                ('publishing_service', f"{self.base_url}/api/v1/frontend/publishing/health")
            ]
            
            for service_name, endpoint in endpoints:
                module_health['services'][service_name] = self._check_service_endpoint(endpoint)
        
        # Test frontend functionality
        frontend_test = self._test_frontend_functionality()
        module_health['frontend_test'] = frontend_test
        
        service_statuses = [service['healthy'] for service in module_health['services'].values()]
        module_health['status'] = 'healthy' if all(service_statuses) and frontend_test['success'] else 'degraded'
        
        self.health_report['modules']['module_4_frontend'] = module_health
        print(f"   Status: {module_health['status'].upper()}")
    
    def check_mock_data_integrity(self):
        """Check integrity of mock data"""
        print("📊 Checking Mock Data Integrity")
        
        data_integrity = {
            'entities': {},
            'relationships': {},
            'content': {},
            'users': {},
            'overall_integrity': 'unknown'
        }
        
        # Check entities
        entity_types = ['creators', 'platforms', 'organizations', 'grants', 'policies']
        for entity_type in entity_types:
            integrity_result = self._check_file_integrity(f"entities/{entity_type}.json")
            data_integrity['entities'][entity_type] = integrity_result
        
        # Check relationships
        relationship_types = ['creator-platform', 'org-support', 'policy-impact']
        for rel_type in relationship_types:
            integrity_result = self._check_file_integrity(f"relationships/{rel_type}.json")
            data_integrity['relationships'][rel_type] = integrity_result
        
        # Check content
        content_types = ['articles', 'news', 'social-posts']
        for content_type in content_types:
            integrity_result = self._check_file_integrity(f"content/{content_type}.json")
            data_integrity['content'][content_type] = integrity_result
        
        # Check users
        user_files = ['profiles', 'interactions']
        for user_file in user_files:
            integrity_result = self._check_file_integrity(f"users/{user_file}.json")
            data_integrity['users'][user_file] = integrity_result
        
        # Check referential integrity
        ref_integrity = self._check_referential_integrity()
        data_integrity['referential_integrity'] = ref_integrity
        
        # Overall integrity status
        all_checks = []
        for category in data_integrity.values():
            if isinstance(category, dict):
                all_checks.extend([check.get('valid', False) for check in category.values()])
        
        data_integrity['overall_integrity'] = 'valid' if all(all_checks) else 'invalid'
        
        self.health_report['data_integrity'] = data_integrity
        print(f"   Status: {data_integrity['overall_integrity'].upper()}")
    
    def check_system_performance(self):
        """Check system performance metrics"""
        print("⚡ Checking System Performance")
        
        performance = {
            'response_times': {},
            'throughput': {},
            'resource_usage': {},
            'overall_performance': 'unknown'
        }
        
        # Mock performance checks
        performance['response_times'] = {
            'ingestion_avg_ms': 250,
            'kg_query_avg_ms': 150,
            'personalization_avg_ms': 300,
            'frontend_render_avg_ms': 80
        }
        
        performance['throughput'] = {
            'content_items_per_hour': 120,
            'kg_queries_per_second': 45,
            'user_requests_per_minute': 200
        }
        
        performance['resource_usage'] = {
            'cpu_usage_percent': 35,
            'memory_usage_percent': 62,
            'disk_usage_percent': 45,
            'network_usage_mbps': 12.5
        }
        
        # Evaluate performance
        response_times_good = all(rt < 500 for rt in performance['response_times'].values())
        resource_usage_good = (
            performance['resource_usage']['cpu_usage_percent'] < 80 and
            performance['resource_usage']['memory_usage_percent'] < 85
        )
        
        performance['overall_performance'] = 'good' if response_times_good and resource_usage_good else 'degraded'
        
        self.health_report['performance_metrics'] = performance
        print(f"   Status: {performance['overall_performance'].upper()}")
    
    def calculate_overall_status(self):
        """Calculate overall system status"""
        module_statuses = [module['status'] for module in self.health_report['modules'].values()]
        data_integrity = self.health_report['data_integrity']['overall_integrity']
        performance = self.health_report['performance_metrics']['overall_performance']
        
        healthy_modules = module_statuses.count('healthy')
        total_modules = len(module_statuses)
        
        if (healthy_modules == total_modules and 
            data_integrity == 'valid' and 
            performance == 'good'):
            self.health_report['overall_status'] = 'healthy'
        elif healthy_modules >= total_modules * 0.75:  # At least 75% modules healthy
            self.health_report['overall_status'] = 'degraded'
        else:
            self.health_report['overall_status'] = 'unhealthy'
    
    def _mock_service_check(self, service_name: str, availability: float) -> Dict:
        """Generate mock service health check"""
        import random
        
        # Simulate service availability
        is_healthy = random.random() < availability
        response_time = random.uniform(50, 200) if is_healthy else random.uniform(1000, 5000)
        
        return {
            'healthy': is_healthy,
            'response_time_ms': round(response_time, 2),
            'last_check': datetime.now().isoformat(),
            'availability': availability
        }
    
    def _check_service_endpoint(self, endpoint: str) -> Dict:
        """Check real service endpoint"""
        try:
            start_time = time.time()
            response = requests.get(endpoint, timeout=5)
            response_time = (time.time() - start_time) * 1000
            
            return {
                'healthy': response.status_code == 200,
                'response_time_ms': round(response_time, 2),
                'status_code': response.status_code,
                'last_check': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e),
                'response_time_ms': None,
                'last_check': datetime.now().isoformat()
            }
    
    def _test_ingestion_pipeline(self) -> Dict:
        """Test ingestion pipeline functionality"""
        try:
            # Mock pipeline test
            test_url = "https://example.com/test-article"
            
            # Simulate processing steps
            steps = ['url_validation', 'content_scraping', 'normalization', 'deduplication', 'quality_filtering']
            step_results = {}
            
            for step in steps:
                # Mock success/failure
                step_results[step] = {
                    'success': True,
                    'processing_time_ms': random.uniform(10, 100)
                }
            
            return {
                'success': True,
                'test_url': test_url,
                'steps': step_results,
                'total_time_ms': sum(step['processing_time_ms'] for step in step_results.values())
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _test_knowledge_graph_operations(self) -> Dict:
        """Test knowledge graph operations"""
        try:
            # Mock KG operations test
            operations = ['entity_creation', 'relationship_mapping', 'graph_query', 'entity_search']
            operation_results = {}
            
            for operation in operations:
                operation_results[operation] = {
                    'success': True,
                    'items_processed': random.randint(5, 50),
                    'processing_time_ms': random.uniform(20, 150)
                }
            
            return {
                'success': True,
                'operations': operation_results,
                'graph_size': {'entities': 1247, 'relationships': 3891}
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _test_reasoning_pipeline(self) -> Dict:
        """Test reasoning and personalization pipeline"""
        try:
            # Mock reasoning test
            test_user_id = 'test_user_001'
            
            reasoning_steps = ['user_profiling', 'content_filtering', 'personalization', 'digest_generation']
            step_results = {}
            
            for step in reasoning_steps:
                step_results[step] = {
                    'success': True,
                    'processing_time_ms': random.uniform(30, 200),
                    'quality_score': random.uniform(0.8, 0.98)
                }
            
            return {
                'success': True,
                'test_user_id': test_user_id,
                'steps': step_results,
                'personalization_accuracy': 0.89
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _test_frontend_functionality(self) -> Dict:
        """Test frontend functionality"""
        try:
            # Mock frontend test
            frontend_components = ['dashboard', 'search', 'visualization', 'user_profile', 'notifications']
            component_results = {}
            
            for component in frontend_components:
                component_results[component] = {
                    'success': True,
                    'load_time_ms': random.uniform(50, 300),
                    'interactive': True
                }
            
            return {
                'success': True,
                'components': component_results,
                'user_experience_score': 0.92
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _check_file_integrity(self, file_path: str) -> Dict:
        """Check integrity of a mock data file"""
        full_path = os.path.join(self.mock_data_path, file_path)
        
        try:
            # Check if file exists
            if not os.path.exists(full_path):
                return {
                    'valid': False,
                    'error': 'File not found',
                    'file_path': full_path
                }
            
            # Check if file is valid JSON
            with open(full_path, 'r') as f:
                data = json.load(f)
            
            # Check if data is list (expected format)
            if not isinstance(data, list):
                return {
                    'valid': False,
                    'error': 'Data is not a list',
                    'data_type': type(data).__name__
                }
            
            # Basic data validation
            item_count = len(data)
            has_required_fields = True
            
            if item_count > 0:
                first_item = data[0]
                required_fields = ['id', 'type'] if 'entities' in file_path else ['id']
                has_required_fields = all(field in first_item for field in required_fields)
            
            return {
                'valid': has_required_fields,
                'item_count': item_count,
                'file_size_bytes': os.path.getsize(full_path),
                'last_modified': datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
            }
            
        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'error': f'Invalid JSON: {str(e)}',
                'file_path': full_path
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'file_path': full_path
            }
    
    def _check_referential_integrity(self) -> Dict:
        """Check referential integrity between entities and relationships"""
        try:
            # Load entities
            entity_ids = set()
            entity_types = ['creators', 'platforms', 'organizations', 'grants', 'policies']
            
            for entity_type in entity_types:
                file_path = os.path.join(self.mock_data_path, f"entities/{entity_type}.json")
                with open(file_path, 'r') as f:
                    entities = json.load(f)
                    entity_ids.update(entity['id'] for entity in entities)
            
            # Check relationships
            relationship_files = ['creator-platform.json', 'org-support.json', 'policy-impact.json']
            total_relationships = 0
            valid_relationships = 0
            
            for rel_file in relationship_files:
                file_path = os.path.join(self.mock_data_path, f"relationships/{rel_file}")
                with open(file_path, 'r') as f:
                    relationships = json.load(f)
                    
                    for rel in relationships:
                        total_relationships += 1
                        if (rel.get('source_id') in entity_ids and 
                            rel.get('target_id') in entity_ids):
                            valid_relationships += 1
            
            integrity_score = valid_relationships / total_relationships if total_relationships > 0 else 0
            
            return {
                'valid': integrity_score > 0.95,  # 95% threshold
                'total_entities': len(entity_ids),
                'total_relationships': total_relationships,
                'valid_relationships': valid_relationships,
                'integrity_score': round(integrity_score, 3)
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }

def main():
    """Main function to run health check"""
    parser = argparse.ArgumentParser(description='Knowledge Graph Lab Health Check')
    parser.add_argument('--base-url', default='http://localhost:8000',
                       help='Base URL for API endpoints')
    parser.add_argument('--mock-mode', action='store_true', default=True,
                       help='Run in mock mode (default: True)')
    parser.add_argument('--output', '-o', help='Output file for health report')
    parser.add_argument('--format', choices=['json', 'text'], default='text',
                       help='Output format')
    
    args = parser.parse_args()
    
    # Create health checker
    health_checker = HealthChecker(base_url=args.base_url, mock_mode=args.mock_mode)
    
    # Run health check
    try:
        health_report = health_checker.run_full_health_check()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🏥 HEALTH CHECK SUMMARY")
        print("=" * 60)
        print(f"Overall Status: {health_report['overall_status'].upper()}")
        print(f"Timestamp: {health_report['timestamp']}")
        
        print("\nModule Status:")
        for module_name, module_data in health_report['modules'].items():
            status_emoji = "✅" if module_data['status'] == 'healthy' else "⚠️" if module_data['status'] == 'degraded' else "❌"
            print(f"  {status_emoji} {module_name}: {module_data['status'].upper()}")
        
        print(f"\nData Integrity: {health_report['data_integrity']['overall_integrity'].upper()}")
        print(f"Performance: {health_report['performance_metrics']['overall_performance'].upper()}")
        
        # Output to file if specified
        if args.output:
            with open(args.output, 'w') as f:
                if args.format == 'json':
                    json.dump(health_report, f, indent=2)
                else:
                    f.write(f"Knowledge Graph Lab Health Report\n")
                    f.write(f"Generated: {health_report['timestamp']}\n")
                    f.write(f"Overall Status: {health_report['overall_status']}\n\n")
                    f.write(json.dumps(health_report, indent=2))
            
            print(f"\n📄 Full report saved to: {args.output}")
        
        # Exit with appropriate code
        if health_report['overall_status'] == 'healthy':
            sys.exit(0)
        elif health_report['overall_status'] == 'degraded':
            sys.exit(1)
        else:
            sys.exit(2)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Health check interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Health check failed with error: {str(e)}")
        sys.exit(3)

if __name__ == '__main__':
    main()