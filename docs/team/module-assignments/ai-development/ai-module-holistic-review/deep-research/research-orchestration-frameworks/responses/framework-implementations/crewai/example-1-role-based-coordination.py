"""
CrewAI Example 1: Role-Based Agent Coordination
Pattern: Agents with defined roles and sequential task execution

Key Learning: CrewAI uses role/task abstraction that feels intuitive.
You think in terms of team members (roles) and their assignments (tasks).
The framework handles coordination automatically. This is the easiest
to understand for teams familiar with human work delegation.

Setup Time: ~25 minutes (quickest to get started)
Code Lines: 40
"""

from crewai import Agent, Task, Crew

# Pattern: Define agents with roles
# Each agent has role, goal, and backstory - very human-like

researcher = Agent(
    role="Research Specialist",
    goal="Find comprehensive information about research gaps",
    backstory="""You are an expert researcher with 10 years of experience
    in information gathering. You excel at finding both web and academic sources,
    always cite properly, and provide confidence ratings.""",
    verbose=True,
    allow_delegation=False  # This agent works independently
)

analyst = Agent(
    role="Data Analyst",
    goal="Extract structured information from research findings",
    backstory="""You are a data analyst who specializes in entity extraction
    and relationship mapping. You create structured knowledge from unstructured text.""",
    verbose=True,
    allow_delegation=False
)

synthesizer = Agent(
    role="Knowledge Synthesizer",
    goal="Combine findings into comprehensive answers",
    backstory="""You are a synthesis expert who combines information from
    multiple sources, identifies contradictions, and creates coherent summaries
    with confidence scores.""",
    verbose=True,
    allow_delegation=False
)

# Pattern: Define tasks
# Tasks are assigned to specific agents and executed sequentially

research_task = Task(
    description="""Research the following gap: 'LLM cost optimization strategies for 2025'.
    Find at least 3 credible sources from both web and academic databases.
    Include URLs and publication dates.""",
    agent=researcher,
    expected_output="List of sources with URLs, titles, and relevance scores"
)

extraction_task = Task(
    description="""Extract structured entities from the research findings.
    Identify: vendors, techniques, price points, and performance metrics.
    Provide confidence scores for each entity.""",
    agent=analyst,
    expected_output="JSON list of entities with types and confidence scores"
)

synthesis_task = Task(
    description="""Synthesize the research and extracted entities into a
    comprehensive answer. Include:
    1. Top 3 strategies with evidence
    2. Confidence level for each
    3. Any contradictions found
    4. Overall recommendation""",
    agent=synthesizer,
    expected_output="Comprehensive answer with confidence assessment"
)

# Pattern: Create crew and execute
# The Crew handles coordination automatically
crew = Crew(
    agents=[researcher, analyst, synthesizer],
    tasks=[research_task, extraction_task, synthesis_task],
    verbose=2  # Show execution details
)

# Execute the research workflow
result = crew.kickoff()

print("\n=== Research Complete ===")
print(result)

# Key Insights:
# ✅ Strengths:
#    - Most intuitive abstraction (roles + tasks)
#    - Fastest to get started
#    - Natural for teams familiar with work delegation
#    - Automatic coordination - just define agents and tasks
#
# ⚠️ Challenges:
#    - Sequential execution is default (can be limiting)
#    - Less control over coordination logic
#    - Logging can be verbose and hard to parse
#    - print/log statements inside tasks don't work well
#
# 💡 Best for: Research teams that want to move fast
#    and prefer intuitive role-based thinking over explicit orchestration
