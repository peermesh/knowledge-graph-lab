"""
Relationship Type Taxonomy for Academic Knowledge Graphs

Defines the core relationship types used in academic paper knowledge graph construction,
including type definitions, validation rules, and examples.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class RelationshipType(Enum):
    """Core academic relationship types"""
    AUTHORSHIP = "authorship"
    CITATION = "citation"
    AFFILIATION = "affiliation"
    PUBLICATION = "publication"
    CONTRIBUTION = "contribution"
    BUILDS_ON = "builds-on"
    STUDIES = "studies"
    COLLABORATION = "collaboration"
    FUNDING = "funding"
    SUPERVISION = "supervision"
    NONE = "none"  # No relationship detected


@dataclass
class RelationshipDefinition:
    """Definition of a relationship type"""
    name: str
    description: str
    examples: List[str]
    typical_patterns: List[str]
    inverse_type: str = None


# Relationship Type Taxonomy
RELATIONSHIP_TAXONOMY: Dict[RelationshipType, RelationshipDefinition] = {
    RelationshipType.AUTHORSHIP: RelationshipDefinition(
        name="authorship",
        description="Author created/wrote a paper or work",
        examples=[
            "Johnson et al. authored 'Neural Networks for KG'",
            "The paper by Smith and collaborators...",
            "'Graph Embeddings' was written by Chen et al."
        ],
        typical_patterns=["wrote", "authored", "published by", "by [author]"],
        inverse_type="authored_by"
    ),

    RelationshipType.CITATION: RelationshipDefinition(
        name="citation",
        description="Paper cites or references another paper",
        examples=[
            "Johnson et al. (2023) cite Smith et al. (2022)",
            "Building on prior work [Smith 2020]...",
            "As shown by Chen et al. [15]..."
        ],
        typical_patterns=["cites", "references", "builds on", "[citation]", "et al."],
        inverse_type="cited_by"
    ),

    RelationshipType.AFFILIATION: RelationshipDefinition(
        name="affiliation",
        description="Author affiliated with an institution or organization",
        examples=[
            "Alice Johnson at Stanford University",
            "Smith, researcher at Google DeepMind",
            "Chen is affiliated with MIT CSAIL"
        ],
        typical_patterns=["at", "affiliated with", "from", "researcher at", "professor at"],
        inverse_type="employs"
    ),

    RelationshipType.PUBLICATION: RelationshipDefinition(
        name="publication",
        description="Paper published in a venue (conference, journal)",
        examples=[
            "Published in Nature Communications",
            "Presented at ACL 2024",
            "Appeared in ICML proceedings"
        ],
        typical_patterns=["published in", "appeared in", "presented at", "proceedings of"],
        inverse_type="published"
    ),

    RelationshipType.CONTRIBUTION: RelationshipDefinition(
        name="contribution",
        description="Author made contributions to a concept, field, or area",
        examples=[
            "Johnson's contributions to graph neural networks",
            "Smith pioneered work in knowledge embeddings",
            "Chen developed novel attention mechanisms"
        ],
        typical_patterns=["contributed to", "pioneered", "developed", "introduced"],
        inverse_type="contributed_by"
    ),

    RelationshipType.BUILDS_ON: RelationshipDefinition(
        name="builds-on",
        description="Concept or work builds upon another concept or work",
        examples=[
            "TransE builds on word2vec embeddings",
            "GAT extends the GCN architecture",
            "Our method is based on prior work in..."
        ],
        typical_patterns=["builds on", "extends", "based on", "inspired by", "improves upon"],
        inverse_type="foundation_for"
    ),

    RelationshipType.STUDIES: RelationshipDefinition(
        name="studies",
        description="Paper investigates, analyzes, or studies a concept or problem",
        examples=[
            "This paper studies link prediction methods",
            "We analyze knowledge graph completion",
            "The work investigates embedding techniques"
        ],
        typical_patterns=["studies", "investigates", "analyzes", "examines", "explores"],
        inverse_type="studied_by"
    ),

    RelationshipType.COLLABORATION: RelationshipDefinition(
        name="collaboration",
        description="Authors collaborated on research or papers",
        examples=[
            "Johnson and Smith co-authored three papers",
            "Chen collaborated with the Stanford team",
            "Joint work between MIT and Google"
        ],
        typical_patterns=["co-authored", "collaborated", "joint work", "with"],
        inverse_type="collaborated_with"
    ),

    RelationshipType.FUNDING: RelationshipDefinition(
        name="funding",
        description="Organization funded research or project",
        examples=[
            "Funded by National Science Foundation",
            "NSF grant NSF-2024-001 supported this work",
            "Google Research provided funding"
        ],
        typical_patterns=["funded by", "supported by", "grant", "funding from"],
        inverse_type="funded"
    ),

    RelationshipType.SUPERVISION: RelationshipDefinition(
        name="supervision",
        description="Advisor supervised student's research",
        examples=[
            "Dr. Smith supervised Johnson's PhD research",
            "Advised by Professor Chen",
            "Martinez was Johnson's doctoral advisor"
        ],
        typical_patterns=["supervised", "advised", "advisor", "mentor"],
        inverse_type="supervised_by"
    ),
}


def get_relationship_definition(rel_type: RelationshipType) -> RelationshipDefinition:
    """Get definition for a relationship type"""
    return RELATIONSHIP_TAXONOMY.get(rel_type)


def get_all_relationship_types() -> List[str]:
    """Get list of all relationship type names"""
    return [rt.value for rt in RelationshipType if rt != RelationshipType.NONE]


def get_relationship_examples(rel_type: RelationshipType) -> List[str]:
    """Get example sentences for a relationship type"""
    definition = RELATIONSHIP_TAXONOMY.get(rel_type)
    return definition.examples if definition else []


def validate_relationship_type(rel_type_str: str) -> bool:
    """Check if a string is a valid relationship type"""
    try:
        RelationshipType(rel_type_str)
        return True
    except ValueError:
        return False


def get_inverse_relationship(rel_type: RelationshipType) -> str:
    """Get the inverse relationship type (e.g., 'cites' -> 'cited_by')"""
    definition = RELATIONSHIP_TAXONOMY.get(rel_type)
    return definition.inverse_type if definition else None


# Relationship annotation guidelines
ANNOTATION_GUIDELINES = {
    "explicit": "Relationship is directly stated with clear linguistic markers",
    "implicit": "Relationship must be inferred from context",
    "confidence_high": "Confidence > 0.9 - Clear, unambiguous relationship",
    "confidence_medium": "Confidence 0.7-0.9 - Likely relationship with some ambiguity",
    "confidence_low": "Confidence < 0.7 - Uncertain or weak relationship signal",
    "negation_handling": "Detect negations (not, no, never) and mark as no relationship",
    "temporal_scope": "Consider temporal context for accuracy (current vs historical)",
    "direction_matters": "Most relationships are directed (e.g., A cites B != B cites A)",
}


if __name__ == "__main__":
    # Demonstrate usage
    print("Academic Relationship Type Taxonomy")
    print("=" * 50)

    for rel_type in RelationshipType:
        if rel_type == RelationshipType.NONE:
            continue

        definition = get_relationship_definition(rel_type)
        print(f"\n{rel_type.value.upper()}")
        print(f"Description: {definition.description}")
        print(f"Example: {definition.examples[0]}")
        print(f"Inverse: {definition.inverse_type}")
