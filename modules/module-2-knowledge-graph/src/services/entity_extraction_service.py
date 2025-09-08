"""
Entity extraction and relationship detection service
"""

import spacy
from typing import List, Dict, Any, Optional, Tuple
import re
import logging
from sentence_transformers import SentenceTransformer
import numpy as np

from ..core.config import settings

logger = logging.getLogger(__name__)

class EntityExtractionService:
    """
    Service for extracting entities and relationships from text content
    
    Uses spaCy for NER and custom rules for creator economy entities.
    """
    
    def __init__(self):
        self.nlp = None
        self.embedding_model = None
        self.custom_patterns = self._load_custom_patterns()
    
    async def initialize(self):
        """Initialize NLP models"""
        try:
            # Load spaCy model
            self.nlp = spacy.load(settings.NER_MODEL)
            logger.info(f"Loaded spaCy model: {settings.NER_MODEL}")
            
            # Load embedding model for similarity
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info(f"Loaded embedding model: {settings.EMBEDDING_MODEL}")
            
            # Add custom entity patterns
            self._add_custom_patterns()
            
        except Exception as e:
            logger.error(f"Failed to initialize entity extraction: {e}")
            # Use mock service for development
            self.nlp = None
            self.embedding_model = None
    
    async def cleanup(self):
        """Clean up resources"""
        pass
    
    def _load_custom_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for detecting creator economy entities"""
        return {
            "PLATFORM": [
                r"YouTube", r"TikTok", r"Instagram", r"Twitter", r"Facebook",
                r"Twitch", r"OnlyFans", r"Patreon", r"Substack", r"Medium",
                r"Discord", r"Clubhouse", r"LinkedIn", r"Snapchat", r"Pinterest"
            ],
            "CREATOR": [
                r"influencer", r"content creator", r"YouTuber", r"streamer",
                r"blogger", r"podcaster", r"artist", r"musician", r"writer"
            ],
            "POLICY": [
                r"terms of service", r"community guidelines", r"content policy",
                r"monetization policy", r"privacy policy", r"copyright policy"
            ],
            "GRANT": [
                r"creator fund", r"grant program", r"funding opportunity",
                r"accelerator program", r"incubator", r"scholarship"
            ]
        }
    
    def _add_custom_patterns(self):
        """Add custom entity recognition patterns to spaCy"""
        if not self.nlp:
            return
        
        # Add pattern matcher
        from spacy.matcher import Matcher
        matcher = Matcher(self.nlp.vocab)
        
        for entity_type, patterns in self.custom_patterns.items():
            for pattern in patterns:
                # Convert to spaCy pattern format
                pattern_list = [{"LOWER": {"REGEX": pattern.lower()}}]
                matcher.add(entity_type, [pattern_list])
    
    async def extract_entities(self, text: str, source_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Extract entities from text content
        
        Returns list of entities with type, confidence, and context.
        """
        if not self.nlp:
            return self._mock_entity_extraction(text)
        
        try:
            # Process text with spaCy
            doc = self.nlp(text)
            
            entities = []
            
            # Standard NER entities
            for ent in doc.ents:
                entity_type = self._map_spacy_to_custom_type(ent.label_)
                if entity_type:
                    entities.append({
                        "text": ent.text,
                        "type": entity_type,
                        "confidence": 0.8,  # Default confidence for spaCy NER
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "context": self._extract_context(text, ent.start_char, ent.end_char),
                        "source": "spacy_ner"
                    })
            
            # Custom pattern matching
            custom_entities = self._extract_custom_entities(text)
            entities.extend(custom_entities)
            
            # Remove duplicates and filter by confidence
            entities = self._deduplicate_entities(entities)
            entities = [e for e in entities if e["confidence"] >= 0.5]
            
            return entities
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return []
    
    def _map_spacy_to_custom_type(self, spacy_label: str) -> Optional[str]:
        """Map spaCy entity labels to custom entity types"""
        mapping = {
            "ORG": "organization",
            "PERSON": "creator", 
            "PRODUCT": "platform",
            "EVENT": "event",
            "GPE": "location",  # Not directly used but good for metadata
            "MONEY": None,  # Skip money entities for now
            "DATE": "event",  # Dates often indicate events
        }
        return mapping.get(spacy_label)
    
    def _extract_custom_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities using custom patterns"""
        entities = []
        
        for entity_type, patterns in self.custom_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entities.append({
                        "text": match.group(),
                        "type": entity_type.lower(),
                        "confidence": 0.7,  # Default confidence for pattern matching
                        "start": match.start(),
                        "end": match.end(),
                        "context": self._extract_context(text, match.start(), match.end()),
                        "source": "pattern_matching"
                    })
        
        return entities
    
    def _extract_context(self, text: str, start: int, end: int, window: int = 100) -> str:
        """Extract context around an entity"""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end].strip()
    
    def _deduplicate_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate entities based on text and type"""
        seen = set()
        unique_entities = []
        
        for entity in entities:
            key = (entity["text"].lower(), entity["type"])
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
        
        return unique_entities
    
    async def extract_relationships(
        self, 
        entities: List[Dict[str, Any]], 
        text: str
    ) -> List[Dict[str, Any]]:
        """
        Extract relationships between entities in the text
        
        Uses dependency parsing and pattern matching to find relationships.
        """
        if not self.nlp or len(entities) < 2:
            return []
        
        try:
            doc = self.nlp(text)
            relationships = []
            
            # Simple relationship extraction based on sentence structure
            for sent in doc.sents:
                sent_entities = [e for e in entities if self._entity_in_sentence(e, sent)]
                
                if len(sent_entities) >= 2:
                    # Find relationships between pairs in the same sentence
                    for i, entity1 in enumerate(sent_entities):
                        for entity2 in sent_entities[i+1:]:
                            relationship = self._detect_relationship(entity1, entity2, sent.text)
                            if relationship:
                                relationships.append(relationship)
            
            return relationships
            
        except Exception as e:
            logger.error(f"Relationship extraction failed: {e}")
            return []
    
    def _entity_in_sentence(self, entity: Dict[str, Any], sentence) -> bool:
        """Check if entity appears in the sentence"""
        return (entity["start"] >= sentence.start_char and 
                entity["end"] <= sentence.end_char)
    
    def _detect_relationship(
        self, 
        entity1: Dict[str, Any], 
        entity2: Dict[str, Any], 
        sentence: str
    ) -> Optional[Dict[str, Any]]:
        """
        Detect relationship between two entities in a sentence
        
        Uses simple pattern matching - could be enhanced with ML.
        """
        patterns = {
            "owns": [r"owns", r"acquired", r"bought"],
            "created_by": [r"created by", r"founded by", r"started by"],
            "partners_with": [r"partners with", r"collaborates with", r"works with"],
            "regulates": [r"regulates", r"governs", r"oversees"],
            "funds": [r"funds", r"sponsors", r"supports financially"],
            "competes_with": [r"competes with", r"rivals", r"alternative to"]
        }
        
        sentence_lower = sentence.lower()
        
        for rel_type, rel_patterns in patterns.items():
            for pattern in rel_patterns:
                if re.search(pattern, sentence_lower):
                    return {
                        "source": entity1["text"],
                        "target": entity2["text"],
                        "type": rel_type,
                        "confidence": 0.6,
                        "context": sentence,
                        "source_entity_type": entity1["type"],
                        "target_entity_type": entity2["type"]
                    }
        
        return None
    
    def _mock_entity_extraction(self, text: str) -> List[Dict[str, Any]]:
        """Mock entity extraction for development"""
        # Simple keyword-based extraction for testing
        mock_entities = []
        
        keywords = {
            "platform": ["YouTube", "TikTok", "Instagram", "Twitter", "platform"],
            "creator": ["creator", "influencer", "artist", "YouTuber"],
            "organization": ["Google", "Meta", "company", "organization"],
            "policy": ["policy", "terms", "guidelines", "rules"]
        }
        
        for entity_type, words in keywords.items():
            for word in words:
                if word.lower() in text.lower():
                    start = text.lower().find(word.lower())
                    if start != -1:
                        mock_entities.append({
                            "text": word,
                            "type": entity_type,
                            "confidence": 0.5,
                            "start": start,
                            "end": start + len(word),
                            "context": text[max(0, start-50):start+50],
                            "source": "mock_extraction"
                        })
        
        return mock_entities
    
    async def calculate_entity_similarity(
        self, 
        entity1_text: str, 
        entity2_text: str
    ) -> float:
        """
        Calculate semantic similarity between two entity mentions
        
        Uses sentence transformer embeddings for similarity.
        """
        if not self.embedding_model:
            # Simple string similarity fallback
            return self._simple_string_similarity(entity1_text, entity2_text)
        
        try:
            # Generate embeddings
            embeddings = self.embedding_model.encode([entity1_text, entity2_text])
            
            # Calculate cosine similarity
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            return self._simple_string_similarity(entity1_text, entity2_text)
    
    def _simple_string_similarity(self, str1: str, str2: str) -> float:
        """Simple string similarity using edit distance"""
        if str1 == str2:
            return 1.0
        
        # Normalize strings
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()
        
        if str1 in str2 or str2 in str1:
            return 0.8
        
        # Simple Jaccard similarity on words
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0