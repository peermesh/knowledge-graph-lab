# KGL Implementation Planning Example

**Date**: September 8, 2025 11:45  
**Tool**: Claude Code  
**Purpose**: Concrete example of journey → stories → implementation for intern team

---

## Process Example: Grant Discovery Journey

**This document shows exactly how to apply the product development process to the Grant Discovery user journey, creating a template the intern team can follow for all features.**

---

## Step 1: Journey Analysis → Technical Requirements

### Selected Journey Step
**From Grant Discovery Journey, Step 4:**
> **Action**: Uses filters for amount ($10k-$20k), deadlines (next 6 months), eligibility (individual creators)  
> **Emotion**: 🙂 Relief - "Now we're getting somewhere"  
> **System Response**: Shows 12 relevant grants with eligibility scoring  
> **Technical Requirement**: Multi-faceted filtering with eligibility matching

### Technical Requirements Extracted
1. **Advanced Filtering Engine** - Multi-criteria search with real-time results
2. **Eligibility Matching System** - Rule-based scoring for grant compatibility  
3. **Real-time UI Updates** - Filter results update without page refresh
4. **Database Query Optimization** - Fast filtering across large grant dataset

---

## Step 2: User Story Generation

### Generated User Stories

**Story US-001: Amount Range Filtering**
```markdown
**As a** content creator  
**I want** to filter grants by amount range using a slider or input fields  
**So that** I only see grants within my funding needs and don't waste time on grants that are too small or unrealistically large

**Acceptance Criteria:**
- [ ] Amount range slider with min ($1K) and max ($100K) bounds
- [ ] Alternative number input fields for precise amounts
- [ ] Results update in real-time as I adjust the range
- [ ] Clear count of matching grants displayed ("Showing 12 of 1,247 grants")
- [ ] Range selection persists during the session
- [ ] Handles edge cases (min > max, $0 amounts)

**Priority**: Must Have  
**Complexity**: M  
**Module Owner**: Module 4 (Frontend) + Module 2 (Knowledge Graph)  
**Dependencies**: Grant data must include amount ranges (US-005)
```

**Story US-002: Deadline Filtering**
```markdown
**As a** content creator  
**I want** to filter grants by deadline proximity  
**So that** I can focus on grants I can realistically apply for based on my timeline

**Acceptance Criteria:**
- [ ] Preset options: "Next month", "Next 3 months", "Next 6 months", "Next year"
- [ ] Custom date range picker for specific timeframes
- [ ] Visual urgency indicators (red for <30 days, yellow for <90 days)
- [ ] Sort option: "Deadline approaching" vs "Amount" vs "Relevance"
- [ ] Deadline timezone handling (user's local timezone)
- [ ] Past deadline grants automatically hidden

**Priority**: Must Have  
**Complexity**: M  
**Module Owner**: Module 4 (Frontend) + Module 2 (Knowledge Graph)  
**Dependencies**: Grant data must include accurate deadline dates (US-006)
```

**Story US-003: Eligibility Scoring**
```markdown
**As a** content creator  
**I want** to see an eligibility score for each grant  
**So that** I can focus my limited time on grants I'm most likely to receive

**Acceptance Criteria:**
- [ ] Eligibility score displayed as percentage (0-100%) with color coding
- [ ] Hover/click shows eligibility breakdown by criteria
- [ ] Green checkmarks for met criteria, red X for unmet, yellow ? for unclear
- [ ] "Improve eligibility" suggestions for partially matching grants
- [ ] Score calculation explanation available ("Based on your profile: Individual creator, Colorado, Video content, 2 years experience")
- [ ] Scores update when user profile changes

**Priority**: Should Have  
**Complexity**: L  
**Module Owner**: Module 2 (Knowledge Graph) + Module 3 (Reasoning)  
**Dependencies**: User profile system (US-010), Grant criteria data (US-007)
```

**Story US-004: Real-time Filter Results**
```markdown
**As a** content creator  
**I want** filter results to update immediately as I change criteria  
**So that** I can quickly explore different grant options without waiting

**Acceptance Criteria:**
- [ ] Results update within 500ms of filter change
- [ ] Loading indicator shown during updates
- [ ] Graceful handling of no results ("No grants match your criteria. Try expanding your filters.")
- [ ] Filter combinations work together (amount AND deadline AND eligibility)
- [ ] URL updates with filters for bookmarking/sharing
- [ ] Filter state survives browser refresh

**Priority**: Should Have  
**Complexity**: M  
**Module Owner**: Module 4 (Frontend) + Module 2 (Knowledge Graph)  
**Dependencies**: Fast grant search API (US-008), Frontend state management (US-009)
```

---

## Step 3: Epic Planning

### Epic Definition
**Epic E-001: Advanced Grant Filtering**

**User Value**: Content creators can quickly find grants that match their specific needs and eligibility, dramatically reducing time spent on irrelevant opportunities.

**Success Metrics**:
- Time to find relevant grant: <2 minutes (from current 15+ minutes)
- User satisfaction: 85%+ rate filtering as "very helpful"  
- Application success rate: 25%+ increase due to better targeting

**Timeline**: Sprint 1 (Weeks 3-4)

**User Stories Included**:
- [x] US-001: Amount Range Filtering (Priority: Must / Complexity: M)
- [x] US-002: Deadline Filtering (Priority: Must / Complexity: M)  
- [x] US-003: Eligibility Scoring (Priority: Should / Complexity: L)
- [x] US-004: Real-time Filter Results (Priority: Should / Complexity: M)

### Module Coordination Plan

**Module 1 (Data Ingestion)** - Prep Work:
- Ensure grant data includes structured amount ranges, deadlines, eligibility criteria
- Validate data quality for filtering accuracy
- Set up data pipelines for regular grant updates

**Module 2 (Knowledge Graph)** - Core Logic:
- Build filtering API endpoints with performance optimization
- Implement eligibility matching algorithm
- Create grant-to-user compatibility scoring system
- Database indexing for fast multi-criteria queries

**Module 3 (Reasoning Engine)** - Intelligence Layer:  
- Eligibility scoring algorithm based on user profile
- Suggestion engine for improving grant matches
- Learning system to improve recommendations over time

**Module 4 (Frontend)** - User Experience:
- Interactive filtering UI components
- Real-time result updates and state management
- Responsive design for mobile grant searching
- User feedback collection for system improvement

---

## Step 4: PRD Section Example

### Product Requirements Document: Advanced Grant Filtering

#### 2. User Research Foundation
**Target Users**: Content creators seeking funding, primarily individual creators with 1K-100K follower range

**User Journey Reference**: Grant Discovery Journey - Steps 3-6 (see complete journey document)

**Current Pain Points**:
- Generic grant databases show irrelevant opportunities (90% irrelevant)
- No understanding of actual eligibility until deep into application process
- Time-consuming manual filtering through hundreds of grants
- Missed deadlines due to poor deadline visibility

**User Value Delivered**:
- 90% reduction in time spent reviewing irrelevant grants
- Clear eligibility understanding before application investment
- Deadline awareness prevents missed opportunities
- Confidence boost through better grant targeting

#### 3. Functional Requirements

**Core Filtering Functionality**:
- **Amount Range Filter**: Slider and numeric input supporting $1K-$1M range with real-time updates
- **Deadline Filter**: Preset time ranges and custom date picker with urgency indicators  
- **Eligibility Matching**: Algorithmic scoring based on user profile and grant criteria
- **Multi-Criteria Search**: All filters work simultaneously with AND logic

**Performance Requirements**:
- Filter response time: <500ms for any combination of filters
- Concurrent filtering: Support 50+ users filtering simultaneously
- Data accuracy: 95%+ accuracy in eligibility scoring
- Real-time updates: Results update within 200ms of filter change

#### 4. Technical Requirements

**API Specifications**:
```
GET /api/grants/filter?amount_min=10000&amount_max=20000&deadline_months=6&user_id=uuid
Response: {
  "grants": [...],
  "total_matching": 12,
  "filters_applied": {...},
  "performance_ms": 245
}
```

**Database Requirements**:
- Indexed grant fields: amount_min, amount_max, deadline, eligibility_criteria
- User profile fields: creator_type, location, experience_level, content_focus
- Query performance: <300ms for filtered queries across 10K+ grants

---

## Step 5: PDD Section Example  

### Product Design Document: Advanced Grant Filtering

#### 2. Database Design

**Grant Entity**:
```sql
CREATE TABLE grants (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    amount_min INTEGER NOT NULL,
    amount_max INTEGER NOT NULL,
    deadline DATE NOT NULL,
    eligibility_criteria JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes for filtering
CREATE INDEX idx_grants_amount ON grants (amount_min, amount_max);
CREATE INDEX idx_grants_deadline ON grants (deadline);
CREATE INDEX idx_grants_eligibility ON grants USING GIN (eligibility_criteria);
```

**User Profile Entity**:
```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    creator_type VARCHAR(50) NOT NULL, -- 'individual', 'team', 'organization'
    location VARCHAR(100),
    experience_years INTEGER,
    content_focus TEXT[], -- ['video', 'podcast', 'writing', 'photography']
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 3. API Design

**Core Filtering Endpoint**:
```python
@app.get("/api/grants/filter")
async def filter_grants(
    amount_min: Optional[int] = None,
    amount_max: Optional[int] = None,
    deadline_months: Optional[int] = None,
    user_id: Optional[UUID] = None,
    page: int = 1,
    limit: int = 20
) -> FilteredGrantsResponse:
    """
    Filter grants based on multiple criteria with optional eligibility scoring
    """
    start_time = time.time()
    
    # Build dynamic query based on provided filters
    query = select(Grant)
    
    if amount_min:
        query = query.where(Grant.amount_max >= amount_min)
    if amount_max:  
        query = query.where(Grant.amount_min <= amount_max)
    if deadline_months:
        cutoff_date = datetime.now() + timedelta(days=30 * deadline_months)
        query = query.where(Grant.deadline <= cutoff_date)
    
    # Execute query with pagination
    grants = await db.execute(
        query.offset((page - 1) * limit).limit(limit)
    )
    
    # Calculate eligibility scores if user provided
    if user_id:
        user_profile = await get_user_profile(user_id)
        for grant in grants:
            grant.eligibility_score = calculate_eligibility_score(
                user_profile, grant.eligibility_criteria
            )
    
    response_time = (time.time() - start_time) * 1000
    
    return FilteredGrantsResponse(
        grants=grants,
        total_matching=len(grants),
        response_time_ms=response_time,
        filters_applied={
            "amount_min": amount_min,
            "amount_max": amount_max, 
            "deadline_months": deadline_months
        }
    )
```

#### 5. Algorithm Design

**Eligibility Scoring Algorithm**:
```python
def calculate_eligibility_score(user_profile: UserProfile, grant_criteria: dict) -> int:
    """
    Calculate 0-100 eligibility score based on grant criteria match
    
    Scoring Logic:
    - Creator type match: 30 points
    - Location eligibility: 25 points  
    - Experience requirements: 20 points
    - Content focus alignment: 15 points
    - Special criteria bonus: 10 points
    """
    score = 0
    
    # Creator type matching
    if user_profile.creator_type in grant_criteria.get("creator_types", []):
        score += 30
    
    # Location eligibility  
    user_location = user_profile.location
    eligible_locations = grant_criteria.get("locations", [])
    if not eligible_locations or user_location in eligible_locations:
        score += 25
    
    # Experience requirements
    required_experience = grant_criteria.get("min_experience_years", 0)
    if user_profile.experience_years >= required_experience:
        score += 20
    
    # Content focus alignment
    user_focus = set(user_profile.content_focus)
    grant_focus = set(grant_criteria.get("content_types", []))
    if user_focus.intersection(grant_focus):
        score += 15
    
    # Special criteria bonus (emerging creator, underrepresented, etc.)
    if check_special_criteria(user_profile, grant_criteria):
        score += 10
    
    return min(score, 100)  # Cap at 100%
```

---

## Implementation Schedule

### Sprint 1 (Weeks 3-4): Core Filtering
**Week 3 Goals**:
- Module 1: Grant data validation and cleanup
- Module 2: Basic filtering API implementation  
- Module 4: Filter UI components (amount, deadline)
- Module 3: Basic eligibility algorithm research

**Week 4 Goals**:
- Module 2: Performance optimization and indexing
- Module 3: Eligibility scoring implementation
- Module 4: Real-time filter integration
- Integration testing across all modules

### Success Validation
**Technical Validation**:
- [ ] Filter API responds <500ms for all test cases
- [ ] UI updates in real-time without page refresh
- [ ] Eligibility scores calculate correctly based on test profiles
- [ ] No crashes under concurrent user load testing

**User Journey Validation**:
- [ ] Complete Grant Discovery Journey Steps 3-6 successfully
- [ ] User can find 3+ relevant grants in <2 minutes  
- [ ] Eligibility scores help users focus on appropriate grants
- [ ] Filter combinations work intuitively together

---

## Module Integration Points

### API Integration Contracts

**Module 1 → Module 2**: Clean grant data format
```json
{
  "id": "uuid",
  "title": "Colorado Arts Media Grant",
  "amount_min": 5000,
  "amount_max": 15000,
  "deadline": "2025-03-15T23:59:59Z",
  "eligibility_criteria": {
    "creator_types": ["individual", "team"],
    "locations": ["Colorado", "Mountain West"],
    "min_experience_years": 1,
    "content_types": ["video", "film", "multimedia"]
  }
}
```

**Module 2 → Module 4**: Filtered results API
```json
{
  "grants": [...],
  "pagination": {"page": 1, "limit": 20, "total": 247},
  "filters_applied": {...},
  "performance_metrics": {"response_time_ms": 245}
}
```

**Module 3 → Module 2**: Eligibility scoring service
```python
async def get_eligibility_scores(user_id: UUID, grant_ids: List[UUID]) -> Dict[UUID, int]:
    """Return eligibility scores for grants given user profile"""
```

### Testing Strategy

**Unit Tests** (Each Module):
- Module 1: Data validation and normalization
- Module 2: Filter logic and query performance  
- Module 3: Eligibility scoring accuracy
- Module 4: UI component behavior and state management

**Integration Tests** (Cross-Module):
- Complete filter workflow from UI to database
- Real-time update performance under load
- Eligibility score integration with filtering
- Error handling across service boundaries

**User Acceptance Tests**:
- Complete Grant Discovery Journey simulation
- A/B test filter vs no-filter user success rates
- User feedback collection on filter usefulness

---

This implementation example provides a complete template the intern team can follow for any user journey. The process ensures user needs drive technical implementation while maintaining clear module boundaries and integration points.

**Ready for tomorrow's kickoff meeting with concrete examples and clear methodology.**

---

*This example demonstrates the complete journey from user need to technical implementation, providing the intern team with a proven methodology for user-centered development.*