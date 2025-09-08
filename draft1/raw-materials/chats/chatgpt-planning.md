Skip to content
Chat history

You said:
I have half a day today to prepare for a launch meeting with four interns to create a project. They are developers working on a project identified as a knowledge graph lab. And I need to get your help in keeping track of my list of things to do today in order to make sure we get it all done. I need to get to the point where I have a schedule of events for them. The process is going to be 10 weeks. They get 10 hours each. We're going to break the project into four sections. And we need to have a ramp up where the first week they do research on what they're working on using deep research prompts in AI. And then the second week we're going to create the PDD and PRD documents to make sure that we are designing something correctly. And then the following weeks, I guess seven weeks, we're going to try to build our modules. And then at the end of last week, we're going to try to put it all together and have a demo day. And each module that these four interns are working on need to work independently as well so that if any one of the interns doesn't get their work done, each intern can still demo the work that they did. and their work will need to be significant and will somehow have to figure out how to balance the work so that nobody is doing too little or too much we have one intern who's going to be doing the systems including setting up a docker container and preparing the system to be deployed to a a remote server and setting up backend code and systems. We're going to have an AI guy who's going to be working on taking the research data and turning it into an ontology and taxonomy and then creating a database that can be used. We're going to have the third person working on the data the publishing tool so that there's a way to publish content to as many platforms as you can get done in that time, including an email where they will be emailing on an interval to a group of recipients and also creating posts that get posted to as many social media locations as well as possibly a centralized tool for for publishing to the project's homepage. And then the fourth intern will be working on the front end, which will include the user interface for somebody to sign up And for them to decide what they, from a given list of things, what they want to be able to produce or what they, what their interests are. And we're going to have, that'll be a like static list of things to choose from. Plus a way to submit new ideas for the research agent to get data for, and then we're going to have some sort of exploratory mode for the project knowledge vault. and you probably want to have some sort of permissions thing so that different parts of the vault can be available or not available and a way to define your email and the interval that you want to receive emails and a way to be removed from the subscription list which obviously will all integrate with the other people's work so and then the biggest problem is there's these shared dependencies that each one of them will need as soon as possible like the database that they're storing data to which maybe we have to create synthetic data for initially and and then a authorization login solution and a few other things. My feeling is we could use Supabase, the open source version locally in the Docker container, but maybe to begin, we could use the free version. And that's the start. That's the first brain dump from me. 
ChatGPT said:

Thought for 1m 5s
Got it. Here’s a tight, meeting-ready plan you can execute today plus the full 10-week structure, module boundaries, and concrete hand-offs.

Today’s 4-Hour Prep Sprint (use as a live checklist)
 T+0:00–0:30 — Lock scope & roles

Confirm 4 modules (Systems, AI/Ontology, Publishing, Frontend) and primary assignees.

Freeze week-by-week cadence (below) and non-goals (limit v1 connectors, keep ontology minimal).

 T+0:30–1:15 — Define shared contracts & DB schema

Approve the JSON contracts + tables in “Shared Data Contracts” and “Core DB Schema Sketch” below.

Generate a small synthetic dataset (see “Seed Data”).

 T+1:15–2:00 — Repo + env

Create monorepo, enable Supabase (free) for Week 1–3, plan Dockerized self-host by Week 4.

Issue labels & milestone skeleton (W1–W10). Create stub services and CI on push.

 T+2:00–2:45 — Draft PRD/PDD templates & Week-1 prompts

Drop the PRD/PDD templates (below) into /docs/.

Paste Week-1 deep-research prompts into /research/.

 T+2:45–3:30 — Finalize meeting agenda & assignments

Map per-intern deliverables for Week 1–2; set acceptance criteria.

 T+3:30–4:00 — Comms & logistics

Share Notion “Interns Hub,” Discord channel, and calendar blocks; post the repo link and milestones.

(If helpful, say “set a 2-hour check-in reminder” and I’ll schedule one.)

10-Week Program (80 hours / intern)
W1 Research (10h): Deep research + competitive scan; capture sources; propose approach.

W2 PDD + PRD (10h): Problem Definition Doc + Product Requirements Doc; finalize milestones; commit to API contracts.

W3–W9 Build (70h): Implement module to MVP, then iterate; weekly demo every Friday.

W10 Integration + Demo (10h): Merge, fix seams, run end-to-end demo; write “What worked / Next” memo.

Modules, Responsibilities, and “Definition of Done”
1) Systems / DevOps
Scope: Monorepo, Docker, local/dev/prod envs, Supabase, CI/CD, secrets, observability.
DoD: docker compose up brings: Postgres (or Supabase local by W4), API, worker, web; seeded data; CI runs tests and type-check; one-command deploy to a remote host.

2) AI / Ontology / KG
Scope: Minimal creator-domain ontology (SKOS-style), ETL from research → normalized entities, JSON-LD export, R/W CRUD via API, basic semantic queries.
DoD: Schema + RLS policies in DB; /api/entities, /api/relations, /api/search?q= live; import/export round-trip; 200+ entities/relations seeded; unit tests for validators.

3) Publishing Tool (Email + 2 social connectors + Homepage)
Scope: Unified “Publisher” interface; job queue; scheduling; email blast; 2 social connectors; write-to-homepage (file or CMS).
DoD: Can schedule & send a test campaign to a sandbox list; dry-run preview; successful post to 2 networks; audit log per job.

4) Frontend (Web UI)
Scope: Sign-up/login (Supabase Auth), interests picker (static list), idea submission to research queue, vault explorer (read-only), email prefs (interval, unsubscribe), basic RBAC.
DoD: User can register/login, pick interests, submit ideas, browse entities, set email frequency, unsubscribe, and view publishing history.

Architecture (minimal, testable seams)
flowchart LR
  FE[Next.js frontend] -- Supabase Auth/JWT --> API[Node/TS Graph API]
  API <---> DB[(Postgres / Supabase)]
  API <--Publisher jobs--> WORKER[Node worker (cron/queue)]
  WORKER --> Email[SMTP/MailHog→Prod SMTP]
  WORKER --> Social[Connectors: Bluesky, Mastodon]
  WORKER --> Home[Homepage writer (repo or CMS)]
Tech choices locked for v1:

Monorepo: pnpm + Turborepo (or plain pnpm workspaces).

API/Worker: Node 20 + TypeScript + Fastify (fast, typed) or Express.

DB: Supabase (free) W1–W3; self-host Supabase in Docker from W4.

Auth: Supabase Auth (email magic link).

Email dev: MailHog in Docker; prod via SMTP (Postmark/Mailgun later).

Social: Start with Bluesky (ATProto) and Mastodon (ActivityPub); add X later if time.

Queue/scheduler: node-cron + DB-backed job table (keeps infra simple).

Shared Data Contracts (freeze these today)
TypeScript shapes the whole team codes against.

// Core knowledge graph
export type Entity = {
  id: string;                // uuid
  kind: "Creator" | "Org" | "Platform" | "Concept";
  name: string;
  slug: string;
  summary?: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, unknown>; // JSONB
};

export type Relation = {
  id: string;
  srcId: string;
  dstId: string;
  type:
    | "USES"
    | "MEMBER_OF"
    | "BUILDS_ON"
    | "BELONGS_TO"
    | "AFFILIATED_WITH";
  note?: string;
  createdAt: string;
};

export type Source = {
  id: string;
  url: string;
  title?: string;
  quoted?: string;
  addedAt: string;
};

export type EntitySource = { entityId: string; sourceId: string };

// Publishing
export type PublicationTarget =
  | { type: "email"; listId: string }
  | { type: "bluesky"; handle: string }
  | { type: "mastodon"; server: string; handle: string }
  | { type: "homepage"; path: string };

export type ContentItem = {
  id: string;
  title?: string;
  bodyMarkdown: string;
  tags?: string[];
  createdByUserId: string;
  createdAt: string;
  // optional binding to KG item to drive content
  entityId?: string;
};

export type PublicationJob = {
  id: string;
  contentId: string;
  target: PublicationTarget;
  status: "queued" | "running" | "ok" | "error";
  runAt: string; // ISO
  result?: Record<string, unknown>;
  createdAt: string;
};

// Frontend user prefs
export type SubscriptionPreference = {
  userId: string;
  interval: "daily" | "weekly" | "monthly" | "never";
  topics: string[]; // slugs from a static catalog
  emailVerified: boolean;
};

export type IdeaSubmission = {
  id: string;
  userId: string;
  title: string;
  description: string;
  createdAt: string;
  status: "new" | "triaged" | "queued" | "researching" | "closed";
};
Core DB Schema Sketch (Postgres / Supabase)
entities(id uuid pk, kind text, name text, slug text unique, summary text, metadata jsonb, created_at, updated_at)

relations(id uuid pk, src_id uuid fk->entities, dst_id uuid fk->entities, type text, note text, created_at)

sources(id uuid pk, url text, title text, quoted text, added_at)

entity_sources(entity_id uuid fk, source_id uuid fk, primary key (entity_id, source_id))

content(id uuid pk, title text, body_md text, tags text[], created_by uuid, entity_id uuid fk, created_at)

publication_jobs(id uuid pk, content_id uuid fk, target jsonb, status text, run_at timestamptz, result jsonb, created_at)

subscription_prefs(user_id uuid pk, interval text, topics text[], email_verified boolean)

idea_submissions(id uuid pk, user_id uuid, title text, description text, status text, created_at)

RLS: enable on all tables; policies for owner-write, authenticated-read where appropriate.

Minimal REST Endpoints
GET /api/entities?kind=&q=; POST /api/entities; GET /api/entities/:id; POST /api/relations

POST /api/content; POST /api/publish/preview; POST /api/publish/schedule

GET /api/jobs?status=; POST /api/prefs; POST /api/ideas

Balanced Weekly Milestones (per module)
W1 (Research)

Systems: compare Supabase free vs local, Docker layout, target host options; pick logging/metrics.

AI: survey creator ontologies; define minimal SKOS concept set; test JSON-LD framing.

Publishing: pick 2 socials (Bluesky, Mastodon); read APIs; define Publisher interface.

Frontend: audit needs; wireframe 5 screens; choose component lib.

W2 (PDD/PRD)

Systems: PDD+PRD for platform; compose file v0; CI plan.

AI: PDD+PRD; initial ERD; validation rules; import/export plan.

Publishing: PDD+PRD; connector spec; scheduling plan; email pipeline.

Frontend: PDD+PRD; routes, auth flows, error states; accessibility baseline.

W3

Systems: Monorepo + CI green; Supabase bound; seed script.

AI: Tables + RLS; seed 200/400 (entities/relations); CRUD endpoints.

Publishing: Content model + preview render; job table + cron worker runs dry-job.

Frontend: Auth working; interests page (reads static catalog).

W4

Systems: Dockerize all; MailHog; env switching; remote deploy (staging).

AI: Search endpoint; JSON-LD export; import from seed JSON.

Publishing: Email preview & send to MailHog; provider adapter interface done.

Frontend: Idea submission flow → idea_submissions.

W5

Systems: Self-host Supabase (optional) or keep free; metrics.

AI: Relation editor POST; simple ranking/search.

Publishing: Bluesky post live; audit logs.

Frontend: Vault explorer (entity list/detail).

W6

Systems: Backups & migrations flow.

AI: Source attachments & citations.

Publishing: Mastodon post live; schedule UI minimal.

Frontend: Email prefs (intervals) + unsubscribe endpoint hooked.

W7

Systems: Hardening; rate limits.

AI: ETL from research JSON → DB; validation tests.

Publishing: Homepage writer (writes Markdown file or Supabase Storage).

Frontend: Content preview page.

W8

Systems: Staging→Prod pipeline.

AI: Query presets (by topic/kind).

Publishing: Retry/backoff & idempotency.

Frontend: Basic RBAC (viewer/admin for vault edit).

W9

Systems: Load test + observability review.

AI: Polishing & doc.

Publishing: Content pack run-through (email + 2 socials + homepage).

Frontend: UX polish, empty states, docs.

W10

All: Integration, smoke tests, demo script, postmortem & next steps.

Launch Meeting (60–75 min) — Agenda & Script
Open (5): Names/roles, constraints (10 weeks, 10 h/wk, weekly demos).

Vision (7): “Knowledge Graph Lab: creator-domain KG + publishing loop; independent modules, shared contracts.”

Architecture (10): Walk the mermaid diagram; confirm tech.

Contracts (10): Review the TypeScript shapes and DB tables; freeze for W1–W2.

Assignments (15): Per-intern deliverables for W1–W2; acceptance criteria.

Milestones (5): Fridays = demo; Mondays = plan; PRD due end of W2.

Risks & Mitigations (5): See below.

Q&A (10): Capture blockers; turn them into Issues.

Next steps (3): Everyone creates 3 issues, picks 1 W1 target, confirms hours this week.

Non-Goals (prevent scope creep)
No third social network until both Bluesky + Mastodon pass E2E.

No vector search or embeddings in v1 (store room for it; ship later).

No custom auth; stick to Supabase Auth.

No multi-tenant complexity; single project env.

Risk Register (top 6) + Mitigations
Shared contracts drift → Freeze TS types + ERD today; contract tests in CI.

API lag blocks others → AI team provides stub endpoints + Postman collection by W2.

Email/provider credentials → Use sandbox (MailHog), then limited prod creds.

Over-broad ontology → Minimal SKOS; max 4 root kinds; 200/400 target this cycle.

Scheduling complexity → Simple cron + DB queue; no external brokers in v1.

Time bleed in design → Wireframes ≤ W1 only; ship functional over pretty.

Seed Data (synthetic)
Create 50 creators, 40 orgs, 30 platforms, 80 concepts; ~400 relations. Keep 5–10 representative fields per entity. Save as /seeds/kg.seed.json and /seeds/content.seed.json.

PRD & PDD Templates (drop into /docs/)
PDD.md (Problem Definition)

Problem Statement • Users/Stakeholders • Success Criteria (quant + qual) • Constraints/Assumptions • Out of Scope • Risks

PRD.md (Product Requirements)

Overview • Goals/Non-Goals • User Stories • Functional Reqs • Data Model & Contracts (link to TS) • API Endpoints • States & Errors • Security & Privacy • Telemetry • Milestones • Acceptance Tests

Minimal Git/Monorepo Bootstrap (optional)
You prefer contiguous bash with no comments; this creates the skeleton ready for the interns.

mkdir kgl && cd kgl
git init
pnpm init
pnpm dlx create-next-app@latest apps/web --ts --eslint --src-dir --app --use-pnpm --no-tailwind
mkdir -p apps/api apps/worker packages/shared docs seeds .github/workflows
pnpm add -w typescript ts-node zod
pnpm add -w -D turbo eslint prettier
printf '{\n  "name":"kgl","private":true,"packageManager":"pnpm@9","workspaces":["apps/*","packages/*"]\n}\n' > package.json
printf 'module.exports = {\n  pipeline: { "build": {}, "dev": {} }\n}\n' > turbo.config.js
printf '{\n  "compilerOptions": { "target":"ES2022","module":"ESNext","moduleResolution":"Bundler","strict":true,"esModuleInterop":true,"skipLibCheck":true,"forceConsistentCasingInFileNames":true },\n  "exclude":["node_modules"]\n}\n' > tsconfig.json
printf 'export * from "./types";\n' > packages/shared/index.ts
printf 'import Fastify from "fastify";\nconst app = Fastify();\napp.get("/health", async () => ({ ok: true }));\napp.listen({ port: 3001 });\n' > apps/api/index.ts
printf 'import cron from "node-cron";\ncron.schedule("*/5 * * * *", () => { console.log("tick"); });\n' > apps/worker/index.ts
git add .
git commit -m "chore: init KGL monorepo skeleton"
Week-1 Deep-Research Prompts (paste into /research/)
AI/Ontology: “Survey current creator-domain ontologies and SKOS vocabularies; extract reusable classes/relations; return a 1-page minimal SKOS with 4 root kinds and ≤20 properties; include 5 concrete examples with sources.”

Publishing: “For Bluesky and Mastodon, list endpoints, auth flows, rate limits, and post payload shapes; produce a ‘Publisher’ interface and two adapter stubs.”

Systems: “Compare Supabase free vs self-host; outline Docker compose for API/Worker/Web/DB/MailHog; list prod deploy options and costs.”

Frontend: “Wireframe five screens (Auth, Interests, Idea Submit, Vault Explorer, Email Prefs); identify required API calls and error states.”

Per-Intern Week-2 Acceptance Criteria (PRD due)
Systems: Compose v1, .env.example, staging deploy, CI green.

AI: Entities/Relations tables + RLS; POST /entities validator; JSON-LD export stub.

Publishing: Email preview → MailHog; POST /publish/preview returns rendered HTML.

Frontend: Auth + session; Interests read/write to subscription_prefs.

Demo Day (W10) Script (5–7 min per intern)
Problem → Design → Live demo → API/contract artifacts → Next steps. Each demo runs without other modules (independent) plus one end-to-end flow together.

Your “Today” To-Do List (copy/paste and tick off)
 Approve tech choices and non-goals.

 Approve data contracts and DB tables.

 Create monorepo and push to GitHub.

 Create milestones W1–W10 and label set.

 Add PRD/PDD templates and research prompts to repo.

 Spin up Supabase (free) and MailHog (dev) or note for W4 self-host.

 Draft and send meeting agenda + links (Notion Hub, Discord, Repo).

 Pre-assign Week-1 deliverables and acceptance criteria per intern.

If you want, say “convert this to GitHub issues,” and I’ll output an issue list ready to paste into the tracker.

You said:
my feeling is we have to define the project and the manageable scope like you're proposing and make sure it makes sense and then we have to break that into those four buckets I kind of gave you an outline of what I think each one of them is but essentially one guy wants to work on web stuff and one guy wants to work on a publishing tool and one guy wants to focus on AI and one guy wants to work on systems engineering on the back end. So it seems like a good balance. 
ChatGPT said:

Thought for 28s
Agreed. Here’s the frozen scope and clean four-bucket split with concrete MVPs, interfaces, and a tight schedule you can hand to the interns.

Project Definition (frozen for this cycle)
Goal: Stand up a minimal “Knowledge Graph Lab” that (a) ingests researched entities/relations into a Postgres/Supabase schema, (b) surfaces them via a typed REST API, (c) lets users sign up, pick interests, and submit research ideas, and (d) publishes periodic content (email + two socials) derived from the graph.
Constraint: 10 weeks, 10 h/wk per intern; each module demos independently + an end-to-end demo in Week 10.

Out of Scope (v1)
No vector search/embeddings, no third social network, no multi-tenant accounts, no custom auth, no heavy RBAC beyond “viewer/admin”.

Shared Platform (locked)
Repo: monorepo (pnpm workspaces).

API/Worker: Node 20 + TypeScript + Fastify/Express.

DB/Auth: Supabase (hosted W1–W3; optional Docker self-host starting W4).

Email: MailHog in dev; single SMTP in prod.

Social: Bluesky (ATProto) + Mastodon (ActivityPub) only.

Queue/Scheduler: DB table + node-cron.

Front-end: Next.js 14 (App Router), Supabase Auth UI.

Cross-Module Contracts (freeze)
Minimal tables and endpoint shapes (these are the seams everyone codes against):

Tables

entities(id, kind, name, slug, summary, metadata jsonb, created_at, updated_at)

relations(id, src_id, dst_id, type, note, created_at)

sources(id, url, title, quoted, added_at) + entity_sources(entity_id, source_id)

content(id, title, body_md, tags[], created_by, entity_id, created_at)

publication_jobs(id, content_id, target jsonb, status, run_at, result jsonb, created_at)

subscription_prefs(user_id, interval, topics[], email_verified)

idea_submissions(id, user_id, title, description, status, created_at)

Endpoints

KG: GET /api/entities?kind=&q=, POST /api/entities, GET /api/entities/:id, POST /api/relations

Content/Publish: POST /api/content, POST /api/publish/preview, POST /api/publish/schedule, GET /api/jobs?status=

User: POST /api/prefs, POST /api/ideas
All responses JSON; auth via Supabase JWT; RLS on.

The Four Buckets (assign one intern each)
1) Systems / DevOps (Backend platform)
MVP

docker compose up brings DB (or Supabase local by W4), API, worker, web, MailHog.

CI runs type-check/tests; .env.example complete; staging deploy script works.

Observability: request logs + basic health checks.

Deliverables

Compose + env switch; one-command deploy to a remote host.

Supabase project (hosted) with schema migrations; optional local self-host by W4.

Independent demo: Live compose run + staging URL + green CI; seed script populates DB.

Dependencies: none (platform first).

2) AI / Ontology / Knowledge Graph
MVP

Minimal SKOS-style model with 4 kinds: Creator|Org|Platform|Concept.

CRUD endpoints live; JSON-LD export; import from research JSON.

Seed 200+ entities / 400+ relations with citations in sources.

Deliverables

Validated POSTs (zod), RLS policies, simple search by kind|q.

ETL script: /research/json → /api/entities|/api/relations.

Independent demo: Import a seed file, query entities, show JSON-LD export.

Dependencies: Systems (DB/API up).

3) Publishing Tool (Email + 2 socials + Homepage)
MVP

Unified “Publisher” interface; job queue with queued|running|ok|error.

Email: preview + send to MailHog; Bluesky + Mastodon adapters post basic text.

Homepage writer: write Markdown/JSON artifact to a path or storage bucket.

Deliverables

Scheduling: runAt ISO + cron tick; idempotent retries; audit log per job.

Independent demo: Queue a content item; watch email + two social posts succeed.

Dependencies: Systems (worker+queue), optional KG (for content binding).

4) Frontend (Web UI)
MVP

Sign-up/login (Supabase Auth), interests picker (static catalog), idea submission.

Vault explorer: read-only browse by kind, entity detail.

Email prefs (daily/weekly/monthly/never) + unsubscribe.

Deliverables

Minimal admin view toggle; error/empty states; accessibility baseline.

Independent demo: New user journey end-to-end without publishing/KG reliance (use seed content).

Dependencies: Systems (auth), optional KG (for explorer).

Workload Balance (target hours, inclusive of testing/docs)
Systems: 18–22h core + 8–10h polish = ~28–32h

AI/KG: 20–24h core + 8–10h polish = ~30–34h

Publishing: 18–22h core + 8–10h polish = ~28–32h

Frontend: 20–24h core + 8–10h polish = ~30–34h
Buffer remains for integration/bugs within 80h each.

10-Week Cadence (fixed)
W1 Research/choices (Deep research prompts).

W2 PDD + PRD; freeze endpoints & schema; seeds ready.

W3–W9 Build; Friday demos; Monday plan updates.

W10 Integration + demo day + short post-mortem.

Today’s Checklist (meeting-ready; tick through)
 Freeze scope: goal, out-of-scope, four buckets, platform choices.

 Approve DB schema + endpoint list (above).

 Decide hosted Supabase (W1–W3) → local self-host target (W4).

 Create monorepo + folders (apps/web, apps/api, apps/worker, packages/shared, docs, seeds).

 Add .env.example, PRD.md, PDD.md, and RESEARCH_PROMPTS.md.

 Stand up Supabase project; create tables; enable RLS; generate anon/service keys.

 Add seed JSON stubs (seeds/kg.seed.json, seeds/content.seed.json).

 Write meeting agenda and per-intern Week-1/2 deliverables (below).

 Create GitHub milestones W1–W10 + labels (area:systems|ai|publishing|frontend, type:feature|doc|bug, prio:P0–P2).

Week-1/2 Deliverables per Bucket (acceptance criteria)
Systems

W1: Compose plan + deploy options; repo scaffold; CI green on hello-world API.

W2: Compose v1; Supabase connected; /health + /api/entities reachable in staging.

AI/KG

W1: Minimal SKOS draft; ERD; validation rules; sample entity/rel JSON.

W2: Migrations applied; CRUD live with zod validation; JSON-LD export stub; 200 entities/400 relations seeded.

Publishing

W1: Endpoint audit (Bluesky/Mastodon), payload shapes, Publisher interface.

W2: Email preview → MailHog; job queue with queued→running→ok|error; dry-run for socials.

Frontend

W1: Wireframes for Auth, Interests, Ideas, Explorer, Email Prefs; API call list.

W2: Auth working; Interests page reads/writes subscription_prefs; Ideas submission persists.

Demo Independence Criteria (per module)
Systems: Fresh clone → docker compose up yields working stack + seed applied.

AI/KG: Import JSON file → query shows new entities/relations + JSON-LD export downloadable.

Publishing: Create content → schedule job → see email in MailHog and posts on dev accounts.

Frontend: New user sign-up → set prefs → submit idea → browse stubbed explorer.

Risks & Controls
Contract drift → Lock types + run contract tests in CI from W2.

API lag blocks others → Provide stubs + Postman collection end of W2.

Auth/RLS mistakes → Start with hosted Supabase; RLS templates + review in W2.

Social API changes/rate-limits → Keep adapters thin; central retry/backoff; sandbox accounts.

Time bleed on design → Wireframes only in W1; ship functional UI first.

Paste-Ready GitHub Issue Backlog (first cut)
Cross-cutting
 Create monorepo skeleton and CI baseline (prio P0, area:systems)

 Define DB schema & apply migrations (P0, area:ai)

 Seed generator scripts for KG + content (P0, area:ai)

 Define REST endpoint contracts in packages/shared (P0, area:systems)

 Author PRD.md and PDD.md templates in /docs (P1, type:doc)

 Add RESEARCH_PROMPTS.md for all four tracks (P1, type:doc)

 Write contribution guidelines + branch strategy (P2, type:doc)

Systems
 Docker Compose v1 for api/worker/web/db/mailhog (P0)

 Supabase project provisioning & RLS baseline (P0)

 Staging deploy script + environment switching (P1)

 Healthcheck & structured logging (P1)

AI/KG
 Minimal SKOS model + ERD (P0)

 CRUD endpoints /api/entities, /api/relations with zod validators (P0)

 JSON-LD export for entities (P1)

 ETL script from research JSON → DB (P1)

 Simple search GET /api/search?q= (P2)

Publishing
 Publisher interface + job model (P0)

 Email preview + send via MailHog (P0)

 Bluesky adapter (create post) (P1)

 Mastodon adapter (create status) (P1)

 Homepage writer (Markdown/JSON artifact) (P2)

 Retry/backoff + idempotency keying (P2)

Frontend
 Auth screens (Supabase Auth UI) (P0)

 Interests picker + save to subscription_prefs (P0)

 Idea submission form → idea_submissions (P1)

 Vault explorer (list/detail by kind) (P1)

 Email preferences + unsubscribe flow (P2)

 Minimal admin toggle for vault editing (P2)

Meeting Agenda (60–75 minutes)
Constraints & roles (5)

Architecture & platform (10)

Contracts & schema (10)

Module briefs + DoD (15)

W1/W2 deliverables + acceptance criteria (10)

Risks & rules of engagement (5)

Q&A + assign first issues (10)

Commitments: each intern claims 2–3 issues for W1 (5)

If you want this turned into a single “Issues CSV” or a gh CLI paste-block to create the backlog and milestones, say the word and I’ll output it in one go.

You said:
Can we just... Before we make any decisions, I would like to have a discussion with you about whether or not this approach seems like I'm missing something important.
ChatGPT said:

Thought for 47s
Short answer: your four-bucket split is solid. The gaps are mostly about integration discipline, safety, and “demo insurance.” Here’s the blunt audit and the minimal fixes to close risk.

What’s Missing (and how to plug it fast)
Steel-thread E2E by Week 3

Problem: Independent modules can pass demos while the system still fails end-to-end.

Fix: Define one thin, immutable flow and ship it early:
“New user → pick interests → submit idea → AI normalizes to Entity → weekly email job renders 1 item → Bluesky + Mastodon posts stub.”
Lock a test script and acceptance checks for this path; every change must keep it green.

Contract versioning & change control

Problem: “Frozen” types drift once coding starts.

Fix: Put OpenAPI for REST + Zod schemas in packages/shared; publish them as a versioned npm workspace. Any contract change requires a bump (minor for additive, major for breaking) and CI contract tests across all apps.

Test strategy beyond unit tests

Problem: Late bugs during W10 integration.

Fix: Three layers:

Contract tests: API responses validated by the shared Zod types.

E2E: Playwright: auth → idea submit → see entity → schedule campaign → MailHog contains email.

Worker tests: Deterministic job runner with fake clock.

Data & demo realism

Problem: “Hello world” seed data doesn’t surface ontology or publishing edge cases.

Fix: Curate a seed pack with: 200+ entities, 400+ relations, 30+ sources, 10 content items with tags, and at least 5 malformed records to exercise validators. Keep it under /seeds/ with a one-shot import.

Privacy, consent, and email law basics

Problem: Easy to violate CAN-SPAM/GDPR norms even in a demo.

Fix:

Double opt-in (email magic link + confirm).

Required unsubscribe in every email; /unsubscribe?token=….

Store consent timestamp, IP, user agent; log every send.

No scraping real emails; use sandbox lists for demos.

Secrets & environment hygiene

Problem: Keys leak; interns commit .env.

Fix: .env.example only, git-ignore real .env. Central secret store (1Password vault or Doppler) with least privilege Supabase keys (service key only in worker/API, never in web). Rotate once mid-program to prove you can.

Observability you’ll actually use

Problem: “It fails on staging” with no clues.

Fix:

Structured logs (request-id, user-id, job-id) to stdout.

job_runs table with status, duration, error, retry_count.

One health endpoint per service returning version hash.

Migrations & rollback

Problem: DB changes break others.

Fix: Drizzle or Prisma migrations in repo; down migrations required. CI runs migrate up + down on a temp DB per PR.

RBAC and RLS minimalism

Problem: Accidental overexposure in Supabase.

Fix: Two roles: viewer (read KG, manage own prefs/ideas) and admin (content + relations write). RLS policies unit-tested (yes, tests for “blocked as expected”).

Social API fragility

Problem: Rate limits, auth churn, or “API moved.”

Fix: Adapters behind a stable Publisher interface with idempotency keys, exponential backoff, and circuit-breaker (stop posting for that adapter after N failures; surface in dashboard).

Runtime guardrails for interns’ time

Problem: 80 hours disappears into “nice to have.”

Fix: Definition of Ready (DOR) + Definition of Done (DOD) per story; WIP limits (each intern works 1 story at a time); Friday 15-min demo every week, no exceptions.

Documentation & handover

Problem: You can’t reuse this after the demo.

Fix: Each module maintains a RUNBOOK.md (install, env, common failures, recovery), plus an API.md linked to OpenAPI.

Minimal Adjustments to Your Plan (zero bloat)
Add a W3 “steel-thread” milestone with a fixed acceptance script.

Adopt a contracts package (packages/contracts: OpenAPI + Zod) and enforce it via CI in all modules.

Add four test jobs to CI: unit, contract, e2e-headless, migrations up/down.

Add consent & unsubscribe fields to the schema now (cheap later, costly if forgotten).

Stand up logging & job_runs today; you’ll thank yourself in W9.

Lock DOR/DOD checklists in /docs/PROCESS.md.

Concrete Acceptance Checks (copy into the repo)
Steel-thread (must pass by end of W3):

Create user → receives confirm email → login succeeds.

Submit idea → row in idea_submissions with status="new".

AI script creates Entity + Relation from a JSON seed and links a Source.

Create ContentItem bound to that Entity.

Schedule PublicationJob with runAt=now+1m.

Worker runs → job_runs.status="ok"; email in MailHog; Bluesky and Mastodon adapters “noop” in dev (log payload), real post behind a feature flag.

Security/RLS:

Auth’d viewer cannot INSERT into relations.

Unauth’d cannot read subscription_prefs.

Admin can write entities/relations/content.

Migrations:

pnpm db:reset drops, migrates up, seeds, migrates down, migrates up again without error.

Decision Points to Lock (before coding, no bikeshedding)
OpenAPI + Zod in packages/contracts – yes/no.

Drizzle vs Prisma for migrations – pick one.

Playwright for e2e – yes/no.

Hosted Supabase to W3 then optional self-host W4 – yes/no.

Two social adapters only (Bluesky, Mastodon) – yes/no.

Single steel-thread scenario wording (as above) – yes/no.

Two roles only (viewer/admin) – yes/no.

Secret management tool (1Password/Doppler/manual) – pick one.

Locking these eliminates 80% of schedule risk.

If you want a sanity check on scope balance
Systems owns: repo, Docker, CI, secrets, migrations pipeline, deploy.

AI/KG owns: schema, validators, JSON-LD, ETL, search, seeds.

Publishing owns: content model, jobs/queue, email adapter, 2 social adapters, homepage writer.

Frontend owns: auth, interests, ideas, explorer, email prefs, unsubscribe.
Each can demo solo and all feed the W3 steel-thread + W10 full demo.

If you want, I can convert this into a paste-ready backlog (GitHub issues + labels) and a one-page PROCESS.md you can drop into /docs/.

You said:
So I feel like you're supposed to be helping me with planning my day and making sure I get through the steps. And instead, you're helping me with deeper decisions that need to be made. Can we step back? I appreciate this input and we should integrate it into the plan for the day. But I need you to help me from a higher level. Like I need to prepare GitHub and I need to give them a complete overview of the project we're building and the process that we're going to go through and how we plan to finish it and what specifically they'll need to be researching for their first week, which would give me some time to get the rest of it ready and that sort of stuff like higher level than this please . I will be sorting this stuff out today, but that isn't your job. Your job is to keep me on track with a higher list of things so that as new things appear that I need to do today, I can tell you about them and you can keep track of them for me. 
ChatGPT said:

Thought for 38s
Understood. I’ll keep you on the rails at a high level and maintain today’s checklist. Use this syntax to manage it in-thread:

Add a task: add: <task>

Mark done: done: <task>

Defer: defer: <task>

I’ll reflect updates immediately and keep the list clean.

Today: High-Level Plan (half-day)
Objective: be meeting-ready with (1) GitHub prepared, (2) a clear one-pager overview, (3) week-1 research briefs per role, (4) a simple agenda and comms links.

Timeboxed flow (adjust start to now)
T+0:00–0:30 — GitHub prep (skeleton only)

Create org repo and top-level folders.

Add README (1-page overview below), docs/ (agenda + briefs), and labels/milestones.

T+0:30–1:15 — Project overview one-pager

Paste the “Intern Overview” section (below) into README.

T+1:15–2:00 — Week-1 research briefs

Paste the “Week-1 Briefs (per role)” into docs/week1-briefs.md.

T+2:00–2:30 — Meeting agenda & assignments

Paste “Kickoff Agenda” into docs/agenda.md. Assign week-1 outcomes.

T+2:30–3:00 — Comms & links

Post repo + agenda + briefs to Discord/Notion; confirm meeting time.

T+3:00–3:30 — Risk & parking lot

Note open decisions to revisit after W1 (I’ll track them).

Intern Overview (paste into README)
Project: Knowledge Graph Lab
Goal: A minimal system that lets us (a) research and normalize domain knowledge into a simple graph, (b) let users sign up, pick interests, and submit ideas, and (c) publish periodic updates (email + 2 socials).
Timeline: 10 weeks, 10 h/week each.
Cadence: Weekly mini-demo every Friday; planning on Mondays.
Modules (1 per intern):

Systems/DevOps: repo, environments, Docker, basic deploy.

AI/Ontology: lightweight schema, import/export, simple search.

Publishing: email preview/send + 2 social posts + basic scheduler.

Frontend: auth, interests, idea submission, vault browsing, email prefs.
Independence rule: each module must demo on its own; integration is a bonus layer, not a blocker.
Default choices (for speed; can revisit after W1): monorepo, Node/TS, Supabase auth+DB (hosted to start), Next.js web, MailHog in dev, Bluesky + Mastodon for social.

Week-1 Briefs (what each person researches and delivers)
Keep outputs short (2–3 pages max each) and actionable.

Systems / DevOps
Question: What’s the simplest way to run web + API + worker + DB locally and push to a cheap remote for demos?

Deliverables: service list, minimal Docker plan, suggested deploy target; env/secrets approach; a 1-page “how to run it” draft.

Artifacts to submit: docs/systems-w1.md + a proposed folder map.

AI / Ontology / KG
Question: What’s the smallest useful concept set for our domain (≤4 kinds) and a simple way to store/query it?

Deliverables: a minimal schema diagram; sample entity/relationship JSON; import/export plan; 10 sample entities w/ brief sources.

Artifacts to submit: docs/ai-w1.md + seeds/sample.json (tiny sample).

Publishing Tool
Question: What is the straightest path to send an email preview, post to Bluesky and Mastodon, and schedule jobs?

Deliverables: endpoint/auth notes for Bluesky/Mastodon; email preview/send plan; a basic job lifecycle sketch (queued → done).

Artifacts to submit: docs/publishing-w1.md with payload examples.

Frontend
Question: What are the 5 essential screens and their states?

Deliverables: lo-fi wireframes (Auth, Interests, Idea submit, Vault browser, Email prefs); list of API calls each screen needs; error/empty states.

Artifacts to submit: docs/frontend-w1.md + images or quick sketches.

Shared week-1 rule: No coding required beyond tiny spikes—goal is clarity and decisions for week-2 PRD/PDD.

Kickoff Agenda (paste into docs/agenda.md)
Welcome & constraints (5 min): roles, 10-week cadence, demo-every-Friday rule.

Project overview (7 min): what we’re building and why; module independence.

Module briefs (10 min): each intern confirms their week-1 brief.

Process (8 min): where docs live, how to file issues, how we review.

Milestones (5 min): W1 research → W2 PDD/PRD → W3–W9 build → W10 demo day.

Q&A (10 min): capture open decisions to the parking lot.

Assignments (5 min): each intern restates their week-1 deliverable and posts their doc link in Discord.

GitHub Prep (high-level only)
Create repo and these top folders: apps/, docs/, seeds/, scripts/.

Add files: README.md (overview), docs/agenda.md, docs/week1-briefs.md, docs/process.md (how we work).

Labels: area:systems|ai|publishing|frontend, type:feature|doc|bug, prio:P0|P1|P2.

Milestones: W1 Research, W2 PDD/PRD, W3–W9 Build, W10 Demo.

Create one issue per intern: “Week-1 brief — <module>” with the 3 deliverables above.

Parking-Lot Decisions (I’ll track; you can ignore until after W1)
Auth/DB provider defaults (Supabase hosted vs self-host later).

Exact schema/endpoint names.

Social adapters beyond Bluesky/Mastodon.

Any non-essential integrations or design polish.

Master Checklist for Today (live tracker)
 Create repo and folder skeleton.

 Paste Intern Overview into README.

 Paste Week-1 Briefs into docs/week1-briefs.md.

 Paste Kickoff Agenda into docs/agenda.md.

 Add labels and milestones.

 Create 4 Week-1 brief issues (one per intern).

 Post repo + agenda + briefs to Discord/Notion.

 Confirm kickoff time with interns.

Tell me add: ... or done: ... and I’ll keep this list updated as we go.

You said:
One of the things I think would be good, but I don't know if I have time to set up, would be using the project management tools in GitHub to do the Kanban board of the work that we're doing. One of the keys here is to use best practices for working with a team so that I'm both teaching them how to do it and also keeping with a structured process, likely a light version of agile development where I'm not just making everything up as we go and we don't miss any important steps. 
ChatGPT said:

Thought for 37s
You’ve got it. Let’s keep this high-level, timeboxed, and practical. Below is a minimal way to spin up a GitHub Project Kanban today, teach a light Agile rhythm, and give interns clear Week-1 research marching orders—without you disappearing into setup hell.

Rapid plan: GitHub Kanban + light Agile (today)
A. 15-minute “good enough” setup (use the new GitHub Projects, not Classic)
Create a Project (repo-scoped is fine for now)

Name: KGL — Sprint Board

Description: “10-week internship project: Systems / AI / Publishing / Frontend”

Add fields (keep it lean)

Status (built-in): To do → In progress → In review → Blocked → Done

Module (single select): Systems, AI/KG, Publishing, Frontend

Priority (single select): P0, P1, P2

Iteration (built-in): create 10 weekly iterations (W1…W10)

Estimate (number, optional): 1, 2, 3, 5

Create views

Board: Group by Status, Sub-group by Module, Sort by Priority

Backlog (Table): Filter Status: To do OR Blocked, Sort by Priority, then Estimate

This Week (Table): Filter Iteration: current

Timeline (optional): Show by Iteration

Turn on automations (Project → Workflows)

On item added → set Status = To do, Iteration = current

When linked issue is closed → Status = Done

When issue re-opened → Status = In progress

Connect issues to the board
Create four issues (one per intern): “Week-1 research brief — {Module}” and add them to the Project, set Module, Priority, and Iteration = W1.

That’s enough to run a team today: one board, clear statuses, and week buckets.

B. If you have 45–60 minutes, add “best-practice” polish
1) Labels (keep to these)
area:systems, area:ai, area:publishing, area:frontend, type:feature, type:doc, type:bug, prio:P0, prio:P1, prio:P2

2) Milestones
W1 Research, W2 PDD/PRD, W3–W9 Build, W10 Demo Day

3) Issue templates (drop in .github/ISSUE_TEMPLATE/)
feature.md

---
name: Feature
about: Feature or task
labels: ["type:feature"]
---

### Summary
What outcome and why it matters.

### Acceptance Criteria
- [ ] Behavior 1
- [ ] Behavior 2
- [ ] Error/empty states covered

### Definition of Ready
- [ ] Scope is small (≤5 points)
- [ ] Dependencies noted
- [ ] API/contract known

### Definition of Done
- [ ] Tests updated
- [ ] Docs updated
- [ ] Demo scenario noted
research.md

---
name: Week-1 Research Brief
about: Short research brief to inform W2 PRD/PDD
labels: ["type:doc"]
---

### Focus Question
What decision will this research enable?

### Findings (bullets only)
- …

### Recommendation (pick one)
- [ ] Option A …
- [ ] Option B …
- Rationale:

### Artifacts
Links to notes, sources, and example payloads.
4) PR template (.github/PULL_REQUEST_TEMPLATE.md)
### Summary
What this change does.

### Scope
- Module: Systems / AI/KG / Publishing / Frontend
- Issue(s): #…

### Checks
- [ ] Tests pass locally
- [ ] Docs updated
- [ ] Demo steps included

### Demo Steps
1. …
2. …
5) Team rhythm (copy into docs/process.md)
Standup (async in GitHub/Discord): three bullets (Yesterday / Today / Blockers).

Planning (Mon, 20 min): pull from Backlog → set Iteration = current; WIP limit = 1 per intern.

Demo (Fri, 15 min): each intern shows 2–3 mins from the board.

Definition of Ready/Done: same checklists as templates above.

Board rules: move your own cards, keep Status truthful, keep Acceptance Criteria concrete.

C. Week-1 research briefs (give these verbatim to the interns)
Systems / DevOps

Outcome: a 1-page “How we run this” (local Docker + cheap remote demo).

Answer: services list, minimal Docker plan, env/secrets approach, deploy target.

Deliverable: docs/systems-w1.md with folder map and one command we’ll standardize on.

AI / Ontology / KG

Outcome: a minimal schema we can build on.

Answer: ≤4 kinds (Creator/Org/Platform/Concept), 10 sample entities + 10 relations, import/export JSON shape.

Deliverable: docs/ai-w1.md and seeds/sample.json (tiny, realistic).

Publishing Tool

Outcome: clearest path to (a) email preview/send, (b) Bluesky + Mastodon posts, (c) basic scheduler.

Answer: auth flows, payload shapes, rate limits, “Publisher interface” sketch.

Deliverable: docs/publishing-w1.md with example request/response bodies.

Frontend

Outcome: 5 must-have screens with required API calls.

Answer: Auth, Interests, Idea Submit, Vault Explorer, Email Prefs; error/empty states.

Deliverable: docs/frontend-w1.md + wireframe images.

Week-1 rule: short briefs, no rabbit holes. Week-2 turns these into PDD/PRD.

D. Kickoff agenda (drop into docs/agenda.md)
Constraints & roles (5)

Project overview (7)

Week-1 briefs handoff (10)

Board walkthrough (8)

Milestones W1→W10 (5)

Q&A (10)

Assign Week-1 issues on the board (5)

E. Your high-level checklist for today (I’ll track this live)
 Create KGL — Sprint Board (GitHub Project) with fields: Status, Module, Priority, Iteration

 Add views: Board, Backlog, This Week, Timeline

 Enable automations (item added → To do; closed → Done; reopened → In progress)

 Create labels and milestones (W1…W10)

 Add issue + PR templates

 Open 4 Week-1 research issues (one per module), attach to Project (W1), set Module/Priority

 Paste agenda + process docs into repo and share links in Discord/Notion

 Confirm kickoff time with interns

Use these commands to manage the list:

add: <task>

done: <task>

defer: <task>

I’ll keep the tracker updated and nudge you if we’re drifting from the plan.

You said:
You're still way too deep into the work. I just need you to help me with a structured plan. I don't wanna hear about every field that I'm supposed to be adding. Can you figure that out, please? What does it take for you to stop diving in so deep? It makes it really hard for me to focus. 
ChatGPT said:

Thought for 12s
You’re right. I’ll stay high-level and act as your tracker.

How we’ll work (simple)
Use: add: <task>, done: <task>, defer: <task>. I’ll maintain the list.

Goal for today: be kickoff-ready (repo + overview + week-1 briefs + agenda + invites).

Today — Half-Day Plan (only the essentials)
Block 1 (30 min) — GitHub basics

Create repo and top-level folders only.

Add a one-page README (use the mini template below).

Create 4 “Week-1 research brief” issues (one per module).

Block 2 (45 min) — Project overview (1 page)

Paste the mini README template.

Sanity-check scope and the four roles.

Block 3 (45 min) — Week-1 briefs (per role)

Create a single docs/week1-briefs.md with 4 short prompts:

Systems: “Propose how we run locally and demo remotely. One page.”

AI/KG: “Propose the smallest useful schema + import/export shape. One page.”

Publishing: “Propose how to send an email preview and post to two socials. One page.”

Frontend: “Propose 5 screens + required API calls. One page.”

Block 4 (30 min) — Kickoff logistics

docs/agenda.md with a 30–45 min kickoff agenda (overview → briefs → Q&A → assignments).

Post links in Discord/Notion. Confirm time with interns.

Block 5 (30 min) — Board (optional)

If time remains, create a single GitHub Project board with three columns: To do / In progress / Done and move the 4 Week-1 issues onto it. If not, skip.

Week-1 → Week-10 (at a glance)
W1: Research briefs only (no coding).

W2: PDD/PRD per module.

W3–W9: Build.

W10: Integration + demo day.

What interns will hear (keep it this simple)
We’re building four independent modules: Systems, AI/KG, Publishing, Frontend.

Weekly rhythm: Mon plan, Fri mini-demo. No exceptions.

Week-1 output: a one-page brief per person that unblocks Week-2 specs.

Every module must be demoable on its own.

Ultra-short README you can paste
# Knowledge Graph Lab (Intern Project)

**Goal:** Build a minimal system that (1) researches and normalizes domain knowledge into a simple graph, (2) lets users sign up, pick interests, and submit ideas, and (3) publishes periodic updates (email + two socials).

**Timeline:** 10 weeks · 10 h/week each · 4 modules (Systems, AI/KG, Publishing, Frontend)

**Cadence:** Mon planning · Fri mini-demos

**Week-1 Deliverables (no code):**
- Systems: 1-pager on how we run locally and demo remotely
- AI/KG: 1-pager minimal schema + import/export shape (+ tiny sample JSON)
- Publishing: 1-pager on email preview + two social posts + basic scheduler
- Frontend: 1-pager on 5 screens + required API calls

**Week-2:** PDD/PRD per module
**Weeks 3–9:** Build
**Week 10:** Integration + Demo Day
Your master checklist for today (I’ll track updates)
 Create repo + top-level folders

 Add the 1-page README

 Create docs/week1-briefs.md

 Create docs/agenda.md

 Open 4 “Week-1 brief — {module}” issues

 Share repo + docs in Discord/Notion

 Confirm kickoff time with interns

 (Optional) Create a simple 3-column GitHub Project board

Reply with add: … / done: … / defer: … and I’ll keep you focused.

You said:
No, the plan for today, goddammit. Just today. Give me a list of the things I should do today. One bullet point for each thing, like set up GitHub, create project outline, that kind of thing. We need to strategize about the things that I need to do, not the details for them. Get it through your head. 
ChatGPT said:

Thought for 10s
Set the kickoff meeting time and send the calendar invite

Create the GitHub repo and push an initial README

Write a one-page project outline in the README (goal, timeline, four roles)

Create a Week-1 research briefs doc (one section per role)

Create a short kickoff agenda doc

Open four Week-1 brief issues (one per intern)

Create a simple Kanban board (To do / In progress / Done) and add those four issues

Share repo + docs links in Discord/Notion for the interns

Confirm interns’ access to GitHub, Discord, and Notion

Prepare your opening talking points (vision, roles, weekly cadence)

Draft the Demo Day goal statement (one sentence)

Start a “parking lot” list for decisions to revisit after Week-1

You said:
Okay so let's add to this so it's more sensible. This is the assumes that I know exactly what the one project outline should have in it. We need to add a research phase before it And we also need a separate page that explains our process better for the interns. Also, the one-page project outline is going to be too thin. A goal, a timeline, and the four roles. Yeah, that's the basics, but what we really need is a schematic that shows how the four modules that are going to be developed can be worked independently and then connected, and what the dependencies are. Again, keep this very high level. I don't want to get into the details. We're just creating a plan for the work I have to do, and it's already taken us half an hour. 
ChatGPT said:

Thought for 11s
Set the kickoff meeting time and send the invite

Create the GitHub repo with a basic docs/ folder

Create a Research Phase page (what each role investigates in Week-1)

Create a Process page (how we work: weekly cadence, demos, issues/PRs)

Draft the Project Outline (2 pages: goal, timeline, roles, deliverables)

Add a high-level schematic page (four modules, their boundaries, and simple dependencies)

Create four Week-1 research brief issues (one per module)

Create a simple 3-column Kanban board and add those four issues

Share the repo and docs links in Discord/Notion

Confirm all interns’ access to GitHub, Discord, and Notion

Prepare your opening talking points (vision, modules, Week-1 → Week-10)

Draft the Demo Day one-sentence goal

Start a parking-lot list for decisions to revisit after Week-1

You said:
No, not the research phase for each role, but the research I have to do today before I write everything. 
ChatGPT said:

Thought for 23s
Skim your existing notes/chats to pull prior decisions and constraints

Decide the minimal scope and the explicit non-goals for this 10-week cycle

Define the four module boundaries in one sentence each (and the “independent demo” rule)

Identify the shared dependencies at a high level (auth/DB, queue/scheduler, content format)

Choose default tools for this cycle (auth/DB, web framework, email, two socials)

Set the weekly cadence (Mon planning, Fri demo) and lock Week-1/Week-2 focus

Write a one-sentence Demo Day success statement

List the top five risks to watch and start a parking-lot list

Create the GitHub repo with a basic docs/ folder

Draft the 2-page Project Outline (goal, timeline, roles, deliverables)

Draft the Process page (how we work: cadence, issues/PRs, demos)

Draft the High-Level Schematic page (four modules + simple dependencies)

Create four Week-1 research brief issues (one per module)

Create a simple 3-column Kanban board and add those four issues

Share repo and docs links in Discord/Notion and confirm intern access

Set the kickoff meeting time and send the calendar invite


