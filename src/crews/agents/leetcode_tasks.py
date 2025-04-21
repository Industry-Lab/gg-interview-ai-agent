"""
LeetCode Task definitions for the CrewAI pattern.

This module contains the task definitions for the LeetCode solution generation system.
"""
from typing import Optional, List, Any
from pydantic import BaseModel, Field
from crewai import Task

class SolutionApproach(BaseModel):
    """Model for a LeetCode solution approach."""
    title: str = Field(..., description="A descriptive name for the approach")
    content: str = Field(..., description="Detailed explanation of how the approach works")
    rank: int = Field(default=999, description="Numeric ranking of this approach (1 = best)")
    time_complexity: str = Field(default="", description="Big O notation for time complexity")
    space_complexity: str = Field(default="", description="Big O notation for space complexity")
    code: str = Field(default="", description="Implementation code in the specified language")
    edge_cases: str = Field(default="", description="How the approach handles edge cases")
    test_examples: str = Field(default="", description="Example test cases showing the solution works")

class Criteria(BaseModel):
    """Model for a Criteria that satisfied the solution"""
    id: str = Field(default="", description="A short key, must be a concise camelCase key (e.g. `subtractRule`)")
    description: str = Field(default="", description="Should be a human‑readable sentence of what to detect, or what to consider that the solution is correct")

    # For Pydantic v2 compatibility
    model_config = {
        "extra": "ignore",  # Ignore extra fields
        "validate_assignment": True,  # Validate when values are assigned
    }
    
    @classmethod
    def model_validate(cls, obj: Any, *args, **kwargs):
        # If pattern is not a string, convert it
        if isinstance(obj, dict) and "pattern" in obj and not isinstance(obj["pattern"], str):
            obj["pattern"] = str(obj["pattern"])
        return super().model_validate(obj, *args, **kwargs)

class SolutionApproaches(BaseModel):
    """Model for a collection of solution approaches."""
    approaches: List[SolutionApproach] = Field(..., description="List of solution approaches")

class SolutionCriteria(BaseModel):
    """Model for solution criteria."""
    criteria: List[Criteria] = Field(..., description="Array of specific criteria that must be satisfied for a valid solution")

class LeetCodeTaskFactory:
    """Factory class for creating CrewAI tasks for LeetCode solution generation."""
    
    @staticmethod
    def create_solution_generation_task(solution_agent, problem_description: str, language: str = "python"):
        """
        Creates a task for generating multiple solution approaches for a LeetCode problem.
        
        Args:
            solution_agent: The agent responsible for generating solutions
            problem_description: The description of the LeetCode problem
            language: The programming language to use (default: python)
            
        Returns:
            A Task object for generating solutions
        """
        return Task(
            description=f"""
            Generate 1 – 2 high‑quality solution approaches for the following Interview problem.
            
            ─────────────────
            PROBLEM:
            {problem_description}
            ─────────────────
            
            GUIDELINES:
            1. Analyze the problem thoroughly, **Read the problem carefully** and solve *exactly* what is asked (do not change the task).
            2. Generate only 1 or 2 solution (that you considering the most popular, and the most acceptable) solutions approaches with time/space complexity
            3. **Approach ordering matters**:
               • **Rank 1** must be the solution that:
                   – Matches the problem requirements most directly
                   – Is the approach the majority of candidates (and the official editorial) typically use  
               • **Rank 2** (optional) may show a more advanced / theoretically optimal alternative (e.g., uses specialised data structures or subtle optimisations).  
                 Include it **only when it offers a genuine improvement** in asymptotics *or* noteworthy insight.
            4. For each approach, provide:
               • `"title"`– short and descriptive (e.g., “Hash‑map Single Pass”).  
               • `"content"`– clear step‑by‑step explanation of the idea.  
               • `"time_complexity"` and `"space_complexity"` – in Big‑O with a brief justification.  
               • `"code"`– well‑commented reference implementation in **{language}** that compiles / runs.  
               • `"edge_cases"`– how the code handles tricky inputs (empty array, duplicates, overflow, etc.).  
               • `"test_examples"`– succinct I/O pairs demonstrating correctness.
            5. **Do not exceed 2 approaches**.  
            6. Rank the approaches from 1 (best) to N based on *Approach ordering matters* Rule above
            7. Output **valid JSON** conforming exactly to this schema:
            {{
              "approaches": [
                {{
                  "title": "Approach name",
                  "content": "Detailed explanation",
                  "rank": 1,
                  "time_complexity": "O(...)",
                  "space_complexity": "O(...)",
                  "code": "# implementation in {language}",
                  "edge_cases": "Edge case handling",
                  "test_examples": "Example test cases"
                }},
                // (optionally one more object with "rank": 2)
                ...
              ]
            }}
            
            Ensure your output is valid JSON and contains all the required fields.
            Your solution must be comprehensive, correct, and educational.
            """,
            expected_output="""
            A JSON object with an 'approaches' array containing multiple solution approaches with all required fields
            """,
            agent=solution_agent,
            output_pydantic=SolutionApproaches
        )
    
    @staticmethod
    def create_criteria_extraction_task(criteria_agent, solution_generation_task):
        """
        Creates a task for extracting specific criteria that a solution must satisfy.
        
        Args:
            criteria_agent: The agent responsible for extracting criteria
            solution_generation_task: The previous task that generated the solutions
            
        Returns:
            A Task object for extracting solution criteria
        """
        return Task(
            description="""
            You will be given one(or more) reference solutions for a coding problem.
            **Chose the RANK 1 solution to create a criteria list only**
            Your job is to extract a **checklist of concrete, observable criteria** the
            candidate’s solution must satisfy, but that criteria should only on Middle Level

            ==========================
            ABSOLUTE RULES
            ==========================
            1. Every criterion must correspond to **something the evaluation system can
               match directly in the candidate’s editor** (code tokens, function name,
               library import, loop structure, explicit branch, etc.).  
               •Do NOT invent abstract “should be efficient” statements without a code‑level cue.  
               •Do NOT combine multiple ideas in one criterion.
            
            2. Each criterion object **must** contain these keys *exactly*: 
            •`id`          – camelCase, 4‑20 chars, unique in the list. 
            •`description` – The clear and deeply detail English telling a reviewer what the 
            criteria is and how should they check. The reviewer will based on the description you provided, 
            then compare the criteria description with what the user is doing on the screen to consider if the 
            criteria is fulfilled. So please detail, specific, singular, and measurable. The more specific detail the 
            better. 
            *Note*: Don't include the exact code character/name like "Check for the expression 'int complement = 
            target - nums[i];'" or "Look for the line where 'return new int[]{map.get(complement), i};'" 
            Because each person have the different style for naming their code, specific the function/class/object/variable/syntax... name or character, code-by-code can cause the problem that even the 
            solution is correct, the reviewer is too strictly follow the rule and don't consider it as correct, be flexible
                     
            3. If the reference solution shows an **edge‑case check**, **complexity
               guarantee**, or **specific library usage**, you *must* create a separate
               criterion for it.
            
            4. If there are more than 5 criteria available, choose only top 5 (or less than 5) criteria that you think the most easiest for candidate to archived, if there are more than 5 criteria available, 
               choose what is the most specific, singular, and measurable to kept
               
            5.
            ==========================
            OUTPUT FORMAT
            ==========================
            A JSON object with a `"criteria"` array whose entries each have `id`, `description`, and `pattern` fields:
            ```json
            {
              "criteria": [
                {
                  "id": "handlesEmptyInput",
                  "description": "Returns an empty result immediately when the input array is empty.",
                },
                {
                  "id": "usesHashMapLookup",
                  "description": "Uses a hash map to achieve O(n) lookup time for complements.",
                },
                {
                  "id": "earlyReturnOnMatch",
                  "description": "Returns indices as soon as a valid pair is found (no full scan).",
                }
                // … more criteria …
              ]
            }
            
            **Remember**: 
            A criterion is only useful if the evaluation is specific, singular, and measurable. The reviewer who use the criteria is the realtime LLM that 
            can only see and hear using websocket, not the real human, if you consider the criteria is hard for that realtime LLM to measure or justify, please re-consider
            """,
            expected_output="""
            A JSON object containing an array of specific, clear criteria that must be satisfied for a solution to be considered correct.
            """,
            agent=criteria_agent,
            context=[solution_generation_task],  # This creates the dependency on the first task
            output_pydantic=SolutionCriteria
        )
