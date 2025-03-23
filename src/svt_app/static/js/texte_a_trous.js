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
    
    let currentOption = null;
    
    // Get the question ID from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const questionId = urlParams.get('question_id') || 1;
    
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
                question_id: parseInt(questionId),
                answer: answer
            })
        })
        .then(response => response.json())
        .then(data => {
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
                        alert('Correct! Bien joué!');
                        
                        // Go to the next question if available
                        const nextButton = document.querySelector('a[href*="question_id=' + (parseInt(questionId) + 1) + '"]');
                        if (nextButton) {
                            window.location.href = nextButton.href;
                        }
                    }, 1000);
                } else {
                    // Incorrect answer
                    blank.classList.add('incorrect');
                    
                    // Shake effect and reset after a delay
                    setTimeout(() => {
                        blank.classList.remove('incorrect', 'filled');
                        blank.textContent = '';
                        blank.dataset.answer = '';
                        
                        // Show the option again
                        if (currentOption) {
                            currentOption.style.display = 'inline-block';
                        }
                    }, 1000);
                }
            } else {
                alert('Erreur: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Une erreur est survenue lors de la validation de votre réponse.');
        });
    }
    
    /**
     * Reset all words to random positions and clear the answer blank if not validated.
     */
    function resetWords() {
        // If there's a word in the blank that hasn't been validated yet
        if (blank && blank.classList.contains('filled') && !blank.classList.contains('correct')) {
            // Get the word that was in the blank
            const blankWord = blank.textContent;
            // Find the corresponding option element
            const option = Array.from(options).find(opt => opt.dataset.option === blankWord);
            if (option) {
                option.style.display = 'inline-block';
            }
            // Clear the blank
            blank.textContent = '';
            blank.classList.remove('filled', 'incorrect');
            blank.dataset.answer = '';
        }
        
        // Randomize position for each word
        options.forEach((option) => {
            if (option.style.display !== 'none') {
                // Random orbital parameters
                const baseRadius = 100 + Math.random() * 50;
                const eccentricity = 0.8 + Math.random() * 0.4;
                const orbitX = baseRadius;
                const orbitY = baseRadius * eccentricity;
                
                // Set custom orbital path
                option.style.setProperty('--orbit-x', `${orbitX}px`);
                option.style.setProperty('--orbit-y', `${orbitY}px`);
                
                // Random timing
                const duration = 8 + Math.random() * 4;
                const delay = Math.random() * -6;
                const direction = Math.random() < 0.5 ? 'normal' : 'reverse';
                
                // Apply new animation parameters
                option.style.setProperty('--orbit-duration', `${duration}s`);
                option.style.setProperty('--orbit-delay', `${delay}s`);
                option.style.animationDirection = direction;
                
                // Reset any drag-related states
                option.classList.remove('dragging');
                option.style.animation = 'none';
                option.offsetHeight; // Trigger reflow
                option.style.animation = '';
            }
        });
    }
}); 