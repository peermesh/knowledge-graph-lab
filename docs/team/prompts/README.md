# 🤖 AI Agent Prompts Directory

This directory contains comprehensive prompt templates and agent instructions that power complex AI agent orchestration systems. Each prompt is carefully designed for specific workflows, ensuring consistent behavior across different agent interactions.

## 📁 Directory Structure

### `agents/` - Specialized Agent Directory
**Comprehensive collection of specialized AI agents for domain-specific tasks**

This directory contains 25+ specialized agents organized by expertise area, from development and research to business operations and creative work. Each agent is designed for specific workflows and can be invoked through various AI platforms.

**📖 [See detailed agents README](agents/README.md)** for complete descriptions of all agents, usage guidelines, and integration instructions across different platforms (Cursor, Claude Code, Gemini, etc.)

**Key Agent Categories:**
- **Core Development**: Project orchestration, QA, implementation
- **Research & Analysis**: Technical research, gap analysis, strategic intelligence
- **Business Operations**: Executive coordination, financial planning, marketing
- **Creative & Design**: UX design, content creation, innovation
- **Technical Infrastructure**: Data analysis, security, tooling, networking

### `creation/` - Artifact Creation Templates
Prompts for generating structured documents and artifacts:

- **`CREATE-AUDITABLE-RECORD.md`** - Generates comprehensive audit trails and compliance documentation with full traceability
- **`CREATE-FEATURE-REQUEST.md`** - Captures detailed feature requirements and specifications for development
- **`CREATE-WORK-PROPOSAL.md`** - Creates detailed work proposals with scope, timeline, and resource requirements

### `general/` - Core Workflow Prompts
Essential prompts for common agent operational workflows:

- **`autonomous-mode-now.md`** - Autonomous engineering mode for independent task completion with documentation-first approach
- **`verify-previous-work.md`** - Skeptical verification of work claims with concrete evidence requirements
- **`prepare-work-for-review.md`** - Packages completed work for peer review with full context and documentation
- **`review-my-plan.md`** - Prepares implementation plans for review before execution begins
- **`do-you-know-what-to-do-next.md`** - Autonomous task progression and state assessment for ongoing work

### `handoffs/` - Work Transfer Protocols
Standardized handoff templates for seamless agent-to-agent work transfers:

- **`HANDOFF.md`** - Standard handoff protocol for routine work transfers
- **`HANDOFF-MINIMAL.md`** - Lightweight handoff for simple, quick transfers
- **`HANDOFF-DETAILED.md`** - Comprehensive handoff with full context, risks, and next steps

### `modes/` - Behavioral Mode Definitions
Special operational modes that change agent behavior:

- **`DISCUSSION-MODE.md`** - Read-only analysis mode for planning, discussion, and theoretical exploration without code changes

### `research/` - Research & Investigation
Specialized prompts for research workflows:

- **`deep-research-prompt-generator.md`** - Transforms research briefs into comprehensive, multi-model research prompts with complexity assessment and execution guidance

### `work-orders/` - Work Order Lifecycle
Complete work order management system:

- **`CREATE-WORK-ORDER.md`** - Generates self-contained, executable work orders with complete context
- **`EXECUTE-WORK-ORDER.md`** - Executes work orders with progress tracking and validation
- **`WORK-ORDER-INDEX.md`** - Maintains work order registries and tracking

## 🚀 Usage Context

These prompts power complex AI agent orchestration systems and are referenced by:

- **AGENTS.md** - Central system configuration and agent definitions
- **Project tracking** - Work order and session management
- **Mode orchestration** - Dynamic behavior switching
- **Work order execution** - Structured task completion pipelines

### When to Use Each Category:

| Category | Use Case |
|----------|----------|
| **agents/** | Define specialized agent roles for specific domains |
| **creation/** | Generate structured documents and proposals |
| **general/** | Handle common development and review workflows |
| **handoffs/** | Transfer work between agents or sessions |
| **modes/** | Change agent behavior for specific contexts |
| **research/** | Conduct deep research and investigation |
| **work-orders/** | Manage structured, trackable work execution |

## 📝 Adding New Prompts

### Process:
1. **Choose Category** - Select the most appropriate subdirectory based on the prompt's primary function
2. **Naming Convention** - Use clear, descriptive names: `ACTION-OBJECT.md` or `ROLE-NAME.md`
3. **Documentation** - Add the new prompt to this README with a clear description
4. **Integration** - Update AGENTS.md if the prompt needs system-wide references

### Quality Guidelines:
- **Purpose-driven** - Each prompt should serve a specific, well-defined function
- **Self-contained** - Include all necessary context and instructions
- **Consistent** - Follow established patterns and formatting
- **Testable** - Should produce predictable, reliable results

## 🔗 Integration Points

These prompts integrate with the broader AI agent infrastructure:

- **AGENTS.md** - Central configuration and mode definitions
- **Project tracking** - Work order and session management
- **Mode orchestration** - Dynamic behavior switching
- **Audit trails** - Comprehensive work documentation

## 🔬 Research System Usage

### 🚨 **MUST USE BRIEF TAGS**
Your research brief **MUST** be wrapped in `<BRIEF></BRIEF>` tags or the generator may try to do the research instead of generate deep research prompts:
```
<BRIEF>
Your research question or requirements here
</BRIEF>
```

### How to Use the Research System

#### Step 1: Generate Research Prompts
1. Start with your research brief or question
2. **CRITICAL**: Wrap your brief in `<BRIEF></BRIEF>` tags (see warning above)
3. Use `research/deep-research-prompt-generator.md` to transform it into comprehensive research prompts
4. The generator will guide you through complexity assessment
5. Generate either single or multiple prompts based on your needs
6. If multiple prompts are recommended, the agent will present this one-liner: "Complexity: N=[N], D=[D] → L=[L]; threshold Y=[Y] → recommended P=ceil(L/Y)=[P]. Choose one: SINGLE, MULTI (P=[P]), or CUSTOM [number]."

#### Step 2: Execute Research

**TWO EXECUTION MODES:**

**Mode A: Automated (For Claude Code Agents)**
1. **Create directory structure** with `claude-cli.md` placeholder
2. **Read all research-prompt.md** files (batch reads)
3. **Launch Task agents IN PARALLEL** (up to 10 at once):
   - Use `subagent_type`: `"deep-research-analyst"`
   - Add `ultrathink` at end of each prompt for maximum reasoning
   - Launch ALL agents in ONE message for parallel execution
4. **Save results** to `claude-cli.md` in each research directory
5. **Create synthesis** and assessment documents

**Mode B: Manual (For Users)**
1. Run your generated prompts across multiple AI models (based on testing):
   - **Perplexity** (3-7x more comprehensive)
   - Claude (structured analysis but less comprehensive)
   - ChatGPT (good but limited on free accounts)
   - Gemini, Grok, DeepSeek (good for validation)
2. Save each output with clear labeling

### Research Output Organization

Organize your research outputs systematically:

```
research/[topic]/
├── research-prompt.md      # Generated research prompt
├── claude-cli.md          # Claude Code agent's automated response
├── claude.md              # Manual Claude submission (optional)
├── chatGPT.md             # ChatGPT's response
├── perplexity.md          # Perplexity's response
├── gemini.md              # Gemini's response (optional)
├── grok.md                # Grok's response (optional)
├── deepseek.md            # DeepSeek's response (optional)
├── research-summary.md     # Synthesis across all responses
└── research-assessment.md  # Confidence levels and contradictions
```

**Note**: `claude-cli.md` is for automated agent execution, while `claude.md` is for manual submission.

### Research Best Practices

- **ALWAYS wrap briefs in `<BRIEF></BRIEF>` tags** - This is mandatory for the generator to work
- **Use Perplexity as primary model** - Testing showed 3-7x more comprehensive outputs
- **Always use multiple AI models** - Each has unique strengths and knowledge
- **Save everything** - Keep all intermediate outputs for reference
- **Follow the process** - Start with the generator, then run across models
- **Label clearly** - Good organization makes review much easier
- **Review and refine** - The final output should be actionable

This is the original, battle-tested research system that has been refined through extensive use. It's designed to produce high-quality, comprehensive research that can inform real decisions.
