# Quick Reference Card - RequirementsKit System

**For experienced users** | One-page cheat sheet | Last updated: 2025-10-09

---

## Quick Command Reference

### Phase 1: Foundation (1-2 hours)
```bash
# Read entry points
Read: guides/quickstart.md
Read: STRATEGY.md
```

### Phase 2: Information Gathering (4-6 hours)
```bash
# Create module workspace
mkdir -p work/[module-name]/

# Index sources
Create: 01-INFORMATION-SOURCES-INDEX.md

# Define integration contracts
Create: 05-INTEGRATION-CONTRACTS.md

# Identify gaps
Create: 03-GAPS-IDENTIFIED.md

# Resolve gaps (research first, then flag)
Create: 04-GAPS-ANSWERS.md
```

### Phase 3: Spec Creation (6-10 hours)
```bash
# Option A: Starter template (recommended)
cp templates/simple-template.md tests/[module-name]/[module]-starter-filled.md
# Fill 8 sections, target 300-500 lines
# Have AI expand to comprehensive (or do manually)

# Option B: Comprehensive template (experienced users)
cp templates/comprehensive-template.md tests/[module-name]/[module]-comprehensive-source.md
# Fill 10 sections, target 800-1,500 lines
```

### Phase 4: SpecKit Processing (3-5 hours)
```bash
# Quality check
Use: checklists/quality-comparison-checklist.md

# Refine spec
Create: 09-SPECKIT-PROCESS-LOG.md
Edit: [module]-comprehensive-source.md → 10-FINAL-SPEC.md
# Target: 500-700 lines, match case study quality
```

### Phase 5: Validation (3-5 hours)
```bash
# Validate completeness and quality
Use: checklists/validation-checklist-template.md

# Create readiness assessment
Create: 11-IMPLEMENTATION-READINESS.md

# Capture learnings
Create: 12-LEARNINGS-FOR-UNIVERSAL-SYSTEM.md
```

---

## Quick File Reference

**Entry points (start here):**
- `README.md` - System overview
- `guides/quickstart.md` - Getting started guide
- `reference/package-extraction.md` - Extraction to other projects

**Guides:**
- `guides/workflow.md` - Visual process flow
- `guides/developer-guide.md` - Complete walkthrough (2,000-3,000 lines)
- `guides/process-overview.md` - 5-phase detailed outline
- `guides/quick-reference-card.md` - This file

**Templates:**
- `templates/simple-template.md` - 8 sections, 300-500 lines
- `templates/comprehensive-template.md` - 10 sections, 800-1,500 lines
- `reference/prd-generation-rules.md` - AI expansion rules

**Checklists:**
- `checklists/mvp-specification-creation-guide.md` - MVP scoping
- `checklists/quality-comparison-checklist.md` - WO-4 quality check
- `checklists/validation-checklist-template.md` - WO-5 validation
- `checklists/technical-accuracy-checklist.md` - Technical validation
- `checklists/when-to-use-specify-guide.md` - When to use /specify

**Working directory setup:**
```bash
mkdir -p work/{module-name}/
```

---

## Phase Checklist (Copy-Paste Ready)

### Phase 1: Foundation
```
[ ] Read guides/quickstart.md (understand system)
[ ] Read STRATEGY.md (understand philosophy)
[ ] Review case study (quality benchmark)
[ ] Understand 5-phase workflow
[ ] Know template options (starter vs comprehensive)
```

### Phase 2: Information Gathering (WO-2)
```
[ ] Create module workspace: tests/[module-name]/
[ ] Create 00-SESSION-LOG.md (track all decisions)
[ ] Index sources: 01-INFORMATION-SOURCES-INDEX.md
[ ] Define contracts: 05-INTEGRATION-CONTRACTS.md
[ ] Identify gaps: 03-GAPS-IDENTIFIED.md
[ ] Resolve gaps: 04-GAPS-ANSWERS.md (research first, then flag)
[ ] Document all decisions in session log
```

### Phase 3: Spec Creation (WO-3)
```
[ ] Choose template (starter for most, comprehensive for experienced)
[ ] Copy template to module workspace
[ ] Fill all required sections (8 for starter, 10 for comprehensive)
[ ] Use session log and gap answers as inputs
[ ] Quantify all metrics (numbers + units)
[ ] Define all integration contracts (JSON schemas)
[ ] Zero [NEEDS CLARIFICATION] for known info
[ ] Document all assumptions
[ ] Target lines: Starter 300-500, Comprehensive 800-1,500
```

### Phase 4: SpecKit Processing (WO-4)
```
[ ] Read comprehensive spec (from Phase 3)
[ ] Read case study benchmark (576 lines)
[ ] Compare section-by-section (use quality-comparison-checklist.md)
[ ] Identify over-specifications (implementation details, redundancy)
[ ] Create 09-SPECKIT-PROCESS-LOG.md (document refinement strategy)
[ ] Refine spec manually to match case study quality
[ ] Remove: SQL schemas, API code, complete test suites
[ ] Focus on: WHAT to build, not HOW to build
[ ] Create 10-FINAL-SPEC.md (target: 500-700 lines)
[ ] Verify abstraction level matches case study
```

### Phase 5: Validation (WO-5)
```
[ ] Use validation-checklist-template.md
[ ] T18: Completeness (all 10 sections filled, no placeholders)
[ ] T19: Quality comparison (500-700 lines, matches case study depth)
[ ] T20: MVP scope (≤5 features, 2-4 weeks timeline)
[ ] T21: Integration points (all contracts defined, stubs specified)
[ ] T22: Final spec confirmation (implementation-ready quality)
[ ] Create 11-IMPLEMENTATION-READINESS.md (GO/NO-GO recommendation)
[ ] Create 12-LEARNINGS-FOR-UNIVERSAL-SYSTEM.md (capture improvements)
[ ] Implement learnings before next module starts
```

---

## Common File Patterns

### Session Documentation
```
00-SESSION-LOG.md               # All decisions, rationale, context
00-[module]-decisions.md        # Alternative naming pattern
```

### Information Gathering (Phase 2)
```
01-INFORMATION-SOURCES-INDEX.md       # Source documents catalog
02-[optional-context].md              # Additional context if needed
03-GAPS-IDENTIFIED.md                 # Unknown items, questions
04-GAPS-ANSWERS.md                    # Gap resolution, research
05-INTEGRATION-CONTRACTS.md           # API contracts, mock specs
```

### Spec Creation (Phase 3)
```
[module]-starter-filled.md            # 300-500 lines (starter approach)
[module]-comprehensive-source.md      # 800-1,500 lines (comprehensive approach)
06-ASSUMPTIONS-DOCUMENTED.md          # Assumptions and constraints
07-[additional-context].md            # Optional supporting docs
```

### Refinement (Phase 4)
```
08-COMPARISON-TO-CASE-STUDY.md        # Section-by-section analysis
09-SPECKIT-PROCESS-LOG.md             # Refinement strategy
```

### Final Outputs (Phase 4-5)
```
10-FINAL-SPEC.md                      # 500-700 lines, implementation-ready
11-IMPLEMENTATION-READINESS.md        # GO/NO-GO assessment
12-LEARNINGS-FOR-UNIVERSAL-SYSTEM.md  # System improvements
```

### Numbering Convention
```
00-09: Process documentation, context, decisions
10-19: Final outputs, deliverables
20-29: Reserved for future extensions
```

---

## Quick Troubleshooting

### "Spec too long (>1,500 lines)"
```
Problem: Comprehensive spec exceeds expected range
Solution:
  1. Check if module is genuinely complex (5+ entities, 4+ integrations)
  2. If yes: Accept higher line count, focus on quality refinement in Phase 4
  3. If no: Condense data model (DDL → entity list), reduce integration details
  4. Use quality-comparison-checklist.md section-by-section
```

### "Gaps found during spec creation"
```
Problem: Missing critical information
Solution:
  1. STOP - Do not guess or invent details
  2. Research first (read source docs, ask stakeholders)
  3. Document in 03-GAPS-IDENTIFIED.md
  4. Resolve in 04-GAPS-ANSWERS.md
  5. If unresolvable: Flag as [TBD: needs research] with clear question
  6. Document decision rationale in 00-SESSION-LOG.md
```

### "Not sure which template to use"
```
Problem: Starter vs comprehensive choice unclear
Solution:
  - Use starter template for most cases (recommended)
  - Use comprehensive if:
    • Experienced with writing specs
    • Have detailed source documents
    • AI will expand starter anyway (use comprehensive as target)
  - Default: Starter (safest, faster, AI can expand)
```

### "Lost context between sessions"
```
Problem: Can't remember previous decisions
Solution:
  1. Always check 00-SESSION-LOG.md first
  2. Review numbered files in sequence (01, 02, 03...)
  3. Check module decisions: 00-[module]-decisions.md
  4. If missing: Recreate session log from file history
  5. Prevention: Update session log after EVERY decision
```

### "SpecKit has [NEEDS CLARIFICATION] flags"
```
Problem: AI detected missing information during expansion/processing
Solution:
  1. Search spec for [NEEDS CLARIFICATION]
  2. Review 03-GAPS-IDENTIFIED.md and 04-GAPS-ANSWERS.md
  3. Add missing quantified metrics (numbers + units)
  4. Specify integration contracts (JSON schemas)
  5. Document all assumptions explicitly
  6. Re-run AI expansion/processing with complete inputs
```

### "Comprehensive spec doesn't match case study quality"
```
Problem: Quality validation failing in Phase 4
Solution:
  1. Use checklists/quality-comparison-checklist.md
  2. Compare section-by-section to case study (576 lines)
  3. Remove: SQL queries, API code, test suites, implementation details
  4. Keep: WHAT to build (requirements), not HOW (implementation)
  5. Target abstraction: Behavior specifications, not algorithms
  6. Check redundancy: Merge duplicate sections
  7. Document refinement in 09-SPECKIT-PROCESS-LOG.md
```

### "MVP scope unrealistic"
```
Problem: Too many features or timeline too long
Solution:
  1. Count features (must-have list)
  2. Target: ≤5 features for MVP
  3. Estimate timeline: 2-4 weeks realistic
  4. Use "nice-to-have" liberally
  5. Ask: Can we ship without this? If yes → defer
  6. Review 00-SESSION-LOG.md for scope decisions
  7. Update decisions document with rationale
```

### "Don't understand a meta-instruction"
```
Problem: Unclear guidance in meta-instructions/
Solution:
  1. Check guides/developer-guide.md for detailed explanation
  2. Review case study for concrete example
  3. Check guides/quickstart.md for navigation help
  4. Look at Publishing module (tests/publishing-module/) as reference
  5. Refer to STATUS.md for current system state
```

---

## Golden Rules for Experienced Users

1. **Always use session log** - Track every decision, no exceptions
2. **Research gaps first** - Never guess critical details
3. **Quantify everything** - Numbers + units for all metrics
4. **MVP = Minimum Viable** - Ruthlessly defer non-essential features
5. **WHAT not HOW** - Requirements describe behavior, not implementation
6. **Case study is benchmark** - All quality comparisons reference 576-line gold standard
7. **Implement learnings** - 100% implementation rate before next module

---

## Publishing Module Metrics (Reference)

```
Phase 2: Information Gathering
  Time: ~4 hours
  Files: 01, 03, 04, 05 + session log

Phase 3: Spec Creation
  Starter: 290 lines (~3 hours)
  Comprehensive: 1,205 lines (~20 min AI expansion)
  Reason for length: 5 entities, 4 integrations, complex module

Phase 4: SpecKit Processing
  Input: 1,205 lines
  Output: 625 lines
  Ratio: 0.597 (close to 0.596 baseline)
  Quality: Matches case study abstraction level

Phase 5: Validation
  Completeness: ✓ All 10 sections filled
  Quality: ✓ Matches case study depth
  MVP scope: ✓ 8 features, 2-4 weeks
  Readiness: ✓ GO for implementation
```

---

**For complete step-by-step guidance:** See `guides/developer-guide.md` (2,000-3,000 lines)

**For system philosophy and approach:** See `STRATEGY.md`

**For current status and roadmap:** See `STATUS.md`
