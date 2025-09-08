# Data Model

**Status**: Draft - To be completed during Week 2 planning
**Purpose**: Define the core entity schema and relationships for the Knowledge Graph Lab

## Overview
This document outlines the basic entity schema for the creator economy knowledge graph, including core entities, their attributes, and relationships.

## Core Entities

### Platform
- **Attributes**: name, website, category, founded_date, headquarters
- **Key Relationships**: COMPETES_WITH, INTEGRATES_WITH, SERVES_CREATORS

### Organization
- **Attributes**: name, type, location, website, founding_year
- **Key Relationships**: FUNDS, PARTNERS_WITH, ADVOCATES_FOR

### Person
- **Attributes**: name, role, affiliations, social_handles
- **Key Relationships**: WORKS_AT, FOUNDED, ADVISES, CREATES_ON

### Grant
- **Attributes**: name, amount, deadline, eligibility, provider
- **Key Relationships**: OFFERED_BY, ELIGIBLE_FOR, REQUIRES

### Policy
- **Attributes**: title, jurisdiction, effective_date, summary
- **Key Relationships**: AFFECTS, ENACTED_BY, SUPERCEDES

### Event
- **Attributes**: name, date, location, type, organizer
- **Key Relationships**: HOSTED_BY, FEATURES, LOCATED_IN

## Relationship Types
- COMPETES_WITH (bidirectional)
- PARTNERS_WITH (bidirectional)
- FUNDS (directional)
- INTEGRATES_WITH (bidirectional)
- OPERATES (directional)

## Details
To be developed based on Week 1 research findings.

## Next Steps
- Review entity extraction research
- Define attribute validation rules
- Establish relationship constraints
- Design data quality metrics
- Create sample data for testing