# AutoGen Framework Examples

## Overview

AutoGen (now transitioning to Microsoft Agent Framework) uses **conversational patterns** for multi-agent orchestration. Agents communicate via message passing, making workflows feel like team discussions.

## Core Philosophy

- **Conversation-Driven**: Agents talk to each other via messages
- **Event-Driven**: Built on asynchronous message passing (v0.4)
- **Flexible**: Supports simple 2-agent chats and complex group conversations
- **Observable**: Full conversation history provides audit trail

## Examples Included

### Example 1: Simple Coordination (`example-1-simple-coordination.py`)
**Pattern**: Two-agent conversation
**Use Case**: Single research gap → researcher agent → coordinator agent
**Key Learning**: Conversation flow is natural and debuggable
**Setup Time**: ~30 minutes
**Code Complexity**: 45 lines

### Example 2: Multi-Agent Collaboration (`example-2-multi-agent-collaboration.py`)
**Pattern**: GroupChat with specialized agents
**Use Case**: Complex research requiring web + academic + synthesis
**Key Learning**: Speaker selection can be LLM-driven or deterministic
**Setup Time**: ~45 minutes
**Code Complexity**: 120 lines

## When to Use AutoGen

✅ **Good Fit:**
- Research workflows with complex, multi-turn discussions
- Need full conversation history for auditability
- Team members comfortable with conversational AI patterns
- Experimental projects where flexibility matters

⚠️ **Challenges:**
- Verbose conversations can lead to high token usage
- Auto speaker selection adds overhead
- Need careful termination conditions
- GroupChat debugging can be opaque

## Key Patterns

### 1. Agent Definition
```python
agent = AssistantAgent(
    name="AgentName",
    system_message="Role description...",
    llm_config=llm_config,
)
```

### 2. Two-Agent Chat
```python
coordinator.initiate_chat(
    researcher,
    message="Research task..."
)
```

### 3. Multi-Agent GroupChat
```python
groupchat = GroupChat(
    agents=[agent1, agent2, agent3],
    speaker_selection_method="auto"
)
manager = GroupChatManager(groupchat=groupchat)
```

## Production Considerations

- **v0.2**: Mature but being phased out
- **v0.4**: Ground-up redesign, event-driven, distributed
- **Microsoft Agent Framework**: Enterprise successor with Azure integration
- **Observability**: Built-in AgentOps integration, OpenTelemetry support
- **Error Handling**: Retry logic, exception handling in conversational loops

## Learning Curve

- **Time to First Agent**: 1-2 hours
- **Time to GroupChat**: 3-4 hours
- **Production Ready**: 8-12 hours (understanding patterns, error handling, observability)
- **Steepness**: Moderate - conversational patterns are intuitive, but GroupChat speaker selection requires understanding

## Verdict

AutoGen's conversational approach is **natural for research workflows** where agents need to discuss, debate, and synthesize. The message-passing model provides excellent observability but can be token-heavy. Best for teams comfortable with AI conversations and willing to invest in understanding the framework's evolution (v0.2 → v0.4 → Microsoft Agent Framework).
