"""
Test template for Module 3: Reasoning & Content Synthesis
Tests the content personalization and synthesis functionality with mock data.
"""

import unittest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

class MockDataLoader:
    """Helper class to load mock data for testing"""
    
    def __init__(self, base_path="/Users/grig/work/peermesh/repo/knowledge-graph-lab/mock-data"):
        self.base_path = base_path
    
    def load_mock_users(self):
        """Load mock user profiles for personalization testing"""
        with open(f"{self.base_path}/users/profiles.json", 'r') as f:
            return json.load(f)
    
    def load_mock_interactions(self):
        """Load mock user interactions for personalization testing"""
        with open(f"{self.base_path}/users/interactions.json", 'r') as f:
            return json.load(f)
    
    def load_mock_content(self):
        """Load mock content for synthesis testing"""
        content = {}
        content_types = ['articles', 'news', 'social-posts']
        
        for content_type in content_types:
            with open(f"{self.base_path}/content/{content_type}.json", 'r') as f:
                content[content_type] = json.load(f)
        return content
    
    def load_mock_entities(self):
        """Load mock entities for content context"""
        entities = {}
        entity_types = ['creators', 'platforms', 'organizations', 'grants', 'policies']
        
        for entity_type in entity_types:
            with open(f"{self.base_path}/entities/{entity_type}.json", 'r') as f:
                entities[entity_type] = json.load(f)
        return entities

class TestUserProfiling(unittest.TestCase):
    """Test user profile analysis and interest modeling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_loader = MockDataLoader()
        self.users = self.mock_loader.load_mock_users()
        self.interactions = self.mock_loader.load_mock_interactions()
    
    def test_interest_extraction(self):
        """Test extraction of user interests from profile and behavior"""
        from modules.module_3_reasoning.src.user_profiler import UserProfiler
        
        profiler = UserProfiler()
        
        # Test with creator user
        creator_user = next(u for u in self.users if u['id'] == 'user_001')
        user_interactions = [i for i in self.interactions if i['user_id'] == 'user_001']
        
        interests = profiler.extract_interests(creator_user, user_interactions)
        
        self.assertIsInstance(interests, list)
        self.assertGreater(len(interests), 0)
        
        # Should include interests from profile
        profile_interests = creator_user['metadata']['interests']
        for interest in profile_interests:
            self.assertTrue(any(interest.lower() in extracted.lower() for extracted in interests))

    def test_preference_learning(self):
        """Test learning user preferences from interactions"""
        from modules.module_3_reasoning.src.preference_learner import PreferenceLearner
        
        learner = PreferenceLearner()
        
        # Get user with content consumption history
        user = next(u for u in self.users if u['id'] == 'user_003')
        user_interactions = [i for i in self.interactions if i['user_id'] == 'user_003']
        
        preferences = learner.learn_preferences(user, user_interactions)
        
        self.assertIsInstance(preferences, dict)
        self.assertIn('content_formats', preferences)
        self.assertIn('topics', preferences)
        self.assertIn('frequency', preferences)
        
        # Check that preferences align with user profile
        expected_formats = user['metadata']['content_preferences']['format']
        for format_pref in expected_formats:
            self.assertIn(format_pref, preferences['content_formats'])

    def test_user_segmentation(self):
        """Test user segmentation into personas"""
        from modules.module_3_reasoning.src.user_segmentation import UserSegmentation
        
        segmentation = UserSegmentation()
        
        # Load all user profiles
        all_users = self.users
        
        segments = segmentation.segment_users(all_users)
        
        self.assertIsInstance(segments, dict)
        self.assertGreater(len(segments), 0)
        
        # Check that all users are assigned to segments
        total_assigned = sum(len(users) for users in segments.values())
        self.assertEqual(total_assigned, len(all_users))
        
        # Verify segment characteristics
        for segment_name, segment_users in segments.items():
            self.assertIsInstance(segment_name, str)
            self.assertGreater(len(segment_users), 0)

class TestContentPersonalization(unittest.TestCase):
    """Test content personalization and recommendation"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
        self.users = self.mock_loader.load_mock_users()
        self.content = self.mock_loader.load_mock_content()
    
    def test_content_relevance_scoring(self):
        """Test content relevance scoring for users"""
        from modules.module_3_reasoning.src.relevance_scorer import RelevanceScorer
        
        scorer = RelevanceScorer()
        
        # Test with policy watcher user
        policy_user = next(u for u in self.users if u['id'] == 'user_002')
        
        # Test with policy-related article
        policy_article = next(a for a in self.content['articles'] 
                            if 'policy' in a['title'].lower())
        
        score = scorer.calculate_relevance(policy_user, policy_article)
        
        self.assertIsInstance(score, float)
        self.assertBetween(score, 0.0, 1.0)
        self.assertGreater(score, 0.5)  # Should be high relevance for policy user

    def test_content_filtering(self):
        """Test content filtering based on user preferences"""
        from modules.module_3_reasoning.src.content_filter import ContentFilter
        
        content_filter = ContentFilter()
        
        # Test with creator user interested in monetization
        creator_user = next(u for u in self.users if u['id'] == 'user_003')
        all_articles = self.content['articles']
        
        filtered_content = content_filter.filter_content(creator_user, all_articles)
        
        self.assertIsInstance(filtered_content, list)
        self.assertGreater(len(filtered_content), 0)
        self.assertLessEqual(len(filtered_content), len(all_articles))
        
        # Verify filtered content is relevant
        user_interests = creator_user['metadata']['interests']
        for article in filtered_content[:3]:  # Check first 3
            title_lower = article['title'].lower()
            abstract_lower = article['metadata'].get('abstract', '').lower()
            content_text = f"{title_lower} {abstract_lower}"
            
            # Should match at least one interest
            self.assertTrue(any(interest.replace('_', ' ').lower() in content_text 
                              for interest in user_interests))

    def test_recommendation_generation(self):
        """Test personalized content recommendation"""
        from modules.module_3_reasoning.src.recommender import ContentRecommender
        
        recommender = ContentRecommender()
        
        # Load user and content
        user = next(u for u in self.users if u['id'] == 'user_001')
        available_content = self.content['articles'] + self.content['news']
        
        recommendations = recommender.recommend(user, available_content, limit=5)
        
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 5)
        
        # Check recommendation structure
        for rec in recommendations:
            self.assertIn('content', rec)
            self.assertIn('relevance_score', rec)
            self.assertIn('reasoning', rec)
            self.assertBetween(rec['relevance_score'], 0.0, 1.0)

class TestContentSynthesis(unittest.TestCase):
    """Test content synthesis and digest generation"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
        self.users = self.mock_loader.load_mock_users()
        self.content = self.mock_loader.load_mock_content()
        self.entities = self.mock_loader.load_mock_entities()
    
    @patch('modules.module_3_reasoning.src.llm_client.LLMClient')
    def test_digest_generation(self, mock_llm):
        """Test personalized digest generation"""
        # Mock LLM response
        mock_llm_instance = Mock()
        mock_llm.return_value = mock_llm_instance
        
        mock_llm_instance.generate_digest.return_value = {
            'headline': 'This Week in Colorado Creator Economy',
            'sections': [
                {
                    'title': 'New Funding Opportunities',
                    'items': [
                        {
                            'summary': 'Colorado Arts Council announces $50K creator grants',
                            'relevance_score': 0.94,
                            'source': 'Colorado Arts Council website',
                            'action_required': 'Applications due October 15'
                        }
                    ]
                }
            ],
            'word_count': 350,
            'reading_time': '2 minutes'
        }
        
        from modules.module_3_reasoning.src.digest_generator import DigestGenerator
        
        generator = DigestGenerator()
        
        # Generate digest for creator user
        creator_user = next(u for u in self.users if u['id'] == 'user_001')
        relevant_content = self.content['articles'][:5] + self.content['news'][:3]
        
        digest = generator.generate_digest(creator_user, relevant_content)
        
        self.assertIsInstance(digest, dict)
        self.assertIn('headline', digest)
        self.assertIn('sections', digest)
        self.assertGreater(len(digest['sections']), 0)

    def test_multi_channel_formatting(self):
        """Test formatting content for different channels"""
        from modules.module_3_reasoning.src.content_formatter import ContentFormatter
        
        formatter = ContentFormatter()
        
        # Sample synthesized content
        content = {
            'headline': 'New Colorado Creator Support Programs Launch',
            'summary': 'Multiple new programs supporting Colorado creators are launching this month, including grants, mentorship, and workspace access.',
            'key_points': [
                'Colorado Arts Council increases grant funding by 40%',
                'Boulder Creative Collective launches residency program', 
                'Denver opens municipal creator support center'
            ],
            'call_to_action': 'Apply for programs before deadlines'
        }
        
        # Test email formatting
        email_format = formatter.format_for_email(content)
        self.assertIn('subject', email_format)
        self.assertIn('body', email_format)
        self.assertIn('call_to_action', email_format)
        
        # Test social media formatting
        social_formats = formatter.format_for_social(content)
        self.assertIn('twitter', social_formats)
        self.assertIn('linkedin', social_formats)
        
        # Check character limits
        self.assertLessEqual(len(social_formats['twitter']), 280)

    def test_content_summarization(self):
        """Test content summarization functionality"""
        from modules.module_3_reasoning.src.summarizer import ContentSummarizer
        
        summarizer = ContentSummarizer()
        
        # Test with long article
        long_article = self.content['articles'][0]  # First article should be comprehensive
        
        # Test different summary lengths
        summary_short = summarizer.summarize(long_article, target_length=100)
        summary_medium = summarizer.summarize(long_article, target_length=250)
        
        self.assertIsInstance(summary_short, str)
        self.assertIsInstance(summary_medium, str)
        self.assertGreater(len(summary_medium), len(summary_short))
        self.assertLess(len(summary_short.split()), 120)  # Approximate word count

class TestReasoningEngine(unittest.TestCase):
    """Test reasoning and decision-making functionality"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
    
    def test_content_prioritization(self):
        """Test content prioritization logic"""
        from modules.module_3_reasoning.src.prioritizer import ContentPrioritizer
        
        prioritizer = ContentPrioritizer()
        
        # Mock content items with different characteristics
        content_items = [
            {
                'id': 'item_1',
                'title': 'Urgent: Platform Policy Changes Affecting Monetization',
                'urgency': 0.9,
                'relevance': 0.8,
                'recency': 0.95,
                'user_interest': 0.7
            },
            {
                'id': 'item_2', 
                'title': 'General Creator Tips for Social Media Growth',
                'urgency': 0.3,
                'relevance': 0.6,
                'recency': 0.4,
                'user_interest': 0.9
            },
            {
                'id': 'item_3',
                'title': 'New Funding Opportunity with Approaching Deadline',
                'urgency': 0.8,
                'relevance': 0.95,
                'recency': 0.7,
                'user_interest': 0.85
            }
        ]
        
        prioritized = prioritizer.prioritize_content(content_items)
        
        self.assertIsInstance(prioritized, list)
        self.assertEqual(len(prioritized), 3)
        
        # Check that items are properly ranked
        for item in prioritized:
            self.assertIn('priority_score', item)
            self.assertBetween(item['priority_score'], 0.0, 1.0)
        
        # Verify ordering (first should have highest priority)
        self.assertGreaterEqual(prioritized[0]['priority_score'], 
                               prioritized[1]['priority_score'])

    def test_action_item_extraction(self):
        """Test extraction of actionable items from content"""
        from modules.module_3_reasoning.src.action_extractor import ActionExtractor
        
        extractor = ActionExtractor()
        
        # Test with grant-related content
        grant_content = {
            'title': 'New Creator Grants Available with December Deadline',
            'content': 'The Colorado Arts Council is accepting applications for individual artist grants up to $7,500. Applications must be submitted by December 15, 2024. Required materials include portfolio, artist statement, and project budget.',
            'metadata': {
                'category': 'funding',
                'deadline': '2024-12-15',
                'requirements': ['portfolio', 'artist statement', 'budget']
            }
        }
        
        actions = extractor.extract_actions(grant_content)
        
        self.assertIsInstance(actions, list)
        self.assertGreater(len(actions), 0)
        
        # Check action structure
        for action in actions:
            self.assertIn('description', action)
            self.assertIn('deadline', action)
            self.assertIn('priority', action)

    def test_context_understanding(self):
        """Test contextual understanding of user needs"""
        from modules.module_3_reasoning.src.context_analyzer import ContextAnalyzer
        
        analyzer = ContextAnalyzer()
        
        # Test with different user scenarios
        user_contexts = [
            {
                'user_type': 'emerging_creator',
                'recent_activities': ['researching_monetization', 'seeking_funding'],
                'current_challenges': ['audience_growth', 'revenue_generation'],
                'time_constraints': 'high'
            },
            {
                'user_type': 'established_creator', 
                'recent_activities': ['brand_partnerships', 'tax_planning'],
                'current_challenges': ['scaling_operations', 'team_management'],
                'time_constraints': 'medium'
            }
        ]
        
        for context in user_contexts:
            analysis = analyzer.analyze_context(context)
            
            self.assertIsInstance(analysis, dict)
            self.assertIn('content_preferences', analysis)
            self.assertIn('priority_topics', analysis)
            self.assertIn('urgency_factors', analysis)

    def assertBetween(self, value, min_val, max_val):
        """Helper assertion for value range"""
        self.assertGreaterEqual(value, min_val)
        self.assertLessEqual(value, max_val)

class TestPersonalizationPipeline(unittest.TestCase):
    """Test end-to-end personalization pipeline"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
    
    def test_full_pipeline_execution(self):
        """Test complete personalization pipeline"""
        from modules.module_3_reasoning.src.personalization_pipeline import PersonalizationPipeline
        
        pipeline = PersonalizationPipeline()
        
        # Mock configuration
        config = {
            'max_content_items': 10,
            'min_relevance_threshold': 0.3,
            'personalization_factors': ['interests', 'behavior', 'context'],
            'output_formats': ['digest', 'email', 'social']
        }
        
        # Test user and content
        user = self.mock_loader.load_mock_users()[0]
        available_content = (
            self.mock_loader.load_mock_content()['articles'][:5] + 
            self.mock_loader.load_mock_content()['news'][:5]
        )
        
        with patch.multiple(
            pipeline,
            _analyze_user=Mock(return_value={'interests': ['creator monetization'], 'segment': 'emerging_creator'}),
            _filter_content=Mock(side_effect=lambda u, c: c[:7]),  # Return first 7 items
            _rank_content=Mock(side_effect=lambda u, c: sorted(c, key=lambda x: x.get('relevance', 0.5), reverse=True)),
            _generate_output=Mock(return_value={'digest': 'Mock digest content'})
        ):
            result = pipeline.run(user, available_content, config)
            
            self.assertIsInstance(result, dict)
            self.assertIn('digest', result)

if __name__ == '__main__':
    # Create test runner with detailed output
    unittest.main(verbosity=2)