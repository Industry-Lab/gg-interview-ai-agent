from crewai import Crew, Process
# Use absolute imports instead of relative imports
from src.test_new.agents import AgentFactory
from src.test_new.tasks import TaskFactory

class CodingCrewManager:
    """
    Manager class for setting up and running the coding solution crew
    """
    
    def __init__(self):
        # Create the agents
        self.solution_agent = AgentFactory.create_solution_agent()
        self.criteria_agent = AgentFactory.create_criteria_agent()
    
    def analyze_problem(self, problem_text, technology=""):
        """
        Set up the crew and tasks to analyze a coding problem
        
        Args:
            problem_text: Plain text description of the coding problem
            
        Returns:
            The result of the crew execution (criteria for the solution)
        """
        # Create the tasks with the appropriate sequence
        solution_task = TaskFactory.create_solution_task(
            self.solution_agent, 
            problem_text,
            technology
        )
        
        criteria_task = TaskFactory.create_criteria_task(
            self.criteria_agent,
            solution_task
        )
        
        # Create the crew with the sequential process
        crew = Crew(
            agents=[self.solution_agent, self.criteria_agent],
            tasks=[solution_task, criteria_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        # Get the specific outputs from each task
        # Access task output correctly - the output is already a string
        solution_output = str(solution_task.output) if solution_task.output else "No solution generated"
        criteria_output = result  # The result is already the criteria from the second task
        
        return {
            "solution": solution_output,
            "criteria": criteria_output
        }
