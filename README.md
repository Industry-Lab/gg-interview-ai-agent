# AI Agent

A Python project for working with AI APIs, including Claude API for algorithm visualization, analysis, and LeetCode solution generation.

## Features

- Algorithm analysis and visualization
- Integration with Claude API
- LeetCode problem solution generation via API endpoint
- FastAPI backend with interactive documentation

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file in the root directory:
   ```
   ANTHROPIC_API_KEY=your_claude_api_key_here
   ```
4. Run the test script: `python -m tests.test_claude_api`

## Running the API Server

Use the included script to start the FastAPI server:

```bash
python run_api.py
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, view the interactive API documentation at:

```
http://localhost:8000/docs
```

## API Endpoints

### Generate LeetCode Solution

```
POST /api/leetcode-solutions
```

Request body:
```json
{
  "problem": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target...",
  "language": "python"
}
```

Response:
```json
{
  "status": "success",
  "solution": {
    "explanation": "...",
    "code": "def two_sum(nums, target):\n    ...",
    "complexity_analysis": "Time complexity: O(n)..." 
  }
}
```

## Testing the API

Use the included test script to verify the LeetCode solutions endpoint:

```bash
python -m tests.test_leetcode_api
```

## Project Structure

- `src/` - Source code
  - `algorithm_visualizer_service.py` - Service for algorithm visualization
  - `claude_client.py` - Client for interacting with Claude API
  - `leetcode_service.py` - Service for generating LeetCode solutions
  - `api.py` - FastAPI application with API endpoints
- `tests/` - Test scripts
  - `test_claude_api.py` - Tests for Claude API integration
  - `test_leetcode_api.py` - Tests for LeetCode solutions API
- `run_api.py` - Script to run the FastAPI server
- `docs/` - Documentation
