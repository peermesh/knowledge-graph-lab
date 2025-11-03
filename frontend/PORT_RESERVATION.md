# Port Reservation - Knowledge Graph Lab Frontend

## Reserved Ports

### Frontend Module
- **Port:** 4300
- **External Mapping:** 4300:80 (host:container)
- **Status:** RESERVED AND IN USE
- **Service:** Knowledge Graph Lab Frontend
- **Container:** frontend-frontend-1

## Project Information
- **Repository:** knowledge-graph-lab
- **Branch:** D-JSimpson/work
- **Module:** frontend (standalone module)
- **Location:** `/Users/grig/work/peermesh/repo/knowledge-graph-lab/frontend`
- **Docker Compose File:** `frontend/docker-compose.yml`

## Usage
The frontend is accessible at:
- **URL:** http://localhost:4300
- **Health Check:** http://localhost:4300/health

## Port Conflicts Checked
The following ports were checked for availability before selecting port 4300:
- 3000: IN USE (Docker containers)
- 3001: IN USE (Docker containers)
- 4200: Available
- 4300: Available ✓ SELECTED
- 4400: Available
- 4500: Available

## Last Updated
2025-10-28 23:40 UTC

## Notes
- Port is bound to 0.0.0.0 (accessible from all network interfaces)
- nginx running on port 80 inside container
- Health check configured at /health endpoint
- Backend proxy disabled (standalone mode)


