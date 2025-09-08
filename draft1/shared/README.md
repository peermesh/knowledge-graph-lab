# Shared Resources Directory

## Overview
This directory contains shared resources, configurations, and utilities used across all Knowledge Graph Lab modules. Following PeerMesh principles, these shared components enable module independence while maintaining consistency.

## Directory Structure

```
shared/
├── config/              # Shared configuration files
│   ├── domains/        # Domain-specific configurations
│   ├── schemas/        # Entity and relationship schemas
│   └── api-specs/      # OpenAPI specifications
├── models/             # Shared data models and types
│   ├── entities.py     # Entity type definitions
│   ├── relationships.py # Relationship definitions
│   └── responses.py    # API response models
├── utils/              # Shared utility functions
│   ├── validation.py   # Input validation utilities
│   ├── auth.py        # Authentication helpers
│   └── logging.py     # Logging configuration
├── constants/          # Shared constants and enums
│   ├── entity_types.py
│   ├── api_endpoints.py
│   └── error_codes.py
└── templates/          # Shared templates
    ├── emails/        # Email digest templates
    ├── prompts/       # LLM prompt templates
    └── responses/     # API response templates
```

## Shared Configurations

### Domain Configuration
`config/domains/creator-economy.json`:
```json
{
  "domain": "creator-economy",
  "description": "Creator economy, platforms, and monetization",
  "entity_types": [
    "Platform",
    "Organization", 
    "Person",
    "Grant",
    "Policy",
    "Event"
  ],
  "key_relationships": [
    "FOUNDED_BY",
    "COMPETES_WITH",
    "PARTNERS_WITH",
    "INVESTS_IN",
    "OPERATES"
  ],
  "geographic_scope": {
    "primary": "Boulder, CO",
    "secondary": "United States",
    "global": true
  },
  "data_sources": {
    "priority": ["techcrunch", "creatoreconomyreport", "patreon-blog"],
    "refresh_frequency": "daily"
  }
}
```

### Entity Schemas
`config/schemas/platform.schema.json`:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Platform",
  "type": "object",
  "required": ["name", "type", "category"],
  "properties": {
    "name": {
      "type": "string",
      "description": "Platform name"
    },
    "type": {
      "type": "string",
      "enum": ["Platform"]
    },
    "category": {
      "type": "string",
      "enum": [
        "subscription-platform",
        "newsletter-platform",
        "video-platform",
        "social-platform",
        "marketplace"
      ]
    },
    "website": {
      "type": "string",
      "format": "uri"
    },
    "founded": {
      "type": "string",
      "format": "date"
    },
    "headquarters": {
      "type": "string"
    }
  }
}
```

## Shared Models

### Python Models (Pydantic)
`models/entities.py`:
```python
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class EntityType(str, Enum):
    PLATFORM = "Platform"
    ORGANIZATION = "Organization"
    PERSON = "Person"
    GRANT = "Grant"
    POLICY = "Policy"
    EVENT = "Event"

class BaseEntity(BaseModel):
    id: str
    name: str
    type: EntityType
    confidence: float = 1.0
    created_at: datetime
    updated_at: datetime
    
class Platform(BaseEntity):
    type: EntityType = EntityType.PLATFORM
    category: str
    website: Optional[HttpUrl]
    founded: Optional[str]
    headquarters: Optional[str]
    
class Grant(BaseEntity):
    type: EntityType = EntityType.GRANT
    amount: Optional[str]
    deadline: Optional[datetime]
    eligibility: Optional[List[str]]
    application_url: Optional[HttpUrl]
```

### TypeScript Types
`models/entities.ts`:
```typescript
export enum EntityType {
  PLATFORM = "Platform",
  ORGANIZATION = "Organization",
  PERSON = "Person",
  GRANT = "Grant",
  POLICY = "Policy",
  EVENT = "Event"
}

export interface BaseEntity {
  id: string;
  name: string;
  type: EntityType;
  confidence: number;
  createdAt: string;
  updatedAt: string;
}

export interface Platform extends BaseEntity {
  type: EntityType.PLATFORM;
  category: string;
  website?: string;
  founded?: string;
  headquarters?: string;
}

export interface Grant extends BaseEntity {
  type: EntityType.GRANT;
  amount?: string;
  deadline?: string;
  eligibility?: string[];
  applicationUrl?: string;
}
```

## Shared Utilities

### Validation Utilities
`utils/validation.py`:
```python
import re
from typing import Optional
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validate URL format and accessibility."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_entity_name(name: str) -> bool:
    """Validate entity name format."""
    if not name or len(name) < 2:
        return False
    # Allow letters, numbers, spaces, and common punctuation
    pattern = r'^[\w\s\-\.&,]+$'
    return bool(re.match(pattern, name))

def validate_confidence_score(score: float) -> bool:
    """Ensure confidence score is between 0 and 1."""
    return 0 <= score <= 1
```

### Authentication Helpers
`utils/auth.py`:
```python
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict

SECRET_KEY = os.getenv("JWT_SECRET", "development-secret")

def create_token(user_id: str, expires_in: int = 3600) -> str:
    """Create JWT token for user."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> Optional[Dict]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

### Logging Configuration
`utils/logging.py`:
```python
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(
    module_name: str,
    log_level: str = "INFO",
    log_file: Optional[str] = None
):
    """Configure logging for a module."""
    logger = logging.getLogger(module_name)
    logger.setLevel(getattr(logging, log_level))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(console_format)
        logger.addHandler(file_handler)
    
    return logger
```

## Shared Constants

### Entity Types
`constants/entity_types.py`:
```python
# Entity type definitions
ENTITY_TYPES = [
    "Platform",
    "Organization",
    "Person",
    "Grant",
    "Policy",
    "Event"
]

# Relationship types
RELATIONSHIP_TYPES = [
    "FOUNDED_BY",
    "COMPETES_WITH",
    "PARTNERS_WITH",
    "INVESTS_IN",
    "OPERATES",
    "INTEGRATES_WITH",
    "WORKS_AT",
    "LEADS"
]

# Platform categories
PLATFORM_CATEGORIES = [
    "subscription-platform",
    "newsletter-platform",
    "video-platform",
    "social-platform",
    "marketplace",
    "creator-tools"
]
```

### API Endpoints
`constants/api_endpoints.py`:
```python
# Service URLs
INGESTION_URL = os.getenv("INGESTION_URL", "http://localhost:8001")
KNOWLEDGE_URL = os.getenv("KNOWLEDGE_URL", "http://localhost:8002")
REASONING_URL = os.getenv("REASONING_URL", "http://localhost:8003")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Common endpoints
HEALTH_ENDPOINT = "/health"
STATS_ENDPOINT = "/api/stats"

# Timeouts
DEFAULT_TIMEOUT = 30  # seconds
LONG_TIMEOUT = 120    # seconds for LLM operations
```

## Shared Templates

### LLM Prompt Templates
`templates/prompts/entity_extraction.txt`:
```
Extract entities from the following text about the creator economy.

Entity Types to identify:
- Platform: Creator platforms and tools (e.g., Patreon, Substack)
- Organization: Companies, funds, accelerators
- Person: Individuals mentioned by name
- Grant: Funding opportunities, creator funds
- Policy: Laws, regulations, platform policies
- Event: Conferences, summits, important dates

Text: {text}

Return as JSON with format:
{
  "entities": [
    {
      "name": "entity name",
      "type": "entity type",
      "context": "surrounding context",
      "attributes": {}
    }
  ]
}
```

### Email Templates
`templates/emails/weekly_digest.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: -apple-system, sans-serif; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .section { margin: 20px 0; padding: 20px; }
        .footer { text-align: center; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ digest_title }}</h1>
        <p>{{ digest_date }}</p>
    </div>
    
    {% for section in sections %}
    <div class="section">
        <h2>{{ section.title }}</h2>
        <div>{{ section.content | safe }}</div>
    </div>
    {% endfor %}
    
    <div class="footer">
        <p>Knowledge Graph Lab - Your AI Research Assistant</p>
    </div>
</body>
</html>
```

## Usage Guidelines

### For Module Developers

1. **Import shared resources** instead of duplicating:
```python
from shared.models.entities import Platform, EntityType
from shared.utils.validation import validate_url
from shared.constants.api_endpoints import KNOWLEDGE_URL
```

2. **Extend shared models** for module-specific needs:
```python
from shared.models.entities import BaseEntity

class ExtendedPlatform(BaseEntity):
    # Add module-specific fields
    ingestion_frequency: str
    last_scraped: datetime
```

3. **Use shared configuration** as base:
```python
import json
from pathlib import Path

shared_config = Path(__file__).parent.parent / "shared/config/domains/creator-economy.json"
with open(shared_config) as f:
    config = json.load(f)
    
# Extend with module-specific config
config['module_specific'] = {...}
```

### For Testing

Use shared test fixtures:
```python
import pytest
from shared.models.entities import Platform

@pytest.fixture
def sample_platform():
    return Platform(
        id="test_platform_001",
        name="Test Platform",
        type="Platform",
        category="subscription-platform",
        website="https://example.com"
    )
```

## Maintenance

### Adding New Shared Resources

1. **Determine if truly shared**: Used by 2+ modules?
2. **Add to appropriate directory**: Follow structure
3. **Document in this README**: Include examples
4. **Update dependent modules**: Ensure compatibility
5. **Add tests**: Shared resources need tests too

### Versioning Shared Resources

When making breaking changes:
1. Use semantic versioning in comments
2. Provide migration path
3. Update all dependent modules
4. Document breaking changes

### Dependencies

Shared resources should have minimal dependencies:
- Standard library preferred
- Common libraries (pydantic, etc.) acceptable
- No module-specific dependencies

## Best Practices

1. **Keep it minimal**: Only truly shared items
2. **Maintain backward compatibility**: Don't break modules
3. **Document thoroughly**: Clear examples and usage
4. **Type everything**: Use type hints/TypeScript types
5. **Test shared code**: Has its own test suite
6. **Version carefully**: Consider impact on all modules

## Common Pitfalls to Avoid

1. **Over-sharing**: Not everything needs to be shared
2. **Tight coupling**: Shared resources shouldn't create dependencies
3. **Module-specific logic**: Keep business logic in modules
4. **Circular imports**: Structure to avoid circular dependencies
5. **Breaking changes**: Always maintain compatibility

## Migration Guide

When moving code to shared:
1. Identify truly shared functionality
2. Extract to shared with tests
3. Update all modules to import from shared
4. Remove duplicated code
5. Run full test suite
6. Document in this README