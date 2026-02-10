# Knowledge Graph Lab - Complete Frontend Specification

## Executive Summary

Knowledge Graph Lab is an AI-powered research platform that transforms information chaos into actionable intelligence. The system automatically discovers opportunities, understands relationships between entities (organizations, people, grants, platforms), builds knowledge graphs, and delivers personalized insights.

**This is NOT a simple note-taking or RSS reader app.** This is an intelligent research system with:
- Entity and relationship visualization
- Knowledge graph exploration
- Personalized opportunity matching
- Multi-channel publishing with approval workflows
- Deep organizational intelligence

The interface must communicate sophistication and intelligence while remaining approachable.

---

## Core Value Proposition

Users waste 10+ hours weekly searching for opportunities across fragmented sources. Knowledge Graph Lab:

1. **Discovers** - Continuously monitors hundreds of sources
2. **Understands** - Builds knowledge graphs of relationships between entities
3. **Reasons** - Identifies patterns, predicts opportunities, calculates relevance
4. **Delivers** - Distributes personalized insights through preferred channels

---

## Target Users

### Primary: Content Creators
Gaming creators, YouTubers, TikTokers seeking grants, sponsorships, and partnerships. They need opportunities to find them, not the reverse.

### Secondary: Organizational Users
- **Multi-Channel Networks (MCNs)**: Managing 50-500 creators, need portfolio intelligence
- **Creator Agencies**: Representing 100-1000 creators, need competitive intelligence
- **Researchers**: Studying creator economy, need comprehensive data
- **Investors**: Tracking emerging platforms, need market intelligence

---

## System Architecture Context

The frontend connects to four backend modules:

1. **Data Ingestion** - Collects from RSS, APIs, websites, documents
2. **Knowledge Graph** - Stores entities, relationships, confidence scores
3. **AI Intelligence** - Extracts entities, maps relationships, generates insights
4. **Publishing** - Delivers content via email, notifications, social

The frontend must visualize and make interactive the intelligence these systems produce.

---

## Information Architecture

### Primary Navigation (5 Modes)

The application operates in five distinct modes, each serving a specific purpose in the user journey.

```
┌─────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE GRAPH LAB                       │
├─────────────┬─────────────┬─────────────┬─────────────┬─────┤
│  DISCOVER   │   EXPLORE   │   ORGANIZE  │   PUBLISH   │  ⚙  │
│   (Feed)    │   (Graph)   │   (Domains) │   (Queue)   │     │
└─────────────┴─────────────┴─────────────┴─────────────┴─────┘
```

#### 1. DISCOVER Mode
**Purpose**: Browse incoming findings, encounter new opportunities, expand research interests.

**Primary View**: Intelligent feed of findings with:
- Entity-rich cards showing extracted organizations, amounts, dates
- Relevance scores explaining why each finding matters to this user
- Relationship hints ("3 connections to entities you track")
- Quick actions for saving, sharing, dismissing

**Secondary Elements**:
- Suggestion cards for expanding research interests
- Trending topics and emerging patterns
- Filter by entity type, confidence level, recency

#### 2. EXPLORE Mode (Knowledge Graph Visualization)
**Purpose**: Navigate the knowledge graph, discover relationships, understand connections.

**Primary View**: Interactive graph visualization showing:
- Entity nodes (organizations, people, grants, platforms) as distinct shapes
- Relationship edges with labeled connections (funds, partners_with, competes_with)
- Confidence indicators on relationships
- Cluster detection for related entity groups

**Interaction Patterns**:
- Click node to see entity detail panel
- Double-click to expand connected entities
- Drag to reposition, scroll to zoom
- Search to locate specific entities
- Filter by entity type, relationship type, confidence threshold

**Graph Features**:
- Multiple layout algorithms (force-directed, hierarchical, radial)
- Time-based filtering (show relationships from specific periods)
- Path finding between entities
- Subgraph extraction for focused exploration

#### 3. ORGANIZE Mode
**Purpose**: Structure research interests, manage tracked entities, configure intelligence priorities.

**Primary View**: Hierarchical domain management with:
- Top-level research domains (e.g., "Creator Economy", "AI Regulation")
- Nested topics and sub-topics
- Tracked entities within each domain
- Finding counts and activity indicators

**Entity Management**:
- Pin specific entities to track closely
- Set alert thresholds for entity changes
- Configure relationship types to monitor
- Merge duplicate entities when detected

**Intelligence Configuration**:
- Priority levels for different domains
- Source preferences (academic, news, social)
- Confidence thresholds for alerts
- Update frequency preferences

#### 4. PUBLISH Mode
**Purpose**: Review pending publications, manage distribution channels, control what goes out.

**Primary View**: Approval queue with:
- Content preview showing exactly what will be published
- Destination indicators (email, Twitter, LinkedIn, etc.)
- Relevance explanation for why this was selected
- Source entity and relationship context

**Publication Controls**:
- Approve / Edit / Skip actions
- Bulk operations for efficiency
- Scheduling adjustments
- Destination overrides

**Channel Management**:
- Configure email digests (frequency, format, sections)
- Connect social accounts
- Set per-channel content rules
- View delivery analytics

#### 5. SETTINGS
**Purpose**: Account management, preferences, integrations.

**Sections**:
- Profile and account
- Notification preferences
- Connected accounts and integrations
- Data export and privacy
- API access (for power users)

---

## Detailed Screen Specifications

### DISCOVER Mode Screens

#### D1: Main Feed
```
┌──────────────────────────────────────────────────────────────┐
│ [Search...]                              [Filters ▼] [View ▼]│
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 🏢 TechArts Foundation                    98% relevance  │ │
│ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │ │
│ │ New $2M Digital Creator Grant Program                    │ │
│ │                                                          │ │
│ │ TechArts Foundation announced a $2M grant program        │ │
│ │ targeting digital creators with audiences 10K-100K...    │ │
│ │                                                          │ │
│ │ ENTITIES: TechArts Foundation · $2M · Gaming · Q1 2025   │ │
│ │ CONNECTIONS: → Twitch (partner) → 3 creators you follow  │ │
│ │                                                          │ │
│ │ [💾 Save] [🔗 Share] [📊 Explore] [✕ Dismiss]            │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 💡 EXPAND YOUR RESEARCH                                  │ │
│ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │ │
│ │ Based on your interest in gaming creators, you might     │ │
│ │ also want to track:                                      │ │
│ │                                                          │ │
│ │ [+ Esports Organizations] [+ Gaming Hardware] [+ VTubers]│ │
│ │                                                          │ │
│ │                                        [Not interested]  │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 📈 PATTERN DETECTED                       New trend      │ │
│ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │ │
│ │ 3 major platforms announced creator funds this week.     │ │
│ │ This suggests increased competition for creator talent.  │ │
│ │                                                          │ │
│ │ [View Pattern Analysis →]                                │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### D2: Finding Detail (Expanded/Modal)
```
┌──────────────────────────────────────────────────────────────┐
│ [← Back to Feed]                                    [✕ Close]│
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ TechArts Foundation Launches $2M Digital Creator Grant       │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                              │
│ SOURCE: TechCrunch · 2 hours ago · 94% confidence            │
│                                                              │
│ [Full article text with entity highlighting...]              │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ EXTRACTED ENTITIES                                      │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │ 🏢 TechArts Foundation    Organization    [View Graph]  │  │
│ │ 💰 $2,000,000             Funding Amount  [Compare]     │  │
│ │ 🎮 Gaming Creators        Target Audience [Track]       │  │
│ │ 📅 March 15, 2025         Deadline        [Add to Cal]  │  │
│ │ 🌍 North America          Geography       [Filter]      │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ DISCOVERED RELATIONSHIPS                                │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │ TechArts Foundation ──[partners_with]──► Twitch         │  │
│ │ TechArts Foundation ──[previously_funded]──► @Creator1  │  │
│ │ TechArts Foundation ──[similar_to]──► YouTube NextUp    │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ WHY THIS MATTERS TO YOU                    98% match    │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │ ✓ Your audience size (45K) is within target range       │  │
│ │ ✓ Gaming content matches grant focus                    │  │
│ │ ✓ TechArts funded 3 creators similar to your profile    │  │
│ │ ✓ Deadline is 6 weeks away (good lead time)             │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                              │
│ [Save to Domain ▼] [Explore in Graph] [Share] [Apply Now →]  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### EXPLORE Mode Screens

#### E1: Knowledge Graph View
```
┌──────────────────────────────────────────────────────────────┐
│ [🔍 Search entities...]    [Filters ▼] [Layout ▼] [Export]   │
├────────────────────────────────────────────┬─────────────────┤
│                                            │ ENTITY DETAIL   │
│                                            │ ━━━━━━━━━━━━━━━ │
│         ┌─────┐                            │                 │
│    ┌────│ You │────┐                       │ TechArts Found. │
│    │    └─────┘    │                       │ Organization    │
│    │               │                       │                 │
│ ┌──▼──┐         ┌──▼──┐                    │ Founded: 2018   │
│ │Grant│─────────│Platf│                    │ Type: Foundation│
│ │ A   │         │ orm │                    │ Sector: Arts    │
│ └──┬──┘         └──┬──┘                    │                 │
│    │               │                       │ RELATIONSHIPS   │
│    │    ┌─────┐    │                       │ → 12 grants     │
│    └────│Org A│────┘                       │ → 3 platforms   │
│         └─────┘                            │ → 47 creators   │
│              │                             │                 │
│         ┌────▼────┐                        │ RECENT ACTIVITY │
│         │Creator B│                        │ • New grant (2h)│
│         └─────────┘                        │ • Partner (1w)  │
│                                            │                 │
│ Legend:                                    │ [Track Entity]  │
│ ○ Organization  □ Grant  ◇ Platform        │ [Expand Graph]  │
│ △ Person  ─── funds  ─·─ partners          │ [View Findings] │
├────────────────────────────────────────────┴─────────────────┤
│ Showing 24 entities, 47 relationships │ Zoom: 100% │ Nodes: ○│
└──────────────────────────────────────────────────────────────┘
```

#### E2: Entity Deep Dive
```
┌──────────────────────────────────────────────────────────────┐
│ [← Back to Graph]                    TechArts Foundation     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ PROFILE                                                 │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │ Type: Non-profit Foundation                             │  │
│ │ Founded: 2018                                           │  │
│ │ Sector: Digital Arts, Creator Economy                   │  │
│ │ Total Funding Distributed: $12.4M                       │  │
│ │ Active Grant Programs: 3                                │  │
│ │ Confidence: 96% (12 sources)                            │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ RELATIONSHIP MAP                                        │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │                                                         │  │
│ │ FUNDS (12)           PARTNERS WITH (3)    SIMILAR TO(5) │  │
│ │ ├─ Creator Grant     ├─ Twitch            ├─ YouTube    │  │
│ │ ├─ Digital Arts      ├─ Adobe               NextUp     │  │
│ │ ├─ Gaming Fund       └─ Patreon           ├─ TikTok    │  │
│ │ └─ [+9 more]                                Creator    │  │
│ │                                             Fund       │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ TIMELINE                                                │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │ 2025-01 ● Announced $2M Creator Grant                   │  │
│ │ 2024-11 ○ Partnered with Twitch                         │  │
│ │ 2024-09 ○ Funded 15 creators in gaming vertical         │  │
│ │ 2024-06 ● Launched Digital Arts Accelerator             │  │
│ │ [Show earlier...]                                       │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ RELATED FINDINGS (24)                      [View All →] │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │ • TechArts Foundation Launches $2M Grant      2h ago    │  │
│ │ • Interview: TechArts on Creator Future       3d ago    │  │
│ │ • Grant Recipients Announced for Q4           2w ago    │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                              │
│ [🔔 Track This Entity] [📊 Compare] [📤 Export Data]         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### ORGANIZE Mode Screens

#### O1: Domain Management
```
┌──────────────────────────────────────────────────────────────┐
│ RESEARCH DOMAINS                    [+ New Domain] [Import]  │
├─────────────────────────────────────┬────────────────────────┤
│                                     │ DOMAIN DETAIL          │
│ ▼ Creator Economy           (124)   │ ━━━━━━━━━━━━━━━━━━━━━━ │
│   ├─ ▶ Grants & Funding      (45)   │                        │
│   │   ├─ Foundation Grants   (23)   │ Gaming Creators        │
│   │   ├─ Platform Programs   (18)   │ 34 findings · 12 entities│
│   │   └─ Government Support   (4)   │                        │
│   ├─ ▼ Gaming Creators       (34)   │ TRACKED ENTITIES       │
│   │   ├─ Esports             (12)   │ ┌────────────────────┐ │
│   │   ├─ Streaming            (8)   │ │🏢 Twitch      [📍] │ │
│   │   └─ Game Dev             (14)  │ │🏢 YouTube     [📍] │ │
│   ├─ ▶ Brand Partnerships    (28)   │ │💰 YT NextUp   [📍] │ │
│   └─ ▶ Platform Changes      (17)   │ │👤 MrBeast     [📍] │ │
│                                     │ └────────────────────┘ │
│ ▶ AI & Technology            (89)   │                        │
│ ▶ Market Intelligence        (56)   │ RECENT ACTIVITY        │
│ ▶ Competitor Tracking        (31)   │ • New grant detected   │
│                                     │   2 hours ago          │
│                                     │ • Entity updated       │
│                                     │   6 hours ago          │
│                                     │                        │
│                                     │ INTELLIGENCE SETTINGS  │
│                                     │ Priority: ●●●○○ High   │
│                                     │ Alerts: Immediate      │
│                                     │ Sources: All           │
│                                     │                        │
│                                     │ [Edit] [Archive]       │
├─────────────────────────────────────┴────────────────────────┤
│ 4 domains · 300 findings · 89 tracked entities               │
└──────────────────────────────────────────────────────────────┘
```

#### O2: Entity Tracking Configuration
```
┌──────────────────────────────────────────────────────────────┐
│ TRACKED ENTITIES                      [+ Add Entity] [Bulk]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 🏢 TechArts Foundation                        TRACKING   │ │
│ ├──────────────────────────────────────────────────────────┤ │
│ │ Alert on: [✓] New grants  [✓] Partnerships  [ ] News    │ │
│ │ Notify via: [✓] Feed  [✓] Email  [ ] Push               │ │
│ │ Threshold: Only high confidence (>80%)                   │ │
│ │ Related: Also track 2-hop connections                    │ │
│ │                                                          │ │
│ │ Last activity: 2 hours ago · 24 findings · 12 relations  │ │
│ │ [Configure ▼]                            [Stop Tracking] │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 💰 YouTube Creator Fund                       TRACKING   │ │
│ ├──────────────────────────────────────────────────────────┤ │
│ │ Alert on: [✓] Updates  [✓] Deadlines  [✓] Changes       │ │
│ │ Notify via: [✓] Feed  [✓] Email  [✓] Push               │ │
│ │                                                          │ │
│ │ ⚠️ Deadline in 14 days: Application closes March 1       │ │
│ │ [Configure ▼]                            [Stop Tracking] │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### PUBLISH Mode Screens

#### P1: Approval Queue
```
┌──────────────────────────────────────────────────────────────┐
│ PENDING PUBLICATIONS                    3 items · 2 channels │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 📧 EMAIL DIGEST                    Scheduled: Tomorrow 8AM│ │
│ ├──────────────────────────────────────────────────────────┤ │
│ │                                                          │ │
│ │ Subject: Your Weekly Creator Economy Briefing            │ │
│ │                                                          │ │
│ │ ┌────────────────────────────────────────────────────┐   │ │
│ │ │ PREVIEW                                            │   │ │
│ │ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │   │ │
│ │ │ 🔥 TOP OPPORTUNITY                                 │   │ │
│ │ │ TechArts Foundation: $2M Gaming Creator Grant      │   │ │
│ │ │ 98% match for your profile                         │   │ │
│ │ │                                                    │   │ │
│ │ │ 📊 THIS WEEK'S PATTERNS                            │   │ │
│ │ │ • 3 new creator funds announced                    │   │ │
│ │ │ • Twitch policy update affects monetization        │   │ │
│ │ │                                                    │   │ │
│ │ │ 🔗 12 more findings in your domains...             │   │ │
│ │ └────────────────────────────────────────────────────┘   │ │
│ │                                                          │ │
│ │ Personalization: Based on Gaming Creators domain         │ │
│ │ Recipients: you@email.com                                │ │
│ │                                                          │ │
│ │ [✓ Approve] [✏️ Edit] [⏰ Reschedule] [✕ Skip]            │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 🐦 TWITTER POST                    Scheduled: Today 2PM  │ │
│ ├──────────────────────────────────────────────────────────┤ │
│ │                                                          │ │
│ │ "🎮 New opportunity for gaming creators: TechArts        │ │
│ │ Foundation just announced a $2M grant program.           │ │
│ │                                                          │ │
│ │ Target: 10K-100K audience                                │ │
│ │ Deadline: March 15                                       │ │
│ │                                                          │ │
│ │ Details: [link]"                                         │ │
│ │                                                          │ │
│ │ Source: Finding #1247 · Generated by AI                  │ │
│ │                                                          │ │
│ │ [✓ Approve] [✏️ Edit] [⏰ Reschedule] [✕ Skip]            │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### P2: Channel Configuration
```
┌──────────────────────────────────────────────────────────────┐
│ PUBLISHING CHANNELS                         [+ Add Channel]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 📧 EMAIL DIGEST                              ●  ACTIVE   │ │
│ ├──────────────────────────────────────────────────────────┤ │
│ │ Frequency: Weekly (Sundays at 8 AM)                      │ │
│ │ Format: Full digest with top 5 opportunities             │ │
│ │ Domains: All tracked domains                             │ │
│ │ Approval: Review before sending                          │ │
│ │                                                          │ │
│ │ Stats: 94% open rate · 23% click rate · 12 sent          │ │
│ │                                                          │ │
│ │ [Configure] [Pause] [View History]                       │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 🐦 TWITTER                                   ●  ACTIVE   │ │
│ ├──────────────────────────────────────────────────────────┤ │
│ │ Account: @yourhandle                                     │ │
│ │ Auto-post: High-relevance opportunities only (>90%)      │ │
│ │ Frequency: Max 3 per day                                 │ │
│ │ Approval: Auto-approve (trusted)                         │ │
│ │                                                          │ │
│ │ Stats: 1.2K avg impressions · 45 posts                   │ │
│ │                                                          │ │
│ │ [Configure] [Pause] [Disconnect]                         │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 📱 PUSH NOTIFICATIONS                        ○  PAUSED   │ │
│ ├──────────────────────────────────────────────────────────┤ │
│ │ Triggers: Deadline reminders, breaking opportunities     │ │
│ │ Quiet hours: 10 PM - 8 AM                                │ │
│ │                                                          │ │
│ │ [Resume] [Configure]                                     │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Component Library

### Entity Components

#### EntityBadge
Compact display of an entity with type indicator.
```
Props: { entity: Entity, size: 'sm' | 'md' | 'lg', showConfidence?: boolean }

Variants by type:
- Organization: 🏢 blue background
- Person: 👤 green background  
- Grant/Funding: 💰 amber background
- Platform: 📱 purple background
- Date/Deadline: 📅 red background (if urgent)
- Amount: 💵 gray background
```

#### EntityCard
Detailed entity display for lists and grids.
```
Props: { entity: Entity, onTrack: fn, onExplore: fn, showRelationships?: boolean }

Displays:
- Entity type icon and name
- Key attributes (varies by type)
- Relationship count summary
- Confidence indicator
- Quick actions
```

#### RelationshipLine
Visual connection between entities.
```
Props: { from: Entity, to: Entity, type: RelationType, confidence: number }

Relationship types with distinct styling:
- funds → solid line, arrow
- partners_with → dashed line, bidirectional
- competes_with → dotted line, red tint
- similar_to → dotted line, gray
- mentions → thin line, gray
```

### Finding Components

#### FindingCard
Rich display of a finding with entity extraction.
```
Props: { finding: Finding, onSave: fn, onExplore: fn, onDismiss: fn }

Sections:
- Header: title, source, timestamp, confidence
- Body: summary with entity highlighting
- Entities: extracted entities as badges
- Relationships: discovered connections
- Relevance: why this matters to user (score + explanation)
- Actions: save, share, explore, dismiss
```

#### FindingDetail
Full finding view with all extracted data.
```
Props: { finding: Finding, onClose: fn }

Additional sections beyond FindingCard:
- Full text with entity annotations
- All extracted entities with confidence
- Relationship diagram
- Source metadata
- Similar findings
```

### Graph Components

#### GraphCanvas
Main knowledge graph visualization.
```
Props: { 
  entities: Entity[], 
  relationships: Relationship[],
  layout: 'force' | 'hierarchical' | 'radial',
  onNodeClick: fn,
  onNodeDoubleClick: fn,
  filters: GraphFilters
}

Features:
- Pan and zoom
- Node dragging
- Selection (single and multi)
- Hover tooltips
- Dynamic layout updates
```

#### GraphNode
Individual node in the graph.
```
Props: { entity: Entity, selected: boolean, highlighted: boolean }

Shape by type:
- Organization: rounded rectangle
- Person: circle
- Grant: diamond
- Platform: hexagon

Size by importance (connection count, relevance)
```

#### GraphControls
Toolbar for graph interaction.
```
Features:
- Layout selector
- Entity type filters
- Relationship type filters
- Confidence threshold slider
- Time range filter
- Search within graph
- Export options
```

### Publishing Components

#### PublicationCard
Preview of pending publication.
```
Props: { publication: Publication, onApprove: fn, onEdit: fn, onSkip: fn }

Shows:
- Channel indicator (email, twitter, etc.)
- Content preview
- Scheduling info
- Source finding/entity
- Personalization explanation
```

#### ChannelConfig
Configuration interface for a publishing channel.
```
Props: { channel: Channel, onUpdate: fn }

Settings vary by channel type:
- Email: frequency, format, sections, approval mode
- Social: account, frequency, auto-post rules
- Push: triggers, quiet hours
```

### Shared Components

#### ConfidenceIndicator
Visual display of AI confidence level.
```
Props: { confidence: number, showLabel?: boolean }

Display:
- 0-60%: Low (yellow)
- 60-80%: Medium (blue)
- 80-100%: High (green)
```

#### RelevanceScore
Why something matters to this user.
```
Props: { score: number, reasons: string[] }

Shows:
- Percentage match
- Expandable list of matching criteria
```

#### TimelineEvent
Single event in an entity or finding timeline.
```
Props: { event: TimelineEvent, isLatest: boolean }

Types:
- Finding discovered
- Relationship added
- Entity updated
- User action
```

---

## Data Types

```typescript
// Core entity types
type EntityType = 
  | 'organization' 
  | 'person' 
  | 'grant' 
  | 'platform' 
  | 'amount' 
  | 'date' 
  | 'location'
  | 'content_type';

interface Entity {
  id: string;
  type: EntityType;
  name: string;
  attributes: Record<string, any>; // Type-specific attributes
  confidence: number; // 0-1
  sourceCount: number;
  relationshipCount: number;
  lastUpdated: Date;
  firstSeen: Date;
}

// Relationship types
type RelationType = 
  | 'funds' 
  | 'funded_by'
  | 'partners_with' 
  | 'competes_with' 
  | 'similar_to'
  | 'mentions'
  | 'created_by'
  | 'targets'
  | 'requires';

interface Relationship {
  id: string;
  fromEntity: string;
  toEntity: string;
  type: RelationType;
  confidence: number;
  attributes: Record<string, any>;
  sources: string[]; // Finding IDs
  firstSeen: Date;
}

// Finding with extracted intelligence
interface Finding {
  id: string;
  title: string;
  summary: string;
  fullText?: string;
  source: {
    name: string;
    url: string;
    credibility: number;
  };
  timestamp: Date;
  extractedEntities: ExtractedEntity[];
  discoveredRelationships: Relationship[];
  relevanceScore: number;
  relevanceReasons: string[];
  domains: string[];
  confidence: number;
}

interface ExtractedEntity {
  entityId: string;
  mentions: TextSpan[];
  confidence: number;
}

interface TextSpan {
  start: number;
  end: number;
  text: string;
}

// Research domain structure
interface Domain {
  id: string;
  name: string;
  parentId: string | null;
  children: Domain[];
  trackedEntities: TrackedEntity[];
  findingCount: number;
  settings: DomainSettings;
}

interface TrackedEntity {
  entityId: string;
  alertOn: string[];
  notifyVia: string[];
  confidenceThreshold: number;
  trackRelated: boolean;
}

interface DomainSettings {
  priority: 1 | 2 | 3 | 4 | 5;
  alertMode: 'immediate' | 'digest' | 'none';
  sourcePreferences: string[];
}

// Publishing types
interface Publication {
  id: string;
  channel: ChannelType;
  content: PublicationContent;
  scheduledFor: Date;
  status: 'pending' | 'approved' | 'sent' | 'failed';
  sourceFindings: string[];
  personalization: PersonalizationInfo;
}

type ChannelType = 'email_digest' | 'email_alert' | 'twitter' | 'linkedin' | 'push';

interface PublicationContent {
  subject?: string;
  body: string;
  preview?: string;
  links: string[];
}

interface Channel {
  id: string;
  type: ChannelType;
  status: 'active' | 'paused' | 'disconnected';
  config: ChannelConfig;
  stats: ChannelStats;
}

// User and preferences
interface User {
  id: string;
  email: string;
  name: string;
  profile: UserProfile;
  preferences: UserPreferences;
}

interface UserProfile {
  contentTypes: string[];
  audienceSize?: number;
  platforms: string[];
  goals: string[];
  location?: string;
}

interface UserPreferences {
  defaultDomain: string;
  graphLayout: 'force' | 'hierarchical' | 'radial';
  confidenceThreshold: number;
  digestFrequency: 'daily' | 'weekly' | 'monthly';
  timezone: string;
  notifications: NotificationPrefs;
}
```

---

## Interaction Patterns

### Graph Navigation
1. **Click** entity node → Show detail panel
2. **Double-click** entity node → Expand to show connected entities
3. **Right-click** entity node → Context menu (track, explore, hide)
4. **Drag** node → Reposition (persists in layout)
5. **Scroll** → Zoom in/out
6. **Drag** background → Pan
7. **Shift+click** → Multi-select nodes
8. **Cmd/Ctrl+click** relationship → Highlight path

### Finding Actions
1. **Click** finding card → Expand inline or open detail modal
2. **Long-press** / **Right-click** → Context menu
3. **Swipe right** (mobile) → Save to default domain
4. **Swipe left** (mobile) → Dismiss
5. **Click** entity badge in finding → Navigate to entity detail
6. **Click** "Explore" → Open finding entities in graph view

### Publishing Workflow
1. **Review** generated content in preview
2. **Edit** if needed (opens editor)
3. **Approve** to confirm scheduling
4. **Reschedule** to change timing
5. **Skip** to cancel without sending

### Keyboard Shortcuts
```
Global:
  1-5     Switch between modes
  /       Focus search
  ?       Show keyboard shortcuts
  Esc     Close modal/panel

Discover:
  j/k     Next/previous finding
  s       Save to domain
  e       Explore in graph
  x       Dismiss

Explore (Graph):
  +/-     Zoom in/out
  r       Reset view
  f       Fit all nodes
  l       Toggle labels

Organize:
  n       New domain
  Enter   Open selected
  Delete  Remove selected

Publish:
  a       Approve
  e       Edit
  s       Skip
```

---

## Visual Design System

### Color Palette

**Entity Type Colors:**
```
Organization: #3B82F6 (blue-500)
Person:       #10B981 (emerald-500)
Grant:        #F59E0B (amber-500)
Platform:     #8B5CF6 (violet-500)
Date:         #EF4444 (red-500) when urgent, #6B7280 otherwise
Amount:       #6B7280 (gray-500)
Location:     #06B6D4 (cyan-500)
```

**Confidence Indicators:**
```
High (80-100%):   #10B981 (emerald)
Medium (60-80%):  #3B82F6 (blue)
Low (0-60%):      #F59E0B (amber)
```

**Relationship Types:**
```
funds:         #10B981 solid
partners_with: #3B82F6 dashed
competes_with: #EF4444 dotted
similar_to:    #6B7280 dotted
mentions:      #D1D5DB thin
```

### Typography
```
Display:    Font for headings, entity names
Body:       Font for content, descriptions
Mono:       Font for data, numbers, IDs

Sizes:
- Heading 1: 24px / 32px line-height
- Heading 2: 20px / 28px
- Heading 3: 16px / 24px
- Body:      15px / 24px
- Small:     13px / 20px
- Caption:   11px / 16px
```

### Spacing System
```
Base unit: 4px

xs:  4px
sm:  8px
md:  16px
lg:  24px
xl:  32px
2xl: 48px
```

### Component Styling

**Cards:**
```
- Background: white (dark: gray-900)
- Border: 1px solid gray-200 (dark: gray-700)
- Border radius: 8px
- Shadow: sm on hover
- Padding: 16px-24px depending on size
```

**Entity Badges:**
```
- Border radius: 9999px (pill)
- Padding: 4px 12px
- Font size: 13px
- Background: entity type color at 10% opacity
- Text: entity type color at 100%
- Border: 1px solid entity type color at 20%
```

**Graph Nodes:**
```
- Organization: 40x24px rounded rectangle
- Person: 28px circle
- Grant: 32px diamond
- Platform: 32px hexagon
- Stroke: 2px
- Fill: entity color at 80%
- Selected: 3px stroke, color at 100%
```

---

## Responsive Behavior

### Breakpoints
```
Mobile:  < 640px
Tablet:  640px - 1024px
Desktop: > 1024px
```

### Mobile Adaptations

**Navigation:**
- Bottom tab bar with 5 icons
- Active mode fills tab
- Settings in hamburger menu

**Discover:**
- Full-width cards
- Swipe gestures for quick actions
- Sticky filter bar at top

**Explore (Graph):**
- Simplified graph view
- Tap to select, tap again for detail
- Two-finger pinch to zoom
- Entity detail as bottom sheet

**Organize:**
- Full-width domain list
- Swipe to reveal actions
- Detail view pushes as new screen

**Publish:**
- Card stack with swipe to approve/skip
- Bottom sheet for editing

### Tablet Adaptations
- Side navigation visible but collapsible
- Two-column layouts where appropriate
- Graph with split view (graph + detail panel)

### Desktop Enhancements
- Keyboard shortcuts enabled
- Right-click context menus
- Hover states and tooltips
- Multi-panel layouts
- Drag and drop

---

## State Management

### Global State
```typescript
interface AppState {
  // User
  user: User | null;
  isAuthenticated: boolean;
  
  // Current view
  activeMode: 'discover' | 'explore' | 'organize' | 'publish' | 'settings';
  
  // Discover
  findings: Finding[];
  findingsLoading: boolean;
  findingsFilter: FindingsFilter;
  
  // Explore
  graphEntities: Entity[];
  graphRelationships: Relationship[];
  selectedEntity: Entity | null;
  graphLayout: GraphLayout;
  graphFilters: GraphFilters;
  
  // Organize  
  domains: Domain[];
  selectedDomain: Domain | null;
  trackedEntities: TrackedEntity[];
  
  // Publish
  pendingPublications: Publication[];
  channels: Channel[];
  publishHistory: Publication[];
  
  // UI
  modals: ModalState[];
  toasts: Toast[];
  sidePanel: SidePanelState | null;
}
```

### Persistence
- User preferences → localStorage + server sync
- Domain structure → server
- Graph view settings → localStorage
- Draft publications → localStorage until sent

---

## API Integration Points

### Endpoints Required

```
// Authentication
POST   /auth/login
POST   /auth/logout
GET    /auth/me

// Findings
GET    /findings
GET    /findings/:id
POST   /findings/:id/save
POST   /findings/:id/dismiss

// Entities
GET    /entities
GET    /entities/:id
GET    /entities/:id/relationships
POST   /entities/:id/track
DELETE /entities/:id/track

// Graph
GET    /graph/subgraph?entities=...
GET    /graph/paths?from=...&to=...
GET    /graph/clusters

// Domains
GET    /domains
POST   /domains
PUT    /domains/:id
DELETE /domains/:id
POST   /domains/:id/entities

// Publishing
GET    /publications/pending
POST   /publications/:id/approve
POST   /publications/:id/skip
PUT    /publications/:id
GET    /channels
PUT    /channels/:id

// Search
GET    /search?q=...&type=...
GET    /search/suggest?q=...
```

### Real-time Updates
WebSocket connection for:
- New findings matching tracked criteria
- Entity updates
- Publication status changes
- Deadline reminders

---

## Onboarding Flow

### Step 1: Welcome
"Knowledge Graph Lab transforms information chaos into actionable intelligence."

Brief value prop with key differentiators.

### Step 2: Profile Setup
- What type of content do you create?
- What's your approximate audience size?
- What platforms are you active on?

### Step 3: Initial Interests
"What do you want to stay informed about?"

- Preset categories to select (Grants, Brand Partnerships, Platform Changes, etc.)
- Free text input for specific interests
- System suggests related topics

### Step 4: First Tracked Entities
"Here are some entities we think you should track based on your interests."

- Show 5-10 suggested entities with explanations
- Let user approve/dismiss each
- Option to search for specific entities

### Step 5: Publishing Setup
"How do you want to receive intelligence?"

- Email digest frequency
- Push notification preferences
- Social media connections (optional)

### Step 6: First Finding
Show a high-relevance finding with full UI, explaining each section.

---

## Definition of Done

### The prototype is complete when:

**Discover Mode:**
- [ ] Feed displays findings with entity extraction visible
- [ ] Relevance scores explain why each finding matters
- [ ] Suggestion cards appear and function
- [ ] Findings can be saved to domains
- [ ] Entity badges are clickable, navigate to explore

**Explore Mode:**
- [ ] Knowledge graph renders with proper node shapes by type
- [ ] Relationships display with appropriate styling
- [ ] Clicking nodes shows detail panel
- [ ] Double-clicking expands connected entities
- [ ] Filters work (entity type, relationship type, confidence)
- [ ] Search locates specific entities
- [ ] Layout can be changed

**Organize Mode:**
- [ ] Domain tree with infinite nesting
- [ ] CRUD operations on domains
- [ ] Entity tracking configuration
- [ ] Alert settings per domain

**Publish Mode:**
- [ ] Pending publications queue
- [ ] Content preview accurate to destination
- [ ] Approve/edit/skip actions work
- [ ] Channel configuration functional
- [ ] History of sent publications viewable

**Cross-Cutting:**
- [ ] Navigation between all 5 modes
- [ ] Entity-to-entity navigation works across modes
- [ ] Responsive on mobile and desktop
- [ ] Loading, empty, and error states
- [ ] Keyboard shortcuts function
- [ ] State persists across sessions

---

## What This Is NOT

This specification describes a sophisticated intelligence platform, not:

- ❌ A simple RSS reader
- ❌ A generic note-taking app
- ❌ A basic task manager
- ❌ A standard dashboard with charts

The UI must convey:
- Intelligence and insight generation
- Entity and relationship understanding
- Personalized relevance
- Professional-grade research capabilities

Every screen should make users feel like they have a team of research analysts working for them.
