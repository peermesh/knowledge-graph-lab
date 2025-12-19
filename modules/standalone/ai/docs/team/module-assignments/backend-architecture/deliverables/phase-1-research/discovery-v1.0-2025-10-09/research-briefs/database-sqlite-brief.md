# Research Brief: MVP Database (SQLite)

**Source:** component-map.md (MVP-1), decisions-made.md (Decision 1), requirements-notes.md

## Context

Backend MVP stores three types of structured data:
- **Sources:** RSS feed URLs, types, status, last_checked timestamps
- **Content:** Title, text, URL, fetched_at, source_id (foreign key)
- **Entities:** Mock data for MVP (real entity extraction later)

**Data model:** Simple relational schema with foreign keys, no complex joins
**Transactions:** Basic ACID for data integrity (prevent duplicate fetches)
**Scale:** MVP targets 5 RSS feeds, 100+ content items, single-user development

## Requirements (Criteria, Not Brands)

- **File-based database:** REQUIRED - no separate database server
- **Zero configuration:** REQUIRED - works out of box, no setup
- **SQLAlchemy compatible:** REQUIRED - Python ORM integration
- **ACID transactions:** REQUIRED - data integrity for feed fetches
- **Docker compatible:** REQUIRED - runs in container, persists to volume
- **Migration support:** PREFERRED - version-controlled schema changes
- **Full-text search:** OPTIONAL - not needed for MVP
- **JSON storage:** OPTIONAL - structured columns sufficient
- **Horizontal scaling:** OUT OF SCOPE - single instance only

**Expected scale:**
- Records: 100-500 content items
- Concurrent connections: 1-5 (local development)
- Queries per second: <10 (low traffic MVP)
- Latency: <200ms for simple queries

## Constraints

- **Budget:** Open-source only (100-hour junior developer MVP)
- **Team expertise:** SQL familiar (junior developer comfort level)
- **Timeline:** Must work immediately (no learning curve)
- **Platform:** Must run in Docker container, file-based persistence
- **Simplicity:** Minimize moving parts (no separate DB server)
- **Portability:** Easy to replace with PostgreSQL later (SQLAlchemy abstracts)

## Research Objectives

Find file-based relational databases for Python MVP that:
1. Work with SQLAlchemy ORM
2. Require zero configuration/setup
3. Support basic ACID transactions
4. Run in Docker containers
5. Allow easy migration to production database later

For each option, document:
- Setup complexity (target: single import statement)
- SQLAlchemy compatibility and ORM features
- Docker volume persistence patterns
- Migration path to PostgreSQL
- Known limitations for production scale

## Output Format

Comparison matrix of file-based databases (SQLite, DuckDB, etc.) ranked by:
1. Setup simplicity
2. SQLAlchemy compatibility
3. Migration path to production DB
4. Community support

Recommendation: Which database for 100-hour MVP, with rationale.
