# CrewAI Framework Examples

## Overview

CrewAI uses **role-based agent coordination** where agents are like team members with specific roles, goals, and backstories. Tasks are assigned to agents and the framework handles orchestration automatically.

## Core Philosophy

- **Human-Centric**: Agents have roles, goals, backstories (like team members)
- **Task-Driven**: Work is organized as tasks assigned to agents
- **Automatic Coordination**: Framework handles agent communication
- **Rapid Prototyping**: Quickest path from concept to working crew

## Examples Included

### Example 1: Role-Based Coordination (`example-1-role-based-coordination.py`)
**Pattern**: Sequential task execution with specialized agents
**Use Case**: researcher → analyst → synthesizer (fixed pipeline)
**Key Learning**: Role/task abstraction is most intuitive
**Setup Time**: ~25 minutes (fastest to get started)
**Code Complexity**: 40 lines (least code needed)

### Example 2: Hierarchical Coordination (`example-2-hierarchical-coordination.py`)
**Pattern**: Manager agent coordinates specialist workers
**Use Case**: Manager delegates to web/academic researchers + validator
**Key Learning**: Hierarchical mode adds oversight and quality control
**Setup Time**: ~40 minutes
**Code Complexity**: 85 lines

## When to Use CrewAI

✅ **Good Fit:**
- Team wants to move fast with minimal orchestration code
- Roles and responsibilities are clear
- Sequential or hierarchical workflows match use case
- Developers prefer high-level abstractions
- Rapid prototyping and iteration needed

⚠️ **Challenges:**
- Less control over coordination logic
- Logging inside tasks can be problematic
- Sequential execution is default (less flexible)
- Hierarchical manager behavior can be opaque
- Verbose output can be hard to parse

## Key Patterns

### 1. Agent Definition
```python
agent = Agent(
    role="Research Specialist",
    goal="Find comprehensive information",
    backstory="Expert with 10 years experience...",
    allow_delegation=False
)
```

### 2. Task Definition
```python
task = Task(
    description="Research the following gap...",
    agent=researcher,
    expected_output="List of sources with URLs"
)
```

### 3. Sequential Crew
```python
crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.sequential
)
result = crew.kickoff()
```

### 4. Hierarchical Crew
```python
crew = Crew(
    agents=[worker1, worker2, validator],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,  # Auto-creates manager
    manager_llm="gpt-4"
)
```

## Production Considerations

- **CrewAI Enterprise (AMP Suite)**: Production features (tracing, observability, control plane)
- **Observability**: Phoenix integration for monitoring
- **Error Handling**: Built-in retry logic and error recovery
- **Deployment**: Cloud and on-premise options
- **Training**: 100,000+ certified developers

## Learning Curve

- **Time to First Crew**: 1-2 hours (most intuitive)
- **Time to Hierarchical**: 3-4 hours
- **Production Ready**: 6-8 hours (fastest to production)
- **Steepness**: Low - role/task model is familiar

## Adoption Metrics

- **GitHub Stars**: 40.5k (highest among the three)
- **Enterprise Users**: IBM, PwC, AWS, Gelato
- **Developers Trained**: 100,000+
- **Execution Scale**: 10M+ agents in 30 days

## Verdict

CrewAI's role-based approach is **best for rapid prototyping and teams that value simplicity**. The role/task abstraction is most intuitive for developers familiar with human team dynamics. Fastest path to working system but trades some control for convenience.

**Choose CrewAI if:** You want to move fast, prefer high-level abstractions, have clear role definitions, and value developer ergonomics over fine-grained orchestration control.

## Framework Evolution

- **Independent**: Built from scratch, not based on LangChain
- **Modern**: Crews (autonomous) + Flows (event-driven control)
- **Enterprise Ready**: AMP Suite for production deployments
- **Community**: Largest developer training program (DeepLearning.AI courses)

## Best Practices

1. **Start Sequential**: Begin with simple sequential workflows
2. **Add Hierarchy Carefully**: Use hierarchical only when oversight needed
3. **Role Clarity**: Clear, distinct roles prevent agent confusion
4. **Expected Outputs**: Be specific about deliverables
5. **Logging**: Use verbose=2 for debugging, verbose=0 for production
