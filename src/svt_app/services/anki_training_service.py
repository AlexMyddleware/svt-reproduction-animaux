"""Service for handling Anki card training."""
from typing import Dict, Any, List, Optional
from ..utils.logging_utils import conditional_log
from .anki_service import AnkiService
from .anki_card_formatter import AnkiCardFormatter
from .anki_card_types import AnkiCardTypes

class AnkiTrainingService:
    """Service for managing Anki card training sessions."""

    def __init__(self, anki_service: AnkiService):
        """Initialize the training service.
        
        Args:
            anki_service: Instance of AnkiService for API communication
        """
        self.anki = anki_service
        self.formatter = AnkiCardFormatter()
        self.card_types = AnkiCardTypes()

    def get_cards_for_review(self, deck_name: str) -> List[Dict[str, Any]]:
        """Get all cards available for review in a deck.
        
        Args:
            deck_name: Name of the deck to get cards from
            
        Returns:
            List of card data dictionaries
        """
        conditional_log("Fetching all reviewable cards for deck: {}", deck_name)
        query = self.card_types.build_deck_query(deck_name)
        
        response, _ = self.anki._make_request("findCards", {
            "query": query
        })
        
        if not response or 'result' not in response:
            conditional_log("No cards found or error occurred")
            return []
            
        card_ids = response['result']
        if not card_ids:
            conditional_log("No cards found in deck")
            return []
            
        # Get card details
        response, _ = self.anki._make_request("cardsInfo", {
            "cards": card_ids
        })
        
        if not response or 'result' not in response:
            return []
            
        raw_cards = response['result']
        conditional_log("Found {} cards", len(raw_cards))
        
        # Format each card's content
        formatted_cards = []
        for card in raw_cards:
            formatted_fields = self.formatter.extract_card_fields(card)
            formatted_card = {
                'cardId': card.get('cardId'),
                'question': formatted_fields['question'],
                'answer': formatted_fields['answer']
            }
            formatted_cards.append(formatted_card)
            
        return formatted_cards

    def answer_card(self, card_id: int, ease: int) -> bool:
        """Submit an answer for a card.
        
        Args:
            card_id: ID of the card being answered
            ease: Ease rating (1=Again, 2=Hard, 3=Good, 4=Easy)
            
        Returns:
            True if answer was submitted successfully
        """
        conditional_log("Answering card {} with ease {}", card_id, ease)
        response, _ = self.anki._make_request("guiAnswerCard", {
            "cardId": card_id,
            "ease": ease
        })
        
        success = response and 'error' not in response
        conditional_log("Answer submission {}", "successful" if success else "failed")
        return success 