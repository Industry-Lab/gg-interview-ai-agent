"""
LeetCode Agent definitions for the CrewAI pattern.

This module contains the agent definitions for the LeetCode solution generation system.
"""
import os
from typing import Dict, Any, List

from crewai import Agent
from pydantic import BaseModel, validator

# Get OpenAI API key from environment
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

class SolutionApproach(BaseModel):
    """Model for a solution approach."""
    title: str = ""
    content: str = ""
    rank: int = 999
    time_complexity: str = ""
    space_complexity: str = ""
    code: str = ""
    edge_cases: str = ""
    test_examples: str = ""
    
    # Validator to convert test_examples to string if it's not already
    @validator('test_examples', pre=True)
    def validate_test_examples(cls, v):
        if isinstance(v, list):
            return str(v)
        return v

class LeetCodeAgentFactory:
    """Factory class for creating CrewAI agents for LeetCode solution generation."""
    
    @staticmethod
    def create_leetcode_agent():
        """
        Creates an agent specialized in generating multiple solution approaches
        for LeetCode problems.
        """
        return Agent(
            role="LeetCode Solution Expert",
            goal="Generate multiple high-quality solution approaches for LeetCode problems",
            backstory="""You are an elite algorithm expert with years of experience solving 
            LeetCode problems. You excel at breaking down complex problems and developing 
            multiple solution approaches with varying time and space complexity. Your solutions
            are always well-structured, optimized, and include detailed explanations.""",
            verbose=True,
            llm_model="o3-mini-2025-01-31",
            # Custom tools can be added here if needed
        )
    
    @staticmethod
    def create_criteria_agent():
        """
        Creates an agent that extracts specific criteria that a solution must satisfy.
        """
        return Agent(
            role="Solution Criteria Analyzer",
            goal="Extract and list the specific criteria that a solution must satisfy",
            backstory="""You are a meticulous code reviewer and software quality expert.
            You excel at identifying the key requirements and success criteria for 
            code solutions. Your strength is in understanding what makes a solution 
            valid and complete. For LeetCode problems, you can analyze a solution and
            determine exactly what criteria make it correct, efficient, and robust.""",
            verbose=True,
            llm_model="o3-mini-2025-01-31",
            # Custom tools can be added here if needed
        )
