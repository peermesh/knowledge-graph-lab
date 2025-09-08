# Data Model

## Overview

The Knowledge Graph Lab data model represents the creator economy as a network of interconnected entities. Each entity type captures a different aspect of the ecosystem, and relationships between entities reveal patterns, opportunities, and insights that would be invisible in traditional databases. This document defines the complete schema that all four modules will use to ensure consistency across the system.

<!-- DIAGRAM NOTE: Add entity relationship diagram here showing all six entity types as nodes with their key relationships as edges. Use different colors for each entity type. -->

## Core Entity Types

### Platform

A Platform represents any digital service where creators produce, distribute, or monetize content. This includes video platforms like YouTube, subscription services like Patreon, newsletter tools like Substack, and social networks like Instagram. Platforms are the foundation of the creator economy infrastructure.

```
Platform {
  id: string (unique identifier, e.g., "platform_patreon_001")
  name: string (display name, e.g., "Patreon")
  website: string (primary URL, e.g., "https://patreon.com")
  category: enum ["video", "audio", "writing", "subscription", "marketplace", "social", "tools"]
  founded_date: date (when the platform launched)
  headquarters: string (primary location, e.g., "San Francisco, CA")
  creator_count: integer (estimated number of active creators)
  monthly_active_users: integer (platform reach)
  revenue_model: array ["ads", "subscription", "transaction_fee", "premium_features"]
  minimum_payout: decimal (smallest withdrawal amount)
  payout_frequency: enum ["daily", "weekly", "monthly", "on_demand"]
  api_available: boolean (whether platform offers developer API)
  last_updated: timestamp (when we last verified this data)
}
```

Example instance:
```
{
  id: "platform_patreon_001",
  name: "Patreon",
  website: "https://patreon.com",
  category: "subscription",
  founded_date: "2013-05-01",
  headquarters: "San Francisco, CA",
  creator_count: 250000,
  monthly_active_users: 8000000,
  revenue_model: ["subscription", "transaction_fee"],
  minimum_payout: 10.00,
  payout_frequency: "monthly",
  api_available: true,
  last_updated: "2025-09-08T10:00:00Z"
}
```

### Organization

An Organization represents any entity that supports, funds, advocates for, or studies creators. This includes creator funds, advocacy groups, research institutions, accelerators, and service providers. Organizations are the support infrastructure of the creator economy.

```
Organization {
  id: string (unique identifier, e.g., "org_creator_fund_001")
  name: string (official name, e.g., "YouTube Black Voices Fund")
  type: enum ["fund", "advocacy", "accelerator", "agency", "research", "education"]
  location: string (headquarters or primary location)
  website: string (primary URL)
  founding_year: integer (when established)
  focus_areas: array ["music", "gaming", "education", "diversity", "sustainability"]
  budget_range: enum ["<100k", "100k-1M", "1M-10M", "10M-100M", ">100M"]
  application_process: enum ["open_application", "invitation_only", "rolling", "cohort_based"]
  eligibility_criteria: object (structured requirements)
  contact_email: string (public contact)
  last_updated: timestamp
}
```

Example instance:
```
{
  id: "org_creator_fund_001",
  name: "YouTube Black Voices Fund",
  type: "fund",
  location: "Mountain View, CA",
  website: "https://www.youtube.com/creators/black-voices-fund/",
  founding_year: 2020,
  focus_areas: ["diversity", "music", "education"],
  budget_range: "10M-100M",
  application_process: "cohort_based",
  eligibility_criteria: {
    "min_subscribers": 1000,
    "geography": ["US", "UK", "Brazil", "Kenya", "Australia"],
    "content_type": "original",
    "identity": "Black creators and artists"
  },
  contact_email: "blackvoicesfund@youtube.com",
  last_updated: "2025-09-08T10:00:00Z"
}
```

### Person

A Person represents an individual creator, executive, investor, or other notable figure in the creator economy. People are tracked when they have significant influence, create notable content, or play key roles in organizations and platforms.

```
Person {
  id: string (unique identifier, e.g., "person_casey_001")
  name: string (public name)
  role: array ["creator", "executive", "investor", "advocate", "researcher"]
  primary_platform: string (where they're most active)
  follower_count: object (followers per platform)
  content_categories: array ["tech", "lifestyle", "gaming", "education", "comedy"]
  verified_accounts: object (platform: handle mapping)
  affiliations: array (organizations or companies)
  location: string (public location if available)
  bio: string (brief description)
  notable_achievements: array (major milestones)
  last_updated: timestamp
}
```

<!-- DIAGRAM NOTE: Add a network diagram here showing how a single Person entity connects to multiple Platforms, Organizations, and Events -->

### Grant

A Grant represents any funding opportunity available to creators. This includes direct grants, accelerator programs, creator funds, competitions, and sponsorship opportunities. Grants are time-sensitive entities that require careful tracking of deadlines and requirements.

```
Grant {
  id: string (unique identifier)
  name: string (official program name)
  provider_id: string (references Organization.id)
  amount_range: object {min: decimal, max: decimal, currency: string}
  deadline: date (application deadline)
  frequency: enum ["one_time", "annual", "quarterly", "rolling"]
  eligibility_requirements: object (structured criteria)
  application_url: string (where to apply)
  required_materials: array ["portfolio", "business_plan", "references", "video_pitch"]
  selection_process: string (how winners are chosen)
  past_recipients: array (notable previous winners)
  success_rate: decimal (percentage of applicants funded)
  geographic_restrictions: array (eligible countries/regions)
  status: enum ["upcoming", "open", "closed", "awarded"]
  last_updated: timestamp
}
```

### Policy

A Policy represents any law, regulation, platform rule, or industry standard that affects creators. This includes copyright laws, tax regulations, content guidelines, monetization policies, and data protection requirements. Policies shape what creators can do and how they operate.

```
Policy {
  id: string (unique identifier)
  title: string (official name or description)
  type: enum ["law", "regulation", "platform_policy", "industry_standard", "tax_code"]
  jurisdiction: string (where it applies)
  effective_date: date (when it takes effect)
  expiry_date: date (if temporary)
  summary: string (plain English explanation)
  full_text_url: string (link to complete policy)
  affected_entities: array (Platform/Organization ids affected)
  key_provisions: array (important points)
  enforcement_mechanism: string (how it's enforced)
  penalties: string (consequences for violation)
  status: enum ["proposed", "active", "repealed", "amended"]
  last_updated: timestamp
}
```

### Event

An Event represents any conference, workshop, competition, or gathering relevant to creators. Events are where the creator economy community connects, learns, and does business. They're time-bound entities that provide networking and learning opportunities.

```
Event {
  id: string (unique identifier)
  name: string (event name)
  type: enum ["conference", "workshop", "competition", "meetup", "online_summit"]
  start_date: datetime
  end_date: datetime
  location: string (physical address or "Online")
  virtual_option: boolean
  organizer_id: string (references Organization.id)
  expected_attendance: integer
  ticket_price: object {early_bird: decimal, regular: decimal, vip: decimal}
  speakers: array (references to Person.id)
  sponsors: array (references to Organization.id)
  topics: array ["monetization", "growth", "tools", "legal", "creativity"]
  registration_url: string
  status: enum ["upcoming", "ongoing", "completed", "cancelled"]
  last_updated: timestamp
}
```

## Relationship Types

<!-- DIAGRAM NOTE: Create a relationship matrix showing which entities can connect to which others, with relationship types labeled on the connections -->

### Platform Relationships

Platforms connect to almost every other entity type in the ecosystem. These relationships reveal competitive dynamics, integration opportunities, and creator migration patterns.

- **COMPETES_WITH** (Platform ↔ Platform): Direct competition for creators and users
- **INTEGRATES_WITH** (Platform ↔ Platform): Technical or business integration
- **HOSTS** (Platform → Person): Creator has active presence
- **FUNDS** (Platform → Grant): Platform provides grant opportunity
- **ENFORCES** (Platform → Policy): Platform implements specific policy

### Organization Relationships

Organizations provide the support structure for creators through funding, advocacy, and services.

- **FUNDS** (Organization → Grant): Organization provides grant
- **PARTNERS_WITH** (Organization ↔ Organization): Formal partnership
- **ADVOCATES_FOR** (Organization → Policy): Lobbies for policy change
- **ORGANIZES** (Organization → Event): Hosts or sponsors event
- **SUPPORTS** (Organization → Person): Provides resources to creator

### Person Relationships

People are at the center of the creator economy, connecting to platforms, organizations, and each other.

- **CREATES_ON** (Person → Platform): Active content creation
- **WORKS_AT** (Person → Organization): Employment or official role
- **FOUNDED** (Person → Platform/Organization): Founding relationship
- **SPEAKS_AT** (Person → Event): Speaking engagement
- **RECEIVED** (Person → Grant): Grant recipient

### Cross-Entity Relationships

Some relationships span multiple entity types, revealing complex ecosystem dynamics.

- **AFFECTS** (Policy → Platform/Organization/Person): Policy impact
- **ELIGIBLE_FOR** (Person → Grant): Meets grant requirements
- **LOCATED_IN** (Event → Location): Geographic relationship
- **REFERENCES** (Grant → Policy): Grant relates to policy
- **DISCUSSES** (Event → Policy/Platform): Event topic focus

## Data Quality Rules

### Validation Requirements

Every entity must pass validation before entering the knowledge graph. Module 2 enforces these rules during entity extraction and resolution.

Required fields must be non-null and properly formatted. URLs must be valid and accessible. Dates must be logical (founded_date before current date, deadline in future). References must point to existing entities. Enums must match defined values.

### Deduplication Strategy

The same real-world entity often appears in multiple data sources with slightly different information. Our deduplication process uses these signals:

First, we check exact matches on unique identifiers (website URLs, official names). Then we use fuzzy matching on names with edit distance <= 2. We verify geographic proximity for physical locations. We cross-reference social media handles and official accounts. Finally, we use temporal alignment to check if dates and timelines match.

### Update Policies

Different entity types have different freshness requirements. Platforms need weekly updates as features change frequently. Organizations need monthly updates unless major changes occur. People need updates when they change platforms or roles. Grants need immediate updates when deadlines approach. Policies need updates when status changes. Events need daily updates as they approach.

## Query Examples

<!-- DIAGRAM NOTE: Add a visual query builder diagram showing how to construct graph queries step by step -->

Here are common queries that demonstrate the power of our connected data model:

Finding opportunities for a specific creator:
```
MATCH (creator:Person {name: "Sarah Chen"})
-[:CREATES_ON]->(platform:Platform)
-[:HOSTS]->(grant:Grant)
WHERE grant.deadline > current_date
AND creator_meets_requirements(creator, grant.eligibility_requirements)
RETURN grant
```

Discovering platform partnerships:
```
MATCH (p1:Platform)-[:INTEGRATES_WITH]-(p2:Platform)
WHERE p1.category = "video" AND p2.category = "subscription"
RETURN p1, p2, integration_benefits
```

Tracking policy impacts:
```
MATCH (policy:Policy {type: "tax_code"})
-[:AFFECTS]->(platform:Platform)
-[:HOSTS]->(creator:Person)
WHERE creator.location IN policy.jurisdiction
RETURN creator, potential_impact
```

## Implementation Notes

Module 1 ingests raw data that contains references to these entities. Module 2 extracts entities from the raw data and resolves them to canonical forms in our schema. Module 3 uses the relationship graph to generate insights and recommendations. Module 4 visualizes the entities and relationships for user exploration.

The schema is designed to be extensible. New entity types can be added without breaking existing relationships. New relationship types can be created as we discover new connections. Attributes can be added to entities as we learn what information is valuable.

This data model is the foundation of Knowledge Graph Lab's intelligence. By representing the creator economy as a rich, interconnected graph rather than isolated tables, we enable discovery of non-obvious patterns and generation of novel insights.