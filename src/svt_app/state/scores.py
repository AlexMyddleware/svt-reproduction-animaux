"""State management module for game scores."""

from typing import Dict, Optional
import os
import json
from dataclasses import dataclass
from flask import session
from svt_app.utils.logging_utils import conditional_log, log_if_enabled

@dataclass
class GameScores:
    """
    Class to manage game scores across the application.
    
    This class provides a centralized way to manage and access game scores
    using both Flask's session and persistent storage.
    """
    
    SCORES_FILE = "assets/Data/scores.json"
    
    @staticmethod
    @log_if_enabled()
    def _ensure_scores_file() -> None:
        """Ensure the scores file exists with default values."""
        os.makedirs(os.path.dirname(GameScores.SCORES_FILE), exist_ok=True)
        if not os.path.exists(GameScores.SCORES_FILE):
            conditional_log("Creating new scores file")
            default_scores = {
                "texte_a_trous": 0,
                "relier_images": 0
            }
            with open(GameScores.SCORES_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_scores, f, indent=2)
    
    @staticmethod
    @log_if_enabled()
    def _load_scores() -> Dict[str, int]:
        """Load scores from persistent storage."""
        GameScores._ensure_scores_file()
        try:
            with open(GameScores.SCORES_FILE, 'r', encoding='utf-8') as f:
                scores = json.load(f)
                conditional_log("Loaded scores from file: {}", scores)
                return scores
        except Exception as e:
            conditional_log("Error loading scores: {}", str(e), level="ERROR")
            return {"texte_a_trous": 0, "relier_images": 0}
    
    @staticmethod
    @log_if_enabled()
    def _save_scores(scores: Dict[str, int]) -> None:
        """Save scores to persistent storage."""
        try:
            GameScores._ensure_scores_file()
            with open(GameScores.SCORES_FILE, 'w', encoding='utf-8') as f:
                json.dump(scores, f, indent=2)
            conditional_log("Saved scores to file: {}", scores)
        except Exception as e:
            conditional_log("Error saving scores: {}", str(e), level="ERROR")
    
    @staticmethod
    @log_if_enabled()
    def get_scores() -> Dict[str, int]:
        """
        Get the current scores from both session and persistent storage.
        
        Returns:
            Dict[str, int]: Dictionary containing game scores.
        """
        if 'scores' not in session:
            conditional_log("Loading scores from persistent storage")
            session['scores'] = GameScores._load_scores()
        else:
            conditional_log("Retrieved existing scores from session: {}", session['scores'])
        return session['scores']
    
    @staticmethod
    @log_if_enabled()
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
        conditional_log("Updated score for {}: {} -> {}", game_type, old_score, score)
    
    @staticmethod
    @log_if_enabled()
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
        conditional_log("Incremented score for {}: {} -> {}", game_type, current_score, new_score)
    
    @staticmethod
    @log_if_enabled()
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
        conditional_log("Retrieved score for {}: {}", game_type, score)
        return score
    
    @staticmethod
    @log_if_enabled()
    def reset_scores() -> None:
        """Reset all game scores to zero."""
        conditional_log("Resetting all scores to zero")
        scores = {
            "texte_a_trous": 0,
            "relier_images": 0
        }
        session['scores'] = scores
        GameScores._save_scores(scores)  # Save to persistent storage
        conditional_log("Scores after reset: {}", scores) 