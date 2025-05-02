"""Service for handling different Anki card types."""
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class CardTypeQuery:
    """Represents a query for a specific card type."""
    query: str
    description: str

class AnkiCardTypes:
    """Service for managing different Anki card types."""
    
    @staticmethod
    def get_card_type_queries() -> List[CardTypeQuery]:
        """Get queries for different card types.
        
        Returns:
            List of CardTypeQuery objects for new, learning, and due cards
        """
        return [
            CardTypeQuery("is:new", "New cards"),
            CardTypeQuery("is:learn", "Learning cards"),
            CardTypeQuery("is:due", "Review cards")
        ]
    
    @staticmethod
    def build_deck_query(deck_name: str) -> str:
        """Build a query that includes all card types for a deck.
        
        Args:
            deck_name: Name of the deck to query
            
        Returns:
            Query string that will find all relevant cards
        """
        type_queries = [q.query for q in AnkiCardTypes.get_card_type_queries()]
        combined_types = " or ".join(type_queries)
        return f"deck:\"{deck_name}\" ({combined_types})" 