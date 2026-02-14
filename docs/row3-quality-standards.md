# Row 3 Quality Standards

Quality metrics, pass/fail thresholds, and testing protocols for the Decomposition Layer.

**Document Version**: 1.0
**Created**: 2026-01-29
**Related Work Order**: WO-KGL-006 (Row 3 Validation Harness)

---

## 1. Quality Metrics Definitions

Each metric quantifies a specific aspect of decomposition quality. All metrics range from 0.0 to 1.0 (or 0% to 100%) unless otherwise specified.

### 1.1 Concept Precision

**Definition**: The proportion of extracted concepts that are correct (present in the golden set or semantically equivalent).

**Formula**:
```
Concept Precision = correct_concepts / total_extracted_concepts
```

**Example**:
- Extracted 20 concepts
- 16 match the golden set (exact or alias match)
- Precision = 16/20 = 0.80 (80%)

**What It Measures**: How accurate the extraction is. High precision means few false positives (hallucinated or irrelevant concepts).

---

### 1.2 Concept Recall

**Definition**: The proportion of expected concepts that were successfully extracted.

**Formula**:
```
Concept Recall = found_expected_concepts / total_expected_concepts
```

**Example**:
- Golden set contains 25 expected concepts
- Decomposition found 18 of them
- Recall = 18/25 = 0.72 (72%)

**What It Measures**: How complete the extraction is. High recall means few false negatives (missed concepts).

---

### 1.3 Concept F1 Score

**Definition**: The harmonic mean of precision and recall, providing a balanced single metric.

**Formula**:
```
Concept F1 = 2 * (precision * recall) / (precision + recall)
```

**Example**:
- Precision = 0.80
- Recall = 0.72
- F1 = 2 * (0.80 * 0.72) / (0.80 + 0.72) = 0.758 (75.8%)

**What It Measures**: Overall concept extraction quality. Balances the tradeoff between precision and recall.

---

### 1.4 Relationship Accuracy

**Definition**: The proportion of extracted relationships that correctly match expected relationships (same source, target, and predicate).

**Formula**:
```
Relationship Accuracy = correct_relationships / total_extracted_relationships
```

**Example**:
- Extracted 40 relationships
- 28 match the golden set (correct source, target, predicate)
- Accuracy = 28/40 = 0.70 (70%)

**What It Measures**: How well the system identifies connections between concepts and assigns correct predicates.

---

### 1.5 Provenance Coverage

**Definition**: The proportion of concepts that include a source quote (provenance) from the original text.

**Formula**:
```
Provenance Coverage = concepts_with_source_quote / total_concepts
```

**Example**:
- Extracted 20 concepts
- 18 have source quotes attached
- Coverage = 18/20 = 0.90 (90%)

**What It Measures**: Grounding quality. High coverage ensures concepts are traceable to source material.

---

### 1.6 Hallucination Rate

**Definition**: The proportion of extracted concepts that appear in the forbidden (hallucination canary) list.

**Formula**:
```
Hallucination Rate = forbidden_concepts_found / total_extracted_concepts
```

**Example**:
- Extracted 20 concepts
- 1 is in the forbidden list (a known hallucination canary)
- Rate = 1/20 = 0.05 (5%)

**What It Measures**: Fabrication risk. Lower is better. Zero is ideal.

**Note**: Forbidden concepts are intentionally plausible-sounding terms that do NOT appear in the source text. If the model extracts them, it is hallucinating.

---

### 1.7 Overall Score (Weighted Composite)

**Definition**: A single score combining all metrics with predefined weights.

**Formula**:
```
Overall Score = (w1 * Recall) + (w2 * Precision) + (w3 * RelAccuracy) + (w4 * Provenance) - (w5 * Hallucination)
```

**Default Weights**:

| Metric | Weight | Rationale |
|--------|--------|-----------|
| Concept Recall | 0.25 | Missing concepts hurts downstream reasoning |
| Concept Precision | 0.20 | False positives pollute the graph |
| Relationship Accuracy | 0.20 | Relationships enable traversal and inference |
| Provenance Coverage | 0.20 | Grounding is essential for trust |
| Hallucination Penalty | 0.15 | Hallucinations are unacceptable in production |

**Calculation Example**:
```
Overall = (0.25 * 0.72) + (0.20 * 0.80) + (0.20 * 0.70) + (0.20 * 0.90) - (0.15 * 0.05)
        = 0.18 + 0.16 + 0.14 + 0.18 - 0.0075
        = 0.6525 (65.25%)
```

**Note**: The hallucination component is subtracted, not added, creating a penalty.

---

## 2. Quality Thresholds

These thresholds define pass/fail criteria for the validation harness.

| Metric | Minimum (Fail) | Target (Pass) | Excellent |
|--------|----------------|---------------|-----------|
| Concept Recall | <60% | >=70% | >=85% |
| Concept Precision | <50% | >=65% | >=80% |
| Relationship Accuracy | <40% | >=60% | >=75% |
| Provenance Coverage | <80% | >=90% | >=98% |
| Hallucination Rate | >5% | <=2% | 0% |
| Overall Score | <65% | >=75% | >=85% |

### Threshold Interpretation

**Fail (Red)**: Decomposition quality is unacceptable. Do not proceed with prompt changes that cause regression to this level.

**Pass (Green)**: Decomposition quality meets minimum acceptable standards for production use.

**Excellent (Gold)**: Decomposition quality exceeds expectations. This is the target for mature prompts.

### Blocking Rules

1. **Any metric in Fail zone**: Block merge/deploy
2. **Hallucination Rate > 0%**: Warning flag, investigate before proceeding
3. **Overall Score regression > 5%**: Requires explicit approval to proceed

---

## 3. Test Case Requirements

Golden test cases are the foundation of the validation harness. They define what "correct" looks like.

### 3.1 Minimum Case Count

- **Minimum**: 5 golden test cases
- **Target**: 10 golden test cases
- **Ideal**: 15+ golden test cases (for statistical significance)

### 3.2 Domain Diversity Requirements

Test cases MUST cover diverse domains to ensure generalization:

| Domain Category | Example Topics | Minimum Cases |
|-----------------|----------------|---------------|
| Ecological/Environmental | Regenerative agriculture, biodiversity, climate systems | 1 |
| Technical/Engineering | Machine learning, quantum computing, blockchain | 1 |
| Social/Political | Public policy, governance, international relations | 1 |
| Economic/Business | Supply chain, market dynamics, financial systems | 1 |
| Interdisciplinary | Topics spanning multiple domains | 1 |

### 3.3 Concept Requirements Per Case

Each golden test case MUST include:

- **Expected Concepts**: 15-25 concepts
  - Minimum 15 (ensures sufficient coverage)
  - Maximum 25 (prevents over-specification)
  - Mix of required (MUST extract) and optional (SHOULD extract) concepts

- **Concept Aliases**: At least 3 concepts per case should have aliases
  - Example: "ML" is an alias for "Machine Learning"

### 3.4 Relationship Requirements Per Case

Each golden test case MUST include:

- **Expected Relationships**: 30-50 relationships
  - Minimum 30 (ensures graph connectivity)
  - Maximum 50 (prevents over-specification)
  - Must use defined predicate types (IS_A, CAUSES, PRECEDES, REQUIRES, RELATES_TO)

### 3.5 Hallucination Canary Requirements

Each golden test case MUST include:

- **Forbidden Concepts**: 5-10 hallucination canaries
  - Plausible-sounding terms NOT in the source text
  - Related to the domain but fabricated
  - Example for ML: "Neural Osmosis Learning" (sounds real, doesn't exist)

- **Forbidden Relationships**: 3-5 forbidden relationships
  - Plausible but incorrect causal/hierarchical relationships
  - Example: "Climate change CAUSES quantum entanglement"

### 3.6 Source Text Requirements

- **Length**: 2-5 paragraphs (300-800 words)
- **Quality**: Well-written, factually accurate source material
- **Origin**: Can be original writing or excerpts from real articles (with citation)
- **Complexity**: Should contain multiple interconnected concepts

---

## 4. Regression Testing Protocol

Regression testing ensures prompt changes do not degrade quality.

### 4.1 When to Run Tests

**Required (Blocking)**:
- Before any prompt template changes
- After any prompt template changes
- Before merging PRs that touch decomposition logic
- Before deploying to production

**Recommended (Non-Blocking)**:
- Daily during active development
- Weekly during maintenance periods

### 4.2 Test Execution Steps

1. **Pre-Change Baseline**
   ```bash
   npm run test:row3 -- --baseline
   # Saves current scores to .baseline.json
   ```

2. **Make Changes**
   - Modify prompt templates
   - Update extraction logic
   - Adjust parameters

3. **Post-Change Validation**
   ```bash
   npm run test:row3 -- --compare
   # Compares against baseline, flags regressions
   ```

4. **Review Report**
   - Check for any metrics in Fail zone
   - Check for regressions > 5%
   - Review specific test case failures

### 4.3 Regression Investigation Threshold

| Score Change | Action Required |
|--------------|-----------------|
| Improvement or no change | Proceed normally |
| Regression 1-5% | Investigate, document reason |
| Regression > 5% | Block merge, investigate before proceeding |
| Any metric enters Fail zone | Block merge, mandatory investigation |

### 4.4 Trend Tracking

- Maintain a `metrics-history.json` file tracking scores over time
- Generate weekly quality trend charts
- Alert if 3+ consecutive runs show declining scores

---

## 5. Prompt Iteration Protocol

Structured process for improving prompts while maintaining quality.

### 5.1 Version Control

All prompts MUST be version controlled:

```
prompts/
  decompose-concepts-v1.0.md
  decompose-concepts-v1.1.md
  decompose-concepts-v2.0.md
  map-ontology-v1.0.md
  CHANGELOG.md
```

### 5.2 Iteration Steps

1. **Create New Version**
   - Copy current prompt to new version file
   - Increment version number (v1.0 -> v1.1 for minor, v1.0 -> v2.0 for major)
   - Document intended changes in CHANGELOG.md

2. **Run Against ALL Golden Test Cases**
   ```bash
   npm run test:row3 -- --prompt decompose-concepts-v1.1
   ```

3. **Compare Metrics to Previous Version**
   - Generate comparison report
   - Review per-test-case deltas
   - Identify which cases improved/regressed

4. **Promotion Decision**
   - **Promote if**: All metrics stable or improved, no new Fail states
   - **Do not promote if**: Any metric regresses > 5% or enters Fail zone

5. **Document Changes**
   - Update CHANGELOG.md with version, date, changes, and metrics delta
   - Archive old version (do not delete)

### 5.3 CHANGELOG Format

```markdown
## v1.1 (2026-01-29)

### Changes
- Added few-shot example for technical domains
- Clarified atomicity rule for compound concepts

### Metrics Impact
| Metric | v1.0 | v1.1 | Delta |
|--------|------|------|-------|
| Recall | 70% | 74% | +4% |
| Precision | 65% | 68% | +3% |
| Overall | 75% | 78% | +3% |

### Notes
- Significant improvement on machine-learning.gold.json
- Slight regression on climate-change-policy.gold.json (investigate)
```

---

## 6. Failure Investigation Checklist

When a test case fails, use this checklist to diagnose the issue.

### 6.1 Recall Issues (Missing Concepts)

- [ ] Which specific concepts were missed?
- [ ] Are the missed concepts mentioned explicitly in the source text?
- [ ] Are the missed concepts implied but not stated?
- [ ] Is the prompt instruction too narrow/restrictive?
- [ ] Would a few-shot example help?

### 6.2 Precision Issues (Hallucinated Concepts)

- [ ] Which concepts were hallucinated?
- [ ] Do they appear in the forbidden list (intentional canaries)?
- [ ] Are they plausible inferences from the source text?
- [ ] Is the prompt instruction too permissive?
- [ ] Is the model temperature too high?

### 6.3 Relationship Issues (Wrong Predicates)

- [ ] Which relationships were incorrect?
- [ ] Was the source/target correct but predicate wrong?
- [ ] Are predicate definitions clear enough in the prompt?
- [ ] Is the relationship directionally reversed?
- [ ] Would predicate examples help?

### 6.4 Provenance Issues (Missing Source Quotes)

- [ ] Which concepts lack provenance?
- [ ] Is the source text sufficiently detailed?
- [ ] Is the prompt instruction for quoting clear?
- [ ] Is the model truncating or paraphrasing quotes?

### 6.5 Golden Test Case Issues

- [ ] Is the expected concept set too strict/lenient?
- [ ] Are concept aliases comprehensive enough?
- [ ] Is the source text ambiguous?
- [ ] Should the golden case be updated?

### 6.6 Investigation Template

```markdown
## Failure Investigation: [Test Case Name]

**Date**: YYYY-MM-DD
**Prompt Version**: vX.Y
**Failing Metric(s)**: [list]

### Symptoms
[What failed and by how much]

### Root Cause
[Why it failed]

### Proposed Fix
[What to change]

### Verification Plan
[How to confirm the fix works]
```

---

## 7. Monitoring in Production

Metrics to track when decomposition is running in production.

### 7.1 Operational Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Concepts per Topic | Average number of concepts extracted | 15-30 |
| Relationships per Topic | Average number of relationships | 30-60 |
| Average Confidence | Mean confidence score across concepts | > 0.75 |
| Decomposition Latency | Time from request to response | < 3000ms |
| Cost per Decomposition | API cost per decomposition call | < $0.05 |

### 7.2 Quality Metrics (Sampled)

For a sample of production decompositions (e.g., 5% random sample):

| Metric | Description | Target |
|--------|-------------|--------|
| Human-Rated Accuracy | Expert review of sample outputs | > 80% acceptable |
| User Feedback Score | Thumbs up/down on concepts | > 4.0/5.0 |
| Provenance Verification | Spot-check that quotes match source | > 95% verified |

### 7.3 Alert Thresholds

Configure alerts for these conditions:

| Condition | Severity | Action |
|-----------|----------|--------|
| Avg confidence drops below 0.7 | Warning | Investigate prompt drift |
| Hallucination rate exceeds 2% | Critical | Pause deployments, investigate |
| Latency exceeds 5000ms | Warning | Check API performance |
| Cost exceeds $0.10/decomposition | Warning | Review token usage |
| Concepts per topic < 10 | Warning | Check extraction completeness |
| Error rate > 1% | Critical | Check API availability |

### 7.4 Dashboard Metrics

The production dashboard should display:

1. **Real-time**
   - Decomposition requests/minute
   - Current latency p50/p95/p99
   - Error rate

2. **Hourly Aggregates**
   - Average concepts per topic
   - Average relationships per topic
   - Confidence distribution

3. **Daily Summaries**
   - Total decompositions processed
   - Quality sample results
   - Cost tracking

---

## 8. Continuous Improvement

Ongoing processes to maintain and improve decomposition quality.

### 8.1 Weekly Review

Every week, review:

- [ ] Lowest-scoring decompositions from production samples
- [ ] User feedback trends (any patterns in negative feedback?)
- [ ] Error logs for failed decompositions
- [ ] Latency trends

**Output**: Weekly quality brief (1 page max)

### 8.2 Monthly Expansion

Every month:

- [ ] Add 1-2 new golden test cases based on production patterns
- [ ] Review and update existing golden cases if needed
- [ ] Analyze correlation between metrics and user satisfaction
- [ ] Update hallucination canaries based on observed fabrications

**Output**: Updated golden test suite, metrics correlation report

### 8.3 Quarterly Optimization

Every quarter:

- [ ] Conduct prompt optimization sprint (dedicated time)
- [ ] A/B test major prompt changes in production
- [ ] Review and adjust quality thresholds if needed
- [ ] Update documentation based on learnings

**Output**: Quarterly quality report, updated thresholds (if any)

### 8.4 Metrics-User Satisfaction Correlation

Track which quality metrics best predict user satisfaction:

| Metric | Correlation with User Satisfaction | Weight Adjustment |
|--------|-----------------------------------|-------------------|
| Recall | [measure] | [adjust if needed] |
| Precision | [measure] | [adjust if needed] |
| Provenance | [measure] | [adjust if needed] |

**Goal**: Ensure the Overall Score formula weights metrics that actually matter to users.

---

## Appendix A: Metric Calculation Reference

### Precision/Recall Calculation

```typescript
function calculatePrecisionRecall(
  extracted: string[],
  expected: string[],
  aliases: Map<string, string[]>
): { precision: number; recall: number } {
  const normalizedExpected = new Set(
    expected.flatMap(e => [e.toLowerCase(), ...(aliases.get(e) || []).map(a => a.toLowerCase())])
  );

  const normalizedExtracted = extracted.map(e => e.toLowerCase());

  const correctCount = normalizedExtracted.filter(e =>
    normalizedExpected.has(e)
  ).length;

  const precision = correctCount / normalizedExtracted.length;
  const recall = correctCount / expected.length;

  return { precision, recall };
}
```

### Overall Score Calculation

```typescript
function calculateOverallScore(metrics: {
  recall: number;
  precision: number;
  relationshipAccuracy: number;
  provenanceCoverage: number;
  hallucinationRate: number;
}): number {
  const weights = {
    recall: 0.25,
    precision: 0.20,
    relationshipAccuracy: 0.20,
    provenanceCoverage: 0.20,
    hallucinationPenalty: 0.15
  };

  return (
    weights.recall * metrics.recall +
    weights.precision * metrics.precision +
    weights.relationshipAccuracy * metrics.relationshipAccuracy +
    weights.provenanceCoverage * metrics.provenanceCoverage -
    weights.hallucinationPenalty * metrics.hallucinationRate
  );
}
```

---

## Appendix B: Golden Test Case Template

```json
{
  "id": "test-case-id",
  "topic": "Topic Name",
  "domain": "ecological|technical|social|economic|interdisciplinary",
  "version": "1.0",
  "created": "2026-01-29",
  "sourceText": "Full source text here (2-5 paragraphs)...",
  "expectedConcepts": [
    {
      "label": "Concept Name",
      "aliases": ["Alias 1", "Alias 2"],
      "required": true
    }
  ],
  "expectedRelationships": [
    {
      "source": "Source Concept",
      "target": "Target Concept",
      "predicate": "CAUSES|IS_A|PRECEDES|REQUIRES|RELATES_TO",
      "required": true
    }
  ],
  "forbiddenConcepts": [
    "Hallucination Canary 1",
    "Hallucination Canary 2"
  ],
  "forbiddenRelationships": [
    {
      "source": "Concept A",
      "target": "Concept B",
      "predicate": "CAUSES"
    }
  ]
}
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-29 | KGL Team | Initial document |
