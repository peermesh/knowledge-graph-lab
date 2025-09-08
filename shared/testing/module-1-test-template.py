"""
Test template for Module 1: Ingestion & Adapters
Tests the data ingestion pipeline and content adapters with mock data.
"""

import unittest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import requests

class MockDataLoader:
    """Helper class to load mock data for testing"""
    
    def __init__(self, base_path="/Users/grig/work/peermesh/repo/knowledge-graph-lab/mock-data"):
        self.base_path = base_path
    
    def load_mock_articles(self):
        """Load mock articles for ingestion testing"""
        with open(f"{self.base_path}/content/articles.json", 'r') as f:
            return json.load(f)
    
    def load_mock_news(self):
        """Load mock news items for ingestion testing"""
        with open(f"{self.base_path}/content/news.json", 'r') as f:
            return json.load(f)
    
    def load_mock_social_posts(self):
        """Load mock social posts for ingestion testing"""
        with open(f"{self.base_path}/content/social-posts.json", 'r') as f:
            return json.load(f)

class TestDataIngestion(unittest.TestCase):
    """Test data ingestion pipeline functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_loader = MockDataLoader()
        self.sample_articles = self.mock_loader.load_mock_articles()
        self.sample_news = self.mock_loader.load_mock_news()
        
    def test_url_validation(self):
        """Test URL validation for ingestion sources"""
        valid_urls = [
            "https://example.com/article",
            "https://blog.example.org/post/123",
            "https://news.site.co.uk/story"
        ]
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "javascript:alert('xss')",
            ""
        ]
        
        # Mock the URL validator
        from modules.module_1_ingestion.src.url_validator import URLValidator
        validator = URLValidator()
        
        for url in valid_urls:
            self.assertTrue(validator.is_valid(url), f"URL should be valid: {url}")
        
        for url in invalid_urls:
            self.assertFalse(validator.is_valid(url), f"URL should be invalid: {url}")

    @patch('requests.get')
    def test_content_scraping(self, mock_get):
        """Test content scraping with mock response"""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Test Article</title></head>
            <body>
                <article>
                    <h1>Sample Article Title</h1>
                    <p>This is sample article content for testing.</p>
                    <time datetime="2024-12-18">December 18, 2024</time>
                </article>
            </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        # Test the scraper
        from modules.module_1_ingestion.src.web_scraper import WebScraper
        scraper = WebScraper()
        
        result = scraper.scrape("https://example.com/test-article")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], "Sample Article Title")
        self.assertIn("sample article content", result['content'])
        self.assertEqual(result['url'], "https://example.com/test-article")

    def test_content_normalization(self):
        """Test content normalization process"""
        # Use mock data for normalization testing
        raw_article = self.sample_articles[0].copy()
        
        from modules.module_1_ingestion.src.normalizer import ContentNormalizer
        normalizer = ContentNormalizer()
        
        normalized = normalizer.normalize(raw_article)
        
        # Check required fields are present
        required_fields = ['id', 'title', 'content', 'published_date', 'source']
        for field in required_fields:
            self.assertIn(field, normalized)
        
        # Check data quality
        self.assertGreater(len(normalized['title']), 0)
        self.assertIsInstance(normalized['published_date'], str)

    def test_duplicate_detection(self):
        """Test duplicate content detection"""
        from modules.module_1_ingestion.src.deduplicator import ContentDeduplicator
        dedup = ContentDeduplicator()
        
        # Create similar content items
        content1 = {
            'id': 'test_1',
            'title': 'Test Article Title',
            'content': 'This is test content for duplicate detection.',
            'url': 'https://example.com/article1'
        }
        
        content2 = {
            'id': 'test_2', 
            'title': 'Test Article Title',  # Same title
            'content': 'This is test content for duplicate detection.',  # Same content
            'url': 'https://example.com/article2'  # Different URL
        }
        
        content3 = {
            'id': 'test_3',
            'title': 'Different Article Title',
            'content': 'This is completely different content.',
            'url': 'https://example.com/article3'
        }
        
        # Test duplicate detection
        self.assertTrue(dedup.is_duplicate(content1, content2))
        self.assertFalse(dedup.is_duplicate(content1, content3))

    def test_quality_filtering(self):
        """Test content quality filtering"""
        from modules.module_1_ingestion.src.quality_filter import QualityFilter
        quality_filter = QualityFilter()
        
        high_quality_content = {
            'title': 'Comprehensive Analysis of the Creator Economy in Colorado',
            'content': 'This detailed analysis examines the growth patterns and economic impact of content creators across Colorado. The research methodology included surveys of over 500 creators and analysis of economic data spanning three years.',
            'word_count': 3200,
            'source_credibility': 0.9
        }
        
        low_quality_content = {
            'title': 'click here now!!!',
            'content': 'short text',
            'word_count': 15,
            'source_credibility': 0.2
        }
        
        self.assertTrue(quality_filter.passes_quality_check(high_quality_content))
        self.assertFalse(quality_filter.passes_quality_check(low_quality_content))

class TestSourceAdapters(unittest.TestCase):
    """Test different source adapters"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
    
    @patch('modules.module_1_ingestion.src.adapters.perplexity.PerplexityAPI')
    def test_perplexity_adapter(self, mock_api):
        """Test Perplexity API adapter"""
        # Mock Perplexity response
        mock_response = {
            "query": "creator economy platforms Boulder Colorado",
            "results": [
                {
                    "title": "Boulder Creator Collective Launches New Platform",
                    "url": "https://example.com/boulder-creators",
                    "content": "Local creator community in Boulder announces new platform...",
                    "entities": ["Boulder Creator Collective", "Colorado", "Platform Launch"],
                    "confidence": 0.89
                }
            ]
        }
        
        mock_api.return_value.search.return_value = mock_response
        
        from modules.module_1_ingestion.src.adapters.perplexity_adapter import PerplexityAdapter
        adapter = PerplexityAdapter()
        
        result = adapter.fetch("creator economy Boulder")
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result['results']), 1)
        self.assertIn("Boulder Creator Collective", result['results'][0]['title'])

    def test_social_media_adapter(self):
        """Test social media content adapter"""
        mock_posts = self.mock_loader.load_mock_social_posts()
        
        from modules.module_1_ingestion.src.adapters.social_adapter import SocialAdapter
        adapter = SocialAdapter()
        
        # Test processing social media post
        processed = adapter.process(mock_posts[0])
        
        self.assertIn('normalized_content', processed)
        self.assertIn('platform_metadata', processed)
        self.assertIn('engagement_metrics', processed)

    def test_rss_adapter(self):
        """Test RSS feed adapter"""
        mock_rss_content = """
        <?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Creator Economy News</title>
                <item>
                    <title>New Creator Funding Available in Colorado</title>
                    <link>https://example.com/creator-funding</link>
                    <description>Colorado announces new funding programs...</description>
                    <pubDate>Mon, 18 Dec 2024 10:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>
        """
        
        from modules.module_1_ingestion.src.adapters.rss_adapter import RSSAdapter
        adapter = RSSAdapter()
        
        with patch('feedparser.parse') as mock_parse:
            mock_feed = Mock()
            mock_feed.entries = [
                Mock(
                    title="New Creator Funding Available in Colorado",
                    link="https://example.com/creator-funding", 
                    description="Colorado announces new funding programs...",
                    published="Mon, 18 Dec 2024 10:00:00 GMT"
                )
            ]
            mock_parse.return_value = mock_feed
            
            results = adapter.fetch("https://example.com/feed.xml")
            
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['title'], "New Creator Funding Available in Colorado")

class TestDataPipeline(unittest.TestCase):
    """Test end-to-end data pipeline"""
    
    def setUp(self):
        self.mock_loader = MockDataLoader()
    
    def test_full_pipeline_execution(self):
        """Test complete ingestion pipeline"""
        from modules.module_1_ingestion.src.pipeline import IngestionPipeline
        
        # Mock configuration
        config = {
            'sources': [
                {'type': 'rss', 'url': 'https://example.com/feed.xml'},
                {'type': 'web', 'url': 'https://example.com/article'}
            ],
            'quality_threshold': 0.7,
            'enable_deduplication': True
        }
        
        pipeline = IngestionPipeline(config)
        
        with patch.multiple(
            pipeline,
            _fetch_from_sources=Mock(return_value=self.mock_loader.load_mock_articles()[:3]),
            _normalize_content=Mock(side_effect=lambda x: x),
            _filter_quality=Mock(side_effect=lambda x: x),
            _deduplicate=Mock(side_effect=lambda x: x)
        ):
            results = pipeline.run()
            
            self.assertIsInstance(results, list)
            self.assertGreater(len(results), 0)

if __name__ == '__main__':
    # Create test runner with detailed output
    unittest.main(verbosity=2)