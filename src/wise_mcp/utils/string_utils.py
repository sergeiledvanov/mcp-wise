"""
String utility functions.
"""

from difflib import SequenceMatcher
from typing import List, Dict, Any


def calculate_name_similarity(name1: str, name2: str) -> float:
    """
    Calculate similarity ratio between two names using fuzzy matching.

    Args:
        name1: First name to compare
        name2: Second name to compare

    Returns:
        Float between 0 and 1 indicating similarity (higher is more similar)
    """
    # Convert names to lowercase for case-insensitive comparison
    name1 = name1.lower()
    name2 = name2.lower()
    
    # Use SequenceMatcher for fuzzy string comparison
    return SequenceMatcher(None, name1, name2).ratio()


def find_best_match_by_name(names: List[str], 
                           name: str) -> str:
    """
    Find the name with the highest similarity from a list of names.

    Args:
        names: List of strings to match against
        name: Name to match against the list of names

    Returns:
        Dictionary containing the best matching name and its similarity score

    Raises:
        Exception: If no matching name is found or names list is empty
    """
    best_match = None
    best_score = -1

    if not names:
        raise Exception("No names provided for matching")
    
    for i, candidate in enumerate(names):
        if not candidate:
            continue

        similarity_score = calculate_name_similarity(name, candidate)
        if similarity_score > best_score:
            best_score = similarity_score
            best_match = candidate

    if best_match is None:
        raise Exception(f"No name similar to '{name}' was found")

    return best_match