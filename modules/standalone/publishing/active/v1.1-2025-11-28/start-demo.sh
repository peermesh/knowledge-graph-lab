#!/bin/bash

# Start Publishing Module Demo
# This script starts the API and frontend without Docker

echo "🚀 Starting Publishing Module Demo..."
echo ""

# Set DEBUG mode for in-memory stores
export DEBUG=true
export PYTHONPATH=/Users/benschreiber/Desktop/knowledge-graph-lab

# Check if port 8080 is already in use
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8080 is already in use. Stopping existing process..."
    kill -9 $(lsof -t -i:8080) 2>/dev/null
    sleep 2
fi

# Start the API server
echo "📡 Starting API server on http://localhost:8080..."
cd /Users/benschreiber/Desktop/knowledge-graph-lab
uvicorn src.publishing.main:app --host 0.0.0.0 --port 8080 --reload &
API_PID=$!

# Wait for API to be ready
echo "⏳ Waiting for API to start..."
for i in {1..30}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ API is ready!"
        break
    fi
    sleep 1
    if [ $i -eq 30 ]; then
        echo "❌ API failed to start. Check the logs above."
        exit 1
    fi
done

# Check if port 3000 is already in use
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 3000 is already in use. Stopping existing process..."
    kill -9 $(lsof -t -i:3000) 2>/dev/null
    sleep 2
fi

# Start the frontend server
echo "🎨 Starting frontend server on http://localhost:3000..."
cd /Users/benschreiber/Desktop/knowledge-graph-lab
python3 -m http.server 3000 > /dev/null 2>&1 &
FRONTEND_PID=$!

echo ""
echo "✨ Publishing Module Demo is running!"
echo ""
echo "📱 Open these URLs in your browser:"
echo "   Frontend:   http://localhost:3000/demo-frontend.html"
echo "   Swagger UI: http://localhost:8080/docs"
echo "   Health:     http://localhost:8080/health"
echo ""
echo "💡 Press Ctrl+C to stop the demo"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping demo..."
    kill $API_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Keep script running
wait

