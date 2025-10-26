"""Relationship mapping service - identifies relationships between entities"""

from typing import List, Dict, Any, Optional
import logging
import re

from src.ai.integrations.llm_client import llm_client

logger = logging.getLogger(__name__)


class RelationshipMapper:
    """Service for identifying relationships between entities"""
    
    RELATIONSHIP_TYPES = [
        'fund',
        'partner',
        'acquire',
        'compete',
        'collaborate',
        'mention'
    ]
    
    # Relationship patterns for rule-based detection
    RELATIONSHIP_PATTERNS = {
        'fund': [
            r'{source}.*(?:invested|funded|financing).*{target}',
            r'{target}.*(?:received|secured).*(?:funding|investment).*{source}',
            r'{source}.*(?:\$[\d.]+\s*(?:million|billion)).*{target}'
        ],
        'partner': [
            r'{source}.*(?:partner(?:ed|ship)|collaborat(?:e|ion)).*{target}',
            r'{source}.*(?:joint venture|alliance).*{target}'
        ],
        'acquire': [
            r'{source}.*(?:acquired|bought|purchased).*{target}',
            r'{target}.*(?:acquired by|sold to).*{source}'
        ],
        'compete': [
            r'{source}.*(?:compet(?:e|ing|itor)).*{target}',
            r'{source}.*(?:rival|versus|vs\.?).*{target}'
        ],
        'collaborate': [
            r'{source}.*(?:work(?:ing)? with|team(?:ed)? up).*{target}',
            r'{source}.*(?:joint|together).*{target}'
        ]
    }
    
    def __init__(self):
        """Initialize relationship mapper"""
        self.llm_client = llm_client
    
    async def identify_relationships(
        self,
        entities: List[Dict[str, Any]],
        text: str,
        relationship_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Identify relationships between entities.
        
        Args:
            entities: List of extracted entities
            text: Source text containing entities
            relationship_types: Types of relationships to identify
        
        Returns:
            List of identified relationships
        """
        if not entities or len(entities) < 2:
            logger.info("Not enough entities for relationship mapping")
            return []
        
        if relationship_types is None:
            relationship_types = self.RELATIONSHIP_TYPES
        
        # Use both rule-based and LLM-based approaches
        rule_based_rels = await self._rule_based_mapping(
            entities,
            text,
            relationship_types
        )
        
        llm_based_rels = await self._llm_based_mapping(
            entities,
            text,
            relationship_types
        )
        
        # Combine and deduplicate
        all_relationships = rule_based_rels + llm_based_rels
        deduplicated = self._deduplicate_relationships(all_relationships)
        
        logger.info(
            f"Identified {len(deduplicated)} relationships "
            f"({len(rule_based_rels)} rule-based, {len(llm_based_rels)} LLM-based)"
        )
        
        return deduplicated
    
    async def _rule_based_mapping(
        self,
        entities: List[Dict[str, Any]],
        text: str,
        relationship_types: List[str]
    ) -> List[Dict[str, Any]]:
        """Identify relationships using pattern matching"""
        relationships = []
        text_lower = text.lower()
        
        # Check all entity pairs
        for i, source_entity in enumerate(entities):
            for target_entity in entities[i+1:]:
                if source_entity['id'] == target_entity['id']:
                    continue
                
                # Try each relationship type
                for rel_type in relationship_types:
                    if rel_type not in self.RELATIONSHIP_PATTERNS:
                        continue
                    
                    # Try each pattern for this relationship type
                    for pattern_template in self.RELATIONSHIP_PATTERNS[rel_type]:
                        # Create pattern with actual entity names
                        pattern = pattern_template.format(
                            source=re.escape(source_entity['text'].lower()),
                            target=re.escape(target_entity['text'].lower())
                        )
                        
                        match = re.search(pattern, text_lower, re.IGNORECASE)
                        if match:
                            # Extract evidence text
                            evidence_start = max(0, match.start() - 50)
                            evidence_end = min(len(text), match.end() + 50)
                            evidence = text[evidence_start:evidence_end]
                            
                            relationships.append({
                                'source_entity_id': source_entity['id'],
                                'target_entity_id': target_entity['id'],
                                'relationship_type': rel_type,
                                'confidence': 0.75,  # Rule-based gets medium confidence
                                'evidence': evidence.strip(),
                                'detection_method': 'rule_based',
                                'metadata': {
                                    'pattern_matched': pattern_template
                                }
                            })
                            break  # Found relationship, stop trying patterns
        
        return relationships
    
    async def _llm_based_mapping(
        self,
        entities: List[Dict[str, Any]],
        text: str,
        relationship_types: List[str]
    ) -> List[Dict[str, Any]]:
        """Identify relationships using LLM"""
        try:
            # Prepare entity list for prompt
            entity_texts = [e['text'] for e in entities]
            
            # Call LLM to identify relationships
            result = await self.llm_client.extract_entities(
                text=text,
                entity_types=[],  # We already have entities
                language='en'
            )
            
            # Process relationship results
            relationships = []
            for rel_data in result.get('relationships', []):
                # Find matching entities
                source_entity = self._find_entity_by_text(
                    entities,
                    rel_data.get('source_entity', '')
                )
                target_entity = self._find_entity_by_text(
                    entities,
                    rel_data.get('target_entity', '')
                )
                
                if source_entity and target_entity:
                    rel_type = rel_data.get('relationship_type', '').lower()
                    if rel_type in relationship_types:
                        relationships.append({
                            'source_entity_id': source_entity['id'],
                            'target_entity_id': target_entity['id'],
                            'relationship_type': rel_type,
                            'confidence': float(rel_data.get('confidence', 0.7)),
                            'evidence': rel_data.get('evidence', ''),
                            'detection_method': 'llm_based',
                            'metadata': {}
                        })
            
            return relationships
        
        except Exception as e:
            logger.warning(f"LLM-based relationship mapping failed: {e}")
            return []
    
    def _find_entity_by_text(
        self,
        entities: List[Dict[str, Any]],
        text: str
    ) -> Optional[Dict[str, Any]]:
        """Find entity by matching text"""
        text_lower = text.lower()
        
        for entity in entities:
            if entity['text'].lower() == text_lower:
                return entity
            
            # Check aliases
            aliases = entity.get('metadata', {}).get('aliases', [])
            if any(alias.lower() == text_lower for alias in aliases):
                return entity
        
        return None
    
    def _deduplicate_relationships(
        self,
        relationships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate relationships"""
        seen = set()
        deduplicated = []
        
        for rel in relationships:
            # Create unique key
            key = (
                rel['source_entity_id'],
                rel['target_entity_id'],
                rel['relationship_type']
            )
            
            if key not in seen:
                seen.add(key)
                deduplicated.append(rel)
            else:
                # If duplicate, keep the one with higher confidence
                existing_idx = next(
                    i for i, r in enumerate(deduplicated)
                    if (r['source_entity_id'], r['target_entity_id'], r['relationship_type']) == key
                )
                
                if rel['confidence'] > deduplicated[existing_idx]['confidence']:
                    deduplicated[existing_idx] = rel
        
        return deduplicated
    
    async def calculate_relationship_strength(
        self,
        relationship: Dict[str, Any],
        entities: List[Dict[str, Any]],
        text: str
    ) -> float:
        """
        Calculate relationship strength based on evidence and context.
        
        Args:
            relationship: Relationship data
            entities: All entities
            text: Source text
        
        Returns:
            Strength score (0.0-1.0)
        """
        # Factors that increase strength:
        # 1. Strong evidence text
        # 2. Multiple mentions
        # 3. Explicit relationship keywords
        # 4. Proximity of entities in text
        
        evidence = relationship.get('evidence', '')
        confidence = relationship.get('confidence', 0.5)
        
        # Base strength from confidence
        strength = confidence
        
        # Boost if evidence is substantial (>50 characters)
        if len(evidence) > 50:
            strength = min(strength * 1.1, 1.0)
        
        # Boost for explicit relationship verbs
        strong_verbs = ['invested', 'acquired', 'partnered', 'funded', 'merged']
        if any(verb in evidence.lower() for verb in strong_verbs):
            strength = min(strength * 1.15, 1.0)
        
        return round(strength, 2)


# Global relationship mapper instance
relationship_mapper = RelationshipMapper()

