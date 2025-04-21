#!/usr/bin/env python3
"""
Simple script to check imports
"""
try:
    print("Checking imports...")
    from src.crews.agents.leetcode_agents import LeetCodeAgentFactory, SolutionApproach
    print("✅ LeetCodeAgentFactory and SolutionApproach imported successfully")
    
    from src.crews.agents.leetcode_tasks import LeetCodeTaskFactory, SolutionApproaches, SolutionCriteria
    print("✅ LeetCodeTaskFactory, SolutionApproaches, and SolutionCriteria imported successfully")
    
    from src.crews.leetcode_crew import LeetCodeCrew
    print("✅ LeetCodeCrew imported successfully")
    
    print("All imports successful!")
except Exception as e:
    print(f"❌ Import error: {str(e)}")
