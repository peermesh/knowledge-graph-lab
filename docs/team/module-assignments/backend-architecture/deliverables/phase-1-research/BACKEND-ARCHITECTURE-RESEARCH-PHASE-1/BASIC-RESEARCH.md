# INTERNSHIP_FALL_2025

I will be implementing the entire core backend infastructure that powers the Knowledge Graph Lab System

TOPIC 1: 
Docker Compose Patterns for Multi-Service Applications

Download docker in terminal
    - type "sudo dockerd" in terminal
    - this starts docker

*Docker Compose Patterns for Multi-Service Applications*

1. There is a single docker-compose.yml file
    - Define app, database, cache and more in a single file
    - sort of a blueprint for the application stack
    - defines how multiple containers should work together
    - file defines dependencies, networks, volumes, and configuration

2. Override file
    - docker-compose.override.yml for local dev overrrides

3. For multiple files in the environment
    - docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
    - type this in terminal

4. Resuable Services
    - Use YAML anchors (<<: ) to avoid duplication

5. Dependency management: 
    - depends_on ensures services start in order (though healthchecks are better).

*Basic Docker Scripting*

1. Environment Configurations
    - .env files with docker-compose for development, staging or production
    - docker run --env-file .env.prod ... is an example for what to type into terminal

2. Mounted Directories
    - volumes: in docker-compose.yml for local dev code sync

3. Volume Strategies for Databases
    - Named volumes (db_data:/var/lib/postgresql/data) survive container restarts

4. Configure file Templating
    - Use tools like envsubst, gomplate, or Compose’s variable substitution (${VAR}) 

*Data persistence between container restarts*

1. Database Volumes
    - Use named volumes for persistence

2. Settings and configuration persistence
    - Mount config files from host for dev
    - Store production configs in secrets or config management tools

3. Backup and restore strategies
    - Use docker exec + dump commands (e.g. pg_dump)
    - Mount a backup directory with cron jobs
    - For production: use database-native tools or cloud-managed backup systems

*Security in Docker*

1. Basic secrets management (environment variables, .env files) 
    - Dev: .env + .gitignore
    - Prod: docker secrets (Swarm) or external secret managers (Vault, AWS Secrets Manager)

2. Non-root container execution
    - In Dockerfile, set:
        RUN adduser -u 1000 appuser
        USER appuser

3. Network isolation* and security groups*
    - Place services in custom user-defined networks
    - Only expose what needs to be public (e.g., ports: for app, not DB)

4. Image vulnerability scanning**
    - Use docker scan (Snyk), Trivy, or GitHub Actions security scans

5. Minimize Attack Surface
    - Use small base images (alpine, distroless)
    - Regularly update images

*KEY QUESTIONS*

How do we manage different mounted directories for dev vs production?

1. Development:
    Use bind mounts so code changes on your host machine are reflected inside the container. Example:

        volumes:
            - ./src:/usr/src/app

2. Production:
    Avoid host mounts. Instead:

        - Bake your code/configs into the Docker image.

        - Use named volumes only for persistent data (like databases).

        - Override configs using environment variables or .env files.

3. Best Practice: 
    - Use docker-compose.override.yml for dev mounts and keep production clean with baked images

What’s the best approach for secrets that works locally and in cloud?

1. Local Development:
    - Store secrets in .env (git-ignored)
    - Example:

        DB_USER=devuser
        DB_PASS=devpass

    - Loaded automatically by Docker Compose

2. Production:
    - Never hardcode or bake secrets into images
    - Options:

        Docker Secrets (if using Swarm).

        Cloud Secret Managers (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault).

        Kubernetes Secrets if deploying to K8s

3. Hybrid approach: 
    - Use .env for local dev, and environment variable injection or secret manager in production

How do we handle database migrations in containerized environments?

1. Option 1: Migration container
    Create a service in docker-compose.yml dedicated to running migrations (one-off job). Example:

    services:
        migrate:
        image: myapp
        command: npm run migrate
        depends_on:
            - db

2. Option 2: Run migrations at startup
    - Your app runs migrations automatically when it boots. Useful for dev, but risky in prod (unexpected schema changes)

3. Option 3: CI/CD integrationOption 3: CI/CD integration
    - Run migrations as part of your deployment pipeline before new containers are rolled out

4. Best practice
    - Dev: auto-run migrations in the container for convenience
    - Prod: run migrations as a separate step in CI/CD to maintain control and rollback safety


# 🗄️ Topic 2: Database Selection

---

## 🔹 Primary Database Choice

**Focus on simplicity** → Start with **PostgreSQL** as the main database. Add other databases only if a specific need arises.

---

### PostgreSQL (Primary)
- Relational database for **core application data**.  
- Use cases:
  - User data
  - Content storage
  - Relationships between entities
- Key features:
  - Native **JSON support** for semi-structured data
  - Built-in **full-text search** capabilities

---

### Redis (Optional)
- In-memory database used for **performance and caching**.  
- Use cases:
  - Session storage
  - Cache layer to reduce DB load
  - Simple **pub/sub messaging** if needed

---

### SQLite (Dev & Testing)
- Lightweight database for **development, testing, and edge deployments**.  
- Use cases:
  - Local development database
  - Isolated test runs
  - Edge/IoT deployments with minimal footprint

## 🔹 Phase 2 Databases (For AI/Graph Features)

As the system evolves beyond core features, consider specialized databases for **AI, graph relationships, and analytics**.  
Start with **PostgreSQL** and extend only if a clear performance or feature need arises.

---

### Vector Databases (Phase 2 – AI Features)
- Use cases:
  - Store **embeddings** for semantic search (RAG implementations).
  - Enable similarity search across documents.  
- Options:
  - **Dedicated vector DBs**: Pinecone, Weaviate, Qdrant  
    - Run locally in Docker (Qdrant, Weaviate support local dev).  
    - Best for scale and specialized vector operations.  
  - **Postgres + pgvector extension**  
    - Simpler to start with.  
    - Good for proof-of-concept and smaller-scale use cases.  
- Research item: **Compare performance** of pgvector vs dedicated vector DBs.

---

### Neo4j (Phase 2 – Graph Relationships)
- Use cases:
  - **Knowledge graph** features.  
  - Visualizing and querying complex relationships.  
- Considerations:
  - **Postgres with recursive CTEs** is often sufficient for graph-like queries.  
  - **Neo4j Community Edition** is free and runs in Docker.  
- Research item: When do graph queries **actually require Neo4j** vs relational DB?

---

### DuckDB (Phase 3 – Analytics, Optional)
- Use cases:
  - Local **OLAP-style analytics** and fast columnar queries.  
  - Works well for **ad-hoc analytics** and integration with data science tools (e.g., Python, Jupyter).  

---

### Time-Series Databases (Phase 3 – Metrics, Optional)
- Use cases:
  - Storing and analyzing **metrics, logs, and time-series events**.  
- Options:
  - **TimescaleDB**: Postgres extension for time-series workloads.  
  - **InfluxDB**: Popular standalone time-series DB.  
- Consider if:
  - Application requires detailed **metrics tracking**.  
  - Long-term analysis of event/time-series data is a priority.

### Key Questions

#### 🔹 Can PostgreSQL handle our graph queries with recursive CTEs?
- **Yes, often sufficient**: Recursive CTEs can handle tree/graph traversal in many cases.  
- **When Postgres works**: Hierarchical data, simple relationship queries, limited depth.  
- **When Neo4j shines**:  
  - Deep, complex traversals  
  - Pathfinding queries (shortest path, centrality, community detection)  
  - When graph visualization is a core feature  

---

#### 🔹 Do we really need a separate vector database or can we use pgvector?
- **Start with pgvector**:  
  - Lightweight, simple, stays within Postgres.  
  - Good for MVPs and moderate embedding workloads.  
- **Dedicated vector DB (Qdrant, Weaviate, Pinecone) when**:  
  - You need horizontal scaling  
  - Advanced vector indexing & similarity search  
  - Real-time, large-scale embedding queries  
- **Best practice**: Prototype with pgvector → migrate only if scale/performance demands it.  

---

#### 🔹 What’s the simplest database setup that meets our needs?
- **Phase 1 (MVP)**: PostgreSQL only  
  - Use JSON columns for flexible schemas  
  - Use pgvector for embeddings if needed  
  - Use recursive CTEs for graph-like queries  
- **Phase 2 (if needed)**:  
  - Add Redis for caching  
  - Add Qdrant/Weaviate if pgvector hits performance limits  
  - Add Neo4j if graph queries/visualization become essential  
- **Phase 3 (optional)**:  
  - Add DuckDB for analytics  
  - Add TimescaleDB/InfluxDB for time-series workloads  

---

## Topic 3: Authentication & Authorization

### Core Authentication Architecture

When planning authentication, we need to balance **cost, complexity, and control**. Options fall into two broad categories:

---

#### 🔹 All-in-One Solutions
- **Supabase**  
  - Database + Auth + Realtime + Storage  
  - Open-source available, can self-host with Docker  
  - Great for rapid MVPs, but can lock you into their ecosystem if not self-hosted  

- **Firebase Auth**  
  - Tight integration with Google ecosystem  
  - Free tier available, but not self-hostable  
  - Best for fast prototyping, not ideal for long-term self-hosting  

- **AWS Cognito**  
  - Scales well within AWS ecosystem  
  - Pay-per-use model, not open-source  
  - Setup can be complex compared to other options  

---

#### 🔹 Dedicated Auth Services
- **Auth0 / Okta**  
  - Enterprise-grade, polished features  
  - Expensive at scale, not open-source  
  - Best suited for teams willing to pay for ease of use  

- **Keycloak** (⭐ Recommended for self-hosting)  
  - Open-source, free, enterprise-ready  
  - Supports OAuth2, OpenID Connect, SAML  
  - Runs easily in Docker for local and production use  
  - Can integrate with multiple identity providers (Google, GitHub, etc.)  

- **FusionAuth**  
  - Community edition free, enterprise support available  
  - Easier to set up than Keycloak, but smaller community  
  - Supports SSO, 2FA, passwordless  

- **Ory**  
  - Cloud-native, modular open-source auth stack  
  - Includes Ory Kratos (identity), Hydra (OAuth2), Keto (authorization)  
  - Good for modern microservices architectures  

- **Clerk**  
  - Modern developer-friendly auth service  
  - Paid only, not open-source  
  - Very easy to integrate but costs add up  

---

### Cost Priority:  
We want to **avoid monthly fees** and keep flexibility.  
- **Best Open-Source Options**:  
  - **Keycloak** → battle-tested, enterprise-ready  
  - **Ory** → modern and modular  
  - **Supabase (self-hosted)** → good for fast MVP  

---

### Next Steps / Research
- Decide: centralized auth service (Keycloak/Ory) vs embedded (Supabase)  
- Prototype: run Keycloak in Docker alongside PostgreSQL  
- Evaluate integration with app stack: REST APIs, JWT, or session-based auth  

### Supabase vs Separated Best-in-Class Auth

**Critical decision**: Should auth be bundled with database or use dedicated auth service?

**Supabase approach (bundled)**:
- **Pros**:
- Open-source version available (self-hostable)
- Integrated Row Level Security (RLS)
- Single service to manage
- Built-in user management UI
- Realtime subscriptions with auth
- **Cons**:
- Couples database and auth concerns
- May not have all auth features of dedicated services
- Limited to PostgreSQL for RLS benefits

**Separated best-in-class approach**:
- **Pros**:
- Use most feature-rich auth service (Auth0, Okta)
- Better enterprise features (SSO, advanced MFA)*
- More authentication provider options
- Database-agnostic
- Cleaner separation of concerns
- **Cons**:
- More services to manage
- Need to implement authorization layer
- Higher complexity
- **Potential monthly fees** (Auth0, Okta have paid tiers)

### Standard OAuth & Social Login

**Focus: Practical authentication setup for Week 1–2**

---

#### 🔹 Social Login Providers
Enable quick and user-friendly sign-in options:
- **Google Sign-In** → widely used, easy setup, strong user trust
- **Apple Sign-In** → required for iOS apps with third-party login
- **GitHub OAuth** → great for developer-focused apps
- **Microsoft Account** → useful for enterprise/education integrations
- **Facebook Login** → optional, declining in popularity but still widely available

---

#### 🔹 Email Authentication
Support for users who prefer email-based login:
- **Magic links (passwordless login)** → send sign-in link via email
- **Email + password** (with secure hashing)  
- **Password reset flows** → forgot password with tokenized link
- **Email verification process** → confirm ownership before full account activation

---

#### 🔹 Implementation Considerations
Core technical flows to handle securely:
- **OAuth 2.0 flow** → authorization code grant with PKCE for web/native apps
- **Redirect URI handling** → whitelist all expected callback URLs
- **Token exchange & storage** → securely handle access/refresh tokens
- **Profile data sync** → map provider’s profile info (name, email, avatar) to local user record
- **Session management** → JWTs vs. server sessions (decide per app stack)

---

#### 🔹 Quick Start Plan
1. Choose initial providers: **Google + GitHub** (most common for devs/students).  
2. Add **email + magic link** as fallback.  
3. Store user profiles in **PostgreSQL** (via auth service or custom implementation).  
4. Test with local redirect URIs in Docker (e.g., `http://localhost:3000/auth/callback`). 

### User Data Isolation (Simple Approach)

---

#### 🔹 Basic User Separation
- Enforce **per-user data filtering** by `user_id` in all queries.  
- Each user can **only access their own research/content**.  
- Allow optional **public/shared content** if needed (e.g., published notes, shared datasets).

---

#### 🔹 Keep It Simple
- Start with **basic user accounts + permissions**.  
- Avoid complex **multi-tenant architectures** at MVP stage.  
- Add **teams/groups/roles** later only if real need arises.  

---

#### 🔹 Implementation Notes
- Database design: Add `user_id` column to core tables.  
- Middleware / query layer should **automatically filter** by `user_id`.  
- Ensure **auth layer integration** → map authenticated user → database `user_id`.  

### Token Management

---

#### 🔹 Token Types
- **JWT (JSON Web Tokens)** → stateless, portable, widely supported  
- **Opaque tokens** → random strings validated against auth server  
- **Access + Refresh tokens** → short-lived access, long-lived refresh  
- **Session tokens** → traditional server-stored sessions (stateful)

---

#### 🔹 Token Storage
- **Secure cookies** (HttpOnly, Secure, SameSite=strict) → recommended for web apps  
- **Local storage** → convenient but vulnerable to XSS; avoid for sensitive tokens  
- **Token rotation strategies*** → periodically refresh tokens to reduce risk  
- **Revocation mechanisms*** → ability to revoke compromised tokens (blacklists, TTLs)

---

#### 🔹 Implementation Notes
- For MVP:  
  - Use **JWT access tokens** + **refresh tokens**.  
  - Store tokens in **secure cookies** (preferred) or encrypted local storage for native apps.  
  - Implement **short TTL for access tokens** (e.g., 15 min) + **longer refresh tokens** (e.g., 7 days).  
  - Add rotation & revocation in later phases.  

### Authorization Patterns

---

#### 🔹 Access Control Models
- **RBAC (Role-Based Access Control)** → assign roles (user, admin, moderator)  
- **ABAC (Attribute-Based Access Control)*** → rules based on attributes (time, location, resource type)  
- **ReBAC (Relationship-Based Access Control)** → permissions based on relationships (e.g., friends, team members)  
- **Policy-based authorization** → centralized policies (e.g., OPA, Casbin) for fine-grained rules  

---

#### 🔹 Simple Authorization (MVP)
- Each **user owns their data** → filter by `user_id`.  
- **Admin role** for system-level management.  
- **Public/private content flags** → allow optional sharing or publishing.  

---

#### 🔹 Implementation Notes
- Start simple: **RBAC + data ownership filtering**.  
- Add complexity later:
  - **Teams/groups** → extend RBAC or adopt ReBAC.  
  - **Attribute checks** → integrate ABAC if business rules demand.  
  - **Policy engines** → consider OPA or Casbin in later phases for complex authorization logic.  

### Implementation Considerations

---

#### 🔹 Session Management
- **Stateless sessions** → JWTs (self-contained, no DB lookup required)  
- **Stateful sessions** → stored in Redis or database (easier revocation, centralized control)  
- **Cross-service session sharing*** → consider when scaling across multiple microservices  
- **Session timeout strategies** → short-lived sessions + sliding expiration for security & usability  

---

#### 🔹 Security Best Practices
- Follow **OWASP authentication guidelines**  
- **Rate-limit login attempts** to prevent brute force attacks  
- **Account lockout policies** for repeated failed logins  
- **Audit logging*** → track auth events (logins, failures, token refresh, revocations)  

---

#### 🔹 MVP Recommendation
- Use **JWTs + refresh tokens** (stateless) for simplicity.  
- Store tokens in **secure cookies** (preferred for web).  
- Add **rate limiting + lockouts** in the auth service.  
- Plan for **audit logging + cross-service session sharing** in later phases.  

### Key Questions & Answers

**Q1. Is Supabase’s open-source version truly self-hostable without limitations?**  
✅ Yes. Supabase’s open-source stack (Postgres + GoTrue for auth + storage + realtime) is fully self-hostable under the Apache 2.0 license.  
⚠️ Limitations: Hosting it yourself means **you manage scaling, backups, updates, and monitoring**. Supabase’s managed service just removes that overhead.  

---

**Q2. Which auth service provides the best OAuth provider support?**  
- **Auth0/Okta** → Most complete set of providers, but cost and vendor lock-in are issues.  
- **Keycloak** → Excellent open-source support for OAuth/SAML/social logins.  
- **Supabase** → Good built-in OAuth for common providers (Google, GitHub, Apple, etc.), but fewer enterprise connectors than Keycloak/Auth0.  
👉 For MVP: **Supabase (if using their stack)** or **Keycloak (if you want self-hosted + flexibility)**.  

---

**Q3. How to implement authorization if using a separated auth service?**  
- Auth service (e.g., Keycloak, Ory, Supabase) issues **JWTs with claims** (user_id, roles, permissions).  
- Your app verifies JWT and applies **authorization rules** locally:  
  - Example: `user_id` in token must match `user_id` in DB rows.  
- For RBAC: roles are embedded in JWT claims → checked at middleware or service layer.  
- For more complex rules: integrate a **policy engine** (OPA, Casbin) later.  

---

**Q4. What’s the simplest path to secure authentication for MVP?**  
1. Pick **Google + GitHub OAuth** (covers 80% of early users).  
2. Add **email + magic link login** as fallback.  
3. Store user profiles in **Postgres** with `user_id` as primary key.  
4. Use **JWT access tokens (15 min)** + **refresh tokens (7 days)** stored in secure cookies.  
👉 This balances **simplicity + security** while avoiding heavy infra at MVP stage.  

---

**Q5. How to handle user sessions across multiple services?**  
- Use a **single auth provider** (Supabase, Keycloak, Ory) to issue JWTs.  
- Each microservice verifies JWT with the shared **public key** (no central DB lookup needed).  
- For revocation:  
  - Short-lived access tokens (15 min) + refresh token rotation.  
  - Optionally store refresh tokens in **Redis** for centralized invalidation if needed.  
👉 For MVP: **stateless JWTs** are enough. Add **Redis-backed revocation lists** when scaling to multiple services.  

# 🔌 Topic 4: API Design with Test Harness

---

## API Architecture Choice

**Principle:** Keep it simple → choose one main approach and stick to it for MVP.  
(Complexity comes later, when data access patterns demand it.)

---

### 🔹 REST API
- **Strengths**
  - Well-established, widely understood by devs.
  - Mature tooling (Postman, cURL, OpenAPI/Swagger docs).
  - Straightforward for CRUD operations (Create/Read/Update/Delete).
  - Easy to debug (each resource = URL, clear HTTP verbs).
- **Weaknesses**
  - Over-fetching/under-fetching data (client may get more or less than it needs).
  - Rigid structure if you need highly flexible queries.
- **When to use**
  - MVPs where speed + simplicity matter most.
  - Small teams without specialized GraphQL expertise.
  - APIs consumed by multiple clients (web + mobile) that need stability.

---

### 🔹 GraphQL
- **Strengths**
  - Flexible: clients ask for exactly what they need.
  - Single endpoint simplifies routing.
  - Strong type system → autocompletion + validation.
  - Great for complex data relationships (nested queries).
- **Weaknesses**
  - More complex to implement (needs schema + resolvers).
  - Harder caching, pagination, and rate-limiting compared to REST.
  - Security challenges (query depth, expensive queries, query cost analysis).
- **When to use**
  - Apps with highly dynamic frontends that query data differently per view.
  - Scenarios with many nested/relational data requirements.
  - Teams comfortable with GraphQL ecosystem.

---

### 🔹 Hybrid Approach
- **Concept**
  - Use **REST** for basic CRUD + system endpoints.
  - Use **GraphQL** for advanced querying/aggregation.
- **Strengths**
  - Keeps REST simplicity for core API.
  - Enables GraphQL where flexibility is needed (e.g., search, dashboards).
- **Weaknesses**
  - Adds **operational complexity** (two APIs to maintain).
  - Testing and security rules need to be duplicated or unified.
- **When to use**
  - Only after MVP if clear GraphQL-heavy use cases emerge.
  - Example: REST for user management, GraphQL for analytics queries.

---

## ✅ MVP Recommendation
- Start with **REST API only**:  
  - Faster to build, easy to test, plenty of tooling.  
  - Define resources cleanly (`/users`, `/projects`, `/auth/login`).  
  - Document using **OpenAPI/Swagger**.  

- Consider GraphQL **later** if:  
  - The frontend needs flexible nested queries.  
  - Clients complain about multiple round-trips/over-fetching.  

---

## 🧪 Test Harness Considerations
- **Unit tests** for controllers/services (use JUnit, pytest, etc. depending on stack).  
- **Integration tests** with test database (Dockerized PostgreSQL/SQLite).  
- **API contract tests** (use Postman/Newman or Pact for consumer-driven contracts).  
- **Load tests** (k6, Locust) to validate scaling.  
- **Automation** → run tests in CI pipeline with Docker Compose.  

---

### Basic API Requirements

---

#### 🔹 Core Endpoints
- **Authentication**
  - Endpoints: `/auth/login`, `/auth/logout`, `/auth/refresh`
  - Handle access + refresh tokens securely (JWT or opaque tokens).
- **User Management**
  - Endpoints: `/users`, `/users/{id}`
  - Create, update, delete, and fetch user profiles.
  - Include role/permissions attributes for authorization.
- **Content CRUD Operations**
  - Endpoints: `/content`, `/content/{id}`
  - Support create/read/update/delete for user-generated data.
  - Enforce user_id filtering for data isolation.
- **Search & Filtering**
  - Endpoints: `/search?query=...`
  - Support query params for filtering/sorting.
  - Paginate results (limit/offset or cursor-based).
- **Data Ingestion Triggers**
  - Endpoints: `/ingest/start`, `/ingest/status`
  - Used to kick off background jobs (e.g., file uploads, external API fetches).
  - Return async job IDs for progress tracking.

---

#### 🔹 API Standards
- **Consistent Naming Conventions**
  - Use **plural nouns** for resources (`/users`, `/projects`).
  - Follow RESTful patterns: `GET /users`, `POST /users`.
- **Proper HTTP Status Codes**
  - `200 OK` → successful read/update  
  - `201 Created` → successful resource creation  
  - `400 Bad Request` → invalid input  
  - `401 Unauthorized` → auth required  
  - `403 Forbidden` → access denied  
  - `404 Not Found` → missing resource  
  - `500 Internal Server Error` → unhandled exceptions
- **Error Handling Patterns**
  - Standardized error response format:  
    ```json
    {
      "error": "InvalidInput",
      "message": "Username is required",
      "details": { "field": "username" }
    }
    ```
- **Request/Response Validation**
  - Validate incoming payloads (e.g., using JSON schema, Joi, or middleware).
  - Sanitize outputs to avoid leaking sensitive info.
- **API Versioning Strategy**
  - Prefix endpoints with version (`/api/v1/...`).
  - Keep breaking changes isolated to new versions.
  - Deprecate old versions gradually with warnings.

---

#### ✅ MVP Recommendation
- Start with **REST endpoints for auth, users, and content CRUD**.  
- Add **search + ingestion** only after core flows are stable.  
- Document all endpoints with **OpenAPI/Swagger** and keep schema validation in place.  

### Documentation & Testing (REQUIRED)

---

#### 🔹 API Documentation & Test Harness
- **OpenAPI / Swagger (REST APIs – MANDATORY)**
  - Provides an **interactive API testing interface** for developers and QA.  
  - **Auto-generates client SDKs** for multiple languages if needed.  
  - Enables **“Try it out”** functionality for all endpoints directly in the browser.  
  - Must be **available from Day 1** to ensure clarity and reduce onboarding friction.  
- **GraphQL Playground** (if using GraphQL)
  - Interactive query editor for testing GraphQL queries/mutations.  
  - Visualizes schema, types, and relations.  
- **Example Requests / Responses**
  - Document **every endpoint** with sample payloads.  
  - Include **authentication flow examples** (access tokens, refresh tokens).  
  - Provide error response examples for all common failure scenarios.  

---

#### 🔹 Testing Strategy
- **Unit Tests**
  - Test core business logic independently of the API.  
  - Ensure correctness of calculations, validations, and data transformations.  
- **Integration Tests**
  - Test API endpoints against a **test database** (Dockerized Postgres/SQLite).  
  - Verify auth flows, data isolation, and response correctness.  
- **Automated API Testing**
  - Use OpenAPI spec to drive **automated tests** (Postman/Newman, Dredd, or Swagger Codegen tests).  
  - Covers endpoint correctness, schema validation, and auth enforcement.  
- **Load Testing Basics***  
  - Perform simple load tests on critical endpoints (k6, Locust) to check performance under stress.  
  - Identify bottlenecks and validate scaling assumptions.  

---

#### ✅ MVP Recommendation
- Deliver **OpenAPI documentation** from Day 1.  
- Write **unit + integration tests** alongside feature development.  
- Include **example requests/responses** in the docs for developers and QA.  
- Add load testing later once core endpoints are stable and used by multiple clients.  

### Key Questions & Answers

**Q1. REST or GraphQL for our use case?**  
- **REST is recommended for MVP**:
  - Simpler to implement and test.
  - Well-understood by all team members.
  - Works well with core CRUD endpoints (auth, users, content, search).
  - Plenty of tools for documentation and automated testing (OpenAPI/Swagger).  
- **GraphQL can be added later** if:
  - Clients need highly flexible queries or nested data.
  - You want to reduce multiple round-trips for complex front-end views.  
- **Hybrid approach** is an option post-MVP:
  - REST for simple endpoints, GraphQL for complex queries.

---

**Q2. How to handle API versioning?**  
- **MVP Strategy: URL prefix versioning**
  - Example: `/api/v1/users`, `/api/v1/content`
  - Simple, explicit, easy to manage.
- **Other options (for future)**:
  - Header-based versioning (`Accept: application/vnd.example.v1+json`)  
  - Query-parameter versioning (`?version=1`)  
- **Best practice**: Always increment version for **breaking changes** and keep old versions running until clients are migrated.

---

**Q3. What’s the minimum API surface for MVP?**  
- **Core endpoints only**:
  - **Authentication**: `/auth/login`, `/auth/logout`, `/auth/refresh`
  - **User management**: `/users`, `/users/{id}`
  - **Content CRUD**: `/content`, `/content/{id}`
  - **Search/filtering**: basic query parameters for content or users
  - **Data ingestion trigger**: if required by MVP features  
- **Optional / Phase 2**:
  - Advanced filtering, batch operations, analytics endpoints.
- **MVP goal**: only implement endpoints required to support early users and core workflows; everything else can be added in later iterations.

# 📥 Topic 5: Data Ingestion Pipeline

---

## What You’re Building

**Goal:** Create a pipeline that reliably imports research content from multiple sources into our knowledge graph / database for AI use.

**Core Steps for the Pipeline:**

1. **Accept Input**
   - **Sources:** File uploads (PDF, DOCX, CSV), URLs, external APIs.
   - **Validation:** Ensure file types, size limits, and proper authentication.
   - **Queueing:** Use a job queue (e.g., RabbitMQ, Redis Queue, or Celery) for asynchronous ingestion.

2. **Process Content**
   - **Text extraction:** Parse text from PDFs, Word docs, or HTML pages.
   - **Metadata extraction:** Capture author, timestamp, title, source URL, tags.
   - **Relationship identification:** Optional initial step for AI/graph later (links, references, citations).
   - **Data cleaning:** Remove duplicates, normalize formatting, and sanitize input.

3. **Store Data**
   - **Primary database:** PostgreSQL (or vector DB if embeddings are needed).  
   - **AI/graph usage:** Pre-process embeddings (optional pgvector or dedicated vector DB).  
   - **Storage options:**  
     - File storage for raw files (S3, local storage)  
     - Database for structured metadata and extracted text

---

## MVP Recommendation
- **Step 1:** Accept user uploads (PDF + DOCX) via a simple REST endpoint (`POST /ingest`).  
- **Step 2:** Extract text + basic metadata → store in PostgreSQL.  
- **Step 3:** Queue ingestion jobs for future processing (embeddings, AI enrichment).  
- **Optional:** Start simple with synchronous ingestion; switch to async queue once volume grows.

---

## Implementation Notes
- Use **Dockerized pipeline components** for local-first development.  
- Keep the pipeline **modular**: input → processing → storage → AI consumption.  
- Log every step for **debugging & auditing**.  
- Start with **single source ingestion**, expand to URLs and APIs in later phases.  

### Core Research Areas

---

### 🔹 Input Methods

Research and prototype ways to ingest data from multiple sources reliably. Focus on **handling different formats and integration points**.

---

#### 1. File Uploads
- **Supported file types**: PDF, DOCX, Markdown, CSV, JSON  
- **Batch processing**: Allow multiple files to be uploaded at once.  
- **Validation**:
  - Check file type and size.
  - Ensure correct encoding (UTF-8 or similar).  
- **Processing**:
  - Extract text from PDFs/Word/Markdown.
  - Parse structured data from CSV/JSON.
  - Normalize and sanitize data before storing.

---

#### 2. Web Content Ingestion
- **Single URL fetching**:
  - Fetch and parse HTML content.
  - Extract metadata (title, author, date, tags).  
- **RSS/Atom feed monitoring**:
  - Poll feeds periodically to ingest new content automatically.
- **Website crawling**:
  - Crawl limited pages for content (respect `robots.txt`).
  - Implement throttling to avoid overloading sites.
  - Optionally, use headless browsers if JavaScript-heavy pages need parsing.

---

#### 3. API Integrations
- **GitHub repositories**: Extract README, code comments, documentation.  
- **Notion exports**: Import pages, databases, and structured content.  
- **Google Drive documents**: PDFs, Docs, Sheets; handle permissions and OAuth.  
- **Academic paper APIs**: arXiv, PubMed, or other open-access APIs for research articles.  
  - Fetch metadata (title, authors, abstract, publication date) and full text when available.

### Processing Pipeline Architecture

**Simple queue-based approach (recommended for MVP)**

- **Flow:** User uploads/submits content → Queue → Processor → Database  
- **Queue implementation:** Use Redis, RabbitMQ, or even a database table for job management.  
- **Processing:** Start with **one item at a time** to simplify debugging.  
- **Scaling:** Add parallel processing later when throughput demands increase.  

**Key Decisions to Research**

- **Synchronous vs Asynchronous**:  
  - MVP: synchronous for small uploads is acceptable.  
  - Async queue recommended for larger files or multiple sources.  
- **Progress feedback:**  
  - Provide status updates (e.g., queued, processing, complete, error).  
  - Use polling or WebSocket notifications for frontend.  
- **Error handling & retries:**  
  - Retry failed jobs automatically (with exponential backoff).  
  - Log errors and alert for persistent failures.  
- **File size & rate limits:**  
  - Enforce limits to protect system resources.  
  - Reject oversized files gracefully with proper error messages.  

---

### Content Processing Steps

1. **Validation**
   - Check file format (PDF, DOCX, Markdown, CSV/JSON).  
   - Enforce size limits and encoding rules.  
   - Reject unsupported or corrupted files.  

2. **Extraction**
   - Pull text from documents, code, or web pages.  
   - Extract metadata: author, title, date, tags, source URL.  
   - Capture structural elements if relevant (headings, tables).  

3. **Enrichment**
   - Add additional info: timestamps, user ID, source information.  
   - Apply user-provided tags or categories.  
   - Optional: generate preliminary embeddings for AI/semantic search.  

4. **Storage**
   - Save structured content in **PostgreSQL** or another relational DB.  
   - Store raw files optionally in S3/minio or local volumes.  
   - Ensure data isolation per user (user_id) and integrity.  

5. **Indexing**
   - Prepare content for search and AI consumption.  
   - Create indexes for full-text search or vector embeddings.  
   - Ensure incremental updates do not overwrite existing processed content.  

---

#### MVP Recommendation
- Start with **synchronous, single-threaded queue** for uploads.  
- Focus on **basic validation → extraction → storage** workflow.  
- Enrichment and indexing can be **modular background jobs** to add later.  
- Keep logs and error reporting in place to troubleshoot ingestion issues quickly.  

### Integration with AI Pipeline

**Critical:** This connects ingestion to the AI/knowledge graph pipeline.

- **Text readiness:** Ensure all extracted text is clean, structured, and normalized for embedding generation.  
- **Metadata for RAG:** Capture necessary fields (source, author, timestamp, tags, user_id) to support retrieval-augmented generation.  
- **Content updates:** Implement versioning or update logic to avoid overwriting embeddings when content changes.  
- **Incremental processing:** Large documents or batches can be processed in chunks to prevent timeouts and memory issues.  

---

### Key Questions & Answers

**Q1: What’s the simplest way to handle file uploads reliably?**  
- Use **multipart HTTP POST endpoints** with validation for type and size.  
- Store files temporarily in a **staging directory** or Docker volume before processing.  
- Provide feedback to the user: accepted, rejected, queued for processing.  

**Q2: Should processing be real-time or batch?**  
- **MVP:** synchronous real-time for small files.  
- **Scaling:** asynchronous batch processing for larger files or high volume.  
- Job queue allows retries and parallelization without blocking API responses.  

**Q3: How to handle large files (>10MB PDFs)?**  
- Split processing into **chunks** (pages or sections).  
- Enforce **upload size limits** and provide user guidance for large files.  
- Use streaming extraction libraries (e.g., `pdfminer.six` or `PyMuPDF`) to reduce memory usage.  

**Q4: What happens when ingestion fails midway?**  
- Implement **retry strategies** with exponential backoff.  
- Log failure details and notify the user or admin.  
- Optionally, store **partial results** to avoid complete loss of work.  

**Q5: How to prevent duplicate content?**  
- Calculate **hashes or fingerprints** of text content.  
- Check existing records in DB/vector store before storing.  
- Consider versioning for updates rather than overwriting.  

**Q6: How to track where content came from (provenance)?**  
- Store **source metadata**: URL, file name, original repository, or API ID.  
- Track **user_id** and timestamp of ingestion.  
- Maintain **version history** for updates to the same content.  

---

#### MVP Recommendation
- Start with **real-time, small file ingestion** using a simple REST endpoint.  
- Store extracted text + metadata for AI/embedding pipelines.  
- Use **hashing + provenance metadata** to prevent duplicates and track sources.  
- Add **incremental/chunked processing** for large files as needed.  

### MVP Implementation Focus

For the initial implementation, prioritize simplicity and reliability to get a working ingestion pipeline fast.

1. **Simple file upload endpoint**
   - REST API: `POST /ingest`  
   - Accept multipart files, validate type and size.  
   - Return immediate acknowledgment (queued or processed).

2. **Basic queue**
   - Can use a **database table** as a simple job queue for MVP.  
   - Track job status: `queued`, `processing`, `completed`, `failed`.  
   - Support retry logic for failures.

3. **Supported formats**
   - Focus on **PDF, Markdown (MD), TXT, JSON** initially.  
   - Ensure extraction and metadata capture works reliably for these types.

4. **Progress indicator**
   - Simple progress tracking via API (`GET /ingest/status/{job_id}`).  
   - Show high-level status: queued, processing, done, failed.  
   - Optional: percentage completion for multi-step processing.

5. **User-friendly error messages**
   - Return clear messages if:
     - File type is unsupported
     - File exceeds size limits
     - Extraction fails
     - Queue or system error occurs
   - Avoid exposing internal system details.

---

#### MVP Goal
- Provide a **working ingestion pipeline** that can reliably handle small-to-medium files.  
- Make it **easy for users to understand status and errors**.  
- Keep pipeline **modular and extensible** for future enhancements (parallel processing, additional formats, AI embedding integration).  

# 🛠 Topic 6: Support Systems & Monitoring

---

## Essential Support Infrastructure

---

### 🔹 Logging
- **Application logs**: Capture key events, requests, and user actions.  
- **Error tracking**: Record stack traces, exceptions, and failed operations.  
- **Log aggregation**: Use a simple solution to centralize logs (e.g., local file + optional ELK stack or Loki for later).  
- **Structured logging**: Prefer JSON format to make logs machine-readable and searchable.  

---

### 🔹 Monitoring Basics
- **Health check endpoints**:
  - `/health` or `/status` returning service status.
  - Check app, database connections, and dependencies.  
- **Basic metrics**:
  - Response time, request rate, error rate, throughput.  
  - Can be collected with Prometheus, StatsD, or lightweight alternatives.  
- **Uptime monitoring**:
  - External service to ping endpoints and alert on downtime (UptimeRobot, Healthchecks.io).  
- **Database connection pooling**:
  - Monitor active connections to prevent exhaustion.  
  - Configure pool size and idle timeout appropriately for dev/prod.  

---

### 🔹 Development Tools
- **Local development setup**:
  - Docker Compose for databases, queue, API, and supporting services.  
  - Standard `.env` files for environment configuration.  
- **Seed data management**:
  - Scripts to populate test/development databases.  
  - Include default users, sample content, and metadata.  
- **Database migrations**:
  - Version-controlled migration scripts (Flyway, Liquibase, Alembic, or Django migrations).  
  - Ensure repeatable setup for dev, test, and prod.  
- **Environment management**:
  - Use `.env` or config files for dev/staging/prod.  
  - Keep secrets out of source control; use vault or docker secrets for prod.  

---

#### MVP Recommendation
- Implement **basic logging + structured errors** immediately.  
- Add a **health check endpoint** for API and database.  
- Start with **local dev setup using Docker Compose** and simple seed data.  
- Database migrations should be automated for reproducible environments.  
- Optional: basic metrics collection can be added once MVP endpoints are stable.  

### Key Questions & Answers

**Q1: What monitoring is essential from day one?**  
- **Health check endpoint** (`/health` or `/status`) to confirm API and database are reachable.  
- **Basic error logging** for API requests and background jobs.  
- **Uptime alerts** (simple external ping service like UptimeRobot or Healthchecks.io).  
- **Elaboration:** Full metrics dashboards can be added later; the MVP focus is detecting outages and critical failures quickly.

---

**Q2: How to balance local dev simplicity with production similarity?**  
- **Use Docker Compose** to replicate prod-like services locally (database, queue, API).  
- **Environment variables**: `.env` files for dev vs production.  
- **Seed data**: provide realistic but lightweight data for dev/testing.  
- **Elaboration:** Avoid overcomplicating local dev with full monitoring stacks initially; keep the core services aligned with production to reduce surprises.

---

**Q3: What’s the minimum observability needed?**  
- **MVP focus**:  
  - Basic logging of errors and important events.  
  - Health endpoint to confirm service and database status.  
  - Simple job status tracking for ingestion/queue systems.  
- **Elaboration:** Advanced metrics, dashboards, and alerting can be added incrementally after MVP to avoid slowing development.

# PHASE 2: INTELLIGENCE LAYER

## Topic 7: AI & Graph Database Integration

**Goal:** Build the foundation to store, process, and query AI embeddings and graph-based relationships.

---

### 🔹 Key Integration Areas

1. **Vector Database Setup**
   - Options: Pinecone, Weaviate, Qdrant, or PostgreSQL + pgvector.  
   - Run locally in Docker for development/testing.  
   - Configure indexes and storage for semantic embeddings.  
   - Research: performance and memory trade-offs between pgvector vs dedicated vector DB.

2. **Embedding Pipeline Integration**
   - Ensure extracted content from ingestion pipeline is ready for embedding generation.  
   - Integrate embedding generation as a background job or pipeline step.  
   - Store embeddings in vector database for semantic search/RAG (retrieval-augmented generation).  

3. **Graph Database Evaluation**
   - Options: Neo4j (Community Edition, Docker) vs PostgreSQL with recursive CTEs.  
   - Use case: capture relationships between content, authors, and citations.  
   - Research:
     - When dedicated graph DB improves query performance.
     - Whether recursive CTEs in PostgreSQL are sufficient for MVP graph queries.

4. **Search & Retrieval Optimization**
   - Integrate vector search with metadata filters.  
   - Support hybrid queries: full-text + vector search.  
   - Plan for incremental updates as new content is ingested.  

---

### 🔹 MVP Recommendation
- Start with **PostgreSQL + pgvector** for embeddings to keep infrastructure simple.  
- Graph relationships can be implemented with **PostgreSQL recursive CTEs** initially.  
- Ensure ingestion pipeline produces content suitable for embedding generation.  
- Evaluate dedicated vector DB or Neo4j later, only if scaling or performance requires it.  
