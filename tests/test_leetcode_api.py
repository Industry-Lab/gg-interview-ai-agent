"""
Test script for the LeetCode Solutions API endpoint.

This script demonstrates how to make requests to the LeetCode Solutions API endpoint.
"""
import requests
import json
import sys
import os
import time

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Default API URL (when running locally)
API_URL = "http://localhost:8000/api/leetcode-solutions"

# Sample LeetCode problem - Two Sum
SAMPLE_PROBLEM = """
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:
2 <= nums.length <= 10^4
-10^9 <= nums[i] <= 10^9
-10^9 <= target <= 10^9
Only one valid answer exists.
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

def test_leetcode_api(language="python"):
    """Test the LeetCode Solutions API with a sample problem."""
    print_colored("\n=== TESTING LEETCODE SOLUTIONS API ===", "cyan")
    print(f"Requesting solution in {language}...")
    
    # Prepare the request payload
    payload = {
        "problem": SAMPLE_PROBLEM,
        "language": language
    }
    
    try:
        # Make the API request
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        elapsed = time.time() - start_time
        
        # Display results
        print(f"Request completed in {elapsed:.2f} seconds with status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("status") == "success":
                print_colored("✅ Successfully generated solution!", "green")
                
                solution = result.get("solution", {})
                
                # Print the solution code
                print_colored("\nSOLUTION CODE:", "blue")
                print("```")
                print(solution.get("code", "No code found in response"))
                print("```")
                
                # Print the explanation (shortened for readability)
                explanation = solution.get("explanation", "No explanation found")
                max_explanation_lines = 10
                explanation_lines = explanation.split("\n")
                
                print_colored("\nEXPLANATION:", "blue")
                if len(explanation_lines) > max_explanation_lines:
                    for line in explanation_lines[:max_explanation_lines]:
                        print(line)
                    print(f"... [truncated, {len(explanation_lines) - max_explanation_lines} more lines]")
                else:
                    print(explanation)
                
                # Print complexity analysis
                print_colored("\nCOMPLEXITY ANALYSIS:", "blue")
                print(solution.get("complexity_analysis", "No complexity analysis found"))
                
                return True
            else:
                print_colored(f"❌ Error: {result.get('error', 'Unknown error')}", "red")
                return False
        else:
            print_colored(f"❌ API request failed with status code {response.status_code}", "red")
            print(response.text)
            return False
            
    except Exception as e:
        print_colored(f"❌ Exception occurred: {str(e)}", "red")
        print("Make sure the API server is running (python run_api.py)")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the LeetCode Solutions API")
    parser.add_argument("--language", default="python", help="Programming language for the solution")
    parser.add_argument("--url", default=API_URL, help="API endpoint URL")
    
    args = parser.parse_args()
    API_URL = args.url
    
    test_leetcode_api(args.language)
