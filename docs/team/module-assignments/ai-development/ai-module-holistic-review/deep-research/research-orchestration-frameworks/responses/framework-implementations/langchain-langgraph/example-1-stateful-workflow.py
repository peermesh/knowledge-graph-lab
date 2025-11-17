"""
LangGraph Example 1: Stateful Research Workflow
Pattern: Graph-based workflow with persistent state

Key Learning: LangGraph thinks in terms of graphs (nodes + edges) where
state flows between nodes. This is powerful for deterministic workflows
where you know the research steps ahead of time. State is first-class,
making it easy to checkpoint and resume.

Setup Time: ~20 minutes (but steeper learning curve conceptually)
Code Lines: 55
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# Pattern: Define state schema
# This is where LangGraph shines - explicit state management
class ResearchState(TypedDict):
    """State that flows through the research workflow"""
    gap_description: str
    search_queries: Annotated[list, operator.add]  # Accumulates queries
    documents_found: Annotated[list, operator.add]  # Accumulates docs
    extracted_entities: Annotated[list, operator.add]
    synthesis_result: str
    confidence_score: float

# Pattern: Define node functions
# Each node is a pure function: state_in -> state_out
def generate_queries(state: ResearchState) -> ResearchState:
    """Node: Generate search queries from gap description"""
    gap = state["gap_description"]

    # In production, this would call LLM to generate queries
    # Here we show the pattern
    queries = [
        f"{gap} latest research",
        f"{gap} case studies 2025",
        f"{gap} academic papers"
    ]

    return {"search_queries": queries}

def search_documents(state: ResearchState) -> ResearchState:
    """Node: Search for documents using queries"""
    queries = state["search_queries"]

    # In production, this would call search APIs
    docs = []
    for query in queries:
        docs.append({
            "query": query,
            "title": f"Document for {query}",
            "url": "https://example.com/doc",
            "relevance": 0.85
        })

    return {"documents_found": docs}

def extract_information(state: ResearchState) -> ResearchState:
    """Node: Extract entities from documents"""
    docs = state["documents_found"]

    # In production, this would call entity extraction LLM
    entities = [
        {"type": "technique", "value": "Quantization", "confidence": 0.9},
        {"type": "vendor", "value": "Anthropic", "confidence": 0.95},
    ]

    return {"extracted_entities": entities}

def synthesize_findings(state: ResearchState) -> ResearchState:
    """Node: Synthesize all findings into answer"""
    entities = state["extracted_entities"]

    synthesis = f"Found {len(entities)} key entities from research."
    confidence = sum(e["confidence"] for e in entities) / len(entities)

    return {
        "synthesis_result": synthesis,
        "confidence_score": confidence
    }

# Pattern: Build the graph
# This is the orchestration layer - explicit flow definition
workflow = StateGraph(ResearchState)

# Add nodes
workflow.add_node("generate_queries", generate_queries)
workflow.add_node("search", search_documents)
workflow.add_node("extract", extract_information)
workflow.add_node("synthesize", synthesize_findings)

# Pattern: Define edges (workflow flow)
# This makes the research pipeline explicit and reviewable
workflow.set_entry_point("generate_queries")
workflow.add_edge("generate_queries", "search")
workflow.add_edge("search", "extract")
workflow.add_edge("extract", "synthesize")
workflow.add_edge("synthesize", END)

# Compile into runnable
app = workflow.compile()

# Pattern: Execute workflow
initial_state = {
    "gap_description": "LLM cost optimization strategies",
    "search_queries": [],
    "documents_found": [],
    "extracted_entities": [],
    "synthesis_result": "",
    "confidence_score": 0.0
}

# The workflow executes deterministically following the graph
result = app.invoke(initial_state)

print(f"Synthesis: {result['synthesis_result']}")
print(f"Confidence: {result['confidence_score']:.2f}")

# Key Insights:
# ✅ Strengths:
#    - Explicit state schema makes workflows type-safe
#    - Graph structure is easy to visualize and review
#    - State persistence enables checkpointing
#    - Deterministic flow is predictable and testable
#
# ⚠️ Challenges:
#    - Requires upfront workflow design
#    - Graph thinking has steeper learning curve
#    - Less flexible for dynamic, conversation-style research
#
# 💡 Best for: Research workflows with known steps where
#    state management and resumability matter
