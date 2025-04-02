"""State management module for game scores."""

from typing import Dict, Optional
import os
import json
from dataclasses import dataclass
from flask import session
from svt_app.utils.debug import debug_log

@dataclass
class GameScores:
    """
    Class to manage game scores across the application.
    
    This class provides a centralized way to manage and access game scores
    using both Flask's session and persistent storage.
    """
    
    SCORES_FILE = "assets/Data/scores.json"
    
    @staticmethod
    def _ensure_scores_file() -> None:
        """Ensure the scores file exists with default values."""
        os.makedirs(os.path.dirname(GameScores.SCORES_FILE), exist_ok=True)
        if not os.path.exists(GameScores.SCORES_FILE):
            debug_log("Creating new scores file")
            default_scores = {
                "texte_a_trous": 0,
                "relier_images": 0
            }
            with open(GameScores.SCORES_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_scores, f, indent=2)
    
    @staticmethod
    def _load_scores() -> Dict[str, int]:
        """Load scores from persistent storage."""
        GameScores._ensure_scores_file()
        try:
            with open(GameScores.SCORES_FILE, 'r', encoding='utf-8') as f:
                scores = json.load(f)
                debug_log("Loaded scores from file: {}", scores)
                return scores
        except Exception as e:
            debug_log("Error loading scores: {}", str(e))
            return {"texte_a_trous": 0, "relier_images": 0}
    
    @staticmethod
    def _save_scores(scores: Dict[str, int]) -> None:
        """Save scores to persistent storage."""
        try:
            GameScores._ensure_scores_file()
            with open(GameScores.SCORES_FILE, 'w', encoding='utf-8') as f:
                json.dump(scores, f, indent=2)
            debug_log("Saved scores to file: {}", scores)
        except Exception as e:
            debug_log("Error saving scores: {}", str(e))
    
    @staticmethod
    def get_scores() -> Dict[str, int]:
        """
        Get the current scores from both session and persistent storage.
        
        Returns:
            Dict[str, int]: Dictionary containing game scores.
        """
        if 'scores' not in session:
            debug_log("Loading scores from persistent storage")
            session['scores'] = GameScores._load_scores()
        else:
            debug_log("Retrieved existing scores from session: {}", session['scores'])
        return session['scores']
    
    @staticmethod
    def update_score(game_type: str, score: int) -> None:
        """
        Set the score for a specific game type to a specific value.
        
        Args:
            game_type (str): The type of game to update score for.
            score (int): The new score value to set.
        """
        scores = GameScores.get_scores()
        old_score = scores.get(game_type, 0)
        scores[game_type] = score
        session['scores'] = scores
        GameScores._save_scores(scores)  # Save to persistent storage
        debug_log("Updated score for {}: {} -> {}", game_type, old_score, score)
    
    @staticmethod
    def increment_score(game_type: str, increment: int = 1) -> None:
        """
        Increment the score for a specific game type.
        
        Args:
            game_type (str): The type of game to increment score for.
            increment (int, optional): The amount to increment by. Defaults to 1.
        """
        scores = GameScores.get_scores()
        current_score = scores.get(game_type, 0)
        new_score = current_score + increment
        scores[game_type] = new_score
        session['scores'] = scores
        GameScores._save_scores(scores)  # Save to persistent storage
        debug_log("Incremented score for {}: {} -> {}", game_type, current_score, new_score)
    
    @staticmethod
    def get_score(game_type: str) -> Optional[int]:
        """
        Get the score for a specific game type.
        
        Args:
            game_type (str): The type of game to get score for.
            
        Returns:
            Optional[int]: The score for the game type, or None if not found.
        """
        scores = GameScores.get_scores()
        score = scores.get(game_type)
        debug_log("Retrieved score for {}: {}", game_type, score)
        return score
    
    @staticmethod
    def reset_scores() -> None:
        """Reset all game scores to zero."""
        debug_log("Resetting all scores to zero")
        scores = {
            "texte_a_trous": 0,
            "relier_images": 0
        }
        session['scores'] = scores
        GameScores._save_scores(scores)  # Save to persistent storage
        debug_log("Scores after reset: {}", scores) 