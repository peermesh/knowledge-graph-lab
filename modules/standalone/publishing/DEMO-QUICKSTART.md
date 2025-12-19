# Publishing Module - Demo Quickstart Guide

This guide will help you see the Publishing Module in action with a visual frontend!

## 🚀 Quick Start (Easiest Method)

### Option 1: Docker Compose (Recommended)

```bash
# 1. Navigate to the project
cd /Users/benschreiber/Desktop/knowledge-graph-lab

# 2. Start everything with Docker
docker-compose up --build

# 3. Open your browser
#    Frontend: http://localhost:3000
#    Swagger UI: http://localhost:8080/docs
#    Health Check: http://localhost:8080/health
```

That's it! You now have:
- ✅ Publishing Module API running on port 8080
- ✅ Demo frontend running on port 3000
- ✅ In-memory mode (no database needed)

### Option 2: Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set DEBUG mode
export DEBUG=true

# 3. Start the API
uvicorn src.publishing.main:app --host 0.0.0.0 --port 8080 --reload

# 4. In another terminal, serve the frontend
cd /Users/benschreiber/Desktop/knowledge-graph-lab
python -m http.server 3000

# 5. Open http://localhost:3000/demo-frontend.html
```

## 🎯 What You Can Do

### 1. Check System Health
- Click "Check Health Status" to verify the API is running
- You should see a green "✅ System Healthy" status

### 2. Create Channels
- Enter a channel name (e.g., "Email Newsletter")
- Select a channel type (Email, Slack, Discord, Webhook)
- Click "Create Channel"
- Click "List All Channels" to see all created channels

### 3. Add Subscribers
- Enter an email address
- Add topics of interest (comma-separated)
- Click "Create Subscriber"
- Click "List Subscribers" to see all subscribers

### 4. Schedule Publications
- Enter content IDs (or leave blank for demo UUIDs)
- Select publication type (Newsletter, Alert, Digest)
- Click "Schedule Newsletter"
- Click "List Publications" to see scheduled items

### 5. Track Engagement
- Enter a publication ID (or leave blank)
- Click "Track Open" or "Track Click"
- Click "Get Engagement Summary" to see metrics

### 6. View Analytics
- Click "Get Engagement Summary" for open/click stats
- Click "Get Performance Metrics" for system performance

## 📚 Alternative: Interactive API Documentation

The Publishing Module includes Swagger UI out of the box:

```bash
# Start the API
docker-compose up api

# Open Swagger UI
open http://localhost:8080/docs
```

Swagger UI provides:
- ✅ Full API documentation
- ✅ Try-it-out functionality for all 21 endpoints
- ✅ Request/response examples
- ✅ Schema validation

## 🔧 Troubleshooting

### Port Already in Use
```bash
# If port 8080 or 3000 is already in use
docker-compose down
lsof -ti:8080 | xargs kill -9  # macOS/Linux
lsof -ti:3000 | xargs kill -9
```

### Docker Build Issues
```bash
# Rebuild without cache
docker-compose build --no-cache
docker-compose up
```

### API Not Responding
```bash
# Check API logs
docker-compose logs api

# Check health endpoint directly
curl http://localhost:8080/health
```

## 📊 What's Running in DEBUG Mode

When `DEBUG=true`, the Publishing Module uses in-memory stores:
- **IN_MEMORY_CHANNELS**: Stores channel configurations
- **IN_MEMORY_SUBSCRIBERS**: Stores subscriber preferences
- **IN_MEMORY_PUBLICATIONS**: Stores publication records
- **IN_MEMORY_ENGAGEMENT**: Stores open/click metrics

This means:
- ✅ No database required
- ✅ Fast startup
- ✅ Perfect for demos and testing
- ⚠️ Data is lost when the container stops

## 🎨 Frontend Features

The demo frontend (`demo-frontend.html`) includes:
- **Modern UI**: Gradient design with cards and animations
- **Real-time Stats**: Open/click metrics display
- **Interactive Forms**: Create channels, subscribers, publications
- **Status Indicators**: Visual feedback for API responses
- **Responsive Layout**: Works on desktop and mobile

## 📝 Example Workflow

Try this complete workflow:

1. **Check Health** → Verify system is running
2. **Create Channel** → Add "Email Newsletter" channel
3. **Create Subscriber** → Add subscriber with email
4. **Schedule Newsletter** → Create a newsletter publication
5. **Track Engagement** → Simulate open and click events
6. **View Analytics** → See engagement metrics

## 🔗 Useful Endpoints

- **Frontend**: http://localhost:3000
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **Health Check**: http://localhost:8080/health
- **API Base**: http://localhost:8080/api/v1

## 🛑 Stopping the Demo

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 📖 Next Steps

- Read the [API Documentation](docs/modules/publishing-tools/API-Documentation.md)
- Explore [Integration Scenarios](specs/001-publishing-module/quickstart.md)
- Check [Performance Guide](docs/modules/publishing-tools/Performance-Optimization.md)
- Review [Security Hardening](docs/modules/publishing-tools/Security-Hardening.md)

## 🎉 Enjoy!

You now have a fully functional Publishing Module demo with a visual interface. Experiment with creating channels, subscribers, and tracking engagement metrics!

**Questions?** Check the documentation in `docs/modules/publishing-tools/` or the OpenAPI spec in `specs/001-publishing-module/contracts/api-spec.yaml`.

