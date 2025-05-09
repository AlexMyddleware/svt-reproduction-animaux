// Training UI state
let currentCards = [];
let currentCardIndex = 0;
let totalCards = 0;
let currentCardId = null;
let isShowingAnswer = false;
let lastAnsweredCardId = null;

// UI Elements
const elements = {
    question: document.getElementById('question'),
    answer: document.getElementById('answer'),
    remainingCount: document.getElementById('remaining-count'),
    currentCard: document.getElementById('current-card'),
    answerButtons: document.querySelector('.answer-buttons'),
    progress: document.getElementById('progress')
};

const wooshAudio = new Audio('/static/audio/short_woosh.mp3');
wooshAudio.preload = 'auto';

const deckCompletedAudio = new Audio('/static/audio/deck-completed.mp3');
deckCompletedAudio.preload = 'auto';

async function loadCards() {
    try {
        const response = await fetch(`/api/anki/cards/${deckName}`);
        const data = await response.json();
        console.log("this is the data tarzan", data);
        
        if (data.success && data.cards.length > 0) {
            // If more than one card, and the first is the last answered, rotate the array
            if (data.cards.length > 1 && data.cards[0].cardId === lastAnsweredCardId) {
                // Move the first card to the end
                data.cards.push(data.cards.shift());
            }
            currentCards = data.cards;
            totalCards = data.cards.length;
            currentCardIndex = 0;
            updateProgress();
            showNextCard();
        } else {
            showMessage('Tu as fini de révijouer ce paquet!');
            deckCompletedAudio.play();
        }
    } catch (error) {
        console.error('Error loading cards:', error);
        showMessage('Error loading cards');
    }
}

function showNextCard() {
    console.log("this is the show next card function", currentCardIndex, currentCards.length);
    if (currentCardIndex >= currentCards.length) {
        showMessage('Tu as fini de révijouer ce paquet!');
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
    elements.currentCard.classList.add('review-complete');
}

function toggleCard() {
    if (!currentCardId) return; // Don't toggle if showing a message
    
    if (!isShowingAnswer) {
        wooshAudio.currentTime = 0; // rewind to start
        wooshAudio.play();

        elements.currentCard.classList.add('flipped');
        elements.answerButtons.style.display = 'flex';
        isShowingAnswer = true;
    }
}

async function submitAnswer(ease) {
    console.log('Making request with cardId:', currentCardId, 'and ease:', ease);
    const requestData = {
        cardId: currentCardId,
        ease: ease
    };

    try {
        const response = await fetch('/api/anki/answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        console.log("Response received:", response);
        const data = await response.json();
        console.log("Response data:", data);
        
        if (data.success) {
            console.log("Answer submission successful");
            lastAnsweredCardId = currentCardId;
            await loadCards();
        } else {
            console.error("Answer submission failed:", data.error);
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