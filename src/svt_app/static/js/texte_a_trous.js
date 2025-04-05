/**
 * JavaScript for the Texte à trous (Fill in the blanks) game.
 * Handles drag and drop functionality and answer validation.
 */

document.addEventListener('DOMContentLoaded', function() {
    const options = document.querySelectorAll('.option');
    const blank = document.getElementById('answer-blank');
    const validateBtn = document.getElementById('validate-btn');
    const resetBtn = document.getElementById('reset-btn');
    const questionText = document.getElementById('question-text');
    const questionContainer = document.querySelector('.question-container');
    
    let currentOption = null;
    
    // Get the question ID from the data attribute
    const questionId = questionContainer ? parseInt(questionContainer.dataset.questionId) : 1;
    
    // Initialize the drag and drop functionality
    initDragAndDrop();
    
    // Add event listeners to buttons
    if (validateBtn) {
        validateBtn.addEventListener('click', validateAnswer);
    }
    
    if (resetBtn) {
        resetBtn.addEventListener('click', resetWords);
    }
    
    /**
     * Initialize drag and drop functionality for the options.
     */
    function initDragAndDrop() {
        // Make options draggable
        options.forEach((option, index) => {
            option.setAttribute('draggable', true);
            
            // Random orbital parameters
            const baseRadius = 100 + Math.random() * 50; // Base orbit radius 100-150px
            const eccentricity = 0.8 + Math.random() * 0.4; // Orbit eccentricity 0.8-1.2
            const orbitX = baseRadius;
            const orbitY = baseRadius * eccentricity;
            
            // Set custom orbital path
            option.style.setProperty('--orbit-x', `${orbitX}px`);
            option.style.setProperty('--orbit-y', `${orbitY}px`);
            
            // Random timing
            const duration = 8 + Math.random() * 4; // 8-12 seconds per orbit
            const delay = Math.random() * -6; // Start at random points in the orbit
            const direction = Math.random() < 0.5 ? 'normal' : 'reverse'; // Random direction
            
            option.style.setProperty('--orbit-duration', `${duration}s`);
            option.style.setProperty('--orbit-delay', `${delay}s`);
            option.style.animationDirection = direction;
            
            // Add drag event listeners
            option.addEventListener('dragstart', dragStart);
            option.addEventListener('dragend', dragEnd);
            
            // Add click event for mobile
            option.addEventListener('click', handleOptionClick);
        });
        
        // Make blank a drop target
        if (blank) {
            blank.addEventListener('dragover', dragOver);
            blank.addEventListener('dragenter', dragEnter);
            blank.addEventListener('dragleave', dragLeave);
            blank.addEventListener('drop', drop);
        }
    }
    
    /**
     * Handle the start of dragging an option.
     * @param {DragEvent} e - The drag event.
     */
    function dragStart(e) {
        this.classList.add('dragging');
        e.dataTransfer.setData('text/plain', this.dataset.option);
        currentOption = this;
    }
    
    /**
     * Handle the end of dragging an option.
     */
    function dragEnd() {
        this.classList.remove('dragging');
    }
    
    /**
     * Handle dragging over the blank.
     * @param {DragEvent} e - The drag event.
     */
    function dragOver(e) {
        e.preventDefault();
    }
    
    /**
     * Handle entering the blank with a dragged option.
     * @param {DragEvent} e - The drag event.
     */
    function dragEnter(e) {
        e.preventDefault();
        this.classList.add('drag-over');
    }
    
    /**
     * Handle leaving the blank with a dragged option.
     */
    function dragLeave() {
        this.classList.remove('drag-over');
    }
    
    /**
     * Handle dropping an option into the blank.
     * @param {DragEvent} e - The drag event.
     */
    function drop(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
        
        const optionText = e.dataTransfer.getData('text/plain');
        this.textContent = optionText;
        this.classList.add('filled');
        this.dataset.answer = optionText;
        
        // Hide the dragged option
        if (currentOption) {
            currentOption.style.display = 'none';
        }
    }
    
    /**
     * Handle clicking on an option (for mobile devices).
     */
    function handleOptionClick() {
        if (blank && !blank.classList.contains('filled')) {
            const optionText = this.dataset.option;
            blank.textContent = optionText;
            blank.classList.add('filled');
            blank.dataset.answer = optionText;
            
            // Hide the clicked option
            this.style.display = 'none';
            currentOption = this;
        }
    }
    
    /**
     * Validate the answer provided by the user.
     */
    function validateAnswer() {
        if (!blank || !blank.classList.contains('filled')) {
            alert('Veuillez d\'abord placer un mot dans l\'espace vide.');
            return;
        }
        
        const answer = blank.dataset.answer;
        
        // Send the answer to the server for validation
        fetch('/game/check_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                game_type: 'texte_a_trous',
                question_id: questionId,
                answer: answer
            })
        })
        .then(response => {
            console.log('Raw response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Server response:', data);  // Full response logging
            console.log('Success:', data.success);
            console.log('Correct:', data.correct);
            console.log('Score:', data.score);
            console.log('Next question ID:', data.next_question_id);
            
            if (data.success) {
                if (data.correct) {
                    // Correct answer
                    blank.classList.add('correct');
                    
                    // Update the score display
                    const scoreDisplay = document.querySelector('.score-display p');
                    if (scoreDisplay) {
                        scoreDisplay.textContent = `Score: ${data.score}`;
                    }
                    
                    // Show success message and proceed to next question after a delay
                    setTimeout(() => {
                        // Go to the next question using the ID from the server response
                        console.log('Preparing navigation...');
                        console.log('Current question ID:', questionId);
                        console.log('Next question ID:', data.next_question_id);
                        
                        if (data.next_question_id !== null && data.next_question_id !== undefined) {
                            const nextUrl = window.location.pathname + '?question_id=' + data.next_question_id;
                            console.log('Navigating to:', nextUrl);
                            window.location.replace(nextUrl);  // Using replace instead of href
                        } else {
                            console.log('No next question ID, returning to first question');
                            window.location.replace(window.location.pathname);
                        }
                    }, 1500);  // Increased delay to ensure we see the logs
                } else {
                    // Incorrect answer
                    blank.classList.add('incorrect');
                    setTimeout(() => {
                        blank.classList.remove('incorrect');
                        resetWords();
                    }, 1000);
                }
            } else {
                console.error('Server returned error:', data.message);
                alert(data.message || 'Une erreur est survenue lors de la validation.');
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            alert('Une erreur est survenue lors de la validation.');
        });
    }
    
    /**
     * Reset the game state, showing all options and clearing the blank.
     */
    function resetWords() {
        // Show all options
        options.forEach(option => {
            option.style.display = '';
        });
        
        // Clear and reset the blank
        if (blank) {
            blank.textContent = '';
            blank.classList.remove('filled', 'correct', 'incorrect');
            blank.dataset.answer = '';
        }
        
        currentOption = null;
    }
}); 