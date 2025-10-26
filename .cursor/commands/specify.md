---
description: "Create specifications from comprehensive requirements"
---

# SpecKit Specify Command

Creates implementation-ready specifications from comprehensive requirements documents.

**Usage:**
1. Create a comprehensive requirements document (800-1500 lines) following the 10-section template
2. Run this command with the requirements document as input
3. Review and refine the generated specification

**Input:** Comprehensive requirements document (800-1500 lines)
**Output:** Implementation-ready specification (400-600 lines)

**Key Features:**
- Transforms detailed requirements into actionable specs
- Validates specification completeness
- Identifies integration points and dependencies
- Removes implementation details, focuses on requirements

**Example:**
```
Create a specification for the AI Development Module based on the comprehensive requirements in work/ai-development/05-COMPREHENSIVE-SPEC.md
```

**Troubleshooting:**
- If output is too generic (<200 lines), your input requirements aren't comprehensive enough
- If output has [NEEDS CLARIFICATION] markers, add missing details to your requirements
- For best results, use the RequirementsKit methodology first


