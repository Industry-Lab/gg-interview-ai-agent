"""
LeetCode CrewAI implementation for solution generation.

This module contains the CrewAI implementation for generating and enhancing
LeetCode problem solutions using the standard CrewAI Agents pattern.
"""
import os
from typing import Dict, Any, List
from crewai import Crew, Process
from pydantic import BaseModel

from src.crews.agents.leetcode_agents import LeetCodeAgentFactory
from src.crews.agents.leetcode_tasks import LeetCodeTaskFactory, SolutionApproach, Criteria


class SolutionResult(BaseModel):
    """Model for the complete solution result."""
    approaches: List[SolutionApproach] = []
    criteria: List[Criteria] = []
    status: str = "success"
    error: str = ""

class LeetCodeCrew:
    """
    Manager class for the LeetCode solution generation crew.
    This class replaces the previous Flow-based implementation with standard CrewAI agents.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the LeetCode crew with necessary agents.
        
        Args:
            api_key: Optional OpenAI API key (defaults to environment variable)
        """
        # Set API key if provided
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            
        # Create the agents
        self.leetcode_agent = LeetCodeAgentFactory.create_leetcode_agent()
        self.criteria_agent = LeetCodeAgentFactory.create_criteria_agent()
    
    def solve_leetcode_problem(self, problem_description: str, language: str = "python") -> Dict[str, Any]:
        """
        Generate and enhance solutions for a LeetCode problem.
        
        Args:
            problem_description: The description of the LeetCode problem
            language: The programming language to use (default: python)
            
        Returns:
            A dictionary containing the solution approaches and educational insights
        """
        try:
            # Create the tasks
            solution_task = LeetCodeTaskFactory.create_solution_generation_task(
                self.leetcode_agent,
                problem_description,
                language
            )
            
            criteria_task = LeetCodeTaskFactory.create_criteria_extraction_task(
                self.criteria_agent,
                solution_task
            )
            
            # Create the crew with the sequential process
            crew = Crew(
                agents=[self.leetcode_agent, self.criteria_agent],
                tasks=[solution_task, criteria_task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the crew
            result = crew.kickoff()
            
            # Process results into a structured format
            solution_result = SolutionResult(status="success")
            
            print("\nDEBUG - Processing solution approaches from task output")
            
            try:
                # Get the approaches directly from the Pydantic model in the task output
                # This is much simpler thanks to the output_pydantic parameter
                if hasattr(solution_task.output, 'pydantic'):
                    # Access the structured Pydantic output from the task
                    approaches_data = solution_task.output.pydantic
                    
                    if hasattr(approaches_data, 'approaches'):
                        # Get the approaches list from the Pydantic model
                        approaches_list = approaches_data.approaches
                        
                        # Sort approaches by rank (best first)
                        approaches_list = sorted(approaches_list, key=lambda x: x.rank)
                        solution_result.approaches = approaches_list
                        print(f"DEBUG - Successfully processed {len(approaches_list)} approaches from structured output")
                    else:
                        print("ERROR - No approaches found in Pydantic output")
                        # Create a single fallback approach
                        solution_result.approaches = [SolutionApproach(
                            title="Fallback Solution",
                            content="No structured approaches were generated. Please try again.",
                            rank=1
                        )]
                else:
                    print("ERROR - Task output does not have expected Pydantic structure")
                    # Create a single fallback approach
                    solution_result.approaches = [SolutionApproach(
                        title="Fallback Solution",
                        content="No structured approaches were generated. Please try again.",
                        rank=1
                    )]
                
            except Exception as e:
                print(f"Error parsing solution approaches: {str(e)}")
                solution_result.error = f"Error parsing solution approaches: {str(e)}"
            
            # Extract solution criteria from the second task output
            print("\nDEBUG - Processing solution criteria from task output")
            
            try:
                # Get the criteria directly from the Pydantic model in the task output
                # This is much simpler thanks to the output_pydantic parameter
                if hasattr(criteria_task.output, 'pydantic'):
                    # Access the structured Pydantic output
                    criteria_data = criteria_task.output.pydantic
                    
                    # Add criteria to solution result directly from the Pydantic model
                    solution_result.criteria = criteria_data.criteria
                    
                    print(f"DEBUG - Successfully processed {len(criteria_data.criteria)} criteria from structured output")
                else:
                    print("ERROR - Task output does not have expected Pydantic structure")
                    # Use fallback values - create a single fallback criterion
                    solution_result.criteria = [Criteria(
                        id="fallbackCriterion",
                        description="No structured criteria were generated.",
                        pattern=""
                    )]
                
            except Exception as e:
                print(f"Error parsing educational insights: {str(e)}")
                solution_result.error += f" Error parsing educational insights: {str(e)}"
            
            return solution_result.dict()
            
        except Exception as e:
            print(f"Error in LeetCodeCrew: {str(e)}")
            return SolutionResult(
                status="error",
                error=f"Error in LeetCodeCrew: {str(e)}"
            ).dict()
