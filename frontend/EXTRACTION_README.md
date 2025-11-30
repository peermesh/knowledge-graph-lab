# Entity Extraction UI

A user-friendly interface for extracting entities and relationships from text using Perplexity AI.

## Features

- **Text Input**: Enter or paste text to extract entities from
- **JSON Output**: View the complete extraction results in formatted JSON
- **Entity List**: Browse extracted entities with details
- **Relationship List**: View relationships between entities
- **Graph Visualization**: Interactive graph showing how entities connect
- **Real-time Stats**: See extraction statistics (entity count, relationship count, processing time)

## Usage

1. **Start the Backend API**: Make sure your FastAPI server is running (default: `http://localhost:8000`)

2. **Open the UI**: Open `extraction.html` in your browser or serve it via a web server

3. **Configure Settings**:
   - **API Base URL**: Set the base URL of your API (default: `http://localhost:8000`)
   - **Confidence Threshold**: Minimum confidence score (0.0-1.0, default: 0.7)
   - **Source Type**: Type of document source (news, academic, social_media, document, unknown)
   - **Entity Types**: Optional comma-separated list of entity types to extract (leave empty for all types)

4. **Enter Text**: Paste or type the text you want to extract entities from

5. **Extract**: Click "Extract Entities" to start the extraction process

6. **View Results**:
   - **JSON Tab**: View the complete API response in JSON format
   - **Entities Tab**: Browse extracted entities with type, confidence, and metadata
   - **Relationships Tab**: View relationships between entities with evidence text
   - **Graph**: Interactive visualization showing entity connections

## API Configuration

Make sure your backend has the `PERPLEXITY_API_KEY` environment variable set:

```bash
export PERPLEXITY_API_KEY=your_api_key_here
```

Or add it to your `.env` file:

```
PERPLEXITY_API_KEY=your_api_key_here
```

## Example

Input text:
```
Acme Ventures invested $5 million in NovaBio, a Boston-based biotech startup founded by Dr. Lina Ortiz on October 22, 2024.
```

Extracted entities:
- Organizations: Acme Ventures, NovaBio
- Person: Dr. Lina Ortiz
- Location: Boston
- Amount: $5 million
- Date: October 22, 2024

Relationships:
- Acme Ventures → invested in → NovaBio
- Dr. Lina Ortiz → founded → NovaBio

## Notes

- Large documents (>10KB) will be processed asynchronously
- The UI will poll for job status if async processing is used
- Graph visualization uses vis-network for interactive exploration
- All results are displayed in real-time as they're extracted

