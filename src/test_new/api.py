"""
FastAPI application to expose the CrewAI coding solution crew as an API
"""
import os
import json
from typing import Dict, List, Optional, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Import our crew manager
from src.test_new.crew import CodingCrewManager

# Load environment variables
load_dotenv()

# Ensure OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it before starting the API."
    )

# Create FastAPI app
app = FastAPI(
    title="Coding Problem Analysis API",
    description="API for analyzing coding problems using CrewAI agents",
    version="1.0.0",
)

# Define request and response models
class ProblemRequest(BaseModel):
    problem: str = Field(..., description="The coding problem to analyze")
    technology: Optional[str] = Field(None, description="The technology or programming language to use")

class CriteriaResponse(BaseModel):
    criteria: List[str] = Field(..., description="Array of criteria for a valid solution")
    solution: str = Field(..., description="The generated solution")

# Create a crew manager instance
crew_manager = CodingCrewManager()

@app.post("/analyze", response_model=CriteriaResponse, tags=["Analysis"])
async def analyze_problem(request: ProblemRequest) -> Dict[str, Union[List[str], str]]:
    """
    Analyze a coding problem and return both the solution and solution criteria
    
    This endpoint:
    1. Uses Agent 1 to generate a solution for the given problem
    2. Uses Agent 2 to extract criteria from the solution
    3. Returns both the solution and the criteria as a JSON response
    """
    try:
        # Run the crew analysis
        result = crew_manager.analyze_problem(
            problem_text=request.problem,
            technology=request.technology or ""
        )
        
        # Debug information to understand CrewOutput structure
        print(f"Result type: {type(result)}")
        if hasattr(result, 'tasks_output'):
            print(f"Has tasks_output with {len(result.tasks_output)} tasks")
        
        # Default values
        solution = "No solution generated"
        criteria_array = []
        
        # Handle if result is a CrewOutput object
        if hasattr(result, 'tasks_output') and result.tasks_output:
            # Print debug info about task outputs
            for i, task in enumerate(result.tasks_output):
                print(f"Task {i} type: {type(task)}")
                print(f"Task {i} has raw: {hasattr(task, 'raw')}")
            
            # Extract solution from first agent (task 0)
            if len(result.tasks_output) > 0:
                solution = str(result.tasks_output[0].raw) if hasattr(result.tasks_output[0], 'raw') else str(result.tasks_output[0])
            
            # Extract criteria from second agent (task 1)
            if len(result.tasks_output) > 1:
                criteria_text = str(result.tasks_output[1].raw) if hasattr(result.tasks_output[1], 'raw') else str(result.tasks_output[1])
                print(f"Criteria text: {criteria_text[:100]}...") # Debug first 100 chars
                
                # Try to parse JSON
                try:
                    # Handle if it's already valid JSON
                    if criteria_text.strip().startswith('[') and criteria_text.strip().endswith(']'):
                        criteria_array = json.loads(criteria_text)
                    else:
                        criteria_array = [criteria_text]
                except json.JSONDecodeError:
                    # If JSON parsing fails, strip the escaped JSON and try again
                    try:
                        # Find the opening bracket by searching for "["
                        start_idx = criteria_text.find('["')
                        end_idx = criteria_text.rfind('"]')
                        
                        if start_idx >= 0 and end_idx >= 0 and end_idx > start_idx:
                            # Extract the JSON part
                            json_content = criteria_text[start_idx:end_idx+2]
                            # Clean up escaped quotes
                            json_content = json_content.replace("\\\"", "\"")
                            print(f"Extracted JSON: {json_content[:50]}...") # Debug
                            criteria_array = json.loads(json_content)
                        else:
                            # Fallback - split by newlines and remove quote marks
                            criteria_array = [line.strip().strip('"') for line in criteria_text.split('\n') if line.strip()]
                    except Exception as e:
                        print(f"Fallback parsing error: {e}")
                        # Last resort: return it as a single item
                        criteria_array = [criteria_text]
        
        # Handle if result is a dictionary
        elif isinstance(result, dict):
            solution = str(result.get("solution", "No solution generated"))
            criteria_text = str(result.get("criteria", "No criteria generated"))
            
            # Try to parse JSON
            try:
                if criteria_text.strip().startswith('[') and criteria_text.strip().endswith(']'):
                    criteria_array = json.loads(criteria_text)
                else:
                    criteria_array = [criteria_text]
            except Exception:
                criteria_array = [criteria_text]
        
        # If we still have no criteria, provide a default
        if not criteria_array:
            criteria_array = ["No criteria could be extracted"]
        
        # Ensure all items are strings
        criteria_array = [str(item).strip() for item in criteria_array if item]
        
        # Create the response
        return {
            "solution": str(solution),
            "criteria": criteria_array
        }
    
    except Exception as e:
        # Log the full exception for debugging
        import traceback
        print(f"Error analyzing problem: {str(e)}")
        print(traceback.format_exc())
        
        # Return a more detailed error response
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing problem: {str(e)}"
        )

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health check endpoint to verify the API is running
    """
    return {"status": "healthy"}

# Run the application if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
