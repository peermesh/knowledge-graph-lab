"""
RAG (Retrieval-Augmented Generation) service for knowledge queries
"""

from typing import List, Dict, Any, Optional
import json
import logging
import openai
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..core.config import settings
from ..core.database import SessionLocal, Entity, Relationship

logger = logging.getLogger(__name__)

class RAGService:
    """
    RAG service for answering questions using the knowledge graph
    
    Retrieves relevant entities and relationships, then generates
    coherent answers using AI models.
    """
    
    def __init__(self):
        self.openai_client = None
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def answer_query(
        self, 
        query: str, 
        context_limit: int = 10
    ) -> Dict[str, Any]:
        """
        Answer a natural language query using RAG
        
        1. Retrieve relevant entities and relationships
        2. Generate context from knowledge graph
        3. Use AI model to generate coherent answer
        """
        try:
            # Retrieve relevant knowledge
            context = await self._retrieve_relevant_context(query, context_limit)
            
            if not context["entities"] and not context["relationships"]:
                return {
                    "answer": "I don't have enough information in the knowledge base to answer that question.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Generate answer using AI
            answer = await self._generate_answer(query, context)
            
            return {
                "answer": answer["text"],
                "sources": context["sources"],
                "confidence": answer["confidence"],
                "entities_used": len(context["entities"]),
                "relationships_used": len(context["relationships"])
            }
            
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return {
                "answer": "I encountered an error while processing your query. Please try again.",
                "sources": [],
                "confidence": 0.0
            }
    
    async def generate_summary(
        self,
        topic: str,
        focus_areas: Optional[List[str]] = None,
        max_entities: int = 10,
        include_relationships: bool = True
    ) -> str:
        """
        Generate a comprehensive summary about a topic
        
        Uses knowledge graph data to create structured summaries.
        """
        try:
            # Retrieve topic-relevant entities
            entities = await self._find_topic_entities(topic, max_entities)
            
            # Get relationships if requested
            relationships = []
            if include_relationships and entities:
                relationships = await self._get_entity_relationships(
                    [e["id"] for e in entities], 
                    limit=20
                )
            
            # Create context for summary generation
            context = {
                "topic": topic,
                "entities": entities,
                "relationships": relationships,
                "focus_areas": focus_areas or []
            }
            
            # Generate summary
            summary = await self._generate_topic_summary(context)
            return summary
            
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return f"Unable to generate summary for '{topic}'. Please try again later."
    
    async def _retrieve_relevant_context(
        self, 
        query: str, 
        limit: int
    ) -> Dict[str, Any]:
        """
        Retrieve entities and relationships relevant to the query
        
        Uses simple text matching - could be enhanced with vector search.
        """
        db = SessionLocal()
        
        try:
            # Extract keywords from query
            keywords = self._extract_query_keywords(query)
            
            # Find relevant entities
            entities = []
            for keyword in keywords:
                entity_matches = db.query(Entity).filter(
                    Entity.name.ilike(f"%{keyword}%") |
                    Entity.description.ilike(f"%{keyword}%")
                ).limit(limit // len(keywords) + 1).all()
                
                entities.extend(entity_matches)
            
            # Remove duplicates
            seen_ids = set()
            unique_entities = []
            for entity in entities:
                if entity.id not in seen_ids:
                    seen_ids.add(entity.id)
                    unique_entities.append(entity)
            
            entities = unique_entities[:limit]
            
            # Get relationships between found entities
            relationships = []
            if len(entities) > 1:
                entity_ids = [e.id for e in entities]
                relationships = db.query(Relationship).filter(
                    Relationship.source_id.in_(entity_ids) |
                    Relationship.target_id.in_(entity_ids)
                ).limit(limit).all()
            
            # Format context
            context = {
                "entities": [
                    {
                        "id": e.id,
                        "name": e.name,
                        "type": e.entity_type,
                        "description": e.description,
                        "confidence": e.confidence_score
                    } for e in entities
                ],
                "relationships": [
                    {
                        "source": r.source_entity.name,
                        "target": r.target_entity.name,
                        "type": r.relationship_type,
                        "context": r.context,
                        "confidence": r.confidence_score
                    } for r in relationships
                ],
                "sources": self._extract_sources(entities, relationships)
            }
            
            return context
            
        finally:
            db.close()
    
    async def _find_topic_entities(
        self, 
        topic: str, 
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Find entities most relevant to a topic
        """
        db = SessionLocal()
        
        try:
            # Search entities by topic relevance
            entities = db.query(Entity).filter(
                Entity.name.ilike(f"%{topic}%") |
                Entity.description.ilike(f"%{topic}%") |
                Entity.metadata.ilike(f"%{topic}%")
            ).order_by(Entity.confidence_score.desc()).limit(limit).all()
            
            return [
                {
                    "id": e.id,
                    "name": e.name,
                    "type": e.entity_type,
                    "description": e.description,
                    "confidence": e.confidence_score,
                    "metadata": json.loads(e.metadata) if e.metadata else {}
                } for e in entities
            ]
            
        finally:
            db.close()
    
    async def _get_entity_relationships(
        self, 
        entity_ids: List[int], 
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Get relationships involving the specified entities
        """
        db = SessionLocal()
        
        try:
            relationships = db.query(Relationship).filter(
                Relationship.source_id.in_(entity_ids) |
                Relationship.target_id.in_(entity_ids)
            ).order_by(Relationship.confidence_score.desc()).limit(limit).all()
            
            return [
                {
                    "source": r.source_entity.name,
                    "target": r.target_entity.name,
                    "type": r.relationship_type,
                    "context": r.context,
                    "confidence": r.confidence_score
                } for r in relationships
            ]
            
        finally:
            db.close()
    
    def _extract_query_keywords(self, query: str) -> List[str]:
        """
        Extract meaningful keywords from a query
        
        Simple implementation - could use NLP for better extraction.
        """
        # Remove common stop words
        stop_words = {
            "what", "is", "are", "how", "where", "when", "why", "who", "which",
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "with", "by", "about", "into", "through", "during", "before", "after",
            "above", "below", "up", "down", "out", "off", "over", "under", "again",
            "further", "then", "once"
        }
        
        words = query.lower().split()
        keywords = [word.strip(".,!?;:") for word in words if word not in stop_words and len(word) > 2]
        
        return keywords[:5]  # Limit to top 5 keywords
    
    def _extract_sources(
        self, 
        entities: List, 
        relationships: List
    ) -> List[str]:
        """
        Extract source URLs from entities and relationships
        """
        sources = set()
        
        for entity in entities:
            if entity.source_urls:
                try:
                    urls = json.loads(entity.source_urls)
                    sources.update(urls)
                except json.JSONDecodeError:
                    pass
        
        for relationship in relationships:
            if relationship.source_urls:
                try:
                    urls = json.loads(relationship.source_urls)
                    sources.update(urls)
                except json.JSONDecodeError:
                    pass
        
        return list(sources)
    
    async def _generate_answer(
        self, 
        query: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate an answer using AI model and retrieved context
        """
        if not self.openai_client:
            return self._generate_mock_answer(query, context)
        
        try:
            # Create context string
            context_str = self._format_context_for_prompt(context)
            
            prompt = f"""
Based on the following knowledge graph information, answer the user's question comprehensively and accurately.

Context:
{context_str}

Question: {query}

Please provide a clear, informative answer based on the available information. If the information is incomplete, acknowledge what you don't know. Include relevant entity names and relationships in your response.
"""
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a knowledgeable assistant specializing in the creator economy and digital platforms. Provide accurate, well-structured answers based on the provided context."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            return {
                "text": response.choices[0].message.content,
                "confidence": 0.8  # Default confidence for AI-generated content
            }
            
        except Exception as e:
            logger.error(f"AI answer generation failed: {e}")
            return self._generate_mock_answer(query, context)
    
    async def _generate_topic_summary(self, context: Dict[str, Any]) -> str:
        """
        Generate a topic summary using AI model
        """
        if not self.openai_client:
            return self._generate_mock_summary(context)
        
        try:
            context_str = self._format_context_for_summary(context)
            
            prompt = f"""
Create a comprehensive summary about "{context['topic']}" based on the following knowledge graph data:

{context_str}

The summary should:
1. Provide an overview of the topic
2. Highlight key entities and their roles
3. Explain important relationships
4. Identify current trends or developments
5. Be well-structured and informative

Please write in a clear, professional style suitable for someone learning about this topic.
"""
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert researcher and writer specializing in the creator economy and digital platforms. Create clear, comprehensive summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI summary generation failed: {e}")
            return self._generate_mock_summary(context)
    
    def _format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """Format context data for AI prompt"""
        formatted = "Entities:\n"
        for entity in context["entities"]:
            formatted += f"- {entity['name']} ({entity['type']}): {entity['description']}\n"
        
        if context["relationships"]:
            formatted += "\nRelationships:\n"
            for rel in context["relationships"]:
                formatted += f"- {rel['source']} {rel['type']} {rel['target']}"
                if rel['context']:
                    formatted += f": {rel['context']}"
                formatted += "\n"
        
        return formatted
    
    def _format_context_for_summary(self, context: Dict[str, Any]) -> str:
        """Format context data for summary generation"""
        formatted = f"Topic: {context['topic']}\n\n"
        
        if context["focus_areas"]:
            formatted += f"Focus Areas: {', '.join(context['focus_areas'])}\n\n"
        
        formatted += "Key Entities:\n"
        for entity in context["entities"]:
            formatted += f"- {entity['name']} ({entity['type']}): {entity['description']}\n"
        
        if context["relationships"]:
            formatted += "\nKey Relationships:\n"
            for rel in context["relationships"]:
                formatted += f"- {rel['source']} {rel['type']} {rel['target']}\n"
        
        return formatted
    
    def _generate_mock_answer(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock answer for development"""
        entities = context["entities"]
        relationships = context["relationships"]
        
        if entities:
            entity_names = [e["name"] for e in entities[:3]]
            answer = f"Based on the available information, your query about '{query}' relates to entities like {', '.join(entity_names)}."
            
            if relationships:
                answer += f" The knowledge graph shows {len(relationships)} relationships between these entities."
        else:
            answer = f"I found limited information about '{query}' in the current knowledge base."
        
        return {
            "text": answer,
            "confidence": 0.5
        }
    
    def _generate_mock_summary(self, context: Dict[str, Any]) -> str:
        """Generate mock summary for development"""
        topic = context["topic"]
        entities = context["entities"]
        
        summary = f"# Summary: {topic}\n\n"
        
        if entities:
            summary += f"The topic '{topic}' involves {len(entities)} key entities:\n\n"
            for entity in entities[:5]:
                summary += f"- **{entity['name']}** ({entity['type']}): {entity['description'][:100]}...\n"
        else:
            summary += f"Limited information is currently available about '{topic}' in the knowledge base."
        
        summary += "\n*This is a development summary. Full AI-generated summaries require API configuration.*"
        
        return summary