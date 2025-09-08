# Knowledge Graph Lab - Integration Testing Procedures

**Date**: September 7, 2025 18:50  
**Tool**: Claude Code  
**Purpose**: Comprehensive testing procedures to validate system integration

---

## 🧪 INTEGRATION TESTING FRAMEWORK

### Testing Philosophy
- **End-to-End Validation**: Test complete workflows from user input to final output
- **Service Communication**: Validate all inter-module communication
- **Data Flow Integrity**: Ensure data consistency across all system components
- **Performance Baselines**: Establish expected response times and resource usage
- **Error Handling**: Test failure scenarios and recovery mechanisms

---

## 🔧 TEST ENVIRONMENT SETUP

### Prerequisites
```bash
# Ensure all services are running
docker-compose up -d

# Verify service health
docker-compose ps
# Expected: All services show "Up" status

# Activate Python virtual environment
source .venv/bin/activate

# Install testing dependencies
pip install pytest requests pytest-asyncio pytest-mock httpx
```

### Environment Configuration
```bash
# Copy test environment configuration
cp .env.example .env.test

# Configure test-specific settings
# DATABASE_URL=sqlite:///./test_kgl.db
# TESTING=true
# LOG_LEVEL=DEBUG
```

---

## 🏗️ SERVICE INTEGRATION TESTS

### 1. Database Connectivity Tests

**Test File**: `tests/integration/test_database_integration.py`

```python
"""Database integration tests."""
import pytest
import asyncio
from shared.database.connection import get_database_connection
from shared.database.models import Base
import sqlalchemy as sa

@pytest.mark.asyncio
async def test_database_connection():
    """Test basic database connectivity."""
    conn = await get_database_connection()
    assert conn is not None
    
    # Test basic query
    result = await conn.execute(sa.text("SELECT 1"))
    assert result.scalar() == 1
    await conn.close()

@pytest.mark.asyncio
async def test_database_table_creation():
    """Test that all required tables can be created."""
    conn = await get_database_connection()
    
    # Create all tables
    Base.metadata.create_all(conn.engine)
    
    # Verify tables exist
    tables = await conn.execute(sa.text(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ))
    table_names = [row[0] for row in tables.fetchall()]
    
    required_tables = ['users', 'entities', 'relationships', 'documents']
    for table in required_tables:
        assert table in table_names
    
    await conn.close()
```

**Run Test**:
```bash
pytest tests/integration/test_database_integration.py -v
# Expected: All tests pass
```

### 2. Vector Database Integration Tests

**Test File**: `tests/integration/test_vector_db_integration.py`

```python
"""Vector database (Qdrant) integration tests."""
import pytest
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

@pytest.fixture
def qdrant_client():
    """Create Qdrant client for testing."""
    return QdrantClient("localhost", port=6333)

def test_qdrant_health(qdrant_client):
    """Test Qdrant service health."""
    response = requests.get("http://localhost:6333/")
    assert response.status_code == 200

def test_collection_operations(qdrant_client):
    """Test collection creation and operations."""
    collection_name = "test_collection"
    
    # Create collection
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=100, distance=Distance.COSINE)
    )
    
    # Verify collection exists
    collections = qdrant_client.get_collections()
    assert collection_name in [c.name for c in collections.collections]
    
    # Insert test vector
    points = [
        PointStruct(
            id=1,
            vector=[0.1] * 100,
            payload={"text": "test document"}
        )
    ]
    qdrant_client.upsert(collection_name=collection_name, points=points)
    
    # Search test
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=[0.1] * 100,
        limit=1
    )
    assert len(search_result) == 1
    assert search_result[0].payload["text"] == "test document"
    
    # Cleanup
    qdrant_client.delete_collection(collection_name)
```

**Run Test**:
```bash
pytest tests/integration/test_vector_db_integration.py -v
```

### 3. API Gateway Integration Tests

**Test File**: `tests/integration/test_api_integration.py`

```python
"""API integration tests across all modules."""
import pytest
import httpx
import asyncio

BASE_URLS = {
    "ingestion": "http://localhost:8001",
    "knowledge_graph": "http://localhost:8002", 
    "reasoning": "http://localhost:8003",
    "frontend_api": "http://localhost:3000/api"
}

@pytest.mark.asyncio
async def test_all_module_health_checks():
    """Test that all module APIs are responding."""
    async with httpx.AsyncClient() as client:
        for module, base_url in BASE_URLS.items():
            try:
                response = await client.get(f"{base_url}/health")
                assert response.status_code == 200, f"{module} health check failed"
                
                health_data = response.json()
                assert health_data.get("status") == "healthy"
                assert "timestamp" in health_data
                
            except httpx.ConnectError:
                pytest.fail(f"Cannot connect to {module} at {base_url}")

@pytest.mark.asyncio
async def test_cross_module_communication():
    """Test communication between modules."""
    async with httpx.AsyncClient() as client:
        # Test: Ingestion -> Knowledge Graph
        ingestion_data = {
            "url": "https://example.com/test-article",
            "content_type": "article"
        }
        
        # Start ingestion
        ing_response = await client.post(
            f"{BASE_URLS['ingestion']}/ingest",
            json=ingestion_data
        )
        assert ing_response.status_code == 200
        
        job_id = ing_response.json()["job_id"]
        
        # Wait for processing (polling)
        for _ in range(10):  # Max 10 seconds
            status_response = await client.get(
                f"{BASE_URLS['ingestion']}/status/{job_id}"
            )
            status = status_response.json()["status"]
            
            if status == "completed":
                break
            elif status == "failed":
                pytest.fail(f"Ingestion job failed: {status_response.json()}")
                
            await asyncio.sleep(1)
        else:
            pytest.fail("Ingestion job did not complete within timeout")
        
        # Verify knowledge graph received the data
        kg_response = await client.get(
            f"{BASE_URLS['knowledge_graph']}/entities",
            params={"source_job": job_id}
        )
        assert kg_response.status_code == 200
        entities = kg_response.json()["entities"]
        assert len(entities) > 0
```

**Run Test**:
```bash
pytest tests/integration/test_api_integration.py -v
```

---

## 🔄 WORKFLOW INTEGRATION TESTS

### End-to-End User Workflows

**Test File**: `tests/integration/test_e2e_workflows.py`

```python
"""End-to-end workflow integration tests."""
import pytest
import httpx
import asyncio

@pytest.mark.asyncio
async def test_complete_knowledge_extraction_workflow():
    """Test complete workflow from URL to knowledge graph."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Step 1: Submit URL for ingestion
        workflow_data = {
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "extraction_type": "full",
            "generate_insights": True
        }
        
        response = await client.post(
            "http://localhost:8001/workflows/extract-knowledge",
            json=workflow_data
        )
        assert response.status_code == 200
        workflow_id = response.json()["workflow_id"]
        
        # Step 2: Monitor workflow progress
        workflow_complete = False
        for attempt in range(30):  # 30 second timeout
            status_response = await client.get(
                f"http://localhost:8001/workflows/{workflow_id}/status"
            )
            
            status_data = status_response.json()
            status = status_data["status"]
            
            if status == "completed":
                workflow_complete = True
                break
            elif status == "failed":
                pytest.fail(f"Workflow failed: {status_data.get('error')}")
            
            await asyncio.sleep(1)
        
        assert workflow_complete, "Workflow did not complete within timeout"
        
        # Step 3: Verify extracted entities in knowledge graph
        entities_response = await client.get(
            f"http://localhost:8002/entities",
            params={"workflow_id": workflow_id}
        )
        assert entities_response.status_code == 200
        entities = entities_response.json()["entities"]
        assert len(entities) > 0
        
        # Verify entity types
        entity_types = {e["type"] for e in entities}
        expected_types = {"PERSON", "ORGANIZATION", "CONCEPT"}
        assert entity_types.intersection(expected_types), "No expected entity types found"
        
        # Step 4: Verify relationships were created
        relationships_response = await client.get(
            f"http://localhost:8002/relationships",
            params={"workflow_id": workflow_id}
        )
        assert relationships_response.status_code == 200
        relationships = relationships_response.json()["relationships"]
        assert len(relationships) > 0
        
        # Step 5: Test reasoning engine insights
        insights_response = await client.get(
            f"http://localhost:8003/insights/{workflow_id}"
        )
        assert insights_response.status_code == 200
        insights = insights_response.json()["insights"]
        assert len(insights) > 0
        assert all("confidence" in insight for insight in insights)

@pytest.mark.asyncio
async def test_user_query_workflow():
    """Test user question answering workflow."""
    async with httpx.AsyncClient(timeout=15.0) as client:
        
        # Submit user query
        query_data = {
            "question": "What is machine learning?",
            "context_limit": 5,
            "include_sources": True
        }
        
        response = await client.post(
            "http://localhost:8003/query",
            json=query_data
        )
        assert response.status_code == 200
        
        result = response.json()
        assert "answer" in result
        assert "sources" in result
        assert "confidence" in result
        assert result["confidence"] > 0.5
```

---

## 📊 PERFORMANCE INTEGRATION TESTS

### Load and Performance Testing

**Test File**: `tests/integration/test_performance.py`

```python
"""Performance and load integration tests."""
import pytest
import httpx
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

@pytest.mark.asyncio
async def test_concurrent_ingestion():
    """Test system behavior under concurrent ingestion load."""
    async with httpx.AsyncClient() as client:
        
        # Create multiple ingestion requests
        test_urls = [
            f"https://httpbin.org/json?id={i}" for i in range(5)
        ]
        
        start_time = time.time()
        
        # Submit all requests concurrently
        tasks = [
            client.post(
                "http://localhost:8001/ingest",
                json={"url": url, "content_type": "json"}
            )
            for url in test_urls
        ]
        
        responses = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Verify all requests succeeded
        assert all(r.status_code == 200 for r in responses)
        
        # Verify reasonable performance (should complete within 10 seconds)
        assert duration < 10.0, f"Concurrent ingestion took {duration} seconds"

@pytest.mark.asyncio
async def test_vector_search_performance():
    """Test vector database search performance."""
    async with httpx.AsyncClient() as client:
        
        # Setup: Create test collection with many vectors
        setup_response = await client.post(
            "http://localhost:8002/test/setup-performance-collection",
            json={"vector_count": 1000}
        )
        assert setup_response.status_code == 200
        
        # Performance test: Multiple searches
        search_times = []
        
        for _ in range(10):
            start_time = time.time()
            
            search_response = await client.post(
                "http://localhost:8002/search",
                json={
                    "query": "test query",
                    "limit": 10
                }
            )
            
            end_time = time.time()
            search_times.append(end_time - start_time)
            
            assert search_response.status_code == 200
        
        # Verify performance metrics
        avg_search_time = sum(search_times) / len(search_times)
        max_search_time = max(search_times)
        
        assert avg_search_time < 0.5, f"Average search time too high: {avg_search_time}s"
        assert max_search_time < 1.0, f"Max search time too high: {max_search_time}s"
```

---

## 🚨 ERROR HANDLING INTEGRATION TESTS

### Failure Scenario Testing

**Test File**: `tests/integration/test_error_handling.py`

```python
"""Error handling and recovery integration tests."""
import pytest
import httpx
import asyncio

@pytest.mark.asyncio
async def test_service_failure_recovery():
    """Test system behavior when services temporarily fail."""
    async with httpx.AsyncClient() as client:
        
        # Test with invalid URL
        response = await client.post(
            "http://localhost:8001/ingest",
            json={"url": "https://invalid-domain-12345.com", "content_type": "article"}
        )
        
        # Should return error but not crash
        assert response.status_code in [400, 422]
        error_data = response.json()
        assert "error" in error_data
        
        # Verify service is still healthy after error
        health_response = await client.get("http://localhost:8001/health")
        assert health_response.status_code == 200

@pytest.mark.asyncio
async def test_database_connection_handling():
    """Test handling of database connection issues."""
    async with httpx.AsyncClient() as client:
        
        # This test would require more sophisticated setup to
        # temporarily disconnect database, but we can test
        # the error handling endpoints
        
        response = await client.get(
            "http://localhost:8002/test/database-error-simulation"
        )
        
        # Should handle gracefully
        assert response.status_code in [500, 503]
        error_data = response.json()
        assert "error" in error_data
        assert "retry" in error_data  # Should suggest retry

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test API rate limiting behavior."""
    async with httpx.AsyncClient() as client:
        
        # Send many requests quickly
        tasks = [
            client.get("http://localhost:8002/entities")
            for _ in range(100)
        ]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Should get some rate limit responses
        status_codes = [
            r.status_code for r in responses 
            if not isinstance(r, Exception)
        ]
        
        # Should see mix of successful and rate-limited responses
        assert 200 in status_codes
        assert any(code in [429, 503] for code in status_codes)
```

---

## 🎯 INTEGRATION TEST EXECUTION

### Running All Integration Tests

**Complete Test Suite**:
```bash
# Run all integration tests
pytest tests/integration/ -v --tb=short

# Run with coverage reporting
pytest tests/integration/ --cov=src --cov-report=html

# Run specific test categories
pytest tests/integration/test_database_integration.py -v
pytest tests/integration/test_api_integration.py -v
pytest tests/integration/test_e2e_workflows.py -v

# Run performance tests (may take longer)
pytest tests/integration/test_performance.py -v -s
```

### Continuous Integration Setup

**GitHub Actions Workflow** (`.github/workflows/integration-tests.yml`):
```yaml
name: Integration Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
    
    - name: Start Qdrant
      run: |
        docker run -d -p 6333:6333 qdrant/qdrant
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest httpx pytest-asyncio pytest-cov
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 📋 INTEGRATION TEST CHECKLIST

### Pre-Test Setup
- [ ] All services are running (`docker-compose ps`)
- [ ] Test database is clean
- [ ] API keys are configured for testing
- [ ] Test data is loaded
- [ ] Network connectivity verified

### Test Execution
- [ ] Database integration tests pass
- [ ] Vector database tests pass
- [ ] API integration tests pass
- [ ] End-to-end workflow tests pass
- [ ] Performance tests within acceptable limits
- [ ] Error handling tests pass

### Post-Test Validation
- [ ] Test coverage reports generated
- [ ] Performance metrics documented
- [ ] Failed tests documented with reproduction steps
- [ ] Test artifacts cleaned up

### Success Criteria
- **Pass Rate**: >95% of integration tests pass
- **Performance**: API responses <2s, vector searches <500ms
- **Error Handling**: All error scenarios handled gracefully
- **Coverage**: Integration test coverage >80%

---

**INTEGRATION TESTING COMPLETE**: System ready for intern onboarding when all test suites pass consistently