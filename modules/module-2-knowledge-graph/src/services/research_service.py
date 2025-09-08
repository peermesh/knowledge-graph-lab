"""
Autonomous research service for knowledge graph expansion
"""

import asyncio
import openai
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime, timedelta

from ..core.config import settings
from ..core.database import SessionLocal, ResearchTopic, ResearchSession, Entity, Relationship, KnowledgeGap
from .entity_extraction_service import EntityExtractionService

logger = logging.getLogger(__name__)

class ResearchService:
    """
    Autonomous research system that discovers and expands knowledge
    
    This service generates research prompts, executes them via AI models,
    and processes the results to build the knowledge graph.
    """
    
    def __init__(self):
        self.openai_client = None
        self.entity_extractor = EntityExtractionService()
        self.research_templates = self._load_research_templates()
    
    async def initialize(self):
        """Initialize the research service"""
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        await self.entity_extractor.initialize()
        logger.info("Research service initialized")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.entity_extractor.cleanup()
        logger.info("Research service cleaned up")
    
    def _load_research_templates(self) -> Dict[str, str]:
        """Load research prompt templates for different domains"""
        return {
            "creator-economy": """
Research the creator economy topic: "{topic}"

Focus on finding:
1. Platforms involved and their policies
2. Key creators or organizations  
3. Recent developments and trends
4. Funding opportunities or grant programs
5. Regulatory or policy impacts

Geographic scope: {location_scope}
Research depth: {research_depth}

Provide structured information about entities and their relationships.
For each entity found, specify:
- Name and type (platform/creator/organization/policy/grant/event)
- Description and key details
- Relationships to other entities
- Confidence in the information (0.0-1.0)
- Source URLs for verification

Return the information in JSON format suitable for knowledge graph construction.
            """,
            
            "platform-policies": """
Research platform policies related to: "{topic}"

Focus on finding:
1. Which platforms have relevant policies
2. Policy details and recent changes
3. Impact on creators and content
4. Regulatory drivers behind policies
5. Creator and industry responses

Geographic scope: {location_scope}
Research depth: {research_depth}

For each policy or platform found, provide:
- Platform/organization name
- Policy details and effective dates
- Affected creator types or content categories
- Related regulatory requirements
- Source documentation URLs

Structure the response as JSON with entities and relationships.
            """,
            
            "monetization-strategies": """
Research monetization strategies for: "{topic}"

Focus on finding:
1. Available monetization methods and platforms
2. Success stories and case studies  
3. Barriers and challenges creators face
4. Platform revenue-sharing models
5. Alternative funding sources (grants, sponsorships)

Geographic scope: {location_scope}
Research depth: {research_depth}

For each monetization method or platform:
- Method/platform name and type
- Revenue sharing or fee structure
- Creator eligibility requirements
- Success metrics and case studies
- Integration requirements

Return structured JSON data for knowledge graph integration.
            """
        }
    
    async def research_topics_batch(self, session_ids: List[str], topic_ids: List[int]):
        """
        Research multiple topics in a batch with controlled concurrency
        """
        semaphore = asyncio.Semaphore(settings.RESEARCH_BATCH_SIZE)
        
        async def research_with_semaphore(session_id: str, topic_id: int):
            async with semaphore:
                await self.research_single_topic(session_id, topic_id)
        
        tasks = [
            research_with_semaphore(session_id, topic_id)
            for session_id, topic_id in zip(session_ids, topic_ids)
        ]
        
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"Completed batch research of {len(topic_ids)} topics")
    
    async def research_single_topic(self, session_id: str, topic_id: int):
        """
        Research a single topic and extract knowledge
        """
        db = SessionLocal()
        
        try:
            # Get research session and topic
            session = db.query(ResearchSession).filter(ResearchSession.session_id == session_id).first()
            topic = db.query(ResearchTopic).filter(ResearchTopic.id == topic_id).first()
            
            if not session or not topic:
                logger.error(f"Session {session_id} or topic {topic_id} not found")
                return
            
            # Update session status
            session.status = "processing"
            session.research_prompt = self._generate_research_prompt(topic)
            session.model_used = "GPT-4"
            db.commit()
            
            # Perform research
            research_results = await self._execute_research(session.research_prompt, topic)
            
            if research_results:
                # Process results and extract entities
                entities_created, relationships_created = await self._process_research_results(
                    research_results, topic, db
                )
                
                # Update session with results
                session.status = "completed"
                session.completed_at = datetime.now()
                session.raw_response = json.dumps(research_results)
                session.entities_discovered = entities_created
                session.relationships_discovered = relationships_created
                session.quality_score = self._calculate_research_quality(research_results)
                
                # Update topic status
                topic.status = "completed"
                topic.last_researched = datetime.now()
                topic.research_depth = min(topic.research_depth + 1, settings.MAX_RESEARCH_DEPTH)
                
                logger.info(f"Successfully researched topic '{topic.topic}': {entities_created} entities, {relationships_created} relationships")
                
            else:
                session.status = "failed"
                session.completed_at = datetime.now()
                topic.status = "pending"  # Keep it available for retry
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error researching topic {topic_id}: {e}")
            if session:
                session.status = "failed"
                session.error_message = str(e)
                session.completed_at = datetime.now()
                db.commit()
        
        finally:
            db.close()
    
    def _generate_research_prompt(self, topic: ResearchTopic) -> str:
        """
        Generate a research prompt based on the topic and domain
        """
        template = self.research_templates.get(topic.domain, self.research_templates["creator-economy"])
        
        return template.format(
            topic=topic.topic,
            location_scope=topic.location_scope,
            research_depth=topic.research_depth,
            domain=topic.domain
        )
    
    async def _execute_research(self, prompt: str, topic: ResearchTopic) -> Optional[Dict[str, Any]]:
        """
        Execute research using AI model
        """
        if not self.openai_client:
            logger.warning("OpenAI client not configured, using mock research results")
            return self._generate_mock_research_results(topic)
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a research assistant specializing in the creator economy and digital platforms. Provide accurate, structured information suitable for building a knowledge graph."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If not valid JSON, wrap in structure
                return {
                    "raw_content": content,
                    "entities": [],
                    "relationships": [],
                    "needs_manual_processing": True
                }
                
        except Exception as e:
            logger.error(f"Failed to execute research: {e}")
            return None
    
    def _generate_mock_research_results(self, topic: ResearchTopic) -> Dict[str, Any]:
        """
        Generate mock research results for development/testing
        """
        return {
            "topic": topic.topic,
            "domain": topic.domain,
            "entities": [
                {
                    "name": f"Mock Platform for {topic.topic}",
                    "type": "platform",
                    "description": f"A digital platform related to {topic.topic}",
                    "confidence": 0.6,
                    "metadata": {
                        "domain": topic.domain,
                        "location": topic.location_scope,
                        "discovered_via": "mock_research"
                    }
                },
                {
                    "name": f"Mock Organization for {topic.topic}",
                    "type": "organization", 
                    "description": f"An organization working on {topic.topic}",
                    "confidence": 0.7,
                    "metadata": {
                        "domain": topic.domain,
                        "location": topic.location_scope,
                        "discovered_via": "mock_research"
                    }
                }
            ],
            "relationships": [
                {
                    "source": f"Mock Platform for {topic.topic}",
                    "target": f"Mock Organization for {topic.topic}",
                    "type": "partners_with",
                    "context": f"Partnership discovered through research on {topic.topic}",
                    "confidence": 0.5
                }
            ],
            "source_urls": ["https://example.com/mock-research"]
        }
    
    async def _process_research_results(
        self, 
        results: Dict[str, Any], 
        topic: ResearchTopic, 
        db
    ) -> tuple[int, int]:
        """
        Process research results and create entities/relationships
        """
        entities_created = 0
        relationships_created = 0
        
        # Process entities
        entity_map = {}  # Name -> Entity ID mapping
        
        for entity_data in results.get("entities", []):
            try:
                # Check if entity already exists
                existing = db.query(Entity).filter(
                    Entity.name == entity_data["name"],
                    Entity.entity_type == entity_data["type"]
                ).first()
                
                if existing:
                    entity_map[entity_data["name"]] = existing.id
                    continue
                
                # Create new entity
                entity = Entity(
                    name=entity_data["name"],
                    entity_type=entity_data["type"],
                    description=entity_data.get("description", ""),
                    confidence_score=entity_data.get("confidence", 0.5),
                    metadata=json.dumps(entity_data.get("metadata", {})),
                    source_urls=json.dumps(results.get("source_urls", []))
                )
                
                db.add(entity)
                db.flush()  # Get ID without committing
                
                entity_map[entity_data["name"]] = entity.id
                entities_created += 1
                
            except Exception as e:
                logger.error(f"Failed to create entity {entity_data.get('name', 'unknown')}: {e}")
        
        # Process relationships
        for rel_data in results.get("relationships", []):
            try:
                source_id = entity_map.get(rel_data["source"])
                target_id = entity_map.get(rel_data["target"])
                
                if not source_id or not target_id:
                    continue
                
                # Check if relationship already exists
                existing = db.query(Relationship).filter(
                    Relationship.source_id == source_id,
                    Relationship.target_id == target_id,
                    Relationship.relationship_type == rel_data["type"]
                ).first()
                
                if existing:
                    continue
                
                # Create new relationship
                relationship = Relationship(
                    source_id=source_id,
                    target_id=target_id,
                    relationship_type=rel_data["type"],
                    context=rel_data.get("context", ""),
                    confidence_score=rel_data.get("confidence", 0.5),
                    source_urls=json.dumps(results.get("source_urls", []))
                )
                
                db.add(relationship)
                relationships_created += 1
                
            except Exception as e:
                logger.error(f"Failed to create relationship: {e}")
        
        return entities_created, relationships_created
    
    def _calculate_research_quality(self, results: Dict[str, Any]) -> float:
        """
        Calculate quality score for research results
        """
        score = 0.0
        
        # Entity quality (0.4 max)
        entities = results.get("entities", [])
        if entities:
            avg_entity_confidence = sum(e.get("confidence", 0) for e in entities) / len(entities)
            score += min(0.4, avg_entity_confidence * 0.4)
        
        # Relationship quality (0.3 max) 
        relationships = results.get("relationships", [])
        if relationships:
            avg_rel_confidence = sum(r.get("confidence", 0) for r in relationships) / len(relationships)
            score += min(0.3, avg_rel_confidence * 0.3)
        
        # Source quality (0.2 max)
        sources = results.get("source_urls", [])
        if sources:
            score += min(0.2, len(sources) * 0.05)
        
        # Content completeness (0.1 max)
        if results.get("raw_content") or results.get("topic"):
            score += 0.1
        
        return min(1.0, score)
    
    async def identify_knowledge_gaps(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Analyze the knowledge graph to identify gaps that need research
        
        This is a simplified implementation - a full version would use
        more sophisticated analysis of entity coverage and relationships.
        """
        db = SessionLocal()
        
        try:
            gaps = []
            
            # Find entities with few relationships (potential isolation)
            isolated_entities = db.query(Entity).outerjoin(Relationship, 
                (Entity.id == Relationship.source_id) | (Entity.id == Relationship.target_id)
            ).group_by(Entity.id).having(func.count(Relationship.id) < 2).limit(10).all()
            
            for entity in isolated_entities:
                gap = KnowledgeGap(
                    gap_description=f"Entity '{entity.name}' has limited connections in the knowledge graph",
                    gap_type="entity_isolated",
                    priority_score=7.0,
                    context=f"This {entity.entity_type} needs more relationship discovery",
                    related_entity_ids=json.dumps([entity.id]),
                    suggested_research_topics=json.dumps([
                        f"Research connections for {entity.name}",
                        f"Find organizations working with {entity.name}"
                    ])
                )
                db.add(gap)
                gaps.append({
                    "description": gap.gap_description,
                    "priority": gap.priority_score,
                    "entity_name": entity.name
                })
            
            db.commit()
            return gaps
            
        finally:
            db.close()