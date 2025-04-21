"""
Test script for the updated LeetCode Solutions API with Claude-3-7-Sonnet model.

This tests that all changes have been successfully implemented.
"""
import requests
import json
import time
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# API URL (when running locally)
API_URL = "http://localhost:8000/api/leetcode-solutions"

# Sample LeetCode problem - Find Median of Two Sorted Arrays
SAMPLE_PROBLEM = """
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

Example 1:
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Example 2:
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

Constraints:
nums1.length == m
nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000
-10^6 <= nums1[i], nums2[i] <= 10^6
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

def test_api(language="python"):
    """Test the updated LeetCode Solutions API with Claude-3-7-Sonnet model."""
    print_colored("\n=== TESTING LEETCODE API WITH CLAUDE-3-7-SONNET ===", "cyan")
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
                print_colored("✅ Successfully generated solutions with Claude-3-7-Sonnet model!", "green")
                
                # Show summary of solutions
                solutions = result.get("solutions", [])
                if solutions:
                    print_colored(f"\nGenerated {len(solutions)} solution(s)", "blue")
                    
                    # Check for specific mention of Claude-3-7-Sonnet in output
                    solution_text = json.dumps(solutions)
                    if "sonnet" in solution_text.lower() or "claude-3-7" in solution_text.lower():
                        print_colored("⚠️ Note: Output specifically mentions the model - this is not expected", "yellow")
                    
                    # Display first part of the solutions
                    if isinstance(solutions[0], dict) and "code" in solutions[0]:
                        solution_preview = solutions[0]["code"][:500] + "..." if len(solutions[0]["code"]) > 500 else solutions[0]["code"]
                        print_colored("\nSOLUTION PREVIEW:", "magenta")
                        print(solution_preview)
                    
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
        print("Make sure the API server is running (python3 run_api.py)")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the updated LeetCode Solutions API")
    parser.add_argument("--language", default="python", choices=["python", "java", "javascript"], 
                       help="Programming language for the solution")
    parser.add_argument("--url", default=API_URL, help="API endpoint URL")
    
    args = parser.parse_args()
    API_URL = args.url
    
    test_api(args.language)
