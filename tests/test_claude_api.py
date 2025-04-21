"""
Test script for verifying Claude API connectivity and functionality.

This script provides a simple test to check if the Claude API
is working correctly with the algorithm visualizer service.

Usage:
    python -m tests.test_claude_api

Environment variables:
    ANTHROPIC_API_KEY: Your Claude API key (required)
"""
import os
import sys
import json
import time
from typing import Dict, Any

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.claude_client import ClaudeClient
from src.algorithm_visualizer_service import AlgorithmVisualizerService

# Test algorithm - Merge Sorted Array (LeetCode #88)
TEST_CODE = """
def merge(nums1, m, nums2, n):
    # Start from the end of both arrays
    p1 = m - 1  # Pointer for nums1
    p2 = n - 1  # Pointer for nums2
    p = m + n - 1  # Pointer for the merged array (in nums1)
    
    # While there are elements in both arrays
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
    
    # If there are remaining elements in nums2, copy them to nums1
    # (If there are remaining elements in nums1, they are already in place)
    nums1[:p2 + 1] = nums2[:p2 + 1]
"""

TEST_PROBLEM = """
You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, 
and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be stored inside 
the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements 
denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. 
nums2 has a length of n.

Example:
Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
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

def test_claude_api() -> None:
    """Test the Claude API connectivity and functionality."""
    print_section("CLAUDE API TEST")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print_colored("Error: ANTHROPIC_API_KEY environment variable is not set.", 'red')
        print("Please set your API key with:")
        print_colored("export ANTHROPIC_API_KEY=your_api_key_here", 'yellow')
        return
    
    print_colored("Testing Claude API with a simple completion...", 'blue')
    try:
        client = ClaudeClient(api_key)
        start_time = time.time()
        response = client.get_completion("Hello, Claude! Can you verify that you're working correctly?")
        elapsed = time.time() - start_time
        
        if "error" in response:
            print_colored("Error calling Claude API:", 'red')
            print_json(response)
            return
        
        print_colored("Claude API is working! ✓", 'green')
        print(f"Response received in {elapsed:.2f} seconds")
        print_colored("Response content:", 'blue')
        print(response["content"][:500] + "..." if len(response["content"]) > 500 else response["content"])
        print("\nUsage statistics:")
        print(f"Input tokens: {response['usage']['input_tokens']}")
        print(f"Output tokens: {response['usage']['output_tokens']}")
        print(f"Total tokens: {response['usage']['input_tokens'] + response['usage']['output_tokens']}")
        
    except Exception as e:
        print_colored(f"Error testing Claude API: {str(e)}", 'red')
        return
    
    print_section("ALGORITHM ANALYSIS TEST")
    print_colored("Testing algorithm analysis functionality...", 'blue')
    
    try:
        visualizer = AlgorithmVisualizerService(api_key)
        start_time = time.time()
        result = visualizer.analyze_algorithm(TEST_CODE, TEST_PROBLEM)
        elapsed = time.time() - start_time
        
        if "error" in result:
            print_colored("Error analyzing algorithm:", 'red')
            print_json(result)
            return
        
        print_colored("Algorithm analysis successful! ✓", 'green')
        print(f"Analysis completed in {elapsed:.2f} seconds")
        
        if "analysis" in result:
            print_colored("Algorithm analysis results:", 'blue')
            print_json(result["analysis"])
        
    except Exception as e:
        print_colored(f"Error analyzing algorithm: {str(e)}", 'red')
        return
    
    print_section("VISUALIZATION GENERATION TEST")
    print_colored("Testing visualization generation...", 'blue')
    
    try:
        start_time = time.time()
        result = visualizer.generate_visualization(TEST_CODE, TEST_PROBLEM)
        elapsed = time.time() - start_time
        
        if result.get("status") != "success":
            print_colored("Error generating visualization:", 'red')
            print_json(result)
            return
        
        print_colored("Visualization generation successful! ✓", 'green')
        print(f"Visualization generated in {elapsed:.2f} seconds")
        
        if "diagram_specification" in result:
            print_colored("Diagram specification:", 'blue')
            spec = result["diagram_specification"]
            print(f"Diagram type: {spec['diagram_type']}")
            print(f"Number of steps: {len(spec['steps'])}")
            print_colored("Mermaid definition:", 'magenta')
            print(spec["mermaid_definition"])
        
    except Exception as e:
        print_colored(f"Error generating visualization: {str(e)}", 'red')

if __name__ == "__main__":
    test_claude_api()
