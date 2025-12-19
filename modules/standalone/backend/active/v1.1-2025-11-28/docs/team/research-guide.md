# Research Methodology Guide

**Purpose**: Systematic approach to evaluate technologies for your module

---

## Quick Process

### 1. Define Requirements (30 min)
- What must this technology do?
- What constraints exist? (Docker, resources, timeline)
- How does it integrate with other modules?

### 2. Identify Options (1 hour)
- Use AI assistants to find 3-5 alternatives
- Look at what similar projects use

### 3. Evaluate & Compare (2 hours)
Create comparison matrix:
| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Learning Curve | Low | Medium | High |
| Availability | Open Source | Cloud Service | Open Source |
| Docker Support | Yes | Yes | No |
| Documentation | Excellent | Good | Poor |
| Community | Large | Medium | Small |

### 4. Test Feasibility (1 hour)
- Quick proof of concept
- Check Docker compatibility
- Verify integration approach

### 5. Document Decision (1 hour)
- Write 2-page research brief
- Include rationale
- Note risks and mitigation

---

## Research Tools

### AI Assistants
Use multiple for different perspectives:
- **Claude**: Deep technical analysis
- **ChatGPT**: Broad alternatives
- **Perplexity**: Current information with sources
- **Gemini**: Large-scale comparison

### Example Prompts

```
"I need to choose a [technology type] for [use case] that:
- Runs in Docker
- Integrates with [other module]
- Has good learning resources
- Available as open source or with free tier
Compare top 5 options with pros/cons"
```

```
"What database would you recommend for:
- Storing knowledge graph relationships
- 100K+ entities
- Fast traversal queries
- Docker deployment
- PostgreSQL vs Neo4j vs other?"
```

---

## Evaluation Framework

### Technical Criteria (40%)
- Meets functional requirements
- Performance characteristics
- Scalability potential
- Security features

### Practical Criteria (30%)
- Learning curve
- Documentation quality
- Community support
- Debugging tools

### Integration Criteria (20%)
- Works with other modules
- Standard protocols (REST, GraphQL)
- Data format compatibility
- Docker deployment

### Future Criteria (10%)
- Maintenance outlook
- Community trajectory
- Company stability
- Migration paths

---

## Common Research Patterns

### For Backend Modules
1. Framework → Database → Cache → Queue
2. Consider: FastAPI + PostgreSQL + Redis
3. Alternative: Express + MongoDB + Redis
4. Research: Performance, ecosystem, learning curve

### For Frontend Modules  
1. Framework → UI Library → State Management → Build Tools
2. Consider: Next.js + Tailwind + Zustand
3. Alternative: Vite + Material UI + Redux
4. Research: Bundle size, performance, DX

### For AI Modules
1. LLM Provider → Vector DB → Orchestration
2. Consider: OpenAI + Pinecone + LangChain
3. Alternative: Anthropic + Qdrant + Custom
4. Research: Performance, accuracy, latency

### For Publishing Modules
1. Email Service → Distribution → Analytics
2. Consider: SendGrid + Custom + Segment
3. Alternative: Resend + Zapier + PostHog
4. Research: Deliverability, capabilities, features

---

## Research Brief Template

```markdown
# [Module Name] Technology Selection

## Executive Summary
[1-2 sentences on chosen approach]

## Requirements
- Functional: [What it must do]
- Technical: [Constraints and needs]
- Integration: [How it connects]

## Options Evaluated
### Option A: [Name]
- Pros: [List]
- Cons: [List]
- Requirements: [Resource needs]

### Option B: [Name]
[Same structure]

## Recommendation: [Chosen Option]
### Rationale
[Why this option wins]

### Implementation Plan
- Phase 1: [Setup and basics]
- Phase 2: [Core features]
- Phase 3: [Integration]

### Risks & Mitigation
- Risk: [Description]
  Mitigation: [Approach]

## Open Questions
- [Questions for team discussion]
```

---

## Tips for Good Research

### Do's
✅ Time-box your research (5 hours max)  
✅ Build small proof of concepts  
✅ Check Docker compatibility early  
✅ Consider team expertise  
✅ Think about debugging/monitoring

### Don'ts
❌ Analysis paralysis  
❌ Choose only based on popularity  
❌ Ignore integration requirements  
❌ Forget about local development  
❌ Over-engineer for Phase 1

---

## Advanced Research Tools

For AI-powered research assistance, see:
- [Deep Research Prompt Generator](../research/prompts/deep-research-prompt-generator.md) - Generate comprehensive research prompts

## Need Help?

- **Stuck on requirements?** Ask in #kgl-[module]
- **Can't find options?** Try different AI assistants
- **Integration questions?** Post in #kgl-integration
- **Decision paralysis?** Office hours are perfect for this