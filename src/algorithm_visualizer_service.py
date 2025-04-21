"""
Algorithm Visualizer Service

This module provides services for analyzing algorithms and generating visualizations using Claude API.
"""
import json
from typing import Dict, Any, Optional, List, Union

from .claude_client import ClaudeClient

class AlgorithmVisualizerService:
    """Service for analyzing algorithms and generating visualizations."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the service with a Claude client.
        
        Args:
            api_key: Claude API key. If None, will look for ANTHROPIC_API_KEY environment variable.
        """
        self.claude_client = ClaudeClient(api_key)
    
    def analyze_algorithm(self, code: str, problem_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze an algorithm using Claude API.
        
        Args:
            code: The code to analyze
            problem_description: Optional description of the problem the code solves
            
        Returns:
            Dict containing analysis results
        """
        return self.claude_client.analyze_algorithm(code, problem_description)
    
    def generate_visualization(self, code: str, problem_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a visualization for an algorithm.
        
        Args:
            code: The code to visualize
            problem_description: Optional description of the problem the code solves
            
        Returns:
            Dict containing visualization specification
        """
        analysis = self.analyze_algorithm(code, problem_description)
        
        if "error" in analysis:
            return {
                "status": "error",
                "error": analysis["error"],
                "diagram_specification": self._generate_error_diagram(analysis["error"])
            }
        
        # Generate a visualization based on the analysis
        try:
            diagram_spec = self._generate_diagram_from_analysis(analysis, code, problem_description)
            return {
                "status": "success",
                "algorithm_analysis": analysis.get("analysis", {}),
                "diagram_specification": diagram_spec,
                "performance": {
                    "elapsedTimeSeconds": 0.0  # Placeholder, would be calculated in a real implementation
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "algorithm_analysis": analysis.get("analysis", {}),
                "diagram_specification": self._generate_error_diagram(str(e))
            }
    
    def _generate_diagram_from_analysis(self, analysis: Dict[str, Any], code: str, problem_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a diagram specification from algorithm analysis.
        
        Args:
            analysis: The algorithm analysis
            code: The original code
            problem_description: Optional problem description
            
        Returns:
            Dict containing the diagram specification
        """
        # In a real implementation, this would call Claude again to generate a diagram
        # For this example, we'll create a simple mermaid diagram based on the analysis
        
        if "analysis" not in analysis or not analysis["analysis"]:
            raise ValueError("No analysis available to generate diagram from")
        
        algorithm_analysis = analysis["analysis"]
        algorithm_name = algorithm_analysis.get("algorithm_name", "Unknown Algorithm")
        algorithm_type = algorithm_analysis.get("algorithm_type", "")
        key_steps = algorithm_analysis.get("key_steps", [])
        
        # Create a simple flowchart
        mermaid_def = ["flowchart TD"]
        
        # Add algorithm name and type
        mermaid_def.append(f"    title[\"{algorithm_name}\"]")
        
        # Add nodes for key steps
        for i, step in enumerate(key_steps[:5]):  # Limit to 5 steps for simplicity
            node_id = f"step{i+1}"
            step_text = step.replace('"', "'")  # Escape quotes
            mermaid_def.append(f"    {node_id}[\"{step_text}\"]")
            
            # Connect steps
            if i > 0:
                prev_node = f"step{i}"
                mermaid_def.append(f"    {prev_node} --> {node_id}")
            elif i == 0:
                mermaid_def.append(f"    title --> {node_id}")
        
        # Add styling
        mermaid_def.append("    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px")
        
        # Create steps for animation
        steps = []
        for i in range(len(key_steps[:5])):
            step_nodes = [f"step{j+1}" for j in range(i+1)]
            steps.append({
                "step_id": i+1,
                "active_nodes": step_nodes,
                "description": key_steps[i] if i < len(key_steps) else ""
            })
        
        return {
            "diagram_type": "mermaid",
            "mermaid_definition": "\n".join(mermaid_def),
            "steps": steps
        }
    
    def _generate_error_diagram(self, error_message: str) -> Dict[str, Any]:
        """Generate an error diagram with the error message."""
        mermaid_def = [
            "flowchart TD",
            "    error[\"Error Occurred\"]",
            "    details[\"" + error_message.replace('"', "'") + "\"]",
            "    error --> details",
            "    classDef default fill:#f9d6d6,stroke:#a33,stroke-width:1px"
        ]
        
        return {
            "diagram_type": "mermaid",
            "mermaid_definition": "\n".join(mermaid_def),
            "steps": [{"step_id": 1, "active_nodes": ["error", "details"], "description": "Error occurred during processing"}]
        }
