"""Routes for Anki integration."""
from typing import Dict, Any
from flask import Blueprint, jsonify, render_template, session, request
from ..services.anki_service import AnkiService
from ..services.anki_training_service import AnkiTrainingService
from ..utils.logging_utils import conditional_log

anki_bp = Blueprint('anki', __name__)
anki_service = AnkiService()
training_service = AnkiTrainingService(anki_service)

@anki_bp.route('/anki/authenticate', methods=['GET'])
def authenticate() -> Dict[str, Any]:
    """Authenticate with Anki.
    
    Returns:
        JSON response indicating authentication status
    """
    conditional_log("Attempting Anki authentication")
    is_authenticated, error_diagnosis = anki_service.authenticate()
    
    if is_authenticated:
        session['anki_authenticated'] = True
        conditional_log("Anki authentication successful")
        return jsonify({
            'authenticated': True,
            'message': 'Successfully authenticated with Anki'
        })
    else:
        session['anki_authenticated'] = False
        conditional_log("Anki authentication failed: {}", error_diagnosis)
        return jsonify({
            'authenticated': False,
            'message': 'Failed to authenticate with Anki',
            'error': error_diagnosis
        })

@anki_bp.route('/anki/test-connection', methods=['GET'])
def test_anki_connection() -> Dict[str, Any]:
    """Test the connection to Anki.
    
    Returns:
        JSON response indicating connection status
    """
    conditional_log("Testing Anki connection")
    is_connected, error_diagnosis = anki_service.test_connection()
    
    if is_connected:
        return jsonify({
            'connected': True,
            'message': 'Successfully connected to Anki'
        })
    else:
        conditional_log("Connection test failed: {}", error_diagnosis)
        return jsonify({
            'connected': False,
            'message': 'Failed to connect to Anki',
            'error': error_diagnosis
        })

@anki_bp.route('/anki/decks', methods=['GET'])
def get_decks() -> Dict[str, Any]:
    """Get all available Anki decks.
    
    Returns:
        JSON response containing list of deck names
    """
    if not session.get('anki_authenticated'):
        conditional_log("Attempting to get decks without authentication")
        return jsonify({
            'success': False,
            'error': {
                'message': 'Not authenticated',
                'suggestions': ['Please authenticate first']
            }
        })

    try:
        conditional_log("Fetching Anki decks")
        response, error_diagnosis = anki_service._make_request("deckNames")
        
        if response and 'result' in response:
            decks = response['result']
            conditional_log("Successfully retrieved {} decks", len(decks))
            return jsonify({
                'success': True,
                'decks': decks
            })
        else:
            conditional_log("Failed to retrieve decks: {}", error_diagnosis)
            return jsonify({
                'success': False,
                'error': error_diagnosis
            })
    except Exception as e:
        conditional_log("Error fetching Anki decks: {}", str(e), level='ERROR')
        return jsonify({
            'success': False,
            'error': str(e)
        })

@anki_bp.route('/anki', methods=['GET'])
def anki_page() -> str:
    """Render the Anki integration page.
    
    Returns:
        Rendered HTML template
    """
    conditional_log("Rendering Anki page")
    return render_template('anki.html')

@anki_bp.route('/training/<deck_name>')
def training_view(deck_name: str):
    """Render the training view for a deck.
    
    Args:
        deck_name: Name of the deck to train
    """
    return render_template('anki_training.html', deck_name=deck_name)

@anki_bp.route('/cards/review/<deck_name>', methods=['GET'])
def get_review_cards(deck_name: str) -> Dict[str, Any]:
    """Get cards available for review in a deck.
    
    Args:
        deck_name: Name of the deck to get cards from
        
    Returns:
        JSON response with cards data
    """
    cards = training_service.get_cards_for_review(deck_name)
    return jsonify({'cards': cards})

@anki_bp.route('/cards/answer', methods=['POST'])
def submit_answer() -> Dict[str, Any]:
    """Submit an answer for a card.
    
    Expected request data:
        cardId: ID of the card being answered
        ease: Ease rating (1=Again, 2=Hard, 3=Good, 4=Easy)
        
    Returns:
        JSON response indicating success
    """
    data = request.get_json()
    card_id = data.get('cardId')  # Changed from card_id to cardId
    ease = data.get('ease')
    
    if not card_id or not ease:
        return jsonify({'error': 'Missing required parameters'}), 400
        
    success = training_service.answer_card(card_id, ease)
    return jsonify({'success': success}) 