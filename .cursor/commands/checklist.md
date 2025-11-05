---
description: "Validate specifications against quality criteria"
---

# SpecKit Checklist Command

Validates specifications against established quality criteria and acceptance standards.

**Usage:**
1. Have a completed specification document
2. Run this command to validate against checklist
3. Review results and address any gaps

**Input:** Specification document (implementation-ready spec)
**Output:** Validation report with pass/fail status for each criterion

**Validation Categories:**
- **Completeness**: All required sections present
- **Quality**: No vague terms, specific measurements
- **Consistency**: No contradictions between sections
- **Testability**: All requirements are verifiable
- **Scope**: Clear boundaries and out-of-scope items

**Quality Criteria:**
- [ ] Problem statement with specific numbers (not "it's slow")
- [ ] 10+ use cases with scale and success criteria
- [ ] Complete data model with exact schema (if applicable)
- [ ] 3-5 example workflows with actual commands/queries
- [ ] Performance targets with numbers (<Xms, Y concurrent users)
- [ ] 3-7 implementation phases with deliverables
- [ ] 20+ edge cases documented
- [ ] Technology choices with rationale
- [ ] Out of scope list clearly defined
- [ ] Testing strategy with acceptance criteria

**Example:**
```
Validate the AI Development Module specification against the quality checklist. Check for completeness, consistency, and testability.
```

**Pass/Fail Results:**
- ✅ **PASS**: All criteria met, ready for implementation
- ⚠️ **REVIEW**: Most criteria met, minor issues to address
- ❌ **FAIL**: Significant gaps requiring revision

**Common Issues:**
- Vague performance targets (use specific numbers)
- Missing use cases (need 10+ scenarios)
- Incomplete data models (show actual schema)
- No edge cases (document 20+ failure scenarios)


