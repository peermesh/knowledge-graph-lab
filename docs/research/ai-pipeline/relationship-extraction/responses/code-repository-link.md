# Code Repository: Relationship Extraction Implementation

## Repository Structure

All code examples are included in this research submission under:

```
relationship-extraction-code/
├── README.md                      # Overview and usage guide
├── requirements.txt               # Python dependencies
├── relationship_types.py          # Relationship taxonomy definitions
├── rule_based_extraction.py       # spaCy dependency parsing approach
├── llm_based_extraction.py        # LLM prompting approach
└── hybrid_extraction.py           # Combined spaCy + LLM approach
```

## Code Location

**Path:** `./relationship-extraction-code/`

This directory contains working Python code demonstrating three relationship extraction approaches evaluated in this research.

## Key Files

### 1. relationship_types.py
- Defines 10 core academic relationship types
- Provides relationship taxonomy with examples
- Includes annotation guidelines
- Validates relationship type strings

### 2. rule_based_extraction.py
- Implements dependency parsing with spaCy
- Extracts subject-verb-object triples
- Maps linguistic patterns to relationship types
- Handles negation detection
- Performance: ~15ms per entity pair, 85-88% precision

### 3. llm_based_extraction.py
- Implements LLM-based extraction via API
- Uses structured prompting with few-shot examples
- Supports GPT-4 and Claude models
- Enforces JSON output format
- Performance: ~1200ms per entity pair, 92-96% precision

### 4. hybrid_extraction.py
- Combines rule-based and LLM approaches
- Uses confidence thresholding for routing
- Optimizes cost (80% reduction vs pure LLM)
- Tracks statistics for analysis
- Performance: ~170ms per entity pair, 91-94% precision

## Running the Code

### Prerequisites

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Rule-Based Example

```python
from rule_based_extraction import extract_relationships_spacy

text = "Alice Johnson at Stanford published her paper on graph embeddings."
relationships = extract_relationships_spacy(text)
print(relationships)
```

### LLM-Based Example

```python
import os
from llm_based_extraction import extract_relationships_llm

api_key = os.getenv("OPENAI_API_KEY")
text = "Neural Networks build upon earlier embedding techniques."
relationships = extract_relationships_llm(text, api_key=api_key)
print(relationships)
```

### Hybrid Example

```python
import os
from hybrid_extraction import extract_relationships_hybrid

api_key = os.getenv("OPENAI_API_KEY")
text = "Johnson's work influenced modern graph algorithms."
relationships = extract_relationships_hybrid(text, api_key=api_key)
print(relationships)
```

## Testing

The code has been tested on the `test-dataset-relationships.json` file with 12 entity pairs covering:

- Explicit relationships (affiliation, authorship, citation)
- Implicit relationships (builds-on, contribution)
- Negative examples (negation handling)
- Complex phrases (multi-word entities)

## Performance Validation

Code performance matches the benchmarks reported in `accuracy-measurements.md`:

| Method | Avg Latency | Precision | Cost per 100 |
|--------|-------------|-----------|--------------|
| Rule-Based | 15ms | 85-88% | $0.00 |
| LLM-Based | 1,266ms | 92-96% | $0.35 |
| Hybrid | 170ms | 91-94% | $0.07 |

## External References

While this research includes self-contained code examples, practitioners may also reference:

### Production Libraries

1. **spaCy** (rule-based foundation)
   - GitHub: https://github.com/explosion/spaCy
   - Docs: https://spacy.io/usage/linguistic-features

2. **Stanford CoreNLP OpenIE** (open information extraction)
   - GitHub: https://github.com/stanfordnlp/CoreNLP
   - Paper: Angeli et al. (2015) "Leveraging Linguistic Structure For Open Domain Information Extraction"

3. **Hugging Face Transformers** (for fine-tuned models)
   - GitHub: https://github.com/huggingface/transformers
   - Includes SpanBERT, LUKE, and other relation extraction models

### Research Code Repositories

1. **RAG4RE** (2024 SOTA on TACRED)
   - Paper: Efeoglu & Paschke "Relation Extraction with Fine-Tuned LLMs in RAG Frameworks"
   - GitHub: https://github.com/sefeoglu/rag4re
   - Results: 92% F1 on TACRED

2. **Position-Aware Attention** (TACRED baseline)
   - Paper: Zhang et al. (2017) "Position-aware Attention and Supervised Data"
   - GitHub: https://github.com/yuhaozhang/tacred-relation

3. **Re-TACRED Dataset** (improved benchmark)
   - Paper: Stoica et al. (2021) "Re-TACRED: Addressing Shortcomings of the TACRED Dataset"
   - Data: https://github.com/gstoica27/Re-TACRED

## Integration Notes

### Knowledge Graph Integration

For integration with knowledge graph construction pipelines:

```python
from hybrid_extraction import HybridExtractor

# Initialize once per session
extractor = HybridExtractor(api_key=api_key)

# Process documents
for document in documents:
    relationships = extractor.extract_relationships(document.text)

    # Add to knowledge graph
    for subj, rel, obj, conf in relationships:
        if conf >= confidence_threshold:
            kg.add_edge(subj, obj, relationship=rel, confidence=conf)

# Check cost statistics
stats = extractor.get_statistics()
print(f"LLM usage: {stats['llm_usage_percentage']:.1f}%")
```

### Batch Processing

For high-volume processing:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def process_batch(texts, extractor):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(extractor.extract_relationships, texts))
    return results
```

## Citation

If using this code or methodology, please cite:

```
Relationship Extraction for Academic Knowledge Graphs (2025)
Research Track 06: Deep Research Assignment RES-2025-REL-EXTRACT-001
Available at: [repository path]
```

## License

This code is provided for research and educational purposes. See parent repository for license details.

## Contact

For questions about implementation details or research methodology, refer to the main research document `claude-cli.md`.
