"""
This module handles high scores with dates.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple

SCORES_FILE = "high_scores.json"

def load_high_scores() -> List[Dict[str, any]]:
    """
    Loads high scores from file.
    
    Returns:
        List of score dictionaries with 'score' and 'date' keys.
    """
    if not os.path.exists(SCORES_FILE):
        return []
    
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_high_scores(scores: List[Dict[str, any]]) -> None:
    """
    Saves high scores to file.
    
    Args:
        scores: List of score dictionaries to save.
    """
    try:
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
    except Exception as e:
        print(f"Error saving high scores: {e}")

def add_score(new_score: int) -> bool:
    """
    Adds a new score to the high scores list if it qualifies.
    
    Args:
        new_score: The score to potentially add.
        
    Returns:
        True if the score was added to top 5, False otherwise.
    """
    scores = load_high_scores()
    
    # Add new score with current date
    new_entry = {
        "score": new_score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    scores.append(new_entry)
    
    # Sort by score (descending) and keep only top 5
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:5]
    
    save_high_scores(scores)
    
    # Return True if the new score made it to top 5
    return any(entry["score"] == new_score and entry["date"] == new_entry["date"] for entry in scores)

def get_top_scores() -> List[Dict[str, any]]:
    """
    Gets the top 5 high scores.
    
    Returns:
        List of top 5 score dictionaries.
    """
    return load_high_scores()[:5]

def get_best_score() -> int:
    """
    Gets the highest score.
    
    Returns:
        The highest score, or 0 if no scores exist.
    """
    scores = load_high_scores()
    if not scores:
        return 0
    return scores[0]["score"]

def format_scores_for_display() -> List[str]:
    """
    Formats scores for display in the menu.
    
    Returns:
        List of formatted score strings.
    """
    scores = get_top_scores()
    if not scores:
        return ["No high scores yet!"]
    
    formatted = []
    for i, entry in enumerate(scores, 1):
        formatted.append(f"{i}. {entry['score']} pts - {entry['date']}")
    
    return formatted
