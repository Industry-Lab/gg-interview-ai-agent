"""
Crew-based LeetCode API

This module provides a FastAPI application with a crew-based architecture
for generating LeetCode solutions using multiple specialized agents.
"""
import os
import dotenv
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic.functional_validators import model_validator

# Load environment variables from .env file
dotenv.load_dotenv()

# Import the new crew implementation
from src.crews.leetcode_crew import LeetCodeCrew

# Initialize FastAPI app
app = FastAPI(
    title="LeetCode Crew API",
    description="API for AI-powered LeetCode solutions using a crew of specialized agents",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define request and response models using Pydantic
class LeetCodeSolutionRequest(BaseModel):
    # Primary fields
    title: str = Field(..., description="Problem title")
    content: str = Field(..., description="The LeetCode problem content/description in HTML format")
    category: Optional[list] = Field(None, description="Problem categories/tags")
    constraints: Optional[list] = Field(None, description="Problem constraints")
    url: Optional[str] = Field(None, description="Problem URL")
    
    # Language fields - make programmingLanguage optional to handle both formats
    programmingLanguage: Optional[str] = Field(None, description="Programming language for the solution (python, java, javascript, etc.)")
    programLanguage: Optional[str] = Field(None, description="Programming language (alternative field name)")
    language: Optional[str] = Field(None, description="Programming language (legacy field)")
    
    # Other optional fields for compatibility
    id: Optional[str] = Field(None, description="LeetCode problem ID")
    difficulty: Optional[str] = Field(None, description="Problem difficulty")
    hasSolution: Optional[bool] = Field(None, description="Whether the problem has a solution")
    titleSlug: Optional[str] = Field(None, description="Problem title slug")
    exampleTestcases: Optional[str] = Field(None, description="Example test cases")
    problem: Optional[str] = Field(None, description="The LeetCode problem description (legacy field)")
    
    # Model validators
    @model_validator(mode="after")
    def check_language_field(self) -> "LeetCodeSolutionRequest":
        """Ensure at least one language field is set, and set a default if none is provided."""
        if not any([self.programmingLanguage, self.programLanguage, self.language]):
            # If no language is specified, default to Python
            self.programmingLanguage = "python"
        return self

class ApproachDetail(BaseModel):
    """Details of a single solution approach"""
    rank: int = Field(..., description="Rank/order of the approach (1 is best)")
    title: str = Field(..., description="Title of the approach")
    content: str = Field(..., description="Full content of the approach")
    time_complexity: Optional[str] = Field(None, description="Time complexity analysis")
    space_complexity: Optional[str] = Field(None, description="Space complexity analysis")
    code: Optional[str] = Field(None, description="Code implementation of the approach")

class Criteria(BaseModel):
    """Model for a single criterion that a solution must satisfy"""
    id: str = Field("", description="A short key in camelCase format (e.g. `subtractRule`)")
    description: str = Field("", description="Human-readable sentence describing the requirement")
    pattern: str = Field("", description="Code pattern or hint to recognize this criterion")
    
    def __init__(self, **data):
        # Directly ensure pattern is a string before initialization
        if 'pattern' in data and not isinstance(data['pattern'], str):
            data['pattern'] = str(data['pattern'])
        super().__init__(**data)

class SolutionCriteria(BaseModel):
    """Criteria that a LeetCode solution must satisfy"""
    criteria: List[Criteria] = Field([], description="Specific criteria that must be satisfied for a solution to be correct")

class ApproachResponse(BaseModel):
    """Model for a solution approach in the API response"""
    title: str = Field("", description="Title of the approach")
    content: str = Field("", description="Full content of the approach")
    rank: int = Field(999, description="Rank of the approach (lower is better)")
    time_complexity: str = Field("", description="Time complexity analysis")
    space_complexity: str = Field("", description="Space complexity analysis")
    code: str = Field("", description="Code implementation of the approach")
    edge_cases: str = Field("", description="Edge cases handled by the approach")
    test_examples: str = Field("", description="Test examples for the approach")

class LeetCodeSolutionResponse(BaseModel):
    """Response model for LeetCode solution generation"""
    status: str = Field("success", description="Status of the solution generation request")
    introduction: Optional[str] = Field(None, description="Brief introduction to the problem and solution")
    solutions: Optional[List[Dict[str, Any]]] = Field(None, description="List of solution objects")
    full_text: Optional[str] = Field(None, description="Complete solution text")
    approach_count: Optional[int] = Field(None, description="Number of solution approaches generated")
    approaches: Optional[List[ApproachResponse]] = Field(None, description="List of solution approaches")
    language: Optional[str] = Field(None, description="Programming language used for the solutions")
    solution_criteria: Optional[Dict[str, Any]] = Field(None, description="Criteria that the solution must satisfy")
    criteria_error: Optional[str] = Field(None, description="Error message if criteria extraction failed")

# Dependency to get LeetCodeCrew instance
def get_leetcode_crew():
    """
    Function to get or create the LeetCode crew.
    This implementation ensures we reuse a single crew throughout the lifetime of the application.
    """
    # Create a new LeetCodeCrew instance if one doesn't exist
    if not hasattr(get_leetcode_crew, "crew"):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
            )
        get_leetcode_crew.crew = LeetCodeCrew(api_key=api_key)
    
    return get_leetcode_crew.crew

@app.post("/api/leetcode-solutions", response_model=LeetCodeSolutionResponse)
async def generate_leetcode_solution(
    request: LeetCodeSolutionRequest
):
    """
    Generate multiple solution approaches for a LeetCode problem using an AI agent crew.
    
    This endpoint:
    1. Takes a LeetCode problem description and language preference
    2. Passes the request to a specialized crew of AI agents
    3. Returns multiple solution approaches with detailed explanations
    """
    try:
        problem_description = request.content
        language = next((lang for lang in [request.programmingLanguage, 
                                           request.programLanguage, 
                                           request.language] if lang), "python")
        
        print(f"📝 Generating solutions for: {problem_description[:50]}...")
        print(f"🔤 Using language: {language}")
        
        # Check if we have a valid problem description
        if not problem_description or len(problem_description.strip()) < 10:
            return {
                "status": "error",
                "message": "Problem description is too short or empty."
            }
        
        # Get the LeetCode crew
        crew = get_leetcode_crew()
        
        # Solve the problem using the CrewAI agent-based approach
        print("🤖 Running LeetCode agents to solve the problem...")
        solution_result = crew.solve_leetcode_problem(
            problem_description=problem_description,
            language=language
        )
        
        # Initialize the result structure
        result = {
            "leetcode_problem": problem_description,
            "language": language,
            "approaches": [],
            "solution_criteria": {},
            "status": "success"
        }
        
        # Process approaches from the solution result
        approaches_list = []
        solutions_list = []
        introduction = ""
        full_text = ""
        approach_count = 0
        
        if "approaches" in solution_result and solution_result["approaches"]:
            # Convert approaches to ApproachResponse objects for the API response
            approach_responses = []
            for approach in solution_result["approaches"]:
                # First convert to dictionary if needed
                if isinstance(approach, dict):
                    approach_dict = approach
                else:
                    # Try to convert to dictionary if it's not already
                    try:
                        approach_dict = approach.dict() if hasattr(approach, 'dict') else dict(approach)
                    except:
                        # Fallback: create minimal dictionary
                        approach_dict = {"title": "Solution Approach", "content": str(approach)}
                
                # Create an ApproachResponse object with all fields (default values will be used for missing fields)
                approach_response = ApproachResponse(
                    title=approach_dict.get('title', ''),
                    content=approach_dict.get('content', ''),
                    rank=approach_dict.get('rank', 999),
                    time_complexity=approach_dict.get('time_complexity', ''),
                    space_complexity=approach_dict.get('space_complexity', ''),
                    code=approach_dict.get('code', ''),
                    edge_cases=approach_dict.get('edge_cases', ''),
                    test_examples=approach_dict.get('test_examples', '')
                )
                
                approach_responses.append(approach_response)
                
                # Create string representations for the approaches and solutions lists
                rank_prefix = f"{approach_dict.get('rank', 0)}: " if 'rank' in approach_dict else ""
                approaches_list.append(f"{rank_prefix}{approach_dict.get('title', 'Solution Approach')}")
                solutions_list.append(approach_dict)
            
            result["approaches"] = approach_responses
            approach_count = len(approach_responses)
            
            # Create an introduction from the best approach (first one after sorting by rank)
            if approach_responses:
                best_approach = min(approach_responses, key=lambda x: x.rank if x.rank is not None else 999)
                introduction = f"{best_approach.title} - {best_approach.content[:200]}..."
                
                # Create a full text representation of all solutions
                full_text_parts = []
                for i, approach in enumerate(approach_responses):
                    full_text_parts.append(f"## Approach {i+1}: {approach.title or 'Solution'}\n\n")
                    full_text_parts.append(f"{approach.content}\n\n")
                    full_text_parts.append(f"**Time Complexity**: {approach.time_complexity or 'Not specified'}\n")
                    full_text_parts.append(f"**Space Complexity**: {approach.space_complexity or 'Not specified'}\n\n")
                    
                    if approach.code:
                        full_text_parts.append(f"```{language}\n{approach.code}\n```\n\n")
                    
                    if approach.edge_cases:
                        full_text_parts.append(f"**Edge Cases**: {approach.edge_cases}\n\n")
                        
                    if approach.test_examples:
                        full_text_parts.append(f"**Test Examples**:\n{approach.test_examples}\n\n")
                full_text = ''.join(full_text_parts)
        
        # Add the calculated fields to the result
        result["solutions"] = solutions_list
        result["introduction"] = introduction
        result["full_text"] = full_text
        result["approach_count"] = approach_count
        
        # Process solution criteria - with safer direct approach
        try:
            # Prepare raw criteria data first to avoid model validation issues
            raw_criteria = []
            
            if "criteria" in solution_result and solution_result["criteria"]:
                for criterion in solution_result["criteria"]:
                    try:
                        # Create a clean dictionary with string values
                        criterion_dict = {}
                        
                        if isinstance(criterion, dict):
                            # Get values from dict with string conversion
                            criterion_dict["id"] = str(criterion.get("id", "") or "")
                            criterion_dict["description"] = str(criterion.get("description", "") or "")
                            criterion_dict["pattern"] = str(criterion.get("pattern", "") or "")
                        elif hasattr(criterion, "id") and hasattr(criterion, "description"):
                            # Get values from object with string conversion
                            criterion_dict["id"] = str(criterion.id) if criterion.id else ""
                            criterion_dict["description"] = str(criterion.description) if criterion.description else ""
                            
                            if hasattr(criterion, "pattern"):
                                criterion_dict["pattern"] = str(criterion.pattern) if criterion.pattern is not None else ""
                            else:
                                criterion_dict["pattern"] = ""
                        else:
                            # Fallback for simple string
                            criterion_dict["id"] = f"criterion{len(raw_criteria) + 1}"
                            criterion_dict["description"] = str(criterion) if criterion else ""
                            criterion_dict["pattern"] = ""
                            
                        # Add cleaned dictionary to raw criteria
                        raw_criteria.append(criterion_dict)
                    except Exception as e:
                        print(f"Error processing individual criterion: {str(e)}")
                        # Add a fallback criterion
                        raw_criteria.append({
                            "id": f"fallbackCriterion{len(raw_criteria) + 1}",
                            "description": "Error processing criterion",
                            "pattern": ""
                        })
            
            # Now create Criteria objects from clean data
            criteria_list = []
            for raw_criterion in raw_criteria:
                # Direct dictionary construction to avoid validation issues
                criteria_list.append({
                    "id": raw_criterion["id"],
                    "description": raw_criterion["description"],
                    "pattern": raw_criterion["pattern"]
                })
            
            # Create SolutionCriteria with raw dictionaries
            solution_criteria = {"criteria": criteria_list}
            
        except Exception as e:
            print(f"Error processing solution criteria: {str(e)}")
            # Create a fallback solution criteria as raw dict
            solution_criteria = {
                "criteria": [{
                    "id": "errorCriterion",
                    "description": f"Error processing criteria: {str(e)}",
                    "pattern": ""
                }]
            }
        result["solution_criteria"] = solution_criteria
        
        # Check for errors
        if solution_result.get("status") == "error":
            result["status"] = "error"
            result["message"] = solution_result.get("error", "Unknown error occurred")
            raise HTTPException(status_code=500, detail=result["message"])
    
        # Ensure we have approaches
        if not result.get("approaches") or len(result.get("approaches", [])) == 0:
            print("⚠️ No solution approaches generated")
            return {
                "status": "error",
                "message": "No solution approaches could be generated. Please try again or modify your problem description."
            }
        
        # Ensure we have solution criteria
        if not result.get("solution_criteria") or not isinstance(result["solution_criteria"], dict) or "criteria" not in result["solution_criteria"]:
            # Set default criteria if none were generated
            result["solution_criteria"] = {
                "criteria": [{
                    "id": "defaultCriterion",
                    "description": "The solution must handle the given test cases correctly.",
                    "pattern": ""
                }]
            }
        
        print(f"✅ Generated {len(result.get('approaches', []))} solution approaches")
        return result
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        import traceback
        print(f"Error generating solution: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error generating solution: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint for the API"""
    return {
        "status": "healthy", 
        "model": "o3-mini-2025-01-31", 
        "architecture": "agent-based", 
        "agents": ["leetcode-solutions", "criteria-analyzer"],
        "features": [
            "structured solutions", 
            "solution criteria", 
            "solution validation", 
            "correctness assessment",
            "multi-approach solutions",
            "sequential task execution"    
        ]
    }

# Main entry point for running the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.crew_api:app", host="0.0.0.0", port=8000, reload=True)
