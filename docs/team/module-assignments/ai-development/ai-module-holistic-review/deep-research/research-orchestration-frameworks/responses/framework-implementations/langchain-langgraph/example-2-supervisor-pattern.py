"""
LangGraph Example 2: Supervisor Multi-Agent Pattern
Pattern: Supervisor agent coordinates specialized worker agents

Key Learning: The supervisor pattern is LangGraph's answer to multi-agent
coordination. A supervisor agent decides which worker to invoke based on
task requirements. This is more deterministic than AutoGen's GroupChat
but less conversational.

Setup Time: ~50 minutes (understanding routing logic)
Code Lines: 95
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal, Annotated
import operator

# Pattern: State includes routing information
class SupervisorState(TypedDict):
    """State managed by supervisor"""
    task_description: str
    next_agent: str  # Supervisor decision
    messages: Annotated[list, operator.add]
    web_results: Annotated[list, operator.add]
    academic_results: Annotated[list, operator.add]
    final_synthesis: str

# Pattern: Specialized agent functions
# Each agent is a node that performs specific research

def web_research_agent(state: SupervisorState) -> SupervisorState:
    """Agent: Search web for current information"""
    task = state["task_description"]

    # Simulate web search
    results = [
        {"source": "blog", "title": "Latest on " + task, "relevance": 0.8},
        {"source": "news", "title": "Industry view on " + task, "relevance": 0.7},
    ]

    return {
        "web_results": results,
        "messages": [f"WebAgent: Found {len(results)} web sources"]
    }

def academic_research_agent(state: SupervisorState) -> SupervisorState:
    """Agent: Search academic databases"""
    task = state["task_description"]

    # Simulate academic search
    results = [
        {"source": "arxiv", "title": "Research on " + task, "confidence": 0.9},
        {"source": "pubmed", "title": "Study of " + task, "confidence": 0.85},
    ]

    return {
        "academic_results": results,
        "messages": [f"AcademicAgent: Found {len(results)} papers"]
    }

def synthesis_agent(state: SupervisorState) -> SupervisorState:
    """Agent: Synthesize all findings"""
    web = state.get("web_results", [])
    academic = state.get("academic_results", [])

    synthesis = f"Synthesized {len(web)} web + {len(academic)} academic sources"

    return {
        "final_synthesis": synthesis,
        "messages": [f"Synthesizer: {synthesis}"]
    }

# Pattern: Supervisor routing logic
# This is the intelligence that decides workflow
def supervisor_router(state: SupervisorState) -> SupervisorState:
    """Supervisor decides which agent to call next"""

    web = state.get("web_results", [])
    academic = state.get("academic_results", [])

    # Routing logic based on current state
    if not web:
        return {"next_agent": "web_researcher"}
    elif not academic:
        return {"next_agent": "academic_researcher"}
    elif not state.get("final_synthesis"):
        return {"next_agent": "synthesizer"}
    else:
        return {"next_agent": "END"}

# Pattern: Conditional routing function
# LangGraph uses this to determine next node dynamically
def route_to_agent(state: SupervisorState) -> Literal["web_researcher", "academic_researcher", "synthesizer", "END"]:
    """Route to next agent based on supervisor decision"""
    next_agent = state.get("next_agent", "web_researcher")
    return next_agent

# Pattern: Build supervisor workflow graph
workflow = StateGraph(SupervisorState)

# Add all agent nodes
workflow.add_node("supervisor", supervisor_router)
workflow.add_node("web_researcher", web_research_agent)
workflow.add_node("academic_researcher", academic_research_agent)
workflow.add_node("synthesizer", synthesis_agent)

# Pattern: Entry point is supervisor
workflow.set_entry_point("supervisor")

# Pattern: Conditional edges based on routing
# This is how supervisor controls flow
workflow.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "web_researcher": "web_researcher",
        "academic_researcher": "academic_researcher",
        "synthesizer": "synthesizer",
        "END": END
    }
)

# After each agent, return to supervisor
workflow.add_edge("web_researcher", "supervisor")
workflow.add_edge("academic_researcher", "supervisor")
workflow.add_edge("synthesizer", "supervisor")

# Compile and run
app = workflow.compile()

initial_state = {
    "task_description": "quantization techniques for LLM inference",
    "next_agent": "",
    "messages": [],
    "web_results": [],
    "academic_results": [],
    "final_synthesis": ""
}

result = app.invoke(initial_state)

print("Messages:")
for msg in result["messages"]:
    print(f"  {msg}")
print(f"\nFinal: {result['final_synthesis']}")

# Key Insights:
# ✅ Strengths:
#    - Supervisor routing is deterministic and debuggable
#    - Each agent's scope is clear and bounded
#    - Easy to visualize workflow as graph
#    - State-based routing is explicit, not hidden in LLM
#
# ⚠️ Challenges:
#    - Routing logic must be hand-coded
#    - Less flexible than conversation-based coordination
#    - Requires thinking in terms of state transitions
#    - Supervisor node can become complex for many agents
#
# 💡 Best for: Research with clear agent roles where
#    deterministic coordination is preferred over LLM-driven routing
