# Master Application Specification: Knowledge Graph Lab (KGL)

**Status**: Draft
**Version**: 1.0.0
**Date**: 2026-01-11
**Objective**: Define the comprehensive user experience, interface requirements, and functional scope for the Knowledge Graph Lab application, translating the architectural backend (Input/Output Gates, Reasoning Engine) into concrete user flows.

---

## 1. Executive Summary
The **Knowledge Graph Lab (KGL)** is an intelligent research platform that allows users to progressively explore complex domains. Unlike a standard search engine, it uses a **Two-Loop Architecture**:
1.  **Outer Loop (Reasoning Engine)**: Plans research, evaluates confidence, and decides strategy.
2.  **Inner Loop (Processing Pipeline)**: Executes specific research tasks (Ingest, Extract, Relate).

This application provides the interface for users to **Command**, **Observe**, and **Utilize** this machinery.

---

## 2. Core User Flows

### Flow 1: Onboarding & Identity (The "Secure Entry")
**Goal**: Establish trust, identity, and the security boundary (Input Gate).

1.  **Landing & Auth**:
    *   Standard Email/Oauth signup.
    *   **Identity Provisioning**: User is assigned a unique `ResearcherID`.
    *   **Schema Connection**: User selects their primary domain ontology (e.g., "Creator Economy", "Biotech", "Legal"). options loaded from the backend registry.

2.  **Input Gate Initialization**:
    *   *System Action*: The browser establishes a secure session with the **Input Gate**.
    *   *User Action*: Agree to "Research Ethics Protocol" (Terms).
    *   *Visuals*: A subtle "Secure Connection" indicator showing active Sanitation schemas (Zod validators) are loaded.

### Flow 2: Exploration Layer (Research Initiation)
**Goal**: Convert "Fuzzy Intent" into "Concrete Questions".

1.  **The "Request Lab" (Chat Interface)**:
    *   **Interface**: A conversational UI similar to ChatGPT/Claude but focused on *structuring* a request.
    *   **Interaction**:
        *   User: "I want to understand the landscape of creator grants." (Fuzzy)
        *   System (Exploration Agent): "Are you interested in a specific region, or global? Any specific creator niche?" (Refinement)
        *   User: "Global, gaming focus."
    *   **Crystallization**: The system displays a **"Research Brief"** card merging the conversation into a structured JSON object (Draft Intent).
    *   **Launch**: User clicks "Start Research Run".

### Flow 3: The Lab Console (Observation Deck)
**Goal**: Provide visibility into the "Reasoning Engine" without overwhelming the user.

1.  **Active Run Dashboard**:
    *   **State Monitor**: A visual status bar showing the current phase: `PLANNING` -> `GATHERING` -> `SYNTHESIZING` -> `VERIFYING`.
    *   **Confidence Gauge**: A real-time dial showing the system's "Confidence" in its current answer (0-100%).
    *   **Budget/Cost Meter**: Live tracking of "Compute/Tokens" used vs. Budget Cap.

2.  **The "Thought Stream" (Outer Loop Visibility)**:
    *   A scrolling log (collapsible) showing the Reasoning Engine's decisions:
        *   *“Confidence is low (40%). Deciding to branch search to 'European Grants'...”*
        *   *“Conflict detected between Source A and B. Triggering Verification Mixin...”*
    *   **Intervention**: User can click "PAUSE" to inject guidance manually if the agent goes off-track.

### Flow 4: Knowledge Vault & Reporting (Output Gate)
**Goal**: Utilize the generated knowledge.

1.  **The Knowledge Vault (Results View)**:
    *   **Grid/Graph View**: Switchable view of entities found (Grants, People, Orgs).
    *   **Filtering**: Faceted search based on the Ontology (e.g., Filter by `Amount > $10k`, `Deadline within 30 days`).
    *   **Date Range Filtering**: *Critical Feature*. "Show data gathered between [Date A] and [Date B]" to avoid stale reports.

2.  **Report Builder & Syndication**:
    *   **Selection**: User checks specific entities/insights to include.
    *   **Format Selection**: Choose output format:
        *   *PDF Report* (Executive Summary)
        *   *CSV Export* (Raw Data)
        *   *Newsletter Draft* (HTML)
    *   **Publishing Channel**: Select "Send to Email List", "Webhook", or "Download".
    *   **Syndication Rules**: "Automatically email me weekly updates matching this filter."

---

## 3. Interface Requirements

### 3.1 Input Gate (Frontend)
*   **Validation**: All text inputs must be validated client-side against Zod schemas *before* transmission.
*   **Sanitization**: No raw HTML allowed in inputs.
*   **Feedback**: Real-time validation errors (e.g., "Query too broad", "Invalid Date Format").

### 3.2 Reasoning Engine Visualization
*   **"Thinking" Animation**: Distinct visual state when the Outer Loop is evaluating (vs. just fetching data).
*   **Graph Widget**: A mini D3/Canvas interactive graph showing new nodes connecting in real-time.

### 3.3 Output Gate (Reporting)
*   **Report Preview**: Real-time rendering of what the PDF/Email will look like.
*   **History**: A list of all past "Research Runs" and generated reports.

---

## 4. Technical Architecture Alignment

| Frontend Component | Backend System | Data Exchange |
| :--- | :--- | :--- |
| **Request Lab** | **Exploration Layer** | WebSocket (Bidirectional Chat) |
| **Lab Console** | **Reasoning Engine** | SSE (Server-Sent Events) for State Updates |
| **Input Forms** | **Input Gate** | HTTPS (POST) with Strict Schema Validation |
| **Report Builder** | **Output Gate** | HTTPS (GET/POST) for Preview/Job Queuing |

---

## 5. Security & Safety
1.  **Prompt Injection**: The Frontend must *never* send raw instructions to an LLM. It sends *structured data* (JSON) to the Input Gate.
2.  **Auth**: All "Lab Console" sessions are protected by short-lived JWTs.
3.  **Audit**: Every "Research Run" is logged with a `RunID` visible in the UI for debugging.
