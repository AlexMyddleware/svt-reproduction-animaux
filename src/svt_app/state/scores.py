"""State management module for game scores."""

from typing import Dict, Optional
from dataclasses import dataclass
from flask import session
from svt_app.utils.debug import debug_log

@dataclass
class GameScores:
    """
    Class to manage game scores across the application.
    
    This class provides a centralized way to manage and access game scores
    using Flask's session for persistence across requests.
    """
    
    @staticmethod
    def get_scores() -> Dict[str, int]:
        """
        Get the current scores from the session.
        
        Returns:
            Dict[str, int]: Dictionary containing game scores.
        """
        if 'scores' not in session:
            debug_log("Initializing new scores in session")
            session['scores'] = {
                "texte_a_trous": 0,
                "relier_images": 0
            }
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
        session['scores'] = scores  # Explicitly update session
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
        session['scores'] = scores  # Explicitly update session
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
        session['scores'] = {
            "texte_a_trous": 0,
            "relier_images": 0
        }
        debug_log("Scores after reset: {}", session['scores']) 