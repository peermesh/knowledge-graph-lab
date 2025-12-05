#!/bin/bash
# Test API paths to verify /api/v1 prefix compliance

BASE_URL="${BASE_URL:-http://localhost:8080}"

echo "Testing API Endpoints..."
echo "========================="
echo "Base URL: $BASE_URL"
echo ""

# Health endpoint (should be at root, not under /api/v1)
echo -n "Health endpoint (/health): "
HEALTH_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health")
echo "$HEALTH_CODE"
if [ "$HEALTH_CODE" != "200" ]; then
    echo "  ⚠️  Warning: Health endpoint returned $HEALTH_CODE"
fi

# API root
echo -n "API root (/api/v1/): "
ROOT_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/")
echo "$ROOT_CODE"

# Publications
echo -n "Publications list: "
PUB_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/publications")
echo "$PUB_CODE"

# Subscribers
echo -n "Subscribers list: "
SUB_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/subscribers")
echo "$SUB_CODE"

# Channels
echo -n "Channels list: "
CHAN_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/channels")
echo "$CHAN_CODE"

# Analytics
echo -n "Analytics engagement: "
ANAL_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/analytics/engagement")
echo "$ANAL_CODE"

# Dashboard
echo -n "Dashboard overview: "
DASH_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/dashboard/overview")
echo "$DASH_CODE"

# Email test status
echo -n "Email test status: "
EMAIL_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/email/status")
echo "$EMAIL_CODE"

# Verify non-prefixed paths return 404
echo ""
echo "Verifying non-prefixed paths return 404:"
echo -n "/publications (should be 404): "
PUB_404=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/publications")
echo "$PUB_404"
if [ "$PUB_404" != "404" ]; then
    echo "  ❌ Error: /publications should return 404 but returned $PUB_404"
fi

echo -n "/api/publications (should be 404): "
API_404=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/publications")
echo "$API_404"
if [ "$API_404" != "404" ]; then
    echo "  ❌ Error: /api/publications should return 404 but returned $API_404"
fi

echo -n "/api/v1/health (should be 404): "
HEALTH_404=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/health")
echo "$HEALTH_404"
if [ "$HEALTH_404" != "404" ]; then
    echo "  ⚠️  Warning: /api/v1/health returned $HEALTH_404 (health should be at /health)"
fi

echo ""
echo "========================="
echo "Testing complete!"
echo ""
echo "Summary:"
echo "  - All /api/v1/* endpoints should return 200 or appropriate status codes"
echo "  - /health should return 200"
echo "  - Non-prefixed paths should return 404"

