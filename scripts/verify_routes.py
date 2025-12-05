#!/usr/bin/env python3
"""Verify all API routes have correct prefixes."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.publishing.main import app
except Exception as e:
    print(f"Error importing app: {e}")
    print("Note: This script requires all dependencies to be installed.")
    print("You can still verify routes by checking the code directly.")
    sys.exit(1)

# Get all routes
routes = []
for route in app.routes:
    if hasattr(route, 'path'):
        methods = list(route.methods) if hasattr(route, 'methods') else []
        routes.append({
            'path': route.path,
            'methods': methods,
            'name': getattr(route, 'name', 'N/A')
        })

# Sort by path
routes.sort(key=lambda x: x['path'])

# Print all routes
print("Registered Routes:")
print("=" * 70)
for route in routes:
    methods = ', '.join(route['methods']) if route['methods'] else 'N/A'
    print(f"{route['path']:45} {methods:20} {route['name']}")

# Verify compliance
print("\n" + "=" * 70)
print("Compliance Check:")
print("=" * 70)

issues = []
compliant = []
for route in routes:
    path = route['path']
    # Health endpoint should be at root
    if path == '/health':
        compliant.append(f"✅ {path} - Health endpoint at root (correct)")
        continue
    # Documentation endpoints are OK
    if path in ['/api/v1/docs', '/api/v1/redoc', '/api/v1/openapi.json']:
        compliant.append(f"✅ {path} - Documentation endpoint (correct)")
        continue
    # All other paths should start with /api/v1
    if not path.startswith('/api/v1/'):
        issues.append(f"❌ {path} - Missing /api/v1 prefix")
    else:
        compliant.append(f"✅ {path}")

# Print compliant routes
for item in compliant:
    print(item)

# Print issues
if issues:
    print("\n" + "=" * 70)
    print("Issues Found:")
    print("=" * 70)
    for issue in issues:
        print(issue)
    sys.exit(1)
else:
    print("\n" + "=" * 70)
    print("✅ All routes comply with /api/v1 prefix requirement!")
    print("=" * 70)
    sys.exit(0)

