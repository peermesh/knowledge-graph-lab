# Official Terminology (Final)

**Date**: 2025-10-08
**Status**: Official - use this consistently

---

## The Three Documents - Official Terminology

**CANONICAL TERMS** (Use these in all documentation):

| # | Primary Term | What It Is | Who Creates | File Name |
|---|--------------|------------|-------------|-----------|
| 1 | **Comprehensive Source** | Detailed input document we create | You/Team | `05-COMPREHENSIVE-SPEC.md` |
| 2 | **SpecKit Specification** | What SpecKit `/specify` produces | SpecKit | `08-{module}-speckit-output.md` |
| 3 | **Implementation Specification** | Final deliverable after refinement | You/Team | `10-FINAL-SPEC.md` |

**ALTERNATE TERMS** (Industry standard equivalents):

| Primary Term | Also Known As | When to Use Alternate |
|--------------|---------------|----------------------|
| Comprehensive Source | PRD (Product Requirements Document) | When communicating with external teams or stakeholders |
| SpecKit Specification | Feature Specification | SpecKit's own documentation uses this term |
| Implementation Specification | Refined Feature Specification | When emphasizing the refinement step |

**WHY TWO SETS OF TERMS?**

- **Primary terms** (Comprehensive Source, etc.) clearly describe what each document is and its purpose in the workflow
- **Alternate terms** (PRD, etc.) are industry standard and familiar to external stakeholders
- **Both are correct** - use context to choose which to use

**WHICH TO USE?**

- **In SpecKit documentation**: Use primary terms for consistency
- **In external communication**: Use alternate terms (PRD, etc.) for familiarity
- **When first introducing**: Use both ("Comprehensive Source PRD") to bridge concepts
- **In file names**: Follow the file naming conventions in the table above

---

## The Two Steps

| # | Step Name | Input | Output | Who Does It |
|---|-----------|-------|--------|-------------|
| 1 | **SpecKit Transformation** | Comprehensive Source | SpecKit Specification | SpecKit `/specify` command |
| 2 | **Manual Refinement** | SpecKit Specification | Implementation Specification | You/Team (manual review) |

**Note**: You may also see these steps described using alternate terms (PRD → Feature Specification → Refined Feature Specification). Both naming conventions refer to the same workflow.

---

## Subsequent SpecKit Commands

| Command | Input | Output | File Name |
|---------|-------|--------|-----------|
| `/plan` | Refined Feature Specification | Implementation Plan | `plan.md` |
| `/tasks` | Implementation Plan | Task List | `tasks.md` |
| `/implement` | Task List | Working Code | (source files) |

---

## Complete Workflow

**Using primary terminology**:
```
Comprehensive Source (your detailed input)
  ↓
  /specify (SpecKit Transformation)
  ↓
SpecKit Specification (SpecKit output)
  ↓
  Manual Refinement
  ↓
Implementation Specification (final deliverable)
  ↓
  /plan
  ↓
Implementation Plan
  ↓
  /tasks
  ↓
Task List
  ↓
  /implement
  ↓
Working System
```

**Alternate terminology** (industry standard):
```
PRD → /specify → Feature Specification → Manual Refinement →
Refined Feature Specification → /plan → /tasks → /implement → Working System
```

**First introduction pattern**: When introducing the Comprehensive Source concept for the first time, use "Comprehensive Source PRD" to bridge both terminologies, then use "Comprehensive Source" in subsequent mentions.

---

## File Naming Convention

**Official file naming** (follows workflow.md conventions):
```
work/{module-name}/
├── 05-COMPREHENSIVE-SPEC.md                    ← Comprehensive Source (what we create)
├── 08-{module}-speckit-output.md              ← SpecKit Specification (SpecKit output)
├── 10-FINAL-SPEC.md                           ← Implementation Specification (final deliverable)
└── (later: plan.md, tasks.md in SpecKit's structure)
```

**Alternate naming you may see**:
```
work/{module-name}/
├── 03-{module}-prd.md                    ← Alternate: PRD
├── 06-{module}-feature-spec.md           ← Alternate: Feature Specification
├── 08-{module}-refined-feature-spec.md   ← Alternate: Refined Feature Specification
```

**Note**: Both conventions are acceptable if used consistently within a project. This documentation uses the official naming shown first.

---

## Quick Reference

| What We Say | Primary Term | Alternate Term |
|-------------|--------------|----------------|
| "The input doc" | **Comprehensive Source** | PRD |
| "What SpecKit spits out" | **SpecKit Specification** | Feature Specification |
| "After we clean it up" | **Implementation Specification** | Refined Feature Specification |
| "SpecKit processing" | **SpecKit Transformation** | (same) |
| "Our manual edits" | **Manual Refinement** | (same) |

---

## Why These Terms

**Primary terminology** (Comprehensive Source / SpecKit Specification / Implementation Specification):
- **Descriptive**: Names clearly describe what each document is and its purpose
- **Workflow-aligned**: Reflects the actual workflow (comprehensive input → process → implement)
- **Used in guides**: Consistent with methodology.md and workflow.md
- **Emphasizes completeness**: "Comprehensive" highlights the detailed nature of the input

**Alternate terminology** (PRD / Feature Specification / Refined Feature Specification):
- **Industry standard**: PRD is universally recognized in product development
- **SpecKit native**: SpecKit's own documentation uses "Feature Specification"
- **External communication**: Familiar to stakeholders outside this project
- **Team history**: Your team may already use "PRD" from prior work

**Recommendation**:
- Use **primary terms** in SpecKit documentation for clarity and consistency
- Use **alternate terms** when communicating with external teams or stakeholders
- When **first introducing** the concept, use both: "Comprehensive Source PRD"

---

## Important Notes

1. **PRD vs Feature Specification are different documents**:
   - PRD is conversational, detailed, our format
   - Feature Specification is SpecKit's structured format

2. **Feature Specification gets refined in place**:
   - SpecKit creates `spec.md`
   - We refine `spec.md`
   - Same file, improved content

3. **Follow SpecKit conventions after refinement**:
   - Use `spec.md`, `plan.md`, `tasks.md` naming
   - Place in SpecKit's expected directory structure

---

**Use this terminology consistently in all documentation, conversations, and file names.**

---

## Further Information

**For detailed workflow**: See [../guides/workflow.md](../guides/workflow.md) - Official process with work orders WO-1 through WO-5

**For methodology**: See [../guides/methodology.md](../guides/methodology.md) - How to create Comprehensive Source documents

**For getting started**: See [../guides/quickstart.md](../guides/quickstart.md) - Navigation and entry point for new users

**For quick reference**: See [../guides/quick-reference-card.md](../guides/quick-reference-card.md) - One-page cheat sheet for experienced users

**For the system overview**: See [../README.md](../README.md) - RequirementsKit documentation hub
