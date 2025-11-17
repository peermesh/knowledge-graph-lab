"""
CrewAI Example 2: Hierarchical Agent Coordination
Pattern: Manager agent coordinates specialized workers

Key Learning: CrewAI's hierarchical process adds a manager agent that
coordinates the crew. The manager delegates tasks, validates outputs,
and ensures quality. This is powerful for complex research requiring
oversight and quality control.

Setup Time: ~40 minutes (understanding hierarchical patterns)
Code Lines: 85
"""

from crewai import Agent, Task, Crew, Process

# Pattern: Define specialized worker agents
# In hierarchical mode, agents don't need to know about each other

web_researcher = Agent(
    role="Web Research Specialist",
    goal="Search web sources for current, practical information",
    backstory="""You specialize in finding blog posts, industry reports,
    and company announcements. You're skilled at evaluating source credibility.""",
    verbose=True,
    allow_delegation=False
)

academic_researcher = Agent(
    role="Academic Research Specialist",
    goal="Search academic databases for peer-reviewed research",
    backstory="""You have access to arXiv, PubMed, and Google Scholar.
    You focus on finding rigorous, peer-reviewed studies and technical papers.""",
    verbose=True,
    allow_delegation=False
)

entity_extractor = Agent(
    role="Entity Extraction Specialist",
    goal="Extract structured entities from documents",
    backstory="""You use NLP and LLM techniques to identify entities
    (vendors, techniques, metrics) from text with high accuracy.""",
    verbose=True,
    allow_delegation=False
)

quality_validator = Agent(
    role="Quality Assurance Specialist",
    goal="Validate research quality and completeness",
    backstory="""You review research outputs for completeness, accuracy,
    and proper citation. You ensure confidence scores are calibrated.""",
    verbose=True,
    allow_delegation=False
)

# Pattern: Define tasks without strict ordering
# The manager will coordinate execution

web_research_task = Task(
    description="""Search web sources for: 'LLM cost optimization strategies 2025'.
    Focus on: industry blogs, vendor announcements, case studies.
    Deliverable: 5+ web sources with URLs and publication dates""",
    agent=web_researcher,
    expected_output="List of web sources with metadata"
)

academic_research_task = Task(
    description="""Search academic sources for: 'LLM inference optimization'.
    Focus on: quantization, distillation, caching techniques.
    Deliverable: 3+ academic papers with DOI/arXiv IDs""",
    agent=academic_researcher,
    expected_output="List of academic papers with citations"
)

extraction_task = Task(
    description="""Extract entities from all research findings:
    - Vendors (companies offering solutions)
    - Techniques (optimization methods)
    - Metrics (cost savings, performance gains)
    - Case Studies (real-world implementations)
    Provide confidence score for each entity.""",
    agent=entity_extractor,
    expected_output="Structured entity list with confidence scores"
)

validation_task = Task(
    description="""Validate the complete research output:
    1. Are sources credible and properly cited?
    2. Are confidence scores reasonable?
    3. Is coverage comprehensive (web + academic)?
    4. Are any contradictions identified?
    Provide quality score (0-100) and recommendations.""",
    agent=quality_validator,
    expected_output="Quality report with score and recommendations"
)

# Pattern: Create crew with hierarchical process
# CrewAI automatically creates a manager agent
crew = Crew(
    agents=[
        web_researcher,
        academic_researcher,
        entity_extractor,
        quality_validator
    ],
    tasks=[
        web_research_task,
        academic_research_task,
        extraction_task,
        validation_task
    ],
    process=Process.hierarchical,  # Manager coordinates agents
    verbose=2,
    # Optional: customize manager behavior
    manager_llm="gpt-4"  # Use specific LLM for manager
)

# Execute with hierarchical coordination
result = crew.kickoff()

print("\n=== Hierarchical Research Complete ===")
print(result)

# Key Insights:
# ✅ Strengths:
#    - Manager provides oversight and quality control
#    - Workers focus on specialized tasks
#    - More sophisticated than sequential execution
#    - Good for complex research requiring validation
#
# ⚠️ Challenges:
#    - Manager coordination adds LLM calls (cost)
#    - Less control over manager's decision-making
#    - Debugging manager behavior can be opaque
#    - Risk of manager delegating inefficiently
#
# 💡 Best for: Complex research workflows where oversight
#    and quality validation are critical, and team is willing
#    to trade some control for automatic coordination

# Pattern Comparison:
# Sequential: researcher -> analyst -> synthesizer (fixed order)
# Hierarchical: manager coordinates 4 specialists (dynamic order)
#
# Choose sequential for: Known workflow, simple coordination
# Choose hierarchical for: Complex research, quality validation, dynamic coordination
