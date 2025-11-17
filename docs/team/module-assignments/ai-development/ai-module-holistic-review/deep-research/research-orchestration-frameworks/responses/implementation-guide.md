# Implementation Guide: Building Research Orchestration in Multi-Agent Frameworks

## Overview

This guide walks through how to build agent orchestration for research workflows in AutoGen, LangGraph, and CrewAI. Each framework has different mental models and implementation patterns. Understanding these patterns is crucial for choosing the right framework.

---

## Part 1: AutoGen - Conversation-Based Orchestration

### Core Philosophy

AutoGen views agent orchestration as **conversations**. Agents communicate by sending messages back and forth, similar to how humans collaborate through discussion. The framework manages conversation flow and tracks message history.

### Mental Model

Think of AutoGen like managing a **Slack channel** where AI agents are team members. They read messages, respond, and collaborate through conversation. Your job is to define agent "personalities" (via system messages) and initiate productive conversations.

### Key Concepts

1. **Agents**: Conversational entities with roles and capabilities
2. **Messages**: Communication units between agents
3. **Conversation Flow**: How messages route between agents
4. **Termination**: When conversation concludes

### Implementation Pattern: Simple Two-Agent Research

```python
from autogen import AssistantAgent, UserProxyAgent

# Pattern 1: Define LLM configuration
# AutoGen uses a config list to support multiple models
llm_config = {
    "config_list": [{"model": "gpt-4", "api_key": "YOUR_KEY"}],
    "temperature": 0.7,
}

# Pattern 2: Create specialized agents
# System message defines agent's role and behavior
researcher = AssistantAgent(
    name="Researcher",
    system_message="""You are a research agent. When given a gap,
    formulate search queries, gather information, and cite sources.
    Reply TERMINATE when research is complete.""",
    llm_config=llm_config,
)

coordinator = UserProxyAgent(
    name="Coordinator",
    human_input_mode="NEVER",  # Autonomous
    max_consecutive_auto_reply=5,  # Prevent infinite loops
    code_execution_config=False,  # Disable code execution for now
)

# Pattern 3: Initiate conversation
# The conversation runs until TERMINATE appears
coordinator.initiate_chat(
    researcher,
    message="Research gap: LLM cost optimization strategies 2025",
)
```

**Key Insight**: Messages flow naturally. Each agent's response becomes the next message. This feels intuitive but can become verbose.

### Implementation Pattern: Multi-Agent GroupChat

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Create specialized agents for different research tasks
web_researcher = AssistantAgent(
    name="WebResearcher",
    system_message="Search web for current information. Provide URLs.",
    llm_config=llm_config,
)

academic_researcher = AssistantAgent(
    name="AcademicResearcher",
    system_message="Search academic databases. Provide DOIs/arXiv IDs.",
    llm_config=llm_config,
)

synthesizer = AssistantAgent(
    name="Synthesizer",
    system_message="Synthesize findings. Reply TERMINATE when done.",
    llm_config=llm_config,
)

# GroupChat manages multi-agent coordination
groupchat = GroupChat(
    agents=[coordinator, web_researcher, academic_researcher, synthesizer],
    messages=[],
    max_round=12,  # Safety limit
    speaker_selection_method="auto",  # LLM decides who speaks next
)

# GroupChatManager orchestrates the conversation
manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

# Initiate multi-agent research
coordinator.initiate_chat(
    manager,
    message="Research: Quantization techniques for LLM inference",
)
```

**Key Insight**: The `speaker_selection_method="auto"` uses an LLM to decide who speaks next. This is powerful but adds token overhead. Use `"round_robin"` for deterministic flow.

### When AutoGen's Patterns Work Well

✅ **Natural Fit:**
- Research requires multi-turn discussion and debate
- Need full conversation audit trail
- Agents should "talk through" complex problems
- Experimental/research projects where flexibility matters

⚠️ **Challenges:**
- Verbose conversations increase token costs
- Auto speaker selection adds LLM calls
- Termination conditions need careful design
- Debugging GroupChat routing can be opaque

---

## Part 2: LangGraph - Graph-Based Orchestration

### Core Philosophy

LangGraph views agent orchestration as **directed graphs**. Nodes are functions that transform state, edges define flow, and state flows through the graph. This makes workflows explicit, testable, and resumable.

### Mental Model

Think of LangGraph like **designing a flowchart**. Each box (node) is a processing step that reads state, does work, and updates state. Arrows (edges) show how control flows. State is the data structure that accumulates as it flows through.

### Key Concepts

1. **State**: Data structure (TypedDict) that flows through graph
2. **Nodes**: Pure functions (state_in → state_out)
3. **Edges**: Control flow (fixed or conditional)
4. **Graph**: Compiled workflow that executes nodes in order

### Implementation Pattern: Linear Research Pipeline

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# Pattern 1: Define state schema
# This is where LangGraph shines - explicit state management
class ResearchState(TypedDict):
    gap: str
    queries: Annotated[list, operator.add]  # Accumulates queries
    documents: Annotated[list, operator.add]  # Accumulates docs
    entities: Annotated[list, operator.add]  # Accumulates entities
    summary: str

# Pattern 2: Define node functions
# Each node is a pure function: state_in -> state_out

def generate_queries(state: ResearchState) -> ResearchState:
    """Node: Generate search queries from gap"""
    gap = state["gap"]
    # In production, call LLM to generate queries
    queries = [f"{gap} latest", f"{gap} case studies"]
    return {"queries": queries}

def search_documents(state: ResearchState) -> ResearchState:
    """Node: Search using queries"""
    queries = state["queries"]
    # In production, call search APIs
    docs = [{"title": q, "url": "...", "relevance": 0.8} for q in queries]
    return {"documents": docs}

def extract_entities(state: ResearchState) -> ResearchState:
    """Node: Extract entities from documents"""
    docs = state["documents"]
    # In production, call entity extraction LLM
    entities = [{"type": "technique", "name": "Quantization", "confidence": 0.9}]
    return {"entities": entities}

def synthesize(state: ResearchState) -> ResearchState:
    """Node: Synthesize findings"""
    entities = state["entities"]
    summary = f"Found {len(entities)} entities"
    return {"summary": summary}

# Pattern 3: Build the graph
workflow = StateGraph(ResearchState)

# Add nodes
workflow.add_node("generate", generate_queries)
workflow.add_node("search", search_documents)
workflow.add_node("extract", extract_entities)
workflow.add_node("synthesize", synthesize)

# Pattern 4: Define edges (workflow flow)
workflow.set_entry_point("generate")
workflow.add_edge("generate", "search")
workflow.add_edge("search", "extract")
workflow.add_edge("extract", "synthesize")
workflow.add_edge("synthesize", END)

# Compile into runnable
app = workflow.compile()

# Execute workflow
result = app.invoke({
    "gap": "LLM cost optimization",
    "queries": [],
    "documents": [],
    "entities": [],
    "summary": ""
})
```

**Key Insight**: The graph structure makes the research pipeline explicit and reviewable. State schema ensures type safety. This is more verbose than AutoGen but far more deterministic.

### Implementation Pattern: Supervisor Coordination

```python
from typing import Literal

class SupervisorState(TypedDict):
    task: str
    next_agent: str  # Supervisor's routing decision
    web_results: Annotated[list, operator.add]
    academic_results: Annotated[list, operator.add]
    synthesis: str

# Specialized agents as node functions
def web_agent(state: SupervisorState) -> SupervisorState:
    # Search web
    return {"web_results": [...]}

def academic_agent(state: SupervisorState) -> SupervisorState:
    # Search academic databases
    return {"academic_results": [...]}

def synthesis_agent(state: SupervisorState) -> SupervisorState:
    # Synthesize all findings
    return {"synthesis": "..."}

# Supervisor decides routing
def supervisor(state: SupervisorState) -> SupervisorState:
    # Routing logic based on state
    if not state.get("web_results"):
        return {"next_agent": "web"}
    elif not state.get("academic_results"):
        return {"next_agent": "academic"}
    elif not state.get("synthesis"):
        return {"next_agent": "synthesis"}
    else:
        return {"next_agent": "END"}

# Routing function for conditional edges
def route(state: SupervisorState) -> Literal["web", "academic", "synthesis", "END"]:
    return state["next_agent"]

# Build supervisor graph
workflow = StateGraph(SupervisorState)

workflow.add_node("supervisor", supervisor)
workflow.add_node("web", web_agent)
workflow.add_node("academic", academic_agent)
workflow.add_node("synthesis", synthesis_agent)

workflow.set_entry_point("supervisor")

# Conditional routing from supervisor
workflow.add_conditional_edges(
    "supervisor",
    route,
    {"web": "web", "academic": "academic", "synthesis": "synthesis", "END": END}
)

# Agents return to supervisor
workflow.add_edge("web", "supervisor")
workflow.add_edge("academic", "supervisor")
workflow.add_edge("synthesis", "supervisor")

app = workflow.compile()
```

**Key Insight**: Routing logic is explicit Python code, not hidden in LLM. This makes it deterministic and testable but requires more upfront design.

### When LangGraph's Patterns Work Well

✅ **Natural Fit:**
- Research workflow has clear, repeatable steps
- Need state persistence and checkpointing
- Want deterministic, testable orchestration
- Production deployment with observability requirements
- Long-running research that must survive failures

⚠️ **Challenges:**
- Requires upfront workflow design
- Graph thinking has steeper learning curve
- State schema must be designed carefully
- Less flexible for dynamic, conversational research

---

## Part 3: CrewAI - Role-Based Orchestration

### Core Philosophy

CrewAI views agent orchestration as **team management**. Agents are team members with roles, goals, and responsibilities. Tasks are assignments given to team members. The framework handles coordination automatically.

### Mental Model

Think of CrewAI like **managing a project team**. You define roles (researcher, analyst, writer), assign tasks, and let the team execute. The framework is the project manager that ensures tasks flow properly.

### Key Concepts

1. **Agents**: Team members with roles, goals, backstories
2. **Tasks**: Assignments with descriptions and expected outputs
3. **Crew**: Collection of agents and tasks
4. **Process**: How tasks execute (sequential, hierarchical)

### Implementation Pattern: Sequential Research Crew

```python
from crewai import Agent, Task, Crew, Process

# Pattern 1: Define agents with roles
# Think of this like writing job descriptions

researcher = Agent(
    role="Research Specialist",
    goal="Find comprehensive information about research gaps",
    backstory="""You're an expert researcher with 10 years of experience.
    You excel at finding web and academic sources, cite properly,
    and provide confidence ratings.""",
    verbose=True,
    allow_delegation=False  # This agent works independently
)

analyst = Agent(
    role="Data Analyst",
    goal="Extract structured information from research",
    backstory="""You specialize in entity extraction and relationship mapping.
    You create structured knowledge from unstructured text.""",
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role="Knowledge Synthesizer",
    goal="Combine findings into comprehensive answers",
    backstory="""You're a synthesis expert who combines information,
    identifies contradictions, and creates coherent summaries.""",
    verbose=True,
    allow_delegation=False
)

# Pattern 2: Define tasks
# Tasks are specific assignments with clear deliverables

research_task = Task(
    description="""Research the following gap: 'LLM cost optimization 2025'.
    Find at least 3 web sources and 2 academic sources.
    Include URLs and publication dates.""",
    agent=researcher,
    expected_output="List of 5+ sources with metadata"
)

analysis_task = Task(
    description="""Extract structured entities from research findings.
    Identify: vendors, techniques, metrics, case studies.
    Provide confidence scores.""",
    agent=analyst,
    expected_output="JSON list of entities with confidence scores"
)

synthesis_task = Task(
    description="""Synthesize findings into comprehensive answer.
    Include top 3 strategies, evidence, and confidence levels.""",
    agent=writer,
    expected_output="Comprehensive answer with confidence assessment"
)

# Pattern 3: Create crew and execute
# The crew handles coordination automatically
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, synthesis_task],
    process=Process.sequential,  # Tasks execute in order
    verbose=2  # Show execution details
)

# Execute the workflow
result = crew.kickoff()
```

**Key Insight**: No explicit coordination code needed. CrewAI handles task flow automatically. This is the fastest path to a working system.

### Implementation Pattern: Hierarchical Research Team

```python
# Define specialized worker agents
web_researcher = Agent(
    role="Web Research Specialist",
    goal="Search web for current information",
    backstory="You specialize in finding blog posts and industry reports.",
    allow_delegation=False
)

academic_researcher = Agent(
    role="Academic Research Specialist",
    goal="Search academic databases",
    backstory="You focus on peer-reviewed papers and technical reports.",
    allow_delegation=False
)

validator = Agent(
    role="Quality Assurance",
    goal="Validate research completeness and accuracy",
    backstory="You ensure research meets quality standards.",
    allow_delegation=False
)

# Define tasks (no strict ordering needed in hierarchical mode)
web_task = Task(
    description="Search web for: 'quantization techniques 2025'",
    agent=web_researcher,
    expected_output="5+ web sources"
)

academic_task = Task(
    description="Search academic sources for quantization papers",
    agent=academic_researcher,
    expected_output="3+ academic papers"
)

validation_task = Task(
    description="Validate research quality and completeness",
    agent=validator,
    expected_output="Quality report with score"
)

# Hierarchical crew - framework creates manager agent
crew = Crew(
    agents=[web_researcher, academic_researcher, validator],
    tasks=[web_task, academic_task, validation_task],
    process=Process.hierarchical,  # Manager coordinates
    manager_llm="gpt-4",  # Optional: specify manager LLM
    verbose=2
)

result = crew.kickoff()
```

**Key Insight**: In hierarchical mode, CrewAI creates a manager agent that coordinates workers. The manager delegates tasks dynamically based on agent capabilities.

### When CrewAI's Patterns Work Well

✅ **Natural Fit:**
- Roles and responsibilities are clear
- Sequential or hierarchical flow matches use case
- Team wants to move fast with minimal coordination code
- Developers prefer high-level abstractions
- Rapid prototyping needed

⚠️ **Challenges:**
- Less control over coordination logic
- Hierarchical manager behavior can be opaque
- Sequential execution default (less flexible)
- Logging inside tasks can be problematic

---

## Part 4: Pattern Comparison

### Research Workflow: Gap Detection → Search → Extraction → Synthesis

#### AutoGen Approach
**Pattern**: Conversation with termination
```python
# Agents discuss until TERMINATE appears
coordinator.initiate_chat(researcher, message="Research gap...")
# Coordination: Implicit in conversation
```

#### LangGraph Approach
**Pattern**: Explicit graph pipeline
```python
# Define nodes and edges explicitly
workflow.add_edge("search", "extract")
workflow.add_edge("extract", "synthesize")
# Coordination: Explicit in graph structure
```

#### CrewAI Approach
**Pattern**: Sequential task execution
```python
# Define tasks in order
crew = Crew(agents=[...], tasks=[search, extract, synthesize])
# Coordination: Automatic
```

### Multi-Agent Coordination

#### AutoGen Approach
**Pattern**: GroupChat with speaker selection
```python
groupchat = GroupChat(agents=[...], speaker_selection_method="auto")
# Who speaks next: LLM decides or round-robin
```

#### LangGraph Approach
**Pattern**: Supervisor with conditional routing
```python
def route(state): return state["next_agent"]
workflow.add_conditional_edges("supervisor", route, {...})
# Who executes next: Explicit routing function
```

#### CrewAI Approach
**Pattern**: Hierarchical with manager
```python
crew = Crew(agents=[...], process=Process.hierarchical)
# Who executes next: Framework's manager agent
```

---

## Recommendations

### Choose AutoGen if you want:
- Conversational, discussion-based research
- Full message audit trail
- Flexibility to experiment
- Comfort with message-passing paradigms

### Choose LangGraph if you want:
- Deterministic, testable workflows
- State persistence and checkpointing
- Production-grade observability
- Maximum control over orchestration

### Choose CrewAI if you want:
- Fastest path to working system
- Intuitive role/task abstraction
- Minimal coordination code
- Rapid prototyping

---

## Next Steps

1. **Prototype**: Implement simple research workflow in preferred framework
2. **Test**: Measure setup time, code complexity, learning curve
3. **Evaluate**: Assess fit for your team's mental models
4. **Decide**: Choose based on timeline, requirements, team skills

The best framework is the one your team will actually use effectively.
