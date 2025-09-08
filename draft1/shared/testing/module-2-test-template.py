"""
Test template for Module 2: Knowledge Graph & AI Research  
Tests the knowledge graph construction and AI research functionality with mock data.
"""

import unittest
import json
import os
from unittest.mock import Mock, patch, MagicMock
import networkx as nx
from datetime import datetime

class MockDataLoader:
    """Helper class to load mock data for testing"""
    
    def __init__(self, base_path="/Users/grig/work/peermesh/repo/knowledge-graph-lab/mock-data"):
        self.base_path = base_path
    
    def load_mock_entities(self):
        """Load all mock entities for knowledge graph testing"""
        entities = {}
        entity_types = ['creators', 'platforms', 'organizations', 'grants', 'policies']
        
        for entity_type in entity_types:
            with open(f"{self.base_path}/entities/{entity_type}.json", 'r') as f:
                entities[entity_type] = json.load(f)
        return entities
    
    def load_mock_relationships(self):
        """Load all mock relationships for knowledge graph testing"""
        relationships = {}
        relationship_types = ['creator-platform', 'org-support', 'policy-impact']
        
        for rel_type in relationship_types:
            with open(f"{self.base_path}/relationships/{rel_type}.json", 'r') as f:
                relationships[rel_type] = json.load(f)
        return relationships
    
    def load_mock_content(self):
        """Load mock content for entity extraction testing"""
        content = {}
        content_types = ['articles', 'news', 'social-posts']
        
        for content_type in content_types:
            with open(f"{self.base_path}/content/{content_type}.json", 'r') as f:
                content[content_type] = json.load(f)
        return content

class TestKnowledgeGraphConstruction(unittest.TestCase):
    """Test knowledge graph construction and management"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_loader = MockDataLoader()
        self.entities = self.mock_loader.load_mock_entities()
        self.relationships = self.mock_loader.load_mock_relationships()
        
    def test_entity_insertion(self):
        """Test entity insertion into knowledge graph"""
        from modules.module_2_knowledge_graph.src.graph_builder import KnowledgeGraphBuilder
        
        builder = KnowledgeGraphBuilder()
        
        # Test creator entity insertion
        creator = self.entities['creators'][0]
        builder.add_entity(creator)
        
        # Verify entity was added
        self.assertTrue(builder.has_entity(creator['id']))
        retrieved = builder.get_entity(creator['id'])
        self.assertEqual(retrieved['name'], creator['name'])
        self.assertEqual(retrieved['type'], creator['type'])

    def test_relationship_creation(self):
        """Test relationship creation between entities"""
        from modules.module_2_knowledge_graph.src.graph_builder import KnowledgeGraphBuilder
        
        builder = KnowledgeGraphBuilder()
        
        # Add entities first
        creator = self.entities['creators'][0]
        platform = self.entities['platforms'][0]
        builder.add_entity(creator)
        builder.add_entity(platform)
        
        # Add relationship
        relationship = self.relationships['creator-platform'][0]
        builder.add_relationship(relationship)
        
        # Verify relationship exists
        self.assertTrue(builder.has_relationship(
            relationship['source_id'], 
            relationship['target_id'], 
            relationship['type']
        ))
        
        # Check relationship metadata
        rel = builder.get_relationship(relationship['source_id'], relationship['target_id'])
        self.assertEqual(rel['type'], 'USES_PLATFORM')
        self.assertIn('confidence', rel['metadata'])

    def test_entity_search(self):
        """Test entity search functionality"""
        from modules.module_2_knowledge_graph.src.search_engine import GraphSearchEngine
        
        search_engine = GraphSearchEngine()
        
        # Load test data
        for entity_type, entity_list in self.entities.items():
            for entity in entity_list[:3]:  # Load first 3 of each type
                search_engine.index_entity(entity)
        
        # Test search by name
        results = search_engine.search("Boulder Music Collective")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]['name'], "Boulder Music Collective")
        
        # Test search by type
        creator_results = search_engine.search_by_type("Creator")
        self.assertGreater(len(creator_results), 0)
        self.assertTrue(all(r['type'] == 'Creator' for r in creator_results))

    def test_graph_traversal(self):
        """Test graph traversal and path finding"""
        from modules.module_2_knowledge_graph.src.graph_traversal import GraphTraversal
        
        traversal = GraphTraversal()
        
        # Build small test graph
        G = nx.Graph()
        G.add_node("creator_001", type="Creator", name="Test Creator")
        G.add_node("platform_001", type="Platform", name="Test Platform") 
        G.add_node("org_001", type="Organization", name="Test Org")
        
        G.add_edge("creator_001", "platform_001", relationship="USES")
        G.add_edge("org_001", "creator_001", relationship="SUPPORTS")
        
        # Test path finding
        path = traversal.find_path(G, "creator_001", "org_001")
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 2)  # Direct connection
        
        # Test neighbor discovery
        neighbors = traversal.get_neighbors(G, "creator_001")
        self.assertEqual(len(neighbors), 2)  # Platform and Organization

    def test_entity_similarity(self):
        """Test entity similarity calculation"""
        from modules.module_2_knowledge_graph.src.similarity import EntitySimilarity
        
        similarity = EntitySimilarity()
        
        creator1 = self.entities['creators'][0]  # Boulder Music Collective
        creator2 = self.entities['creators'][1]  # Colorado Tech Educator
        creator3 = self.entities['creators'][2]  # Mountain Vista Photography
        
        # Test similarity between creators in similar locations
        sim_score_1_2 = similarity.calculate_similarity(creator1, creator2)
        sim_score_1_3 = similarity.calculate_similarity(creator1, creator3)
        
        # Creators in same state should be more similar than those in different states
        self.assertGreater(sim_score_1_2, 0.1)  # Both in Colorado
        self.assertIsInstance(sim_score_1_2, float)
        self.assertBetween(sim_score_1_2, 0.0, 1.0)

    def assertBetween(self, value, min_val, max_val):
        """Helper assertion for value range"""
        self.assertGreaterEqual(value, min_val)
        self.assertLessEqual(value, max_val)

class TestEntityExtraction(unittest.TestCase):
    """Test entity extraction from content"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
        self.content = self.mock_loader.load_mock_content()
    
    @patch('modules.module_2_knowledge_graph.src.nlp.NLPProcessor')
    def test_named_entity_recognition(self, mock_nlp):
        """Test named entity recognition from text"""
        mock_nlp_instance = Mock()
        mock_nlp.return_value = mock_nlp_instance
        
        # Mock NLP response
        mock_nlp_instance.extract_entities.return_value = [
            {'text': 'Boulder', 'label': 'GPE', 'start': 0, 'end': 7},
            {'text': 'Colorado Arts Council', 'label': 'ORG', 'start': 50, 'end': 71},
            {'text': 'YouTube', 'label': 'ORG', 'start': 100, 'end': 107}
        ]
        
        from modules.module_2_knowledge_graph.src.entity_extractor import EntityExtractor
        extractor = EntityExtractor()
        
        article = self.content['articles'][0]
        entities = extractor.extract_from_text(article['metadata']['abstract'])
        
        self.assertGreater(len(entities), 0)
        entity_texts = [e['text'] for e in entities]
        self.assertIn('Boulder', entity_texts)
        self.assertIn('Colorado Arts Council', entity_texts)

    def test_entity_linking(self):
        """Test linking extracted entities to knowledge graph"""
        from modules.module_2_knowledge_graph.src.entity_linker import EntityLinker
        
        linker = EntityLinker()
        
        # Load knowledge base
        knowledge_base = {}
        for entity_type, entity_list in self.mock_loader.load_mock_entities().items():
            for entity in entity_list[:5]:  # Load first 5 of each type
                knowledge_base[entity['id']] = entity
        
        linker.load_knowledge_base(knowledge_base)
        
        # Test linking
        extracted_entity = {
            'text': 'Boulder Music Collective',
            'label': 'ORG',
            'confidence': 0.95
        }
        
        linked = linker.link_entity(extracted_entity)
        self.assertIsNotNone(linked)
        self.assertEqual(linked['id'], 'creator_001')

class TestResearchQueue(unittest.TestCase):
    """Test AI research queue and prioritization"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
    
    def test_research_priority_calculation(self):
        """Test research priority calculation"""
        from modules.module_2_knowledge_graph.src.research_queue import ResearchQueue
        
        queue = ResearchQueue()
        
        # Mock research requests
        requests = [
            {
                'query': 'New creator funding opportunities in Colorado',
                'user_interest': 0.95,
                'knowledge_gap': 0.8,
                'urgency': 0.7,
                'complexity': 0.5
            },
            {
                'query': 'Platform policy changes affecting creators', 
                'user_interest': 0.7,
                'knowledge_gap': 0.9,
                'urgency': 0.95,
                'complexity': 0.3
            }
        ]
        
        # Calculate priorities
        for req in requests:
            priority = queue.calculate_priority(req)
            req['priority'] = priority
            queue.add_request(req)
        
        # Test queue ordering
        next_request = queue.get_next_request()
        self.assertIsNotNone(next_request)
        self.assertIn('priority', next_request)

    @patch('modules.module_2_knowledge_graph.src.ai_researcher.AIResearcher')
    def test_research_execution(self, mock_researcher):
        """Test research execution with mock AI"""
        mock_researcher_instance = Mock()
        mock_researcher.return_value = mock_researcher_instance
        
        # Mock AI research response
        mock_researcher_instance.research.return_value = {
            'query': 'Colorado creator grants',
            'findings': [
                {
                    'source': 'Colorado Arts Council',
                    'content': 'New individual artist grants available...',
                    'relevance': 0.92,
                    'credibility': 0.85
                }
            ],
            'entities_found': ['Colorado Arts Council', 'Individual Artist Grants'],
            'confidence': 0.88
        }
        
        from modules.module_2_knowledge_graph.src.research_executor import ResearchExecutor
        executor = ResearchExecutor()
        
        research_request = {
            'query': 'Colorado creator grants',
            'priority': 0.9,
            'context': 'User seeking funding opportunities'
        }
        
        result = executor.execute_research(research_request)
        
        self.assertIsNotNone(result)
        self.assertIn('findings', result)
        self.assertGreater(len(result['findings']), 0)

class TestKnowledgeGapDetection(unittest.TestCase):
    """Test knowledge gap detection and analysis"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
    
    def test_gap_identification(self):
        """Test identification of knowledge gaps"""
        from modules.module_2_knowledge_graph.src.gap_detector import KnowledgeGapDetector
        
        detector = KnowledgeGapDetector()
        
        # Mock user queries and current knowledge
        user_queries = [
            'creator tax implications Colorado',
            'platform policy changes 2024',
            'rural creator challenges Colorado'
        ]
        
        current_knowledge = self.mock_loader.load_mock_content()['articles']
        
        gaps = detector.identify_gaps(user_queries, current_knowledge)
        
        self.assertIsInstance(gaps, list)
        self.assertGreater(len(gaps), 0)
        
        # Check gap structure
        if gaps:
            gap = gaps[0]
            self.assertIn('topic', gap)
            self.assertIn('confidence', gap)
            self.assertIn('urgency', gap)

    def test_knowledge_coverage_analysis(self):
        """Test analysis of knowledge coverage"""
        from modules.module_2_knowledge_graph.src.coverage_analyzer import CoverageAnalyzer
        
        analyzer = CoverageAnalyzer()
        
        # Mock domain ontology
        domain_topics = [
            'creator_monetization',
            'platform_policies', 
            'creator_rights',
            'funding_opportunities',
            'tax_implications'
        ]
        
        current_content = self.mock_loader.load_mock_content()['articles']
        
        coverage = analyzer.analyze_coverage(domain_topics, current_content)
        
        self.assertIsInstance(coverage, dict)
        self.assertIn('overall_coverage', coverage)
        self.assertIn('topic_coverage', coverage)
        
        # Check coverage scores are valid percentages
        self.assertBetween(coverage['overall_coverage'], 0.0, 1.0)

class TestGraphVisualization(unittest.TestCase):
    """Test knowledge graph visualization components"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
    
    def test_graph_layout_generation(self):
        """Test graph layout generation for visualization"""
        from modules.module_2_knowledge_graph.src.visualizer import GraphVisualizer
        
        visualizer = GraphVisualizer()
        
        # Create test graph
        entities = []
        relationships = []
        
        # Add sample entities
        for creator in self.mock_loader.load_mock_entities()['creators'][:3]:
            entities.append(creator)
        
        for platform in self.mock_loader.load_mock_entities()['platforms'][:2]:
            entities.append(platform)
        
        # Add relationships
        relationships.extend(self.mock_loader.load_mock_relationships()['creator-platform'][:3])
        
        # Generate layout
        layout = visualizer.generate_layout(entities, relationships)
        
        self.assertIsInstance(layout, dict)
        self.assertIn('nodes', layout)
        self.assertIn('edges', layout)
        self.assertGreater(len(layout['nodes']), 0)

    def test_subgraph_extraction(self):
        """Test extraction of relevant subgraphs"""
        from modules.module_2_knowledge_graph.src.subgraph_extractor import SubgraphExtractor
        
        extractor = SubgraphExtractor()
        
        # Build test graph with NetworkX
        G = nx.Graph()
        
        # Add nodes
        creators = self.mock_loader.load_mock_entities()['creators'][:3]
        for creator in creators:
            G.add_node(creator['id'], **creator)
        
        platforms = self.mock_loader.load_mock_entities()['platforms'][:2]
        for platform in platforms:
            G.add_node(platform['id'], **platform)
        
        # Add edges
        relationships = self.mock_loader.load_mock_relationships()['creator-platform'][:2]
        for rel in relationships:
            G.add_edge(rel['source_id'], rel['target_id'], **rel)
        
        # Extract subgraph around specific entity
        subgraph = extractor.extract_neighborhood(G, 'creator_001', radius=2)
        
        self.assertIsInstance(subgraph, nx.Graph)
        self.assertIn('creator_001', subgraph.nodes())

    def assertBetween(self, value, min_val, max_val):
        """Helper assertion for value range"""
        self.assertGreaterEqual(value, min_val)
        self.assertLessEqual(value, max_val)

if __name__ == '__main__':
    # Create test runner with detailed output
    unittest.main(verbosity=2)