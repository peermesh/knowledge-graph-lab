# RequirementsKit - Requirements Development Templates

**Purpose**: Systematic templates for developing comprehensive requirements documentation that feeds into SpecKit's `/specify` command.

---

## Getting Started

**🚀 New user?** Start here: **[guides/quickstart.md](guides/quickstart.md)**

**📝 Creating a spec?** Use: **[templates/simple-template.md](templates/simple-template.md)**

**⚡ Need quick help?** See: **[guides/quick-reference-card.md](guides/quick-reference-card.md)**

---

## What You Get

### Templates (2 files)

**[simple-template.md](templates/simple-template.md)** - Start here
- Fill out this template with your requirements
- 300-500 lines when complete
- Beginner-friendly with guided questions

**[comprehensive-template.md](templates/comprehensive-template.md)** - AI expands to this
- Detailed format for AI processing
- 600-800 lines when expanded
- Ready for SpecKit `/specify` command

### Guides (4 files)

**[quickstart.md](guides/quickstart.md)** - Navigation and getting started
- Entry point for new users
- 5-minute overview
- Directory structure and file navigation

**[methodology.md](guides/methodology.md)** - How to create Comprehensive Source input
- Detailed HOW-TO guide with examples
- Day-by-day execution approach
- Common pitfalls and solutions

**[workflow.md](guides/workflow.md)** - Official process definition
- Work orders WO-1 through WO-5
- Formal workflow with dependencies
- Phase-by-phase breakdown with time estimates

**[quick-reference-card.md](guides/quick-reference-card.md)** - One-page cheat sheet
- Quick command reference for experienced users
- Template sections explained
- Common patterns and tips

### Reference (2 files)

**[prd-generation-rules.md](reference/prd-generation-rules.md)** - For AI expansion
- How AI transforms simple → comprehensive
- Quality rules and standards
- Technical guidance

**[terminology.md](reference/terminology.md)** - Project terms
- Standard terminology
- Naming conventions
- Project-specific definitions

---

## How It Works

```
RequirementsKit → SpecKit Pipeline:

1. Fill out simple-template.md          (you do requirements gathering)
2. AI expands to comprehensive format   (AI reads prd-generation-rules.md)
3. Run SpecKit /specify command         (SpecKit creates final specification)
4. Get implementation-ready PRD         (ready to build)

Without RequirementsKit: SpecKit produces generic 126-line specs
With RequirementsKit: SpecKit produces 500+ line implementation-ready specs
```

---

## Quick Start

1. **Read** [guides/quickstart.md](guides/quickstart.md) (5 minutes)
2. **Copy** [templates/simple-template.md](templates/simple-template.md) to your project
3. **Fill it out** with your requirements
4. **Get help** from [guides/quick-reference-card.md](guides/quick-reference-card.md) if needed

---

## Quality Assurance

### Reviewing Documentation Quality

To validate and improve RequirementsKit documentation quality:

**Quality Review Prompt**: [`.dev/ai/prompts/requirements-kit-quality-review-prompt.md`](../../.dev/ai/prompts/requirements-kit-quality-review-prompt.md)

**How to use**:
1. Provide this prompt to AI models (Claude, GPT-4, Gemini, etc.)
2. Reviews are saved to `.dev/ai/audits/[timestamp]-[model]-speckit-quality-review.md`
3. Run reviews before major releases, after significant changes, or quarterly

**Multi-model strategy**: Running the prompt with different AI models provides:
- **Cross-validation**: Different perspectives catch different issues
- **Bias detection**: Where models disagree often reveals assumptions
- **Comprehensive coverage**: Each model has strengths (precision, vision, balance)
- **High confidence**: Consensus across models = reliable findings

**Recent reviews** (2025-10-09):
- `2025-10-09-04-00-gemini-speckit-quality-review.md` - Strategic consolidation perspective
- `2025-10-09-07-28-sonnet-4-5-speckit-quality-review.md` - Comprehensive systematic analysis
- `2025-10-09-07-30-codex-cli-speckit-quality-review.md` - Forensic precision with line numbers

**Results from multi-model review**:
- Identified terminology conflicts (now resolved)
- Found broken links (now fixed)
- Recommended redundancy reduction (in progress)
- Established quality improvement roadmap

**When to run quality reviews**:
- Before releasing new RequirementsKit versions
- After major documentation restructuring
- Quarterly documentation health checks
- When user feedback suggests documentation issues
- When onboarding new documentation maintainers

**Quality metrics** (after Phase 1 improvements):
- Broken links: 0 (from 3+)
- Terminology consistency: 100% (canonical established)
- Guide accuracy: 100% (counts and listings correct)
- Documentation coverage: Complete

---

## Need More Help?

- **System development files**: See `.dev/requirements-kit/` for examples, checklists, and workflows
- **Case studies**: See `.dev/requirements-kit/case-studies/` for complete examples
- **Extraction guide**: See `.dev/requirements-kit/package-extraction.md` to use this in other projects

---

**Version**: 1.0 (2025-10-09)
**Status**: Production ready
