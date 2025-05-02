"""Routes for Anki training interface."""
from typing import Dict, Any, List, Optional, Union
from flask import Blueprint, jsonify, render_template, session, request
from ..services.anki_service import AnkiService
from ..services.anki_training_service import AnkiTrainingService
from ..utils.logging_utils import conditional_log

training_bp = Blueprint('anki_training', __name__)
anki_service = AnkiService()
training_service = AnkiTrainingService(anki_service)

@training_bp.route('/anki/train/<deck_name>')
def train_deck(deck_name: str) -> str:
    """Render the training interface for a deck.
    
    Args:
        deck_name: Name of the deck to train
        
    Returns:
        Rendered HTML template
    """
    conditional_log("Rendering training interface for deck: {}", deck_name)
    return render_template('anki_training.html', deck_name=deck_name)

@training_bp.route('/api/anki/cards/<deck_name>')
def get_due_cards(deck_name: str) -> Dict[str, Any]:
    """Get cards due for review in a deck.
    
    Args:
        deck_name: Name of the deck
        
    Returns:
        JSON response with card data
    """
    if not session.get('anki_authenticated'):
        return jsonify({
            'success': False,
            'error': 'Not authenticated'
        })

    try:
        cards = training_service.get_cards_for_review(deck_name)
        return jsonify({
            'success': True,
            'cards': cards
        })
    except Exception as e:
        conditional_log("Error getting due cards: {}", str(e), level='ERROR')
        return jsonify({
            'success': False,
            'error': str(e)
        })

@training_bp.route('/api/anki/answer', methods=['POST'])
def submit_answer() -> Dict[str, Any]:
    """Submit an answer for a card.
    
    Returns:
        JSON response indicating success
    """
    if not session.get('anki_authenticated'):
        return jsonify({
            'success': False,
            'error': 'Not authenticated'
        })

    try:
        data = request.get_json()
        cardId = data.get('cardId')
        ease = data.get('ease')
        
        if not cardId or not ease:
            return jsonify({
                'success': False,
                'error': 'Missing cardId or ease'
            })
            
        success = training_service.answer_card(cardId, ease)
        return jsonify({'success': success})
    except Exception as e:
        conditional_log("Error submitting answer: {}", str(e), level='ERROR')
        return jsonify({
            'success': False,
            'error': str(e)
        }) 