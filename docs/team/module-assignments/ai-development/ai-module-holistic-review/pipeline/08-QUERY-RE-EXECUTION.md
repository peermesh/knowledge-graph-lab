# Pipeline Step 8: Query Re-execution

**Layer:** 8 of 8
**Role:** Answer original query using enriched knowledge graph
**Phase:** Technology strategy - Evaluating approaches

---

## Step Element

```mermaid
graph LR
    H["8️⃣ Query<br/>Re-execution"]
    style H fill:#ede7f6,stroke:#311b92,stroke-width:3px
```

---

## Purpose

Answer the original user query using the enriched, updated knowledge graph.

**What it does:**
- Re-queries updated knowledge graph
- Synthesizes comprehensive answer from KB data
- Cites all sources
- Provides confidence scores
- Returns to user with feedback mechanism

---

## System Role & Integration

### **Inputs**
```
← From Knowledge Graph Merge step
  ├── Updated knowledge graph
  ├── New entities added
  ├── Merge statistics
  ├── Original query (from Step 1)
  └── Research conducted? (yes/no)
```

### **Outputs**
```
→ To User
  ├── Answer/response
  ├── Confidence score
  ├── Cited sources
  ├── Related entities
  └── Feedback mechanism

Feedback loops back to Step 1 for improvement
```

---

## Technology Options to Evaluate

### **Answer Synthesis**

| Approach | Method | Quality | Cost |
|----------|--------|---------|------|
| **LLM-based** | Claude synthesizes from KB data | High | High |
| **Template-based** | Fill templates with KB data | Good | Low |
| **Retrieval-based** | Find + rerank best answer | Medium | Low |
| **Hybrid** | Templates + LLM for complex | Very high | Medium |

---

### **Source Citation & Provenance**

| Approach | Implementation | Transparency | Complexity |
|----------|---|---|---|
| **Full lineage** | Show extraction chain | High | High |
| **Source documents** | Link to original docs | Good | Medium |
| **Top sources** | Cite top 3-5 sources | Good | Low |
| **Confidence-based** | More sources if low confidence | Good | Medium |

---

## Evaluation Criteria

**Choose based on:**

1. **Answer Quality**
   - Accuracy of synthesized answer
   - User satisfaction ratings
   - Correctness of cited sources

2. **User Understandability**
   - Clarity of answer
   - Usefulness of citations
   - Confidence score calibration

3. **Performance**
   - Synthesis latency (< 2s)
   - Impact on overall pipeline

4. **Feedback Integration**
   - How to collect user feedback
   - How to improve from feedback
   - Retraining cadence

---

## Testing & Validation

- User satisfaction testing (rate answers 1-5)
- Citation accuracy validation
- Comparison to baseline systems
- A/B testing if possible
- Feedback incorporation testing

---

## Key Decisions

1. **Synthesis Approach** - pure LLM or hybrid?
2. **Citation Detail** - full lineage or summary?
3. **Confidence Scoring** - what factors matter?
4. **Feedback Mechanism** - how to collect and use?
5. **Multi-answer Handling** - return best or all?

---

**Status:** Planning phase - Technology options under evaluation
