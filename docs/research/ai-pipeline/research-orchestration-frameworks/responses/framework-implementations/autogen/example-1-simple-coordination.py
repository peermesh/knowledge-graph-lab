"""
AutoGen Example 1: Simple Agent Coordination
Pattern: Two-agent conversation for research task execution

Key Learning: AutoGen uses conversational patterns where agents communicate
via messages. This feels natural for research workflows where agents need
to "discuss" findings. The message-passing paradigm makes debugging easy
since you can inspect the conversation history.

Setup Time: ~30 minutes (including library installation and config)
Code Lines: 45
"""

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Pattern: Load LLM configuration
# AutoGen uses a config list pattern for multi-model support
config_list = config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={"model": ["gpt-4", "gpt-3.5-turbo"]}
)

llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
    "timeout": 120,
}

# Pattern: Define specialized research agent
# Role definition through system message creates agent "personality"
researcher = AssistantAgent(
    name="Researcher",
    system_message="""You are a research agent specialized in gathering information.
    When given a research gap, you formulate search queries and analyze findings.
    Always cite sources and provide confidence scores for your findings.""",
    llm_config=llm_config,
)

# Pattern: User proxy agent executes tools and manages conversation
# The UserProxyAgent can execute code and manage the research workflow
coordinator = UserProxyAgent(
    name="Coordinator",
    human_input_mode="NEVER",  # Fully autonomous
    max_consecutive_auto_reply=5,
    code_execution_config={"work_dir": "research_output", "use_docker": False},
    llm_config=llm_config,
)

# Pattern: Initiate research conversation
# This is where the magic happens - agents talk until task is complete
research_gap = """
Research Gap: Missing information about LLM cost optimization strategies from 2025.
Task: Find and summarize the top 3 strategies with confidence scores.
"""

# The conversation continues until researcher provides "TERMINATE"
coordinator.initiate_chat(
    researcher,
    message=research_gap,
)

# Key Insight: AutoGen's strength is conversational flow
# - Natural for complex, multi-turn research discussions
# - Message history provides full audit trail
# - Easy to understand what agents are "thinking"
# - Challenge: Can be verbose, leading to high token usage
