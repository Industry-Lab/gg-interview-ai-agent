from crewai import Agent

# Define both agents that will be used in the CrewAI
class AgentFactory:
    @staticmethod
    def create_solution_agent():
        """
        Creates the first agent that generates a basic solution for a coding problem
        """
        return Agent(
            role="Coding Solution Generator",
            goal="Generate a clear and effective basic solution for coding problems",
            backstory="""You are an experienced software developer with expertise in 
            algorithmic problem-solving. You excel at breaking down complex problems
            into simple, understandable solutions. Your focus is on readability and 
            correctness rather than optimization.""",
            verbose=True,
            llm="o3-mini-2025-01-31"  # Specify the OpenAI model
        )
    
    @staticmethod
    def create_criteria_agent():
        """
        Creates the second agent that converts a solution into an array of criteria
        """
        return Agent(
            role="Solution Criteria Analyzer",
            goal="Extract and list the specific criteria that a solution must satisfy",
            backstory="""You are a meticulous code reviewer and software quality expert.
            You excel at identifying the key requirements and success criteria for 
            code solutions. Your strength is in understanding what makes a solution 
            valid and complete.""",
            verbose=True,
            llm="o3-mini-2025-01-31"  # Specify the OpenAI model
        )
