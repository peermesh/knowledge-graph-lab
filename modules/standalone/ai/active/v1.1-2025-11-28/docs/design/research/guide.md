# Research Guide

## Overview

This guide provides the practical, step-by-step process for conducting research. For the underlying philosophy and principles behind our approach, see the [Research Philosophy](./philosophy.md) document.

**Core Principle**: Research everything comprehensively first, then select what's within reason to build, and become expert in those chosen areas as you develop the system.

---

## The Process

### 1. Define Your Question
Write a clear research brief that explains:
- What decision you need to make
- What information would change that decision
- What constraints matter (time, money, complexity)

### 2. Generate Comprehensive Prompt
Use the [deep research prompt generator](../../research/prompts/deep-research-prompt-generator.md) to create a structured research brief that gets good results from AI tools.

### 3. Execute Across AI Tools
Run the same prompt through multiple AI systems:
- **Perplexity** - Web search with citations
- **Claude** - Deep analysis and reasoning
- **ChatGPT** - Broad knowledge synthesis  
- **Gemini** - Large context handling
- **DeepSeek** - Technical depth
- **Grok** - Real-time and social insights

**Note**: Prefer unstructured markdown outputs per the generator. If a tool returns JSON, save it as-is and convert to markdown for review when practical.

### 4. Save Everything
Create a directory for your research topic:
```
research/[topic-name]/
├── prompt.md          # Your original research brief
├── perplexity.json    # AI responses in JSON format
├── claude.json
├── chatgpt.json
├── gemini.json
├── deepseek.json
├── grok.json
└── FINAL.md           # Final combined analysis (markdown)
```

### 5. Summarize and Consolidate
Create a clear, comprehensive markdown summary of findings suitable for decision-making. Avoid over-structuring; follow the generator’s Output Specifications.

---

## When To Use This Process

**Good for:**
- Understanding complex technical landscapes
- Evaluating multiple solution approaches
- Researching competitive markets
- Learning about unfamiliar domains
- Making technology selection decisions

**Not good for:**
- Questions with obvious answers
- Simple factual lookups
- Urgent decisions requiring immediate action
- Topics requiring hands-on experimentation

---

## Quality Guidelines

### A Good Research Brief
- Explains why you need this information
- Specifies what would change your decision
- Includes relevant constraints and context
- Asks for specific, actionable outputs

### A Good Research Summary
- Answers your original question clearly
- Preserves important details from all sources
- Organizes information logically
- Identifies gaps and uncertainties
- Provides clear next steps

---

## Advanced Techniques

### Multi-Prompt Research Campaigns
For complex domains, break research into multiple focused prompts:
1. Create category directory with numbered prompts
2. Write orchestration plan coordinating research efforts
3. Execute prompts systematically
4. Consolidate findings across multiple research areas

### Time-Based Organization
For ongoing research programs:
- Organize research by when it was conducted
- Track how understanding evolves over time
- Update research documents as new information emerges

---

## Common Mistakes

**Over-researching** - Spending more time researching than the decision warrants
**Under-synthesizing** - Collecting information without drawing conclusions
**Single-source bias** - Trusting one AI tool or perspective
**Analysis paralysis** - Researching instead of deciding and acting

---

## Resources

- [Deep Research Prompt Generator](../../research/prompts/deep-research-prompt-generator.md) - Generates effective research briefs

---

Remember: Comprehensive research enables informed decisions. Gather everything, understand the full landscape, then make strategic choices about what to implement.