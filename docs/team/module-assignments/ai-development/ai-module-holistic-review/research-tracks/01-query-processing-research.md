# RESEARCH TRACK 01: Query Processing

## Track Header

**Track Name**: Query Processing and Intent Detection
**Estimated Effort**: 3 days
**Priority**: MEDIUM
**Dependencies**: None (can start immediately)
**Success Criteria**:
- Determined best NLP approach for query parsing (LLM vs traditional NLP)
- Evaluated SpaCy, NLTK, and transformer-based options with benchmarks
- Built proof-of-concept parser for at least 3 common query types
- Documented latency and accuracy metrics
- Clear recommendation with tradeoff analysis

## Research Objectives

### Core Questions
- Can we parse and extract intent from user queries without LLM calls?
- Which NLP library best balances accuracy, speed, and learning curve?
- How do we handle complex, multi-part queries efficiently?
- What's the baseline accuracy we can achieve with traditional NLP?

### Why This Matters
Query processing is the entry point to the research orchestration system. Getting this right means:
- Reducing latency by avoiding unnecessary LLM calls
- Building a reliable, deterministic query parser before research tasks get complex
- Understanding when to use traditional NLP vs LLM-based approaches
- Setting performance baselines for the entire system

### What Decisions This Supports
- Architecture choice: pipeline design depends on parser complexity
- Performance targets: SLA for query processing latency
- API design: error handling strategy for malformed queries
- Integration approach: whether to use FastAPI validators or custom parsing

## Research Areas

### Area 1: Traditional NLP Libraries

**What to Research**
- SpaCy: dependency parsing, entity recognition, intent classification
- NLTK: tokenization, POS tagging, semantic role labeling
- TextBlob: sentiment analysis, noun phrase extraction
- Comparison matrix for each library

**Where to Find Information**
- Official documentation: spacy.io, nltk.org, textblob.readthedocs.io
- Benchmark papers: NLP comparison studies from 2023-2024
- GitHub examples: real-world query parsing implementations
- Stack Overflow: common patterns and pitfalls

**Key Evaluation Criteria**
- Installation complexity and dependencies
- Pre-trained model accuracy (English, domain-specific options)
- Parsing speed (milliseconds per query)
- Customization difficulty for domain-specific terms
- Community size and documentation quality
- License compatibility

**What to Look For**
- Ability to extract entities, intents, and relationships from natural language
- Support for nested queries ("find papers about ML that cite this paper")
- Error handling for malformed or ambiguous input
- Memory footprint and startup time
- Integration with API frameworks (FastAPI)

### Area 2: Transformer-Based and LLM Approaches

**What to Research**
- Hugging Face transformers for intent classification and NER
- Zero-shot classification capabilities
- Fine-tuning requirements and data needs
- LLM APIs: OpenAI, Anthropic, local models
- Cost comparison: per-token vs per-request pricing

**Where to Find Information**
- Hugging Face Model Hub: huggingface.co/models
- Paper research: "Few-shot Learning for Intent Detection" papers
- API documentation: OpenAI, Anthropic, LLaMA
- Benchmark datasets: SQuAD, GLUE, custom domain datasets

**Key Evaluation Criteria**
- Accuracy on test queries (aim for 90%+)
- Latency (ms per query, including model loading)
- Cost per query (important for high-volume scenarios)
- Ability to learn domain-specific terminology
- Handling of edge cases and ambiguous queries
- Reliability and rate limiting

**What to Look For**
- Performance on your specific domain (academic research queries)
- Whether fine-tuning improves accuracy significantly
- Batch processing capabilities
- Fallback options when model confidence is low
- Integration complexity with your system

### Area 3: API Frameworks and Validation

**What to Research**
- FastAPI request validation and error handling
- Pydantic models for query structure
- Type hints and automatic documentation
- Custom validators for domain-specific rules
- Rate limiting and request throttling strategies

**Where to Find Information**
- FastAPI documentation: fastapi.tiangolo.com
- Pydantic docs: docs.pydantic.dev
- REST API design guidelines
- Example implementations in GitHub

**Key Evaluation Criteria**
- Development speed with framework
- Automatic OpenAPI/Swagger documentation
- Error message clarity for invalid queries
- Performance overhead (< 5ms for validation)
- Testing support
- Deployment complexity

**What to Look For**
- How well the framework catches bad input early
- Whether you can create reusable validation rules
- API response format for errors (should guide users)
- Performance of validation layer at scale
- Learning curve for your team

## Research Methodology

### Phase 1: Literature Review (0.5 days)
- Read 5-10 recent papers on query intent detection
- Review benchmark datasets and evaluation metrics
- Document baseline accuracy numbers across approaches
- Create comparison matrix: accuracy vs latency vs cost

### Phase 2: Library Testing (1.5 days)
- Set up SpaCy, NLTK, and one transformer model in isolated environments
- Create 20-30 test queries covering different research scenarios
- Measure latency, accuracy, and resource usage
- Document installation and setup complexity
- Test with domain-specific terminology (papers, citations, graphs)

### Phase 3: API Design Testing (1 day)
- Build FastAPI endpoint with Pydantic validation
- Test with various malformed inputs
- Measure validation performance
- Document error handling strategy
- Create reference implementation for parser integration

### What Data to Collect
- Parsing accuracy (% correct intent detection)
- End-to-end latency per query
- Memory usage during inference
- Model loading time
- Cost per 1,000 queries (if using APIs)
- Installation time and dependency count
- Lines of code needed for integration

### How to Compare Options
- Create scoreboard with weighted criteria
- Run same 30 test queries through each approach
- Document tradeoffs explicitly (accuracy vs speed vs cost)
- Rate subjective factors: learning curve, maintainability, documentation

### Documentation Requirements
- Latency benchmarks with concrete numbers
- Accuracy on test set with breakdown by query type
- Resource requirements (memory, CPU, disk)
- Integration code examples
- Failure mode analysis (what breaks and when)

## Evaluation Framework

### Scoring Categories (Total: 100 points)

**Accuracy (40 points)**
- Intent detection: 90%+ = 15 points, 80-89% = 10 points, <80% = 5 points
- Entity extraction: 90%+ = 15 points, 80-89% = 10 points, <80% = 5 points
- Edge case handling: 10 points for clear error reporting

**Performance (25 points)**
- Latency <50ms per query: 15 points
- Latency 50-100ms: 10 points
- Latency >100ms: 5 points
- Memory <200MB: 10 points

**Integration & Maintainability (20 points)**
- Low dependencies and setup complexity: 10 points
- Clear documentation: 5 points
- Community support and activity: 5 points

**Cost (15 points)**
- Free/open-source: 15 points
- <$0.001 per query: 12 points
- <$0.01 per query: 8 points
- >$0.01 per query: 5 points

### Decision Threshold
- Score 75+: Recommend and move to implementation
- Score 60-74: Viable but has tradeoffs, document carefully
- Score <60: Not suitable, continue research

### Recommendation Criteria
- Must achieve 85%+ accuracy on test queries
- Must handle domain-specific terminology
- Must integrate cleanly with FastAPI
- Must have documented fallback for ambiguous queries

## Deliverables

### Output Format
1. **Comparison Matrix** (CSV/table)
   - Libraries/approaches vs evaluation criteria
   - Latency, accuracy, cost, learning curve scores
   - Clear winner identification

2. **Technical Report** (3-5 pages)
   - Summary of findings
   - Detailed analysis of top 3 options
   - Recommended approach with rationale
   - Risk assessment

3. **Proof of Concept** (GitHub branch)
   - Working FastAPI endpoint
   - Sample queries and responses
   - Performance benchmarks
   - README with setup instructions

4. **Decision Document**
   - Recommendation with confidence level
   - Known limitations and workarounds
   - Next steps for implementation
   - Open questions for Phase 2

### Who Needs This
- Backend team: implements the parser
- Research orchestration track: depends on parser API design
- System architect: affects overall latency budget
- DevOps: needs to understand resource requirements

### Decisions This Enables
- Choose tech stack for query processing
- Set latency SLAs for entire system
- Determine whether to use LLM for parsing (likely no)
- Design API contracts for parser integration

## Timeline

### Days 1-2: Research & Testing (1.5 days)
- Literature review and benchmark study
- Set up test environments for 3-4 candidates
- Run benchmark queries and collect metrics
- First pass analysis and scoring

### Days 2-3: POC & Documentation (1.5 days)
- Build working FastAPI endpoint
- Create comparison matrix with final scores
- Write technical report with recommendation
- Prepare decision document with rationale

### Key Milestones
- End of Day 1: Candidate list finalized, test queries ready
- End of Day 2: Performance data collected, initial recommendation
- End of Day 3: POC code pushed, decision document ready

### Blocking Dependencies
- None: this track is independent

### Quick Win Opportunities
- SpaCy is well-documented; test it first
- Start with simple intent detection before complex entity extraction
- Use existing benchmark datasets to avoid building test set from scratch
- FastAPI is mature; focus on parser logic, not framework learning

## Open Questions for Implementation

1. How do we handle queries that mix structured and natural language?
2. Should we support query reformulation for ambiguous input?
3. What's the fallback when confidence is <70%?
4. How do we version and update intent classifiers?
5. Do we need multi-language support initially?
