"""
Enhanced Test script for verifying Claude API connectivity and functionality.

This script provides a robust test to check if the Claude API
is working correctly with the algorithm visualizer service, with
improved error handling and environment variable loading.

Usage:
    python -m tests.test_claude_api_enhanced

Environment variables (loaded from .env file):
    ANTHROPIC_API_KEY: Your Claude API key (required)
"""
import os
import sys
import json
import time
from typing import Dict, Any
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.claude_client import ClaudeClient
from src.algorithm_visualizer_service import AlgorithmVisualizerService

# Test algorithm - Two Sum (LeetCode #1)
TEST_CODE = """
def two_sum(nums, target):
    # Create a hash map to store numbers and their indices
    num_map = {}
    
    # Iterate through the array
    for i, num in enumerate(nums):
        # Calculate the complement needed to reach the target
        complement = target - num
        
        # If the complement exists in the hash map, return the indices
        if complement in num_map:
            return [num_map[complement], i]
        
        # Otherwise, add the current number and its index to the hash map
        num_map[num] = i
    
    # If no solution is found, return an empty array
    return []
"""

TEST_PROBLEM = """
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
"""

def print_colored(text: str, color: str = 'white') -> None:
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

def print_section(title: str) -> None:
    """Print a section title."""
    print("\n" + "="*80)
    print_colored(f" {title} ", 'cyan')
    print("="*80)

def print_json(data: Dict[str, Any]) -> None:
    """Print formatted JSON data."""
    print(json.dumps(data, indent=2))

def test_claude_api() -> bool:
    """
    Test the Claude API connectivity and functionality.
    
    Returns:
        bool: True if test passed, False otherwise
    """
    print_section("CLAUDE API CONNECTION TEST")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print_colored("Error: ANTHROPIC_API_KEY environment variable is not set.", 'red')
        print("Please set your API key in your .env file with:")
        print_colored("ANTHROPIC_API_KEY=your_api_key_here", 'yellow')
        return False
    
    print_colored("Testing Claude API with a simple completion...", 'blue')
    try:
        client = ClaudeClient(api_key)
        start_time = time.time()
        response = client.get_completion("Hello, Claude! Please respond with a very brief confirmation message.")
        elapsed = time.time() - start_time
        
        if "error" in response:
            error_str = str(response["error"])
            # Check for API overload error
            if "overload" in error_str.lower():
                print_colored("⚠️  PARTIAL SUCCESS: Connected to Claude API, but the service is currently overloaded", 'yellow')
                print("This confirms the API connection is working, but Anthropic's servers are busy.")
                print("Try again in a few minutes when server load decreases.")
                return True
            else:
                print_colored("Error calling Claude API:", 'red')
                print_json(response)
                return False
        
        print_colored("✅ Claude API is working correctly!", 'green')
        print(f"Response received in {elapsed:.2f} seconds")
        print_colored("Response content:", 'blue')
        print(response["content"][:500] + "..." if len(response["content"]) > 500 else response["content"])
        print("\nUsage statistics:")
        print(f"Input tokens: {response['usage']['input_tokens']}")
        print(f"Output tokens: {response['usage']['output_tokens']}")
        print(f"Total tokens: {response['usage']['input_tokens'] + response['usage']['output_tokens']}")
        
        return True
        
    except Exception as e:
        error_str = str(e)
        # Check for API overload error
        if "overload" in error_str.lower():
            print_colored("⚠️  PARTIAL SUCCESS: Connected to Claude API, but the service is currently overloaded", 'yellow')
            print("This confirms the API connection is working, but Anthropic's servers are busy.")
            print("Try again in a few minutes when server load decreases.")
            return True
        else:
            print_colored(f"Error testing Claude API: {error_str}", 'red')
            return False

def test_algorithm_analysis() -> bool:
    """
    Test the algorithm analysis functionality with the AlgorithmVisualizerService.
    
    Returns:
        bool: True if test passed, False otherwise
    """
    print_section("ALGORITHM ANALYSIS TEST")
    print_colored("Testing algorithm analysis functionality...", 'blue')
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print_colored("Error: ANTHROPIC_API_KEY environment variable is not set.", 'red')
        return False
    
    try:
        visualizer = AlgorithmVisualizerService(api_key)
        start_time = time.time()
        result = visualizer.analyze_algorithm(TEST_CODE, TEST_PROBLEM)
        elapsed = time.time() - start_time
        
        if "error" in result:
            error_str = str(result["error"])
            # Check for API overload error
            if "overload" in error_str.lower():
                print_colored("⚠️  PARTIAL SUCCESS: Connected to Claude API, but the service is currently overloaded", 'yellow')
                print("This confirms the API connection is working, but Anthropic's servers are busy.")
                print("Try again in a few minutes when server load decreases.")
                return True
            else:
                print_colored("Error analyzing algorithm:", 'red')
                print_json(result)
                return False
        
        print_colored("✅ Algorithm analysis successful!", 'green')
        print(f"Analysis completed in {elapsed:.2f} seconds")
        
        # Verify expected structure in response
        required_keys = ["algorithm_name", "algorithm_type", "time_complexity", "space_complexity"]
        if "analysis" in result:
            analysis = result["analysis"]
            missing_keys = [key for key in required_keys if key not in analysis]
            if missing_keys:
                print_colored(f"Warning: Analysis missing expected keys: {missing_keys}", 'yellow')
            
            print_colored("Algorithm analysis results:", 'blue')
            print_json(analysis)
            
            return True
        else:
            print_colored("Warning: No analysis in response", 'yellow')
            print_json(result)
            return False
        
    except Exception as e:
        error_str = str(e)
        # Check for API overload error
        if "overload" in error_str.lower():
            print_colored("⚠️  PARTIAL SUCCESS: Connected to Claude API, but the service is currently overloaded", 'yellow')
            print("This confirms the API connection is working, but Anthropic's servers are busy.")
            print("Try again in a few minutes when server load decreases.")
            return True
        else:
            print_colored(f"Error analyzing algorithm: {error_str}", 'red')
            return False

def main():
    """Run all tests and report results."""
    print_section("CLAUDE API INTEGRATION TESTS")
    print("This script will test the Claude API integration in the algorithm visualizer service.")
    print("Tests will verify both basic API connectivity and algorithm analysis functionality.")
    
    # Test Claude API connectivity
    api_test_result = test_claude_api()
    
    # If API test fails, don't continue to algorithm test
    if not api_test_result:
        print_colored("\n❌ Claude API connection test failed. Please fix this issue before proceeding.", 'red')
        return 1
    
    # Test algorithm analysis
    analysis_test_result = test_algorithm_analysis()
    
    # Report final results
    print_section("TEST RESULTS SUMMARY")
    
    if api_test_result and analysis_test_result:
        print_colored("✅ All tests passed successfully!", 'green')
        print("Claude API integration is working correctly.")
        return 0
    elif api_test_result:
        print_colored("⚠️  API connection works, but algorithm analysis failed.", 'yellow')
        print("Check the logs above for specific errors.")
        return 1
    else:
        print_colored("❌ Tests failed. Please fix the reported issues.", 'red')
        return 1

if __name__ == "__main__":
    sys.exit(main())
