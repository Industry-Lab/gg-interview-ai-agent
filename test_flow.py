"""
Test for LeetCodeSolutionFlow implementation

This script tests the refactored Flow-based implementation to ensure it 
correctly handles the solution generation and enhancement process.
"""
import sys
import json
from unittest.mock import patch

# Set up path
sys.path.append('.')

# Import the Flow and agent classes
from src.crews.crew_manager import LeetCodeSolutionFlow, Approach


def print_separator(title):
    """Print a separator with title for better readability"""
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80)


def test_flow_initialization():
    """Test that the flow initializes correctly with problem details in state"""
    print_separator("Testing Flow Initialization")
    
    # Create a flow instance
    flow = LeetCodeSolutionFlow(
        api_key="dummy-key",
        problem_description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        language="python"
    )
    
    # Print the full state for debugging
    print("Flow state attributes:")
    for attr_name in dir(flow.state):
        if not attr_name.startswith('_'):
            attr_value = getattr(flow.state, attr_name)
            if isinstance(attr_value, str) and len(attr_value) > 50:
                print(f"  {attr_name}: {attr_value[:50]}...")
            else:
                print(f"  {attr_name}: {attr_value}")
    
    # Verify that the important state attributes are present
    assert hasattr(flow.state, 'problem_description')
    assert hasattr(flow.state, 'language')
    assert hasattr(flow.state, 'status')
    assert flow.state.problem_description is not None
    assert flow.state.language == "python"
    assert flow.state.status == "pending"
    
    print("✅ Flow initialization test passed!")
    return flow


def test_generate_leetcode_solution(flow):
    """Test that generate_leetcode_solution correctly handles agent responses"""
    print_separator("Testing Generate LeetCode Solution")
    
    # Mock LeetCodeAgent.solve_problem to return a predefined response
    with patch('src.agents.leetcode_agent.LeetCodeAgent.solve_problem') as mock_solve:
        # Configure the mock to return a successful solution
        mock_solution = {
            "status": "success",
            "introduction": "This is a test introduction",
            "solutions": [
                {
                    "rank": 1,
                    "title": "Test Approach 1",
                    "content": "This is the first approach",
                    "time_complexity": "O(n)",
                    "space_complexity": "O(n)",
                    "code": "def two_sum(nums, target):\n    hash_map = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in hash_map:\n            return [hash_map[complement], i]\n        hash_map[num] = i\n    return []",
                    "edge_cases": "Empty array, no solution",
                    "test_examples": "Example 1: [2,7,11,15], target = 9, Output: [0,1]"
                }
            ],
            "full_text": json.dumps({
                "introduction": "This is a test introduction",
                "approaches": [
                    {
                        "rank": 1,
                        "title": "Test Approach 1",
                        "content": "This is the first approach",
                        "time_complexity": "O(n)",
                        "space_complexity": "O(n)",
                        "code": "def two_sum(nums, target):\n    hash_map = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in hash_map:\n            return [hash_map[complement], i]\n        hash_map[num] = i\n    return []",
                        "edge_cases": "Empty array, no solution",
                        "test_examples": "Example 1: [2,7,11,15], target = 9, Output: [0,1]"
                    }
                ]
            })
        }
        mock_solve.return_value = mock_solution
        
        # Call the generate_leetcode_solution method
        approaches_list = flow.generate_leetcode_solution()
        
        # Verify that the state was updated correctly
        print(f"Introduction: {flow.state.introduction}")
        print(f"Status: {flow.state.status}")
        print(f"Approach count: {len(flow.state.approaches)}")
        print(f"Approaches list length: {len(approaches_list)}")
        
        # Check that we have approaches to work with
        assert flow.state.introduction == "This is a test introduction"
        assert flow.state.status == "success"
        assert len(flow.state.approaches) > 0
        assert len(approaches_list) > 0
        assert isinstance(approaches_list[0], Approach)
        assert approaches_list[0].title == "Test Approach 1"
        
        print("✅ Generate solution test passed!")
        return approaches_list


def test_enhance_solution(flow, approaches_list):
    """Test that enhance_solution correctly handles educational insights"""
    print_separator("Testing Enhance Solution")
    
    # Mock HelperAgent.enhance_solution to return predefined insights
    with patch('src.agents.helper_agent.HelperAgent.enhance_solution') as mock_enhance:
        # Configure the mock to return insights
        mock_insights = {
            "explanation": "This is a test explanation of the algorithm",
            "optimization_suggestions": "Consider using a more efficient data structure",
            "interview_tips": "Explain the time-space tradeoff",
            "additional_test_cases": "Test with edge cases like empty arrays"
        }
        mock_enhance.return_value = mock_insights
        
        # Call the enhance_solution method
        insights = flow.enhance_solution(approaches_list)
        
        # Verify that the state was updated correctly
        print(f"Educational insights: {json.dumps(flow.state.educational_insights, indent=2)}")
        
        # Check that we have educational insights
        assert flow.state.educational_insights is not None
        assert flow.state.educational_insights["explanation"] == "This is a test explanation of the algorithm"
        assert insights == mock_insights
        
        print("✅ Enhance solution test passed!")
        return insights


def run_all_tests():
    """Run all tests in sequence"""
    print_separator("RUNNING ALL TESTS")
    
    try:
        # Test flow initialization
        flow = test_flow_initialization()
        
        # Test solution generation
        approaches_list = test_generate_leetcode_solution(flow)
        
        # Test solution enhancement
        insights = test_enhance_solution(flow, approaches_list)
        
        print_separator("ALL TESTS PASSED")
        print("The Flow implementation is working correctly! 🎉")
        
    except AssertionError as e:
        print(f"❌ Test failed: {str(e)}")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
