# API Specification

**Status**: Draft - To be completed during Week 2 planning
**Purpose**: Define the inter-module API contracts for the Knowledge Graph Lab system

## Overview
This document specifies the API contracts between the four modules, ensuring clean interfaces and independent operation.

## Module 1: Data Ingestion API
**Base URL**: `http://localhost:8001`

### Core Endpoints
- `GET /health` - Service health check
- `POST /api/ingest/url` - Ingest single URL
- `POST /api/ingest/bulk` - Bulk ingestion
- `GET /api/ingest/status/{job_id}` - Check ingestion status
- `GET /api/content` - Retrieve normalized content

## Module 2: Knowledge Graph API
**Base URL**: `http://localhost:8002`

### Core Endpoints
- `GET /health` - Service health check
- `POST /api/entities/extract` - Extract entities from text
- `POST /api/entities/resolve` - Resolve entity duplicates
- `GET /api/knowledge/query` - Query knowledge graph
- `POST /api/knowledge/search` - Search entities

## Module 3: Reasoning Engine API
**Base URL**: `http://localhost:8003`

### Core Endpoints
- `GET /health` - Service health check
- `GET /api/frontier/next` - Get next research items
- `POST /api/topics/cluster` - Cluster topics
- `POST /api/digest/generate` - Generate digest
- `POST /api/content/personalize` - Personalize content

## Module 4: Frontend API
**Base URL**: `http://localhost:3000`

### Core Endpoints
- Web interface serving
- WebSocket for real-time updates
- Static asset serving
- API gateway to backend services

## Inter-Module Communication
- Modules communicate via REST APIs
- Authentication via API keys (development)
- Rate limiting per module
- Error handling standards

## Details
To be developed based on Week 1 research findings.

## Next Steps
- Define detailed request/response schemas
- Establish error code standards
- Design authentication strategy
- Create API documentation
- Build mock servers for testing