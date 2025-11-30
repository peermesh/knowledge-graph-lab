# How to Serve the Frontend

## The Problem
Opening `extraction.html` directly (double-clicking) uses the `file://` protocol, which browsers block for security reasons. You need to serve it via HTTP.

## Solution: Use a Local Web Server

### Option 1: Python HTTP Server (Easiest)

**Windows PowerShell:**
```powershell
# Navigate to frontend folder
cd C:\Users\haejeg\Documents\GitHub\knowledge-graph-lab\frontend

# Start server (Python 3)
python -m http.server 8080

# OR if python doesn't work, try:
python3 -m http.server 8080

# OR if you have py launcher:
py -m http.server 8080
```

**Then open in browser:**
```
http://localhost:8080/extraction.html
```

### Option 2: Node.js http-server

If you have Node.js installed:
```powershell
cd frontend
npx http-server -p 8080
```

Then open: `http://localhost:8080/extraction.html`

### Option 3: VS Code Live Server Extension

1. Install "Live Server" extension in VS Code
2. Right-click `extraction.html`
3. Select "Open with Live Server"

### Option 4: Use Backend to Serve Frontend (Advanced)

You can configure FastAPI to serve static files, but the simple HTTP server is easier for testing.

## Quick Start Command

**In PowerShell, run this from the project root:**
```powershell
cd frontend; python -m http.server 8080
```

Then open: `http://localhost:8080/extraction.html`

