/**
 * JavaScript for the Texte à trous (Fill in the blanks) game.
 * Handles drag and drop functionality and answer validation.
 */

document.addEventListener('DOMContentLoaded', function() {
    const options = document.querySelectorAll('.option');
    const blank = document.getElementById('answer-blank');
    const validateBtn = document.getElementById('validate-btn');
    const resetBtn = document.getElementById('reset-btn');
    const questionContainer = document.querySelector('.question-container');
    
    let currentOption = null;
    
    // Get the question ID from the data attribute
    const questionId = questionContainer ? parseInt(questionContainer.dataset.questionId) : 1;

    // Get the focused folder from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const focusedFolder = urlParams.get('focus') || '';
    
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
        options.forEach(option => {
            option.setAttribute('draggable', true);
            
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
        
        // Pause physics simulation during drag
        if (window.gamePhysicsManager) {
            window.gamePhysicsManager.stop();
        }
    }
    
    /**
     * Handle the end of dragging an option.
     */
    function dragEnd() {
        this.classList.remove('dragging');
        
        // Resume physics if not dropped on target
        if (this.style.display !== 'none' && window.gamePhysicsManager) {
            window.gamePhysicsManager.start();
        }
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
            
            // Pause physics for the used element
            if (window.gamePhysicsManager) {
                const physics = window.gamePhysicsManager.getOptionByElement(this);
                if (physics) {
                    physics.element.classList.remove('physics-controlled');
                }
            }
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
        
        // Pause physics during validation
        if (window.gamePhysicsManager) {
            window.gamePhysicsManager.stop();
        }
        
        // Send the answer to the server for validation
        fetch('/game/check_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                game_type: 'texte_a_trous',
                question_id: questionId,
                answer: answer,
                focused_folder: focusedFolder
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
                        if (data.next_question_id !== null && data.next_question_id !== undefined) {
                            // Preserve focus parameter if present
                            const urlParams = new URLSearchParams(window.location.search);
                            const focusParam = urlParams.get('focus');
                            let nextUrl = window.location.pathname + '?question_id=' + data.next_question_id;
                            if (focusParam) {
                                nextUrl += '&focus=' + encodeURIComponent(focusParam);
                            }
                            window.location.replace(nextUrl);
                        } else {
                            // Preserve focus parameter when reloading
                            window.location.replace(window.location.href);
                        }
                    }, 1500);
                } else {
                    // Incorrect answer
                    blank.classList.add('incorrect');
                    setTimeout(() => {
                        blank.classList.remove('incorrect');
                        resetWords();
                    }, 1000);
                }
            } else {
                alert(data.message || 'Une erreur est survenue lors de la validation.');
                // Resume physics if there was an error
                if (window.gamePhysicsManager) {
                    window.gamePhysicsManager.start();
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Une erreur est survenue lors de la validation.');
            // Resume physics if there was an error
            if (window.gamePhysicsManager) {
                window.gamePhysicsManager.start();
            }
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
        
        // Restart physics
        if (window.gamePhysicsManager) {
            window.gamePhysicsManager.start();
        }
    }
}); 