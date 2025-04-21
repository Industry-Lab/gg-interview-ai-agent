"""
Agents Module

This module provides a crew-based architecture for AI agents that work together
to solve problems, with a focus on LeetCode solutions generation.
"""
from .leetcode_agents import LeetCodeAgentFactory, SolutionApproach
from .leetcode_tasks import LeetCodeTaskFactory, SolutionApproaches, SolutionCriteria

__all__ = ["LeetCodeAgentFactory", "SolutionApproach", "LeetCodeTaskFactory", 
           "SolutionApproaches", "SolutionCriteria"]
