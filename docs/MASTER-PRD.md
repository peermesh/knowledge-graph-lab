# Knowledge Graph Lab - Master PRD v1.1

**Project**: Knowledge Graph Lab (PeerMesh Module Demo)  
**Location**: `projects.peermesh.com/knowledge-graph-lab`  
**Timeline**: 10 weeks × 4 interns × 10 hours/week = 400 total hours  
**Team**: 4 developer interns, 1 project lead  
**Version**: 1.1 (integrates original PeerMesh vision)

## 1. Vision & Problem Statement

### The Bigger Vision: Intelligent Knowledge Systems
Imagine a world where research and knowledge discovery is not a manual slog through countless articles, websites, and databases. Instead, AI agents continuously explore domains of knowledge, building rich interconnected maps of everything worth knowing in a field. These systems don't just collect data—they understand relationships, identify gaps, predict what's important to research next, and synthesize insights for humans who need to stay informed.

**Knowledge Graph Lab is the first working demonstration of this vision.**

### What We're Building
A complete end-to-end intelligent research system that:

**🔍 Discovers**: AI agents autonomously explore the creator economy landscape, finding platforms, organizations, grants, policies, events, and people that matter. The system grows its own understanding of what exists and what's worth investigating further.

**🧠 Understands**: Advanced entity resolution and knowledge graph construction turn raw data into rich, interconnected knowledge. The system knows that "Patreon" the company, "patreon.com" the platform, and "@patreon" the social account are all connected. It understands relationships like "Creator X uses Platform Y" and "Policy Z affects Platform A."

**📊 Reasons**: Intelligent frontier queues decide what to research next based on user interests, knowledge gaps, and emerging trends. Topic clustering reveals new research directions. The system doesn't just collect—it thinks about what matters.

**📧 Synthesizes**: Personalized digests transform knowledge into actionable insights. Users receive customized newsletters about creator economy developments that matter to their specific interests and goals.

**🌐 Publishes**: Multi-channel publishing distributes insights across email, social media, and web platforms, ensuring valuable knowledge reaches the right audiences.

### The PeerMesh Demonstration
This project showcases PeerMesh's core thesis: **complex systems are best built as independent, composable modules** that can work alone or together.

Each of our 4 modules demonstrates a different aspect of PeerMesh architecture:
- **Modular Independence**: Each module provides value on its own
- **Clean Interfaces**: Modules communicate through well-defined APIs
- **Horizontal Scalability**: New domains can be added via "Packs" without rebuilding
- **Educational Value**: Interns learn real-world modular system design

### Problems We're Solving

**For PeerMesh**: Prove that modular architecture can handle complex, AI-driven systems while remaining comprehensible to developers.

**For Knowledge Workers**: End the cycle of manual research, bookmark chaos, and information overload. Provide intelligent systems that stay on top of fast-moving fields so humans can focus on higher-level thinking and decision-making.

**For the Creator Economy**: Create the first comprehensive, continuously-updated knowledge base of the creator landscape—platforms, funding opportunities, policy changes, advocacy groups, and emerging trends that creators need to know about.

### Success Criteria
- **Technical Demonstration**: 4 independent modules that each show value, plus seamless integration
- **PeerMesh Validation**: Prove modular architecture works for complex AI systems  
- **Educational Impact**: Interns gain experience building professional, modular systems
- **Domain Extensibility**: Architecture supports multiple knowledge domains (creator economy, investment research, AI tracking, competitive intelligence)
- **Real Utility**: System generates genuinely useful knowledge and insights for end users

## 2. Product Architecture

### Four PeerMesh Module Slices

#### Module 1: Ingestion & Adapters (40 hours)
**Owner**: Data/Backend intern  
**Purpose**: PeerMesh data acquisition and normalization

**Core Deliverables**:
- Source adapters (Perplexity API, RSS, basic web scraping)
- Data normalization and cleaning pipeline  
- Rate limiting and ethical scraping (robots.txt respect)
- FastAPI endpoints for data ingestion
- Docker containerization

**Independent Demo**: "Here's data being ingested from multiple sources and normalized into our schema"

#### Module 2: Knowledge Graph & Entity Resolution (40 hours)
**Owner**: AI/ML intern  
**Purpose**: PeerMesh knowledge organization and entity management

**Core Deliverables**:
- Creator economy schema design (Platform, Organization, Person, Grant, Policy, Event)
- Named Entity Recognition (NER) and entity linking
- Basic entity deduplication and resolution
- SQLite knowledge graph with relationship management
- Domain "Pack" system (pluggable schemas for different domains)

**Independent Demo**: "Here's our knowledge graph showing connected entities with relationship discovery"

#### Module 3: Reasoner & Content Generation (40 hours)
**Owner**: AI/Logic intern  
**Purpose**: PeerMesh intelligence and content synthesis

**Core Deliverables**:
- Frontier queue system (decides what to research next)
- Topic clustering and discovery algorithms
- Digest generation from knowledge base
- Email newsletter templating system
- Basic social media content generation

**Independent Demo**: "Here's the system deciding what to research and generating personalized content"

#### Module 4: Frontend & User Experience (40 hours)
**Owner**: Frontend intern  
**Purpose**: PeerMesh user interaction and publishing interfaces

**Core Deliverables**:
- Next.js 14 + Tailwind + shadcn/ui interface
- User authentication and preference management
- Knowledge vault explorer with search
- Publishing dashboard (email + social posting)
- Subscription management and unsubscribe flows

**Independent Demo**: "Here's users exploring knowledge, setting preferences, and managing publications"

## 3. Shared Dependencies

### Critical Shared Components (Week 1-2 Priority)
- **Database schema** (initially Supabase free tier)
- **Authentication system** (Supabase Auth)
- **Basic user management**
- **Synthetic/seed data** for development and testing
- **API contracts** between modules

### Technology Stack (Based on Original PeerMesh Architecture)
- **Database**: SQLite + LiteFS (simple, portable, scalable)
- **Vector Store**: Qdrant (Docker container)
- **Backend**: FastAPI + Python (async, typed, fast)
- **Frontend**: Next.js 14 + Tailwind CSS + shadcn/ui
- **Containerization**: Docker + Docker Compose
- **Email**: MailHog (dev) → configurable SMTP (prod)
- **Search**: Basic vector similarity + SQLite FTS
- **Authentication**: Magic links or simple JWT

## 4. Timeline & Process

### Week 1: Research & Discovery
Each intern researches their domain and proposes approach:
- **Systems**: Local development setup + deployment options
- **AI/Knowledge**: Creator economy data model + import strategies  
- **Publishing**: Email/social platform APIs + content workflows
- **Frontend**: User interface patterns + authentication flows

**Deliverable**: 1-page research brief per intern

### Week 2: Planning & Design
Create detailed specifications:
- **PDD** (Problem Definition Document) per module
- **PRD** (Product Requirements Document) per module  
- **API contracts** between modules finalized
- **Database schema** locked
- **Integration plan** defined

**Deliverable**: Technical specifications that enable parallel development

### Weeks 3-9: Development (7 weeks)
Parallel module development with:
- **Monday**: Weekly planning and status
- **Friday**: Demo what's working (required, no exceptions)
- **Continuous**: Integration testing as APIs become available

**Deliverable**: Working modules with weekly progress demos

### Week 10: Integration & Demo Day
- **Integration**: Connect all modules for end-to-end flow
- **Demo preparation**: Each intern prepares 5-minute demo
- **Final presentation**: Individual demos + integrated walkthrough
- **Retrospective**: What worked, what didn't, what's next

**Deliverable**: Complete working system + individual portfolio pieces

## 5. Independence Requirement

### Critical Constraint
Each module MUST be demonstrable without the others. This means:

- **Systems**: Can show deployment pipeline with hello-world services
- **AI/Knowledge**: Can import data and serve API responses with Postman/curl
- **Publishing**: Can send emails and post to social with sample content
- **Frontend**: Can show UI workflows with mock/static data

### Why This Matters
- **Risk mitigation**: If one intern falls behind, others can still succeed
- **Portfolio value**: Each intern has a complete working system to show
- **Learning focus**: Forces proper API design and modular thinking
- **Demo day insurance**: Multiple successful demos vs. all-or-nothing integration

## 6. Scope Management

### In Scope (MVP)
- **PeerMesh Module Demo**: 4 modules working independently + integrated
- **Creator Economy Pack**: Initial domain with platforms, organizations, creators, policies
- **Basic AI Pipeline**: NER, entity linking, content generation
- **Multi-channel Publishing**: Email newsletters + 2 social platforms
- **Knowledge Graph**: Entity relationships with basic reasoning
- **Domain Pack System**: Pluggable schemas for different research domains

### Explicitly Out of Scope (Future Versions)  
- **Heavy Crawling**: Large-scale web scraping (use APIs + targeted scraping)
- **Multi-Agent Chat**: Complex conversational AI interfaces
- **Real-time Collaboration**: Multiple users editing simultaneously
- **Advanced ML**: Custom model training (use existing APIs/models)
- **Multi-tenant**: Organization/team separation (single workspace)

### Domain Packs (Future Extensibility)
**Pack #1 (MVP)**: Creator Economy (platforms, creators, grants, policies, events)
**Pack #2 (Future)**: Investment Research (companies, opportunities, markets, regulations)
**Pack #3 (Future)**: AI Research Tracking (papers, researchers, techniques, datasets)
**Pack #4 (Future)**: Competitive Intelligence (competitors, products, strategies, news)

## 7. Success Metrics

### Technical Success
- [ ] All 4 modules demonstrate core functionality independently
- [ ] End-to-end integration flow works (research → knowledge → publication)
- [ ] Code quality allows for future extension
- [ ] System can be deployed and run by external users

### Educational Success  
- [ ] Each intern gains experience with professional development practices
- [ ] Interns can explain their design decisions and trade-offs
- [ ] Portfolio-quality work suitable for job applications
- [ ] Understanding of how systems integrate in larger applications

### Project Success
- [ ] Validates core Knowledge Graph Lab concepts with working prototype
- [ ] Identifies what works/doesn't work for future development
- [ ] Creates foundation for potential continued development
- [ ] Demonstrates value of structured knowledge management

## 8. Risk Management

### Top Risks
1. **Shared dependency bottlenecks** → Prioritize shared components Week 1-2
2. **API integration complexity** → Choose tools based on API simplicity  
3. **Scope creep** → Lock MVP definition, use parking lot for enhancements
4. **Skill level mismatches** → Provide support materials and adjust scope as needed
5. **Integration failures in Week 10** → Ensure independent demos work first

### Mitigation Strategy
- **Independence requirement** ensures partial success even with failures
- **Weekly demos** catch problems early
- **Locked technology stack** prevents decision paralysis
- **Clear MVP definition** prevents scope expansion
- **Parking lot process** captures good ideas for future without disrupting current work

---

## Next Steps
1. **Review and approve** this PRD with project stakeholders
2. **Create Week 1 research assignments** based on this scope
3. **Set up project infrastructure** (GitHub, communication channels)
4. **Schedule kickoff meeting** with all interns
5. **Begin iterative refinement** based on intern feedback and research findings

---

*This PRD will evolve throughout the project. All changes will be tracked and communicated to the full team.*