# RESEARCH TRACK 05: Entity Extraction

## Track Header

**Track Name**: Entity Extraction and Recognition
**Estimated Effort**: 6 days
**Priority**: CRITICAL
**Dependencies**: Track 01 (Query Processing) must be complete
**Success Criteria**:
- Benchmarked at least 5 LLM providers and 3 NER libraries
- Achieved 85%+ F1 score on benchmark dataset
- Documented cost per extraction for each approach
- Identified lowest-cost model that meets accuracy threshold
- Built proof-of-concept with entity deduplication and confidence scoring
- Clear cost-benefit analysis: can we replace Claude 3.5 with Cohere and save 73% per extraction?

## Research Objectives

### Core Questions
- Which LLM model gives 85%+ F1 score for lowest total cost per query?
- Can we use Cohere API instead of Claude 3.5 for entity extraction and save cost?
- How do we score entity confidence reliably without slowing extraction?
- What entity deduplication rate do we need for production quality?
- How much human review is needed and what are the thresholds?

### Why This Matters
Entity extraction is the highest-cost component of our pipeline. Every basis point of accuracy improvement and every cent saved on LLM calls compounds across millions of queries:
- LLM costs represent 60% of total extraction cost (Claude 3.5 at $0.003 per extraction)
- If Cohere works at $0.0008 per extraction, we save $0.27 per full query (3.6x reduction)
- Extraction quality directly impacts graph accuracy and user confidence
- Poor entity deduplication creates false nodes and broken relationships
- This is our biggest cost optimization opportunity in the entire pipeline

### What Decisions This Supports
- LLM provider selection: which API to use long-term
- Entity deduplication strategy: fuzzy matching vs semantic matching vs both
- Confidence threshold policy: when do we flag for human review
- Budget modeling: cost per query and ROI for accuracy improvements
- Scaling economics: which approach lets us scale without proportional cost increase

## Research Areas

### Area 1: LLM Provider Benchmarking

**What to Research**
- Claude 3.5 Sonnet: current baseline, cost $0.003/1K tokens, accuracy on entity extraction
- Claude 3 Haiku: much cheaper ($0.00025/1K tokens), accuracy tradeoff, latency
- GPT-4 vs GPT-4 Mini: accuracy vs cost comparison
- Cohere API: model performance, cost ($0.0005/token), batching capabilities
- Llama 2/3 (local/hosted): setup cost, accuracy, inference latency
- Groq API: latency advantage, cost, model quality
- Mixtral via Together AI: cost efficiency, accuracy
- Comparison matrix: cost per extraction vs F1 score vs latency

**Where to Find Information**
- Official pricing pages: OpenAI, Anthropic, Cohere, Together AI
- Model cards and technical reports
- HuggingFace benchmark leaderboards
- Academic papers: entity extraction benchmarks (CoNLL, ACE datasets)
- Community benchmarks on GitHub (e.g., LLM cost comparison repos)

**Key Evaluation Criteria**
- F1 score on entity extraction (target 85%+)
- Latency: total time per batch of 10 entities (aim <2 seconds)
- Cost per 1,000 entities extracted
- Batch processing efficiency (can we send 10 entities at once?)
- Handling of domain-specific entities (papers, authors, venues, concepts)
- Confidence score reliability (do higher scores correlate with correctness?)
- Consistency: same entity gets same extraction twice

**What to Look For**
- Models that perform well on CoNLL and BiLSTM benchmarks
- API rate limits and burst capacity (we may extract 100K entities in a batch)
- Support for streaming responses (latency improvement)
- Fine-tuning options if accuracy gap emerges
- Cost per token vs fixed pricing vs usage-based

### Area 2: NER Libraries and Traditional ML

**What to Research**
- spaCy: pre-trained NER models, fine-tuning, speed
- Hugging Face transformers: DistilBERT, RoBERTa for NER
- Flair: multi-task learning NER models
- Stanford NER: rule-based and statistical approaches
- BERT-based custom fine-tuning: data requirements, training time
- Hybrid approaches: spaCy preprocessing + LLM validation
- Comparison matrix: accuracy vs latency vs resource usage

**Where to Find Information**
- spaCy documentation and model cards: spacy.io/models
- HuggingFace Model Hub: entity-extraction specific models
- Research papers: "State of NER 2024" benchmarks
- GitHub repos with benchmark comparisons
- Stack Overflow for production deployment patterns

**Key Evaluation Criteria**
- F1 score on domain-specific entities (academic papers, concepts)
- Speed: entities per second (aim for >100/sec on CPU)
- Memory footprint: can we run on 2GB RAM?
- Model size: can we ship with Docker image (<500MB)?
- Fine-tuning requirements: how much training data needed?
- Customization difficulty: can we teach it domain entities?
- Integration complexity with LLM-based approach

**What to Look For**
- Models trained on academic or research text
- Support for custom entity types
- Uncertainty/confidence scoring built-in
- Batch processing support
- Whether hybrid approach (spaCy + LLM) outperforms pure LLM

### Area 3: Entity Deduplication and Confidence Scoring

**What to Research**
- Fuzzy matching algorithms: Levenshtein, Jaro-Winkler for entity text
- Semantic similarity: embedding-based matching (SentenceTransformers)
- LLM-based deduplication: asking Claude "are these the same entity?"
- Deduplication thresholds: what score means "definitely same entity"?
- Confidence scoring: calibration, confidence bounds, risk estimation
- Entity merging strategies: which attributes to keep, conflict resolution
- Provenance tracking: which source each entity came from
- Deduplication accuracy benchmarks

**Where to Find Information**
- Entity resolution papers: "Similarity Joins in Databases" survey
- SentenceTransformers documentation and benchmarks
- Wikidata and DBpedia matching strategies
- Research papers: entity linking and coreference resolution
- Industry solutions: Talend, Informatica approaches (for reference)

**Key Evaluation Criteria**
- Precision: false positive rate (merging different entities) <1%
- Recall: false negative rate (not merging same entities) <5%
- Latency: deduplicate 1,000 entities in <1 second
- Cost: does semantic matching with embedding add significant cost?
- Quality: manual review of merged entities >95% correct
- Scalability: O(n) or O(n log n) complexity vs O(n²)
- Effectiveness: does it prevent duplicate nodes in graph?

**What to Look For**
- Whether fuzzy matching alone is sufficient (usually not)
- Embedding models optimized for entity/semantic matching
- Batch processing options to reduce latency
- Whether LLM-based deduplication is cost-effective
- Edge cases: different entity representations, abbreviations, acronyms

### Area 4: Human Review Workflow and Quality Gates

**What to Research**
- Confidence threshold strategy: which entities need human review
- Review interface design: what do reviewers need to see
- Review speed: time per entity, cost per review
- Appeal and correction workflow: how do corrections flow back
- Quality metrics: inter-rater agreement, correction rates
- Sampling strategy: which entities to always review vs random sampling
- Cost-benefit: human review cost vs error cost in graph

**Where to Find Information**
- Active learning papers: confidence-based sampling
- Human-in-the-loop ML research
- Industry practice: how content moderation at scale works
- Quality management standards (ISO 8601)
- UX research on review interfaces

**Key Evaluation Criteria**
- Review speed: >10 entities per minute per reviewer
- Accuracy: >99% agreement between reviewer and system
- Cost: <$0.01 per entity reviewed
- Scalability: can we handle 100K entities needing review per day?
- User experience: can we make review interface intuitive?
- Feedback loop: do corrections improve future extractions?

**What to Look For**
- Optimal confidence threshold for triggering review
- Whether automatic appeals can catch obvious false positives
- Cost to review vs cost of keeping bad entities
- Whether continuous learning from reviews improves accuracy

### Area 5: Benchmarking and Evaluation Datasets

**What to Research**
- Academic benchmarking datasets: CoNLL, ACE, BiLSTM
- Domain-specific entity extraction benchmarks
- Building custom benchmark dataset for our domain
- Test set creation: sampling strategy, annotation guidelines
- Evaluation metrics: precision, recall, F1, exact match, partial match
- Confidence calibration metrics: ECE, MCE, Brier score

**Where to Find Information**
- CoNLL shared task datasets
- Hugging Face datasets library
- SemEval entity extraction tasks
- Academic papers with public datasets
- Benchmark leaderboards: Papers with Code

**Key Evaluation Criteria**
- Dataset size: 500+ examples minimum for valid comparison
- Diversity: covers all entity types we extract
- Annotation quality: multiple annotators, IAA >0.85
- Representativeness: matches our production data distribution
- Public availability: can we publish results?

**What to Look For**
- Pre-existing academic benchmarks we can use
- Whether domain adaptation is needed
- Cost to create custom benchmark
- How to handle inter-annotator disagreement

## Research Methodology

### Phase 1: Provider Benchmarking (2 days)
- Select 5 LLM providers: Claude 3.5, Claude Haiku, GPT-4 Mini, Cohere, Llama 3
- Build unified evaluation API that can test any provider
- Create benchmark dataset: 200 text samples from academic papers
- Extract entities using each provider
- Measure: accuracy (F1), latency, cost, consistency
- Document confidence score distributions from each provider

### Phase 2: Traditional NER Libraries (1.5 days)
- Set up spaCy, Hugging Face transformer, Flair
- Fine-tune on 100 examples from our domain if time allows
- Run same 200-sample benchmark
- Compare to LLM baselines
- Evaluate hybrid approach: spaCy preprocessing + LLM validation
- Document accuracy/latency/cost for each

### Phase 3: Deduplication and Confidence (1.5 days)
- Implement fuzzy matching baseline (Jaro-Winkler)
- Implement semantic matching (SentenceTransformers)
- Test LLM-based deduplication on sample
- Run deduplication accuracy experiment with manual verification
- Calibrate confidence scoring: check if high-confidence extractions are actually correct
- Build confidence threshold curves for different review strategies

### Phase 4: Integration and Final Benchmarks (1 day)
- Build end-to-end extraction pipeline with best approach
- Test with 1,000 realistic entities
- Measure total latency: extraction + deduplication + confidence scoring
- Document cost breakdown by component
- Create cost vs accuracy pareto frontier
- Final recommendation with confidence level

### What Data to Collect
- F1 scores (precision and recall separately)
- Latency: extraction time, deduplication time, total time
- Cost per entity: base model cost + per-token cost
- Cost per query (assuming 50 entities per query)
- Confidence score distribution
- Deduplication: true positives, false positives, false negatives
- Human review accuracy on flagged entities
- Model consistency: same entity extracted identically
- Edge case coverage: abbreviations, multi-word entities, domain terms

### How to Compare Options
- Create cost vs accuracy matrix
- Run Pareto analysis: can we get 80% F1 for 50% cost?
- Calculate ROI: cost savings vs accuracy loss
- Model recommendation with confidence intervals
- Explicit tradeoff documentation
- Risk analysis for each top choice

### Documentation Requirements
- Benchmark results with 95% confidence intervals
- Latency breakdown: network, model inference, post-processing
- Cost analysis: per-token, per-extraction, per-query
- Accuracy by entity type (which types are hard?)
- Failure case analysis
- Lessons learned from benchmarking

## Evaluation Framework

### Scoring Categories (Total: 100 points)

**Accuracy (40 points)**
- F1 score 90%+: 40 points
- F1 score 85-89%: 30 points
- F1 score 80-84%: 20 points
- F1 score <80%: 10 points

**Cost Efficiency (35 points)**
- <$0.0008 per entity (save 73% vs Claude): 35 points
- $0.0008-$0.001 per entity: 28 points
- $0.001-$0.002 per entity: 20 points
- >$0.002 per entity: 10 points

**Performance (15 points)**
- <1 second for 50 entities: 15 points
- 1-3 seconds: 10 points
- 3-5 seconds: 7 points
- >5 seconds: 3 points

**Confidence Scoring Quality (10 points)**
- Confidence well-calibrated (ECE <5%): 10 points
- Reasonably calibrated (ECE <10%): 7 points
- Poorly calibrated (ECE >10%): 3 points

### Decision Threshold
- Score 85+: Recommend, move to implementation immediately
- Score 75-84: Strong candidate, document tradeoffs carefully
- Score <75: Consider secondary approach or hybrid strategy

### Recommendation Criteria
- MUST achieve 85%+ F1 score
- MUST have reliable confidence scoring
- MUST support batching for cost efficiency
- Total cost per query must be <$0.003 (current baseline)
- Must integrate with deduplication pipeline

## Deliverables

### Output Format

1. **Provider Benchmark Report** (CSV + analysis)
   - All 5 providers: F1 score, cost per entity, latency, consistency
   - Pareto frontier: best accuracy at each cost level
   - Cost breakdown: model + infrastructure + overhead

2. **Cost Comparison Matrix** (Table with scenarios)
   - 100K entities/day scenario: total daily cost for each provider
   - 1M entities/day scenario: cost at scale
   - Break-even analysis: when does cheaper model's lower accuracy hurt?

3. **Deduplication Benchmark** (Report)
   - Deduplication accuracy: precision, recall, F1
   - Cost of deduplication step
   - Recommendations for threshold settings
   - Confidence scoring quality metrics

4. **Technical Implementation Guide**
   - Which LLM provider to use and why
   - Batch processing strategy
   - Deduplication algorithm and thresholds
   - Confidence threshold policy
   - Human review triggers and workflow

5. **Risk Assessment**
   - If chosen model's accuracy drops 2%, what breaks?
   - Cost sensitivity: if volumes 10x, can we maintain cost?
   - Fallback strategy if primary LLM provider fails

### Who Needs This
- Backend team: implements entity extraction service
- Data quality team: sets up human review workflow
- Finance: understands cost implications
- Product: features that depend on extraction quality
- DevOps: infrastructure for LLM API calls and caching

### Decisions This Enables
- LLM provider selection for 12+ months
- Budget allocation for LLM costs
- Entity deduplication policy
- Human review threshold policy
- Scaling strategy for future volume increases

## Timeline

### Day 1: Setup and Initial Testing (1 day)
- Create unified evaluation API
- Build benchmark dataset (200 samples)
- Set up accounts for 5 LLM providers
- Initial testing: one extraction per provider
- Collect sample confidence scores

### Day 2: Provider Benchmarking (1 day)
- Run full benchmark: all 5 providers on 200 samples
- Collect latency and cost data
- Document confidence distributions
- Create cost vs accuracy matrix

### Days 3-4: NER Libraries and Hybrid Testing (1.5 days)
- Set up spaCy, Hugging Face, Flair
- Run benchmark on NER libraries
- Test hybrid approach (spaCy + LLM validation)
- Compare all approaches on same dataset

### Days 5-6: Deduplication and Final Analysis (1.5 days)
- Implement and benchmark deduplication approaches
- Test confidence scoring calibration
- Run end-to-end pipeline test with 1,000 entities
- Create final recommendation and risk assessment
- Document lessons learned

### Key Milestones
- End of Day 1: Evaluation framework ready, initial data flowing
- End of Day 2: Provider comparison complete, top 2 candidates identified
- End of Day 4: All approaches benchmarked, cost vs accuracy clear
- End of Day 6: Final recommendation delivered with confidence intervals

### Blocking Dependencies
- Track 01 must be complete (need query processing)
- Need access to LLM provider accounts (provision early)
- Benchmark dataset should be representative (use production samples)

### Quick Win Opportunities
- Use publicly available CoNLL dataset instead of building from scratch
- Start with Claude Haiku vs Cohere directly (biggest cost comparison)
- Leverage existing HuggingFace NER models (no training needed)
- Use SentenceTransformers off-the-shelf (already trained)

## Open Questions for Implementation

1. Should we cache extractions per-document to avoid re-extracting same entities?
2. How do we handle entity type ambiguity (is "Python" a language or a person)?
3. Can we batch requests to LLM API to reduce latency and cost?
4. Should we use local NER + LLM validation or pure LLM approach?
5. How do we handle entities that span multiple sentences or are implicit?
6. What's the acceptable gap between confidence score and actual accuracy?
7. How often should we re-benchmark as new models are released?
8. Should entity confidence be normalized 0-1 or domain-specific?
9. Can we use entity feedback from graph building to improve extraction?
10. What's our budget for entity extraction cost per month at production scale?

## Deep Research Generated

This research track generated the following deep-research infrastructure:

1. **entity-extraction-llm-benchmarking/** - LLM Provider Comparison for Entity Extraction
   - Location: `deep-research/entity-extraction-llm-benchmarking/`
   - Status: Pending
   - Research ID: RES-2025-ENTITY-LLM-001
   - Focus: Benchmark Claude 3.5, Haiku, GPT-4, Cohere, Llama for entity extraction with target 85%+ F1 and cost optimization

2. **entity-extraction-ner-deduplication/** - NER Libraries and Entity Deduplication
   - Location: `deep-research/entity-extraction-ner-deduplication/`
   - Status: Pending
   - Research ID: RES-2025-ENTITY-NER-001
   - Focus: Evaluate spaCy, Flair, HuggingFace NER models plus fuzzy/semantic/LLM deduplication strategies

