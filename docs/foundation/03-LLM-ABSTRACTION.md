# Knowledge Graph Lab: LLM Abstraction Strategy

**Version:** 1.0.0
**Created:** 2026-01-09
**Status:** Foundational (source of truth)

---

## Strategic Requirement

KGL must support multiple LLM providers without pipeline rewrites. The architecture separates "what we want the LLM to do" from "which LLM does it."

---

## Provider Tiers

### Tier 1: API Providers (Cloud)

| Provider | Models | Use Case | Cost Profile |
|----------|--------|----------|--------------|
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus | Primary reasoning, extraction | $$$ |
| **Google** | Gemini 1.5 Pro, Gemini 1.5 Flash | Development (free tier), fallback | $ |
| **OpenAI** | GPT-4o, GPT-4o-mini | Alternative, comparison | $$ |
| **DeepSeek** | DeepSeek V3 | High-volume extraction (96% F1, 95% cost reduction) | $ |

### Tier 2: Local Models

| Runtime | Models | Use Case |
|---------|--------|----------|
| **Ollama** | Llama 3.1, Mistral, Qwen | Offline, privacy, cost elimination |
| **llama.cpp** | GGUF models | Embedded, edge deployment |
| **vLLM** | Any HF model | Self-hosted production |

### Tier 3: Embedded SDKs

| SDK | Integration | Use Case |
|-----|-------------|----------|
| **Claude Code SDK** | Deep tool integration | Agent orchestration |
| **Gemini SDK** | Google ecosystem | AI Studio prototyping |

---

## Current State

**Prototype (mark-26-01):** Gemini API via `@google/genai`
- Free tier during development
- 3-stage pipeline (Research → Gap Analysis → Report)
- Exposes best practices for Google tooling

**Production target:** Abstraction layer that swaps providers

---

## Abstraction Layer Design

```typescript
interface LLMProvider {
  id: string;           // "anthropic", "google", "ollama"
  name: string;         // "Anthropic Claude"
  
  // Capabilities
  supportsStreaming: boolean;
  supportsTools: boolean;
  supportsVision: boolean;
  maxContextTokens: number;
  
  // Operations
  complete(request: CompletionRequest): Promise<CompletionResponse>;
  stream(request: CompletionRequest): AsyncIterable<StreamChunk>;
  
  // Cost tracking
  estimateCost(request: CompletionRequest): CostEstimate;
  getUsage(): UsageMetrics;
}

interface CompletionRequest {
  messages: Message[];
  systemPrompt?: string;
  temperature?: number;
  maxTokens?: number;
  tools?: ToolDefinition[];
  responseFormat?: "text" | "json";
}

interface CompletionResponse {
  content: string;
  toolCalls?: ToolCall[];
  usage: {
    inputTokens: number;
    outputTokens: number;
  };
  model: string;
  provider: string;
}
```

---

## Provider Configuration

```yaml
llm:
  default_provider: anthropic
  
  providers:
    anthropic:
      api_key: ${ANTHROPIC_API_KEY}
      model: claude-3-5-sonnet-20241022
      max_tokens: 4096
      
    google:
      api_key: ${GOOGLE_AI_KEY}
      model: gemini-1.5-pro
      max_tokens: 8192
      
    ollama:
      base_url: http://localhost:11434
      model: llama3.1:8b
      
    deepseek:
      api_key: ${DEEPSEEK_API_KEY}
      model: deepseek-chat
      
  routing:
    reasoning: anthropic      # Complex decisions
    extraction: deepseek      # High-volume entity extraction
    synthesis: anthropic      # Final output generation
    fallback: google          # When primary fails
```

---

## Task-Based Routing

Different pipeline stages have different requirements:

| Stage | Primary | Fallback | Rationale |
|-------|---------|----------|-----------|
| Query Understanding | Claude Haiku | Gemini Flash | Fast, cheap, reliable |
| Gap Detection | Claude Sonnet | Gemini Pro | Needs reasoning |
| Entity Extraction | DeepSeek V3 | Claude Haiku | Volume, cost |
| Relationship Extraction | spaCy → Claude | DeepSeek | Hybrid: rules first |
| Conflict Resolution | Claude Sonnet | GPT-4o | Complex judgment |
| Answer Synthesis | Claude Sonnet | Gemini Pro | Quality output |

---

## Migration Path

### Phase 1: Prototype (Current)

```
Gemini API directly → Single provider, no abstraction
```

**Status:** Working in mark-26-01

### Phase 2: Basic Abstraction

```
Provider Interface → Multiple providers, manual switching
```

**Implementation:**
1. Define `LLMProvider` interface
2. Implement Anthropic adapter
3. Implement Google adapter
4. Config-based provider selection

### Phase 3: Smart Routing

```
Router → Task-based routing, automatic fallback
```

**Implementation:**
1. Task-to-provider mapping
2. Automatic fallback on failure
3. Cost-based routing options

### Phase 4: Local + Cloud Hybrid

```
Router → Local for cheap/fast, Cloud for complex
```

**Implementation:**
1. Ollama adapter
2. Latency-aware routing
3. Privacy-aware routing (sensitive data local)

---

## Cost Management

### Per-Provider Pricing (Approximate, 2026-01)

| Provider | Model | Input (1M tok) | Output (1M tok) |
|----------|-------|----------------|-----------------|
| Anthropic | Claude 3.5 Sonnet | $3.00 | $15.00 |
| Anthropic | Claude 3 Haiku | $0.25 | $1.25 |
| Google | Gemini 1.5 Pro | $1.25 | $5.00 |
| Google | Gemini 1.5 Flash | $0.075 | $0.30 |
| OpenAI | GPT-4o | $2.50 | $10.00 |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 |
| DeepSeek | V3 | $0.14 | $0.28 |
| Ollama | Local | $0.00 | $0.00 |

### KGL Cost Targets (Per Query)

| Optimization Level | Cost Range | Strategy |
|-------------------|------------|----------|
| Unoptimized | $0.10 - $0.20 | All Claude Sonnet |
| Standard | $0.023 - $0.045 | Task routing |
| Optimized | $0.012 - $0.037 | DeepSeek extraction, local where possible |

---

## Fallback Strategy

```python
async def complete_with_fallback(request: CompletionRequest) -> CompletionResponse:
    providers = [
        get_provider(config.routing.get(request.task, config.default_provider)),
        get_provider(config.routing.fallback)
    ]
    
    for provider in providers:
        try:
            return await provider.complete(request)
        except (RateLimitError, ServiceUnavailableError) as e:
            log.warning(f"{provider.id} failed: {e}, trying fallback")
            continue
        except Exception as e:
            log.error(f"{provider.id} unexpected error: {e}")
            raise
    
    raise AllProvidersFailedError("No providers available")
```

---

## Testing Strategy

### Provider Parity Tests

Ensure all providers produce acceptable results for core tasks:

```python
@pytest.mark.parametrize("provider", ["anthropic", "google", "deepseek", "ollama"])
async def test_entity_extraction(provider):
    result = await extract_entities(
        text=STANDARD_TEST_TEXT,
        provider=get_provider(provider)
    )
    
    assert result.precision >= 0.85
    assert result.recall >= 0.80
    # Allow variation in exact entities found
```

### Cost Tracking Tests

```python
async def test_cost_estimation_accuracy():
    estimate = provider.estimate_cost(request)
    response = await provider.complete(request)
    actual = calculate_actual_cost(response.usage)
    
    # Estimate should be within 20% of actual
    assert abs(estimate - actual) / actual < 0.20
```

---

## Non-Negotiables

1. **No provider lock-in** — Must be able to switch with config change
2. **Graceful degradation** — Fallback always available
3. **Cost transparency** — Every call tracked and reported
4. **Consistent interface** — Same code works with any provider
5. **Local option** — Must support offline operation

---

## Related Documents

- [Architecture Principles](./01-ARCHITECTURE-PRINCIPLES.md) — Pipeline stages that use LLMs
- [Research Synthesis](../research/ai-pipeline/RESEARCH-SYNTHESIS.md) — Model recommendations per stage
- [Implementation Lineage](./04-IMPLEMENTATION-LINEAGE.md) — Current prototype state
