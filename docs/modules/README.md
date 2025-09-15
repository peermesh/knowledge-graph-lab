# Knowledge Graph Lab Modules

This directory contains the implementation documentation for each module when the work is complete and ready for use.

For team documentation, assignments, and work instructions, see `/docs/team/modules/`.

## Core Modules

### AI Development
The intelligence layer of the Knowledge Graph Lab. Processes documents and extracts meaningful information using machine learning and natural language processing. Handles entity extraction, relationship mapping, confidence scoring, and document processing. Produces structured JSON data with entities, relationships, and embeddings.

**Technical Specification**: [AI-Development-Spec.md](ai-development/AI-Development-Spec.md)

### Backend Architecture
Provides the data infrastructure and API services that power the Knowledge Graph Lab. Manages data pipelines, REST endpoints, database storage, job queues, and vector embeddings. Built with PostgreSQL, Qdrant, Redis, FastAPI, and Docker.

**Technical Specification**: [Backend-Architecture-Spec.md](backend-architecture/Backend-Architecture-Spec.md)

### Frontend Design
Creates the user interface that makes the Knowledge Graph Lab accessible and useful. Provides knowledge graph visualization, search interface, dashboard views, user management, and data export. Built with React, D3.js, Redux, WebSocket, and Tailwind CSS.

**Technical Specification**: [Frontend-Design-Spec.md](frontend-design/Frontend-Design-Spec.md)

### Publishing Tools
Handles content distribution and communication with users. Transforms knowledge graph insights into newsletters, reports, and other shareable formats. Manages newsletter generation, content formatting, distribution, templates, and analytics tracking.

**Technical Specification**: [Publishing-Tools-Spec.md](publishing-tools/Publishing-Tools-Spec.md)

Each module works together to create the complete Knowledge Graph Lab system.