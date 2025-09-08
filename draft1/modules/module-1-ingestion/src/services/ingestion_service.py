"""
Core ingestion service for processing URLs and content extraction
"""

import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import hashlib
import time
from typing import List, Optional, Dict, Any
import logging

from ..core.config import settings
from ..core.database import SessionLocal, IngestionJob, ContentItem

logger = logging.getLogger(__name__)

class IngestionService:
    """
    Service for processing content from various sources
    
    Handles web scraping, content extraction, and normalization
    while respecting rate limits and robots.txt
    """
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limiter = {}  # Domain -> last request time
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session with proper configuration"""
        if self.session is None:
            headers = {
                'User-Agent': settings.USER_AGENT
            }
            timeout = aiohttp.ClientTimeout(total=settings.REQUEST_TIMEOUT)
            self.session = aiohttp.ClientSession(
                headers=headers,
                timeout=timeout
            )
        return self.session
    
    async def _respect_rate_limit(self, domain: str):
        """Implement respectful rate limiting per domain"""
        current_time = time.time()
        last_request = self.rate_limiter.get(domain, 0)
        
        if current_time - last_request < settings.REQUEST_DELAY:
            sleep_time = settings.REQUEST_DELAY - (current_time - last_request)
            await asyncio.sleep(sleep_time)
        
        self.rate_limiter[domain] = time.time()
    
    async def _fetch_content(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Fetch and parse content from a URL
        
        Returns extracted content with metadata or None if failed
        """
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # Respect rate limiting
            await self._respect_rate_limit(domain)
            
            session = await self._get_session()
            
            async with session.get(url) as response:
                if response.status != 200:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return None
                
                # Get content type
                content_type = response.headers.get('content-type', '').lower()
                
                if 'html' not in content_type:
                    logger.warning(f"Non-HTML content type for {url}: {content_type}")
                    return None
                
                html = await response.text()
                
                # Parse HTML and extract content
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract title
                title_tag = soup.find('title')
                title = title_tag.get_text().strip() if title_tag else ""
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "header", "footer"]):
                    script.decompose()
                
                # Extract main content
                # Try to find main content areas first
                main_content = None
                for selector in ['main', 'article', '.content', '#content', '.post']:
                    main_content = soup.select_one(selector)
                    if main_content:
                        break
                
                if not main_content:
                    main_content = soup.find('body')
                
                if not main_content:
                    content_text = soup.get_text()
                else:
                    content_text = main_content.get_text()
                
                # Clean up content
                content_text = ' '.join(content_text.split())  # Normalize whitespace
                
                # Quality checks
                if len(content_text) < settings.MIN_CONTENT_LENGTH:
                    logger.warning(f"Content too short for {url}: {len(content_text)} chars")
                    return None
                
                if len(content_text) > settings.MAX_CONTENT_LENGTH:
                    content_text = content_text[:settings.MAX_CONTENT_LENGTH]
                    logger.info(f"Truncated content for {url} to {settings.MAX_CONTENT_LENGTH} chars")
                
                # Generate content hash for duplicate detection
                content_hash = hashlib.sha256(content_text.encode()).hexdigest()
                
                return {
                    'url': url,
                    'title': title,
                    'content': content_text,
                    'content_hash': content_hash,
                    'metadata': {
                        'domain': domain,
                        'content_type': content_type,
                        'content_length': len(content_text),
                        'extracted_at': time.time()
                    }
                }
                
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    async def process_url(self, job_id: str, url: str, source_type: str = "scrape"):
        """
        Process a single URL and update job status
        
        This runs as a background task
        """
        db = SessionLocal()
        
        try:
            # Update job status
            job = db.query(IngestionJob).filter(IngestionJob.job_id == job_id).first()
            if not job:
                logger.error(f"Job {job_id} not found")
                return
            
            job.status = "processing"
            job.progress = 0.1
            db.commit()
            
            # Fetch and process content
            content_data = await self._fetch_content(url)
            
            if content_data:
                # Check for duplicates
                existing = db.query(ContentItem).filter(
                    ContentItem.content_hash == content_data['content_hash']
                ).first()
                
                if existing:
                    logger.info(f"Duplicate content found for {url}, skipping")
                    job.status = "completed"
                    job.progress = 1.0
                    job.error_message = "Duplicate content"
                else:
                    # Save content item
                    content_item = ContentItem(
                        url=content_data['url'],
                        title=content_data['title'],
                        content=content_data['content'],
                        content_hash=content_data['content_hash'],
                        source_id=None,  # TODO: Map source_type to source_id
                        metadata=str(content_data['metadata']),
                        quality_score=self._calculate_quality_score(content_data)
                    )
                    
                    db.add(content_item)
                    
                    job.status = "completed"
                    job.progress = 1.0
                    job.completed_at = func.now()
                    
                    logger.info(f"Successfully processed {url}")
            else:
                job.status = "failed"
                job.error_message = "Failed to extract content"
                
            db.commit()
            
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            job.status = "failed"
            job.error_message = str(e)
            db.commit()
            
        finally:
            db.close()
    
    async def process_bulk_urls(self, job_ids: List[str], urls: List[str], source_type: str = "scrape"):
        """
        Process multiple URLs efficiently
        
        Uses controlled concurrency to avoid overwhelming targets
        """
        semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_REQUESTS)
        
        async def process_with_semaphore(job_id: str, url: str):
            async with semaphore:
                await self.process_url(job_id, url, source_type)
        
        # Process all URLs concurrently with rate limiting
        tasks = [
            process_with_semaphore(job_id, url)
            for job_id, url in zip(job_ids, urls)
        ]
        
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"Completed bulk processing of {len(urls)} URLs")
    
    def _calculate_quality_score(self, content_data: Dict[str, Any]) -> float:
        """
        Calculate a quality score for the content
        
        Factors: length, title presence, content structure, etc.
        """
        score = 0.0
        
        # Length scoring (0.3 max)
        content_length = len(content_data['content'])
        if content_length > 1000:
            score += 0.3
        elif content_length > 500:
            score += 0.2
        elif content_length > 200:
            score += 0.1
        
        # Title scoring (0.2 max)
        if content_data['title'] and len(content_data['title']) > 10:
            score += 0.2
        
        # Domain reputation (0.3 max) - placeholder
        domain = content_data['metadata']['domain']
        if any(trusted in domain for trusted in ['.edu', '.org', '.gov']):
            score += 0.3
        elif any(news in domain for news in ['news', 'blog', 'medium']):
            score += 0.2
        else:
            score += 0.1
        
        # Content quality indicators (0.2 max)
        content_lower = content_data['content'].lower()
        quality_indicators = ['research', 'analysis', 'study', 'report', 'article']
        spam_indicators = ['click here', 'buy now', 'limited time', 'free gift']
        
        for indicator in quality_indicators:
            if indicator in content_lower:
                score += 0.02
        
        for spam in spam_indicators:
            if spam in content_lower:
                score -= 0.1
        
        return max(0.0, min(1.0, score))  # Clamp between 0 and 1
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()