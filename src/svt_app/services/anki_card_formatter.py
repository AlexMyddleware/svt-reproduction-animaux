"""Service for formatting Anki card content."""
from typing import Dict, Any
import re
from bs4 import BeautifulSoup
from ..utils.logging_utils import conditional_log

class AnkiCardFormatter:
    """Service for formatting and cleaning Anki card content."""
    
    @staticmethod
    def format_card_content(content: str) -> str:
        """Format card content by cleaning HTML and handling cloze deletions.
        
        Args:
            content: Raw HTML content from Anki
            
        Returns:
            Cleaned and formatted content
        """
        conditional_log("Formatting card content: {}", content)
        
        # Parse HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove style tags
        for style in soup.find_all('style'):
            style.decompose()
            
        # Handle cloze deletions
        for cloze in soup.find_all(class_='cloze'):
            # Get the actual content that was clozed
            cloze_content = cloze.get('data-cloze', '[...]')
            # Replace with a span that matches our styling
            new_tag = soup.new_tag('span')
            new_tag['class'] = 'cloze-highlight'
            new_tag.string = cloze_content
            cloze.replace_with(new_tag)
            
        # Remove cloze-inactive spans but keep their content
        for inactive in soup.find_all(class_='cloze-inactive'):
            inactive.replace_with(inactive.get_text())
            
        result = str(soup)
        conditional_log("Formatted content: {}", result)
        return result
        
    @staticmethod
    def extract_card_fields(card: Dict[str, Any]) -> Dict[str, str]:
        """Extract and format question and answer fields from an Anki card.
        
        Args:
            card: Raw card data from Anki
            
        Returns:
            Dict with formatted question and answer
        """
        conditional_log("Extracting fields from card: {}", card)
        
        # Extract question and answer from card data
        question = card.get('question', '')
        answer = card.get('answer', '')
        
        # Format both fields
        formatted_question = AnkiCardFormatter.format_card_content(question)
        formatted_answer = AnkiCardFormatter.format_card_content(answer)
        
        return {
            'question': formatted_question,
            'answer': formatted_answer
        } 