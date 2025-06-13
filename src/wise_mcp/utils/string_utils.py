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


def find_best_match_by_name(items: List[Dict[str, Any]], 
                           name: str, 
                           name_extractor=lambda x: x.get("name", {}).get("fullName", "")) -> Dict[str, Any]:
    """
    Find the item with the highest name similarity from a list of items.

    Args:
        items: List of dictionaries that contain name information
        name: Name to match against item names
        name_extractor: Function that extracts the name from an item dictionary
                       Default extracts from Wise API recipient format

    Returns:
        Dictionary containing the best matching item's information

    Raises:
        Exception: If no matching item is found
    """
    best_match = None
    best_score = -1

    for item in items:
        item_name = name_extractor(item)
        if not item_name:
            continue

        similarity_score = calculate_name_similarity(name, item_name)
        if similarity_score > best_score:
            best_score = similarity_score
            best_match = item

    if not best_match:
        raise Exception(f"No item with a name similar to '{name}' was found")

    return best_match