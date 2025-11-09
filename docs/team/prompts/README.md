# Team Prompt Library

This directory contains the centralized prompt library for the Knowledge Graph Lab team, including research prompt generators and module-specific research prompts.

### 🚨 **MUST USE BRIEF TAGS**
Your research brief **MUST** be wrapped in `<BRIEF></BRIEF>` tags or the generator may try to do the research instead of generate deep research prompts:
```
<BRIEF>
Your research question or requirements here
</BRIEF>
```

## The Research System

### 1. Deep Research Prompt Generator (`deep-research-prompt-generator.md`)
Transforms research briefs into comprehensive prompts.

- Intelligently handles both simple and complex multi-topic briefs
- Can generate single comprehensive prompts or multiple focused prompts
- Includes complexity assessment and user interaction
- Designed to produce high-quality, actionable research

## How to Use This System

### Step 1: Generate Research Prompts
1. Start with your research brief or question
2. **CRITICAL**: Wrap your brief in `<BRIEF></BRIEF>` tags (see warning above)
3. Use `deep-research-prompt-generator.md` to transform it into comprehensive research prompts
4. The generator will guide you through complexity assessment
5. Generate either single or multiple prompts based on your needs
6. If multiple prompts are recommended, the agent will present this one-liner: "Complexity: N=[N], D=[D] → L=[L]; threshold Y=[Y] → recommended P=ceil(L/Y)=[P]. Choose one: SINGLE, MULTI (P=[P]), or CUSTOM [number]."


### Step 2: Execute Research

**TWO EXECUTION MODES:**

#### Mode A: Automated (For Claude Code Agents)
If you are a Claude Code agent:

1. **Create directory structure** with `claude-cli.md` placeholder
2. **Read all research-prompt.md** files (batch reads)
3. **Launch Task agents IN PARALLEL** (up to 10 at once):
   - Use `subagent_type`: `"deep-research-analyst"`
   - Add `ultrathink` at end of each prompt for maximum reasoning
   - Launch ALL agents in ONE message for parallel execution
4. **Save results** to `claude-cli.md` in each research directory
5. **Create synthesis** and assessment documents

See `AGENT-EXECUTION-GUIDE.md` (if available in your project) for complete agent instructions.

#### Mode B: Manual (For Users)
1. Run your generated prompts across multiple AI models (based on testing):
   - **Perplexity** (3-7x more comprehensive)
   - Claude (structured analysis but less comprehensive)
   - ChatGPT (good but limited on free accounts)
   - Gemini, Grok, DeepSeek (good for validation)
2. Save each output with clear labeling


## File Organization

### Available Prompts

This directory contains the following prompt files:

- `deep-research-prompt-generator.md` - Main research prompt generator
- `README.md` - This documentation file
- Module-specific research prompts (various publishing and analytics research prompts)

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

## Why This System Works

1. **Comprehensive Coverage**: The generator ensures all angles are explored
2. **Multiple Perspectives**: Different AI models bring different strengths
3. **Quality Output**: Produces research suitable for decision-making
4. **Scalable**: Works for both simple and complex research needs

## Best Practices

- **ALWAYS wrap briefs in `<BRIEF></BRIEF>` tags** - This is mandatory for the generator to work
- **Use Perplexity as primary model** - Testing showed 3-7x more comprehensive outputs
- **Always use multiple AI models** - Each has unique strengths and knowledge
- **Save everything** - Keep all intermediate outputs for reference
- **Follow the process** - Start with the generator, then run across models
- **Label clearly** - Good organization makes review much easier
- **Review and refine** - The final output should be actionable


This is the original, battle-tested research system that has been refined through extensive use. It's designed to produce high-quality, comprehensive research that can inform real decisions.
