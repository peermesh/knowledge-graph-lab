# Knowledge Graph Explorer Frontend

This directory contains a lightweight, framework-free web UI for exploring the Knowledge Graph REST API.

## Features

- Run `entity_search`, `relationship_query`, or `similarity_search` against `POST /ai/v1/graph/query`
- Visualize returned entities and relationships with an interactive force-directed graph
- Inspect entity metadata, confidence scores, and relationship directions
- Works out-of-the-box with the default API CORS configuration

## Getting Started

1. Ensure the FastAPI backend is running locally (default: `http://localhost:8000`).
2. Serve the `frontend` directory with any static file server, for example:

   ```powershell
   cd frontend
   python -m http.server 5173
   ```

3. Open the served URL in your browser (e.g., `http://localhost:5173`).
4. Update the **API Base URL** field if your backend uses a different host/port.
5. Submit a query to populate the graph and results list.

> Tip: `relationship_query` provides the richest graph visualization when connected to a populated database.

## Customisation

- Adjust styles in `styles.css`.
- Extend network configuration or behaviours in `app.js`.
- To bundle as part of a larger frontend, import the static assets or migrate the logic into your framework of choice.

