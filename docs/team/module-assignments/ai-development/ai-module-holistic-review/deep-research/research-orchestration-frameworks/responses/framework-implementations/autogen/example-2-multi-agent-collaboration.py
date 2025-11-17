"""
AutoGen Example 2: Multi-Agent Collaboration with GroupChat
Pattern: Multiple specialized agents coordinating on complex research

Key Learning: GroupChat pattern enables multiple agents to participate in
research. The GroupChatManager acts as a traffic controller, deciding which
agent speaks next. This is powerful for complex research requiring different
expertise (web search, academic papers, synthesis).

Setup Time: ~45 minutes (understanding group chat patterns)
Code Lines: 120
"""

from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

config_list = [{"model": "gpt-4", "api_key": "YOUR_API_KEY"}]

llm_config = {"config_list": config_list, "temperature": 0.7}

# Pattern: Create specialized agents for different research tasks
# Each agent has distinct expertise and responsibilities

web_researcher = AssistantAgent(
    name="WebResearcher",
    system_message="""You search the web for current information.
    Focus on recent articles, blog posts, and industry reports.
    Always provide URLs and publication dates.""",
    llm_config=llm_config,
)

academic_researcher = AssistantAgent(
    name="AcademicResearcher",
    system_message="""You search academic databases (arXiv, PubMed, Google Scholar).
    Focus on peer-reviewed papers and technical reports.
    Provide DOIs or arXiv IDs for all sources.""",
    llm_config=llm_config,
)

synthesizer = AssistantAgent(
    name="Synthesizer",
    system_message="""You synthesize findings from other researchers.
    Combine web and academic sources into coherent summary.
    Identify contradictions and rate confidence.
    When synthesis is complete, reply with TERMINATE.""",
    llm_config=llm_config,
)

coordinator = UserProxyAgent(
    name="Coordinator",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
    llm_config=llm_config,
)

# Pattern: GroupChat manages multi-agent conversation
# The manager decides speaker order based on context
agents = [coordinator, web_researcher, academic_researcher, synthesizer]

# speaker_selection_method can be "auto", "manual", or "round_robin"
# "auto" uses LLM to decide who speaks next - smart but token-heavy
groupchat = GroupChat(
    agents=agents,
    messages=[],
    max_round=12,  # Prevent infinite loops
    speaker_selection_method="auto",  # LLM-driven speaker selection
)

# Pattern: GroupChatManager orchestrates the conversation
# This is the "intelligence layer" for research orchestration
manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

# Pattern: Start research workflow
research_task = """
Research Gap: We lack current information on quantization techniques for LLM inference.
Needed: Latest methods, performance impacts, and production case studies.

Tasks:
1. WebResearcher: Find recent blog posts and industry implementations
2. AcademicResearcher: Find recent papers on quantization methods
3. Synthesizer: Combine findings and identify consensus vs. contradictions
"""

coordinator.initiate_chat(
    manager,
    message=research_task,
)

# Key Insights:
# ✅ Strengths:
#    - Natural division of labor among specialized agents
#    - Speaker selection can be smart (LLM-driven) or deterministic
#    - Conversation history shows complete reasoning chain
#    - Easy to add/remove agents without changing core logic
#
# ⚠️ Challenges:
#    - Auto speaker selection adds significant token overhead
#    - Debugging speaker transitions can be opaque
#    - Risk of agents talking past each other without progress
#    - Need careful termination conditions to prevent loops
#
# 💡 Best for: Complex research requiring diverse expertise where
#    the conversation flow isn't predetermined
