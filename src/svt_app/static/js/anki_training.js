// Training UI state
let currentCards = [];
let currentCardIndex = 0;
let totalCards = 0;
let currentCardId = null;
let isShowingAnswer = false;

// UI Elements
const elements = {
    question: document.getElementById('question'),
    answer: document.getElementById('answer'),
    remainingCount: document.getElementById('remaining-count'),
    currentCard: document.getElementById('current-card'),
    answerButtons: document.querySelector('.answer-buttons'),
    progress: document.getElementById('progress')
};

async function loadCards() {
    try {
        const response = await fetch(`/api/anki/cards/${deckName}`);
        const data = await response.json();
        console.log("this is the data tarzan", data);
        
        if (data.success && data.cards.length > 0) {
            currentCards = data.cards;
            totalCards = data.cards.length;
            updateProgress();
            showNextCard();
        } else {
            showMessage('No cards available for review!');
        }
    } catch (error) {
        console.error('Error loading cards:', error);
        showMessage('Error loading cards');
    }
}

function showNextCard() {
    console.log("this is the show next card function", currentCardIndex, currentCards.length);
    if (currentCardIndex >= currentCards.length) {
        showMessage('Review complete!');
        return;
    }

    const card = currentCards[currentCardIndex];
    currentCardId = card.cardId;
    
    elements.question.innerHTML = card.question;
    elements.answer.innerHTML = card.answer;
    elements.remainingCount.textContent = currentCards.length - currentCardIndex;
    
    // Reset card state
    isShowingAnswer = false;
    elements.currentCard.classList.remove('flipped');
    elements.answerButtons.style.display = 'none';
    elements.currentCard.style.cursor = 'pointer';
}

function showMessage(message) {
    elements.question.innerHTML = message;
    elements.answer.innerHTML = '';
    elements.currentCard.style.cursor = 'default';
    elements.answerButtons.style.display = 'none';
}

function toggleCard() {
    if (!currentCardId) return; // Don't toggle if showing a message
    
    if (!isShowingAnswer) {
        elements.currentCard.classList.add('flipped');
        elements.answerButtons.style.display = 'flex';
        isShowingAnswer = true;
    }
}

async function submitAnswer(ease) {
    console.log("Shady sam this is the submit answer function", ease);
    try {
        const response = await fetch('/api/anki/answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cardId: currentCardId,
                ease: ease
            })
        });
        
        const data = await response.json();
        if (data.success) {
            console.log("martin septim this is the submit answer function", data);
            currentCardIndex++;
            console.log("uriel septim this is the current card index", currentCardIndex);
            updateProgress();
            showNextCard();
        }
    } catch (error) {
        console.error('Error submitting answer:', error);
    }
}

function updateProgress() {
    console.log("this is the update progress function", currentCardIndex, totalCards);
    const progress = (currentCardIndex / totalCards) * 100;
    console.log("this is the progress", progress);
    elements.progress.style.width = `${progress}%`;
    console.log("this is the elements progress width", elements.progress.style.width);
}

// Initialize
elements.currentCard.addEventListener('click', toggleCard);
loadCards(); 