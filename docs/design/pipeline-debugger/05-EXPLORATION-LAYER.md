# Exploration Layer: Pre-Research Discovery

**Version:** 0.1.0  
**Created:** 2026-01-10  
**Status:** Design  
**Purpose:** Discover what users actually need before they know it themselves

---

## The Problem

People rarely know what they need to research until the idea hits them. Traditional search assumes you already know your question. But real research starts with vague intent: "I need to figure out..." or "Something's wrong with..." or "I wonder if..."

The Exploration Layer transforms fuzzy intent into concrete research questions.

---

## Architecture

```
User Arrives (vague intent)
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       EXPLORATION LAYER                                  │
│                                                                          │
│  ┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐   │
│  │ DIALOGUE  │────▶│   USER    │────▶│  CONTEXT  │────▶│CRYSTALLIZE│   │
│  │  ENGINE   │     │  PROFILE  │     │    MAP    │     │           │   │
│  │           │     │           │     │           │     │           │   │
│  │ Surface   │     │ Who they  │     │ Org,      │     │ Concrete  │   │
│  │ latent    │     │ are, how  │     │ stakes,   │     │ research  │   │
│  │ needs     │     │ they      │     │ politics  │     │ questions │   │
│  │           │     │ think     │     │           │     │           │   │
│  └───────────┘     └───────────┘     └───────────┘     └───────────┘   │
│       │                 │                  │                  │         │
│       │                 │                  │                  │         │
│       ▼                 ▼                  ▼                  ▼         │
│   Iterative         Parallel           Parallel         When Ready     │
│   (until ready)     (background)       (background)     (explicit)     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
   ResearchQuestion[]
         │
         ▼
   Research Pipeline
```

---

## Components

### 1. Dialogue Engine

**Purpose:** Surface latent needs through conversation

The Dialogue Engine uses Socratic questioning to help users discover what they actually need. It doesn't ask "what do you want to research?" It asks questions that reveal unstated assumptions, hidden constraints, and the real problem behind the presented problem.

**Conversation Patterns:**

| Pattern | Example | Purpose |
|---------|---------|---------|
| Opening | "What's on your mind?" | Low-pressure entry |
| Deepening | "What would change if you knew that?" | Reveal stakes |
| Reframing | "It sounds like the real question is..." | Surface hidden question |
| Constraint | "What would make an answer unusable?" | Find dealbreakers |
| Blocker | "What's stopping you from just deciding now?" | Identify missing info |

**Anti-Patterns to Avoid:**

- Jumping to solutions before understanding problem
- Accepting first framing without probing
- Asking closed questions that limit exploration
- Ignoring subtext or emotional cues

**Configuration:**

```yaml
dialogue:
  max_turns_before_crystallize: 10
  min_turns_before_crystallize: 2
  question_style: socratic  # socratic | direct | mixed
  patience_level: high      # low | medium | high
```

---

### 2. User Profile Builder

**Purpose:** Build psychological + factual model of the user

The Profile Builder constructs a model of who this user is, how they think, and what they need. This enables personalized research delivery.

**Profile Schema:**

```typescript
interface UserProfile {
  // Factual
  role: string;              // "Product Manager", "Engineer", "Executive"
  organization: string;
  domain_expertise: string[];
  
  // Psychological
  decision_style: "analytical" | "intuitive" | "consensus";
  learning_preference: "reading" | "visual" | "discussion";
  risk_tolerance: "low" | "medium" | "high";
  communication_style: "formal" | "casual" | "technical";
  
  // Inferred from dialogue
  stated_blockers: string[];
  inferred_blockers: string[];
  
  // Context
  stakeholders: string[];
  constraints: string[];
  success_criteria: string[];
}
```

**Inference Signals:**

| Signal | Inference |
|--------|-----------|
| "Just tell me what to do" | Intuitive decision style |
| "What are the tradeoffs?" | Analytical decision style |
| "What did the team decide?" | Consensus decision style |
| "I need to present this to..." | Stakeholder context needed |
| "We tried X before and..." | Historical constraint |

**Configuration:**

```yaml
profile:
  infer_from_dialogue: true
  inference_confidence_threshold: 0.7
  ask_for_confirmation: false  # Don't interrupt flow
  persist_across_sessions: true
```

---

### 3. Context Map

**Purpose:** Understand the organizational environment

Research doesn't happen in a vacuum. The Context Map captures the organizational reality: who cares about this, what constraints exist, what's the political landscape.

**Context Schema:**

```typescript
interface ContextMap {
  // Stakeholders
  stakeholders: Stakeholder[];
  
  // Constraints
  constraints: Constraint[];
  
  // Environment
  timeline: string;
  budget: string;
  decision_process: string;
  
  // Politics (often implicit)
  who_benefits_from_status_quo: string[];
  who_championing_change: string[];
  what_been_tried_before: string[];
  sensitive_topics: string[];
}

interface Stakeholder {
  name: string;
  role: string;
  influence: "decision_maker" | "influencer" | "affected";
  concerns: string[];
  relationship: "sponsor" | "ally" | "neutral" | "skeptic";
}

interface Constraint {
  type: "budget" | "time" | "resource" | "policy" | "technical";
  description: string;
  flexibility: "hard" | "soft" | "negotiable";
  owner: string;
}
```

**Configuration:**

```yaml
context:
  infer_stakeholders: true
  infer_constraints: true
  political_awareness: medium  # low | medium | high
  ask_about_history: true
```

---

### 4. Crystallize

**Purpose:** Transform fuzzy intent into concrete research questions

Crystallize is the final step before research begins. It takes everything learned from Dialogue, Profile, and Context, and produces specific, answerable research questions.

**Good Research Questions Are:**

| Property | Example |
|----------|---------|
| Specific | "What's the market size for X in region Y?" not "How big is the market?" |
| Bounded | "In the next 2 years" not "in the future" |
| Answerable | Can be answered with available sources |
| Actionable | Answer leads to a decision or action |

**Bad Research Questions:**

| Property | Example | Problem |
|----------|---------|---------|
| Vague | "Tell me about AI" | No clear scope |
| Unbounded | "Everything about competitors" | Infinite scope |
| Unanswerable | "Will this succeed?" | Crystal ball needed |
| Academic | "What's the theory of X?" | No action implied |

**Output Schema:**

```typescript
interface ResearchQuestion {
  question: string;
  type: "factual" | "comparison" | "recommendation" | "analysis";
  scope: {
    include: string[];
    exclude: string[];
    constraints: string[];
  };
  success_criteria: string[];
  priority: "high" | "medium" | "low";
  estimated_effort: "quick" | "moderate" | "deep";
}
```

**Configuration:**

```yaml
crystallize:
  min_questions: 1
  max_questions: 5
  require_user_confirmation: true
  decomposition_depth: 2  # How many levels to break down
  scope_strictness: medium  # loose | medium | strict
```

---

## Integration with Pipeline

The Exploration Layer outputs feed directly into the Research Pipeline:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       EXPLORATION LAYER                                  │
│  Dialogue → User Profile → Context Map → Crystallize                    │
└─────────────────────────────────────────────┬───────────────────────────┘
                                              │
                                              │ ResearchQuestion[]
                                              │ UserProfile
                                              │ ContextMap
                                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       REASONING ENGINE                                   │
│                              │                                           │
│              ┌───────────────┼───────────────┐                          │
│              ▼               ▼               ▼                          │
│          CONTINUE         OUTPUT           ASK                          │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      INNER LOOP                                  │   │
│  │  QUERY → GAPS → SEARCH → INGEST → EXTRACT → RELATE → KG → SYNTH │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

**How outputs are used:**

| Output | Used By | Purpose |
|--------|---------|---------|
| ResearchQuestion[] | L1:QUERY | Seeds initial query understanding |
| UserProfile | L8:SYNTH | Personalizes output format and depth |
| ContextMap | All stages | Informs relevance scoring |

---

## Configuration Reference

```yaml
exploration:
  enabled: true
  
  dialogue:
    max_turns_before_crystallize: 10
    min_turns_before_crystallize: 2
    question_style: socratic
    patience_level: high
  
  profile:
    infer_from_dialogue: true
    inference_confidence_threshold: 0.7
    ask_for_confirmation: false
    persist_across_sessions: true
  
  context:
    infer_stakeholders: true
    infer_constraints: true
    political_awareness: medium
    ask_about_history: true
  
  crystallize:
    min_questions: 1
    max_questions: 5
    require_user_confirmation: true
    decomposition_depth: 2
    scope_strictness: medium
```

---

## Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Question clarity score | How specific/bounded questions are | >0.8 |
| User confirmation rate | % of crystallized questions user approves | >90% |
| Research relevance | % of results user finds useful | >85% |
| Profile accuracy | Inferred traits match stated traits | >80% |
| Time to crystallize | Minutes from start to research questions | <5 min |
