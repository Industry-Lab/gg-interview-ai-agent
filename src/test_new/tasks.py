from crewai import Task

# Define both tasks for the CrewAI workflow
class TaskFactory:
    @staticmethod
    def create_solution_task(solution_agent, problem_text, technology=""):
        """
        Creates the first task to generate a basic solution for a coding problem
        
        Args:
            solution_agent: The agent responsible for this task
            problem_text: The plain text description of the coding problem
            technology: The programming language or technology to use (optional)
            
        Returns:
            A Task object for generating a solution
        """
        tech_instruction = f"You must use {technology} to solve this problem." if technology else ""
        
        return Task(
            description=f"""
            Your task is to analyze the following coding problem and generate a clear, basic solution:
            
            PROBLEM:
            {problem_text}
            
            {tech_instruction}
            
            You should:
            1. Understand the problem requirements
            2. Create a working solution using the specified programming language
            3. Explain your approach in comments
            4. Focus on correctness and readability, not optimization
            
            Your solution should be well-structured with appropriate variable names
            and comments explaining your logic.
            """,
            expected_output="""
            A clear and correct solution to the provided coding problem, with:
            - Well-structured code
            - Detailed explanations of your approach
            - Comments explaining key logic
            - Appropriate variable naming
            """,
            agent=solution_agent
        )
    
    @staticmethod
    def create_criteria_task(criteria_agent, solution_task):
        """
        Creates the second task to convert a solution into criteria
        
        Args:
            criteria_agent: The agent responsible for this task
            solution_task: The previous task that generated the solution
            
        Returns:
            A Task object for generating criteria
        """
        return Task(
            description=f"""
            Based on the coding solution provided by your teammate, extract and list
            the specific criteria that are necessary to satisfy this solution.
            
            Your task is to:
            1. Analyze the solution carefully
            2. Identify the key requirements the solution fulfills
            3. Extract the criteria that would be needed to consider a solution correct
            4. Present these criteria as a clear, organized array of items
            
            Be specific about what makes the solution valid, including any edge cases
            that are handled, algorithmic approaches used, and correctness conditions.
            """,
            expected_output="""
            An array of specific, clear criteria that must be satisfied for a solution
            to be considered correct. Each criterion should be concise but complete.
            Format as a JSON array of strings.
            """,
            agent=criteria_agent,
            context=[solution_task]  # This creates the dependency on the first task
        )
