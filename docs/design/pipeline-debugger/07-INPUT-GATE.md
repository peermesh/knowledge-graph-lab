# Input Gate: Security Boundary & Ingress Control

**Version:** 0.1.0  
**Created:** 2026-01-10  
**Status:** Design  
**Purpose:** Single flow-through point for all external input with validation, sanitization, and prompt injection prevention

---

## The Problem

External input is dangerous. Without a clear boundary:
- Prompt injection attacks can manipulate LLM behavior
- Malformed data causes downstream failures
- Debugging is impossible without centralized logging
- No single point to enforce security policies

**The Input Gate creates a "logic gap"** between untrusted external input and the trusted internal system. Everything must be converted to known data structures before entering the queue.

---

## Architecture

```
                    UNTRUSTED ZONE
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                     │
    │  API Requests      │  Webhooks           │
    │  User Input        │  File Uploads       │
    │  Chat Messages     │  External APIs      │
    │                    │                     │
    └────────────────────┼────────────────────┘
                         │
                         ▼
    ╔═══════════════════════════════════════════════════════════════╗
    ║                      INPUT GATE                                ║
    ║═══════════════════════════════════════════════════════════════║
    ║                                                                ║
    ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            ║
    ║  │  VALIDATE   │─▶│  SANITIZE   │─▶│  NORMALIZE  │            ║
    ║  │             │  │             │  │             │            ║
    ║  │ Schema      │  │ Injection   │  │ Known       │            ║
    ║  │ Type check  │  │ XSS/SQLi    │  │ Structures  │            ║
    ║  │ Bounds      │  │ Encoding    │  │ Enums       │            ║
    ║  └─────────────┘  └─────────────┘  └─────────────┘            ║
    ║         │                                  │                   ║
    ║         ▼                                  ▼                   ║
    ║  ┌─────────────┐                   ┌─────────────┐            ║
    ║  │    LOG      │                   │   QUEUE     │            ║
    ║  │             │                   │             │            ║
    ║  │ Full trace  │                   │ Only valid  │            ║
    ║  │ Before/after│                   │ normalized  │            ║
    ║  │ Decisions   │                   │ data enters │            ║
    ║  └─────────────┘                   └─────────────┘            ║
    ║                                          │                     ║
    ╚══════════════════════════════════════════╪═════════════════════╝
                                               │
                         ▼
                    TRUSTED ZONE
                    (Internal Systems)
```

---

## Components

### 1. Validator

**Purpose:** Verify input matches expected schema and constraints

```typescript
interface ValidatorConfig {
  schema_strict: boolean;        // Reject unknown fields
  max_depth: number;             // Nested object depth limit
  max_array_length: number;      // Array size limits
  type_coercion: boolean;        // Allow "123" → 123?
  null_handling: "reject" | "default" | "pass";
  max_string_length: number;
  max_total_size_bytes: number;
}
```

**Validation Rules:**

| Input Type | Validation |
|------------|------------|
| String | Length limits, character whitelist, encoding check |
| Number | Range bounds, integer vs float, NaN/Infinity rejection |
| Array | Length limit, item type validation |
| Object | Schema match, depth limit, required fields |
| File | Size limit, MIME type whitelist, magic byte verification |
| URL | Protocol whitelist (https), domain validation |

---

### 2. Sanitizer

**Purpose:** Remove or neutralize dangerous content

#### Prompt Injection Prevention

This is the critical security function. All text that will be passed to an LLM must be sanitized.

**Strategy: Convert to Known Data**

Instead of trying to filter "bad" prompts (impossible), we convert everything to structured data that has no prompt-like semantics.

```typescript
// WRONG: Passing raw user input to LLM
const response = await llm.complete(`
  Analyze this document: ${userInput}
`);

// RIGHT: Extract structured data first, pass only that
interface DocumentData {
  title: string;           // validated, max 200 chars
  content_hash: string;    // SHA256, not content itself
  word_count: number;      // computed, not user-provided
  detected_language: string; // from detector, enum
  entities: Entity[];      // extracted by our system
}

const docData = await inputGate.process(userInput);
// docData is now KNOWN DATA - no prompt injection possible
```

**Sanitization Layers:**

```python
class Sanitizer:
    def sanitize_for_llm(self, text: str) -> SanitizedText:
        # 1. Encoding normalization
        text = self.normalize_encoding(text)
        
        # 2. Control character removal
        text = self.remove_control_chars(text)
        
        # 3. Instruction delimiter detection
        if self.contains_instruction_patterns(text):
            raise PromptInjectionDetected(text)
        
        # 4. Length truncation
        text = self.truncate(text, max_length=self.config.max_llm_input)
        
        # 5. Wrap in data envelope
        return SanitizedText(
            content=text,
            sanitized_at=datetime.utcnow(),
            original_hash=sha256(text),
            safety_score=self.compute_safety_score(text)
        )
    
    def contains_instruction_patterns(self, text: str) -> bool:
        patterns = [
            r"ignore\s+(previous|above|all)\s+instructions",
            r"you\s+are\s+now\s+[a-z]+",
            r"system\s*:\s*",
            r"<\/?system>",
            r"\[INST\]",
            r"###\s*(instruction|system)",
        ]
        return any(re.search(p, text, re.IGNORECASE) for p in patterns)
```

---

### 3. Normalizer

**Purpose:** Convert sanitized input to known internal data structures

**The key insight:** After normalization, there is no "user input" - only typed, validated data structures that cannot be misinterpreted.

```typescript
// Input types the system accepts
type KnownInput = 
  | ResearchQuery
  | DocumentUpload
  | FeedbackSignal
  | ConfigurationUpdate
  | SubscriptionChange;

// Each has a strict schema
interface ResearchQuery {
  type: "research_query";
  query_text: string;         // sanitized
  constraints: QueryConstraint[];
  user_id: string;
  session_id: string;
  timestamp: Date;
  source: InputSource;
}
```

---

### 4. Logger

**Purpose:** Complete audit trail for debugging and security analysis

**Every input is logged with:**

```typescript
interface InputLog {
  log_id: string;
  timestamp: Date;
  source_ip: string;
  source_type: "api" | "webhook" | "upload" | "chat";
  user_id?: string;
  
  // Raw input (for debugging)
  raw_input_hash: string;      // SHA256, not content
  raw_input_size: number;
  raw_input_sample?: string;   // first 500 chars if safe
  
  // Processing
  validation_result: "pass" | "fail";
  validation_errors?: string[];
  sanitization_flags?: string[];
  normalization_result: "success" | "type_mismatch" | "schema_error";
  
  // Decision
  final_decision: "accept" | "reject" | "review";
  reject_reason?: string;
  processing_time_ms: number;
}
```

**Log Levels:**

| Level | What's Logged | Retention |
|-------|---------------|-----------|
| DEBUG | Full raw input (dev only) | 24 hours |
| INFO | Hashes, decisions, timing | 30 days |
| WARN | Validation failures, sanitization flags | 90 days |
| ERROR | Injection attempts, schema mismatches | 1 year |

---

### 5. Queue Interface

**Purpose:** Only validated, sanitized, normalized data enters the processing queue

```typescript
interface QueueEntry {
  entry_id: string;
  input_log_id: string;    // links to InputLog
  queued_at: Date;
  payload_type: string;
  payload: KnownInput;
  priority: "high" | "normal" | "low";
}
```

---

## Configuration Reference

```yaml
input_gate:
  enabled: true
  
  validator:
    schema_strict: true
    max_depth: 10
    max_array_length: 1000
    type_coercion: false
    null_handling: reject
    max_string_length: 100000
    max_total_size_bytes: 10485760
  
  sanitizer:
    detect_prompt_injection: true
    max_llm_input_length: 50000
    instruction_pattern_action: reject
    detect_query_injection: true
    escape_html: true
    normalize_unicode: true
    remove_control_chars: true
  
  normalizer:
    strict_type_detection: true
    unknown_type_action: reject
    enforce_enums: true
  
  logger:
    log_raw_input: false
    log_input_hash: true
    log_input_sample: true
    sample_max_length: 500
    retention_days:
      debug: 1
      info: 30
      warn: 90
      error: 365
  
  queue:
    max_queue_depth: 10000
    priority_levels: [high, normal, low]
    timeout_seconds: 300
```

---

## Security Guarantees

When the Input Gate is properly configured:

1. **No prompt injection:** LLM never sees raw user input, only KnownInput structures
2. **No query injection:** All database queries use parameterized inputs only
3. **No XSS:** All HTML output is escaped
4. **Complete audit trail:** Every input is logged with full processing history
5. **Single control point:** One place to enforce all input security policies
6. **Fail secure:** Unknown input types are rejected, not passed through
