# 🚀 Quick Start - See Your Publishing Module!

## Easiest Way to Start (No Docker Needed!)

Just run this one command:

```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab
./start-demo.sh
```

Then open your browser to:
- **Frontend Demo**: http://localhost:3000/demo-frontend.html
- **Swagger API Docs**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

Press `Ctrl+C` to stop.

## What You'll See

The demo frontend has 6 interactive sections:
1. 📊 **System Health** - Check if the API is running
2. 📡 **Channels** - Create email, Slack, Discord, webhook channels
3. 👥 **Subscribers** - Add subscribers with email and topics
4. 📰 **Publications** - Schedule newsletters and content
5. 📈 **Engagement** - Track opens and clicks
6. 📊 **Analytics** - View engagement statistics

## Try This Workflow

1. Click "Check Health Status" → See ✅ System Healthy
2. Create a channel → Name: "Email Newsletter", Type: Email
3. Create a subscriber → Add your email
4. Track engagement → Click "Track Open" and "Track Click"
5. View analytics → See the stats update!

## Alternative: Use Swagger UI

For a technical API view:
1. Run `./start-demo.sh`
2. Open http://localhost:8080/docs
3. Try out any of the 21 API endpoints
4. See request/response examples

## Troubleshooting

**Port already in use?**
```bash
# Kill processes on port 8080 or 3000
lsof -ti:8080 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**Dependencies missing?**
```bash
pip3 install -r requirements.txt
```

## What's Running

- **API Server**: FastAPI on port 8080 (with auto-reload)
- **Frontend**: Python HTTP server on port 3000
- **Mode**: DEBUG (in-memory, no database needed)

## About Docker

Docker Desktop is installed but had credential issues. The `start-demo.sh` script runs everything locally without Docker, which is actually easier for development!

If you want to try Docker later once it's fully configured:
```bash
docker compose up --build
```

## Features Implemented

✅ Multi-channel publishing (email, Slack, Discord, webhooks)
✅ Subscriber management with preferences
✅ Newsletter scheduling with timezone awareness
✅ Engagement tracking (opens/clicks)
✅ Real-time analytics
✅ 21 API endpoints
✅ In-memory mode for instant testing

Enjoy exploring your Publishing Module! 🎉

