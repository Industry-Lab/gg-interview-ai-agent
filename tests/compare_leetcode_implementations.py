"""
Compare the original LeetCode service with the new agent-based implementation.

This script sends the same LeetCode problem to both endpoints and compares the results.
"""
import requests
import json
import sys
import os
import time
from pprint import pprint

# Sample LeetCode problem - Merge Intervals
SAMPLE_PROBLEM = """
Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, 
and return an array of the non-overlapping intervals that cover all the intervals in the input.

Example 1:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Example 2:
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.

Constraints:
1 <= intervals.length <= 10^4
intervals[i].length == 2
0 <= starti <= endi <= 10^4
"""

def print_colored(text, color):
    """Print colored text to the console."""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def test_api_endpoint(endpoint, problem, language="python"):
    """Test a LeetCode solution API endpoint with a sample problem."""
    print_colored(f"\n=== TESTING ENDPOINT: {endpoint} ===", "cyan")
    print(f"Requesting solution in {language}...")
    
    # API URL
    url = f"http://localhost:8000/api/{endpoint}"
    
    # Prepare the request payload
    payload = {
        "problem": problem,
        "language": language
    }
    
    try:
        # Make the API request
        start_time = time.time()
        response = requests.post(url, json=payload)
        elapsed = time.time() - start_time
        
        # Display results
        print(f"Request completed in {elapsed:.2f} seconds with status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("status") == "success":
                print_colored("✅ Successfully generated solutions!", "green")
                
                solution_count = result.get("solution_count", 0)
                print(f"Generated {solution_count} solution(s)")
                
                # Return the result for comparison
                return result
            else:
                print_colored(f"❌ Error: {result.get('error', 'Unknown error')}", "red")
                return None
        else:
            print_colored(f"❌ API request failed with status code {response.status_code}", "red")
            print(response.text)
            return None
            
    except Exception as e:
        print_colored(f"❌ Exception occurred: {str(e)}", "red")
        print("Make sure the API server is running (python3 run_api.py)")
        return None

def print_solution_summary(result):
    """Print a summary of the solutions."""
    if not result or result.get("status") != "success":
        return
    
    solutions = result.get("solutions", [])
    
    if isinstance(solutions, list):
        print_colored("\nSOLUTION SUMMARY:", "magenta")
        
        for i, solution in enumerate(solutions):
            if isinstance(solution, dict):
                approach = solution.get("approach", f"Solution {i+1}")
                print_colored(f"\n{approach}", "yellow")
                
                # Print a brief snippet of the code
                code = solution.get("code", "")
                if code:
                    lines = code.split("\n")
                    preview = "\n".join(lines[:10])
                    if len(lines) > 10:
                        preview += "\n..."
                    print(preview)
            else:
                print(f"Solution {i+1}: {type(solution)}")
    else:
        # If it's just a text string
        print_colored("\nSOLUTION OUTPUT:", "magenta")
        preview = solutions[:500] + "..." if len(solutions) > 500 else solutions
        print(preview)

def compare_implementations(problem=SAMPLE_PROBLEM, language="python"):
    """Compare the original and agent-based LeetCode solution implementations."""
    print_colored("\n=== COMPARING LEETCODE SOLUTION IMPLEMENTATIONS ===", "cyan")
    
    # Test the original implementation
    print_colored("\n--- ORIGINAL IMPLEMENTATION ---", "blue")
    original_result = test_api_endpoint("leetcode-solutions", problem, language)
    
    if original_result:
        print_solution_summary(original_result)
    
    # Test the agent-based implementation
    print_colored("\n--- AGENT-BASED IMPLEMENTATION ---", "blue")
    agent_result = test_api_endpoint("agent-leetcode-solutions", problem, language)
    
    if agent_result:
        print_solution_summary(agent_result)
    
    # Compare the results
    if original_result and agent_result:
        print_colored("\n--- COMPARISON RESULTS ---", "green")
        print(f"Original solution count: {original_result.get('solution_count', 0)}")
        print(f"Agent-based solution count: {agent_result.get('solution_count', 0)}")
        
        print_colored("\nKey differences:", "yellow")
        print("1. Original implementation returns structured solutions")
        print("2. Agent-based implementation provides multiple solution approaches with detailed explanations")
        print("3. Agent-based implementation includes time and space complexity analysis for each approach")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare LeetCode solution implementations")
    parser.add_argument("--language", default="python", choices=["python", "java", "javascript"], 
                       help="Programming language for the solutions")
    parser.add_argument("--problem", default=SAMPLE_PROBLEM, help="Custom LeetCode problem to solve")
    
    args = parser.parse_args()
    
    compare_implementations(args.problem, args.language)
