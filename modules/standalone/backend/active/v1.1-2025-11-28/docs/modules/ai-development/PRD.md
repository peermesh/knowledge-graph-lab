**Non-canonical during concept phase — authoritative conceptual PRDs live in .dev/peermesh-canvases/**

# AI Module PRD - MVP Version

## Module Owner: Developer 3

## Executive Summary  
Build a Python/FastAPI service that extracts entities from text. Start with mock responses, then integrate real AI in Phase 2. Total time: 100 hours.

## Goals (MVP)
1. Create API that accepts text and returns entities
2. Start with hardcoded mock responses
3. Add real entity extraction in Phase 2
4. Run in Docker container
5. Support Backend module's needs

## User Stories

### Phase 1 (Weeks 1-6): Mock Implementation
- As the Backend, I can send text and receive entity list
- As the Backend, I can get entity types (person, org, platform, grant)
- As the system, I return consistent mock data for testing
- As a developer, I can test without AI API costs

### Phase 2 (Weeks 7-10): Real AI Integration
- Add OpenAI API integration
- Implement actual entity extraction
- Add entity relationship detection
- Improve extraction accuracy

## Technical Requirements

### Stack
- Python 3.11
- FastAPI
- spaCy (for local NER)
- OpenAI API (Phase 2)
- Docker

### API Endpoints (Minimal)
```python
# 1. Extract entities from text
POST /api/extract
{
  "text": "YouTube announced a new $100M creator fund...",
  "source_id": 123
}
# Response:
{
  "entities": [
    {"name": "YouTube", "type": "platform", "confidence": 0.95},
    {"name": "creator fund", "type": "grant", "confidence": 0.87}
  ],
  "relationships": [
    {"from": "YouTube", "to": "creator fund", "type": "offers"}
  ]
}

# 2. Generate embeddings (optional for MVP)
POST /api/embed
{"text": "content to embed"}
# Response:
{"embedding": [0.1, 0.2, ...]}  # 384 dimensions

# 3. Summarize content
POST /api/summarize
{"text": "long article text..."}
# Response:
{"summary": "YouTube launches $100M creator fund..."}
```

## Implementation Plan

### Week 1-2: Setup
- [ ] Create Docker container
- [ ] Setup FastAPI project  
- [ ] Create mock response system
- [ ] Test with curl/Postman

### Week 3-4: Mock Logic
- [ ] Build entity type detector
- [ ] Create mock entity database
- [ ] Return varied mock responses
- [ ] Add confidence scores

### Week 5-6: Enhanced Mocks
- [ ] Add relationship extraction
- [ ] Implement summarization endpoint
- [ ] Create realistic test data
- [ ] Document API

### Week 7-8: Real AI Integration
- [ ] Integrate OpenAI API
- [ ] Use GPT for entity extraction
- [ ] Test with real content
- [ ] Handle API errors

### Week 9-10: Optimization
- [ ] Improve prompts
- [ ] Add caching
- [ ] Reduce API costs
- [ ] Performance testing

### Week 11-12: Demo Prep
- [ ] Integration testing
- [ ] Bug fixes
- [ ] Prepare demo examples

## Mock Implementation Strategy

### Phase 1: Pattern-Based Mocking
```python
# Simple pattern matching for mock responses
def mock_extract_entities(text):
    entities = []
    
    # Check for platform names
    if "youtube" in text.lower():
        entities.append({"name": "YouTube", "type": "platform"})
    if "tiktok" in text.lower():
        entities.append({"name": "TikTok", "type": "platform"})
    
    # Check for grant keywords
    if "fund" in text.lower() or "grant" in text.lower():
        entities.append({"name": "Creator Fund", "type": "grant"})
    
    # Add some randomness
    if random.random() > 0.5:
        entities.append({"name": "MrBeast", "type": "person"})
    
    return {"entities": entities}
```

### Phase 2: Real AI Prompts
```python
# OpenAI integration
def extract_entities_gpt(text):
    prompt = f"""
    Extract entities from this text about the creator economy.
    Categories: person, organization, platform, grant, program
    
    Text: {text}
    
    Return as JSON list with name, type, and confidence.
    """
    
    response = openai.complete(prompt)
    return json.loads(response)
```

## Success Criteria
- [ ] All 3 endpoints return data
- [ ] Mock responses in < 100ms
- [ ] Real AI responses in < 2s
- [ ] 80% entity extraction accuracy
- [ ] Runs with `docker run`

## Dependencies
- Backend Module: Sends content for processing
- No dependencies on other modules

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| AI API costs | Use mocks until Phase 2 |
| Extraction accuracy | Start simple, improve iteratively |
| API rate limits | Implement caching |
| Complex NLP | Use pre-built libraries |

## Resources Provided
1. FastAPI template
2. Mock entity database
3. OpenAI API examples
4. Docker configuration
5. Test dataset

## Example Code Structure
```
ai/
├── Dockerfile
├── requirements.txt
├── .env.example         # API keys
├── app/
│   ├── main.py         # FastAPI app
│   ├── routers/
│   │   └── extraction.py # Entity endpoints
│   ├── services/
│   │   ├── mock.py     # Mock responses
│   │   └── openai.py   # Real AI (Phase 2)
│   └── data/
│       └── entities.json # Mock entity DB
└── tests/
    └── test_extraction.py
```

## Getting Started
```bash
# Clone repo
git clone <repo>
cd modules/ai

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload

# Build Docker
docker build -t ai-module .

# Run Docker
docker run -p 8001:8001 ai-module

# Test
curl -X POST http://localhost:8001/api/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "YouTube creator fund announced"}'
```

## Configuration
```python
# .env file (Phase 2 only)
OPENAI_API_KEY=sk-...
USE_MOCK_MODE=true  # Set false for real AI
```

## Questions to Resolve
1. Which AI provider? (OpenAI for simplicity)
2. Entity categories needed? (Start with 5)
3. Confidence threshold? (0.7 default)

## Notes
- Start with mocks to save API costs
- Keep prompts simple and clear
- Focus on creator economy entities
- Ask for help with AI/NLP concepts