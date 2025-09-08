# AI & Ontology Single-Track PRD (80h)

**Project:** SaveTheCreators – Knowledge Graph & Ingest Gate  
**Owner:** Ontology/AI Intern (single track)  
**Timebox:** ~10 weeks × 8–10h/week ≈ 80h  
**Goal:** Deliver one simple, authoritative path from research notes → validated knowledge graph → queries for publishing/email/UI. No alternates.

---

## 1) Executive summary (the one true way)
- **Canonical store:** RDF graph (Jena/Fuseki) with **SHACL** validation gates.  
- **Interchange:** **JSON-LD delta packs** with provenance (URL + date + quote).  
- **Modeling:** Thin **OWL/RDFS core** (classes/relations) + **SKOS** schemes for enumerations (roles, mediums, org/platform/group types, revenue models, goals, factors, policy/opportunity types).  
- **Ingestion:** One microservice (**KG Gate**) that validates deltas with SHACL and writes to Fuseki.  
- **Research notes:** Human Markdown but **must embed** a fenced JSON/JSON-LD block (dual-channel).  
- **Reports:** Stored **SPARQL** queries provided by this track; publishing tool turns result tables into email/web.

**Non‑goals:** building scrapers, ER at scale, fancy UI. This track creates the **contracts, ontology, gate, and queries** that the other tracks depend on.

---

## 2) Scope
### In
1) **Ontology package**: `ontology/ce.ttl` (core classes/properties) + SKOS schemes (10 files) + `shapes.ttl`.  
2) **Context & contracts**: `context.jsonld`, JSON Schema for `ce:ResearchDelta` and `ce:OntologyDelta`.  
3) **KG Gate service**: `/ingest` (POST delta → SHACL → write), `/health`, static endpoints for `context.jsonld`, `shapes.ttl`, SKOS .ttl files.  
4) **Seed data**: 30–60 concept terms with definitions; 12 sample deltas (policies/opportunities/platforms).  
5) **Queries**: 2 stored SPARQL views usable by the publishing tool.  
6) **DevOps hooks**: Dockerfile + Compose service + CI validation script.

### Out
- Crawlers/harvesters, entity resolution, front-end application, email sending. (Other teams.)

---

## 3) Architecture & interfaces
```
[Research Notes (Markdown with JSON-LD block)]
          │
          ▼
      [KG Gate]
    - POST /ingest  (JSON-LD delta)
    - GET  /health
    - GET  /context.jsonld
    - GET  /schemas/shapes.ttl
    - GET  /vocabs/*.ttl
          │  (SHACL pass ⇒ write)
          ▼
   [Fuseki (Triplestore)]  ← mounted volume
          │
          ├── SPARQL endpoint (exposed via reverse proxy)
          └── Stored queries (this repo) used by Publishing & Website
```

### API contracts
- **POST /ingest**  
  Input: a single JSON object with `@type: "ce:ResearchDelta"` (or `ce:OntologyDelta`), arrays `entities[]`, `relations[]`, `evidence[]`.  
  Behavior: validate (JSON Schema → SHACL); on success write to graph and return `{status:"ok", triples_written, graph:"/graphs/<date>"}`. On failure: `{status:"fail", errors:[…]}`.

- **SPARQL**  
  Served by Fuseki (mounted). The Gate does **not** proxy SPARQL; ops reverse‑proxies it as `/sparql`.

- **Static**  
  `/context.jsonld`, `/schemas/shapes.ttl`, `/vocabs/*.ttl` for clients to reuse.

---

## 4) Data model (minimal but sufficient)
### Core classes (OWL/RDFS)
- `ce:Creator`, `ce:Organization` (with subclass `ce:SupportOrganization`), `ce:Group`, `ce:Platform`, `ce:Work`, `ce:Policy`, `ce:Opportunity`, `ce:Event`, `ce:Factor`, `ce:Goal`.

### Core properties
- Relations: `ce:creates`, `ce:usesPlatform`, `ce:distributesVia`, `ce:memberOf`, `ce:affiliatedWith`, `ce:receivesFundingFrom`, `ce:licensesUnder`, `ce:hasGoal`, `ce:affectedBy`, `ce:hasPolicy`, `ce:announces`, `ce:appliesIn`.
- Facet links to SKOS: `ce:hasRole`, `ce:hasMedium`, `ce:hasPlatformType`, `ce:hasOrgType`, `ce:hasGroupType`, `ce:hasRevenueModel`, `ce:hasGoalType`, `ce:hasFactorType`, `ce:policyType`, `ce:opportunityType`.
- Data props: `ce:displayName` (string), `ce:validFrom/ce:validTo` (xsd:date), `ce:confidence` (xsd:decimal), `dct:source` (IRI), `dct:date` (xsd:date).

### SKOS concept schemes (10)
- `CreatorRole`, `Medium`, `PlatformType`, `OrgType`, `GroupType`, `RevenueModel`, `GoalType`, `FactorType`, `PolicyType`, `OpportunityType`.

---

## 5) Validation (SHACL) — must pass to write
- **ConceptShape:** every `skos:Concept` must have `skos:prefLabel`, `skos:definition`, `skos:inScheme` (exactly 1). Polyhierarchy allowed; cycle check in CI.
- **CreatorShape:** ≥1 `ce:hasRole`; optional `ce:hasMedium`; if `ce:usesPlatform` then object is `ce:Platform`.
- **PlatformShape:** ≥1 `ce:hasPlatformType`.
- **WorkShape:** exactly 1 `ce:hasMedium`; if `ce:licensesUnder` then object is `ce:License`.
- **PolicyShape:** must have `ce:policyType` and `ce:appliesIn`; if attached to Platform via `ce:hasPolicy`, prefer statement annotations with `ce:validFrom`.
- **OpportunityShape:** must have `ce:opportunityType` and a deadline (`dct:date`), plus organizer link.

---

## 6) JSON-LD delta (contract)
- **Type:** `ce:ResearchDelta` (facts) or `ce:OntologyDelta` (new SKOS concepts).  
- **Required:** `generated_at`, `entities[]`, `relations[]`, `evidence[]` (every asserted field backed by a URL + exact quote).  
- **IDs:** instances under `https://savethecreators.org/id/{type}/{slug}`; concepts under `https://savethecreators.org/vocab/{Scheme}#Term`.

Small example (trimmed):
```json
{
  "@context": {"ce":"https://savethecreators.org/ce#","voc":"https://savethecreators.org/vocab/","skos":"http://www.w3.org/2004/02/skos/core#","dct":"http://purl.org/dc/terms/","schema":"https://schema.org/"},
  "@type":"ce:ResearchDelta",
  "generated_at":"2025-09-06T12:00:00Z",
  "entities":[
    {"@id":"https://savethecreators.org/id/platform/bandcamp","@type":"ce:Platform","schema:name":"Bandcamp","ce:hasPlatformType":["voc:PlatformType/Marketplace","voc:PlatformType/Distribution"]},
    {"@id":"https://savethecreators.org/id/policy/bandcamp-fees-2025","@type":"ce:Policy","skos:prefLabel":"Bandcamp Fee Schedule 2025","ce:policyType":"voc:PolicyType/FeeSchedule","dct:source":"https://example.com/fees","dct:date":"2025-08-30"}
  ],
  "relations":[{"s":"https://savethecreators.org/id/platform/bandcamp","p":"ce:hasPolicy","o":"https://savethecreators.org/id/policy/bandcamp-fees-2025","validFrom":"2025-08-30","confidence":0.94}],
  "evidence":[{"subject":"https://savethecreators.org/id/policy/bandcamp-fees-2025","predicate":"dct:source","url":"https://example.com/fees","quote":"Our standard fee is 10% ..."}]
}
```

---

## 7) Deliverables (this track)
- **/ontology/**  
  - `ce.ttl` (core), `shapes.ttl`, `context.jsonld`  
  - `creator_roles.ttl`, `media.ttl`, `platform_types.ttl`, `org_types.ttl`, `group_types.ttl`, `revenue_models.ttl`, `goal_types.ttl`, `factor_types.ttl`, `policy_types.ttl`, `opportunity_types.ttl` (each with `skos:inScheme`, definitions, top concepts)
- **/contracts/**  
  - `research_delta.schema.json`, `ontology_delta.schema.json`, `delta_example.json`
- **/services/kg-gate/**  
  - `Dockerfile`, `app.py` (FastAPI), `requirements.txt`, `ingest.py` (pySHACL + RDFLib/Jena write), `static/` (context + shapes + vocabs)
- **/queries/**  
  - `policy_changes_14d.sparql`, `open_opportunities_45d.sparql`
- **/ops/**  
  - `compose.yaml` snippet (Fuseki + kg-gate), `validate.sh` (riot + pyshacl + SPARQL cycle checks)

---

## 8) Interfaces to other teams
- **Docker/backend team**  
  - Mount Fuseki data volume; expose `/sparql` publicly via reverse proxy.  
  - Run `kg-gate` container at `/kg` with env vars: `FUSEKI_URL`, `FUSEKI_DATASET`, `WRITE_MODE=quads`.  
  - Healthcheck: GET `/health` → `{ok:true}`.

- **Publishing tool**  
  - Consume stored queries from `/queries/*.sparql`.  
  - Use `/sparql` to fetch tables; render to email/web. Include **query name + hash + list of `dct:source` URLs** in every email.

- **Website**  
  - Use the same `/sparql` for pages; optional: pull `context.jsonld` to enrich client-side JSON.

---

## 9) Week-by-week plan (~80h)
- **W1 (8h) – Reading & seed**: finalize core classes/properties; draft 10 seed roles & types; pick URI strategy; align with teams.
- **W2 (8h) – PRD & contracts**: lock this PRD; write JSON Schema; stub `delta_example.json`.
- **W3 (8h) – SKOS v0.1**: ship 10 scheme files with ~30–60 concepts + definitions; add CI (riot + SPARQL cycle check).
- **W4 (8h) – SHACL**: implement `shapes.ttl`; add pySHACL to `validate.sh`; break/green tests.
- **W5 (8h) – KG Gate skeleton**: FastAPI app, `/ingest`, JSON Schema validate, SHACL stub; healthcheck.
- **W6 (8h) – Fuseki write path**: N-Quads generation; transaction write; error handling; idempotency.
- **W7 (8h) – Provenance enforcement**: require evidence on every fact; reject if missing; log failure reasons.
- **W8 (8h) – Stored queries**: author 2 production queries; return CSV/JSON to publishing.
- **W9 (8h) – Seed dataset**: load 12 sample deltas (policy/opportunity/platform/creator); verify queries produce expected rows.
- **W10 (8h) – Polish & handoff**: docs, runbooks, Compose snippet, demo script, definition-of-done checklist.

---

## 10) Acceptance criteria (definition of done)
- **Validation:** All SKOS & instance data pass SHACL; cycle/dangling-parent ASK queries return false.  
- **Gate:** `/ingest` rejects malformed or evidence-free deltas with actionable errors; accepts valid ones; writes ≥ 500 triples/min locally.  
- **Queries:** both stored queries return results on seed dataset in < 1s locally.  
- **Contracts:** `context.jsonld`, schemas, examples published and used by tests.  
- **Ops:** `compose.yaml` runs Fuseki + kg-gate; healthchecks pass.  
- **Docs:** README with run command and 3-minute demo (curl ingest → SPARQL query → sample email JSON).

---

## 11) Risks & mitigations
- **Ambiguous labels:** enforce `skos:definition`; add `skos:hiddenLabel` for platform nicknames.  
- **LLM drift:** JSON Schema + SHACL gate + evidence requirement.  
- **Over‑modeling:** keep core tiny; push long tail to SKOS; defer reasoning.  
- **URI churn:** freeze URI patterns now; never reuse IRIs.

---

## 12) Repo layout (final)
```
/ontology/
  ce.ttl
  shapes.ttl
  context.jsonld
  creator_roles.ttl
  media.ttl
  platform_types.ttl
  org_types.ttl
  group_types.ttl
  revenue_models.ttl
  goal_types.ttl
  factor_types.ttl
  policy_types.ttl
  opportunity_types.ttl
/contracts/
  research_delta.schema.json
  ontology_delta.schema.json
  delta_example.json
/services/kg-gate/
  Dockerfile
  requirements.txt
  app.py
  ingest.py
  static/{context.jsonld,shapes.ttl,vocabs/*}
/queries/
  policy_changes_14d.sparql
  open_opportunities_45d.sparql
/ops/
  compose.yaml
  validate.sh
README.md
```

---

## 13) Hand‑off checklist
- All files present; `validate.sh` passes.  
- `docker compose up` starts Fuseki + kg-gate.  
- `curl -X POST /ingest` with `delta_example.json` → `{status:"ok"}`.  
- SPARQL queries produce expected rows.  
- Docs explain how publishing calls `/sparql` and maps rows → email/web.

