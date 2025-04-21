# CrewAI Coding Problem Analyzer API

This API uses CrewAI to analyze coding problems with two sequential agents:
1. **Solution Agent**: Generates a basic solution for a coding problem
2. **Criteria Agent**: Extracts criteria from the solution

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set the OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Alternatively, create a `.env` file in this directory with:
```
OPENAI_API_KEY=your-api-key-here
```

## Running the Code

### Running the Example Script

To test the CrewAI implementation with a sample problem:

```bash
# From the project root (/Users/trong/Downloads/GG_Interview/ai_agent)
python -m src.test_new.main
```

### Running the API Server

Start the API server:

```bash
# From the project root (/Users/trong/Downloads/GG_Interview/ai_agent)
python -m uvicorn src.test_new.api:app --reload --port 8000
```

The API will be available at: http://127.0.0.1:8000

## API Endpoints

### Analyze Coding Problem

**POST /analyze**

Request body:
```json
{
  "problem": "Write a function to find the longest substring without repeating characters",
  "technology": "python"  // Optional
}
```

Response body:
```json
{
  "criteria": [
    "The solution should handle empty strings",
    "The solution should track character positions",
    "..."
  ],
  "solution": "def longest_substring(s):\n    # Solution code here..."
}
```

### Health Check

**GET /health**

Response:
```json
{
  "status": "healthy"
}
```

## Interactive API Documentation

When the server is running, you can access interactive documentation at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
