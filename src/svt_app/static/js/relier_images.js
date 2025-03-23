/**
 * JavaScript for the Relier les images (Connect images) game.
 * Handles the connection mechanism between the central image and words.
 */

document.addEventListener('DOMContentLoaded', function() {
    const centralImage = document.getElementById('central-image');
    const words = document.querySelectorAll('.word');
    
    // Get the question ID from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const questionId = parseInt(urlParams.get('question_id')) || 1;
    
    let isDrawing = false;
    let selectedWord = null;
    let connectionLine = null;
    let svgContainer = null;
    
    // Initialize the SVG container for drawing lines
    initSvgContainer();
    
    // Add event listeners to the central image and words
    if (centralImage) {
        centralImage.addEventListener('mousedown', startConnection);
        centralImage.addEventListener('touchstart', handleTouchStart);
    }
    
    /**
     * Initialize the SVG container for drawing connection lines.
     */
    function initSvgContainer() {
        // Create SVG container
        svgContainer = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svgContainer.setAttribute('class', 'connection-svg');
        svgContainer.style.position = 'absolute';
        svgContainer.style.top = '0';
        svgContainer.style.left = '0';
        svgContainer.style.width = '100%';
        svgContainer.style.height = '100%';
        svgContainer.style.pointerEvents = 'none';
        svgContainer.style.zIndex = '5';
        
        // Add the SVG container to the question container
        const questionContainer = document.querySelector('.question-container');
        if (questionContainer) {
            questionContainer.style.position = 'relative';
            questionContainer.appendChild(svgContainer);
        }
    }
    
    /**
     * Start drawing a connection from the central image.
     * @param {MouseEvent} e - The mouse event.
     */
    function startConnection(e) {
        e.preventDefault();
        
        isDrawing = true;
        
        // Create a new line element
        connectionLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        connectionLine.setAttribute('class', 'connection-line');
        connectionLine.setAttribute('stroke', '#29b6f6');
        connectionLine.setAttribute('stroke-width', '2');
        
        // Get the starting position (center of the image)
        const imageRect = centralImage.getBoundingClientRect();
        const containerRect = svgContainer.getBoundingClientRect();
        
        const startX = imageRect.left + imageRect.width / 2 - containerRect.left;
        const startY = imageRect.top + imageRect.height / 2 - containerRect.top;
        
        // Set the starting point of the line
        connectionLine.setAttribute('x1', startX);
        connectionLine.setAttribute('y1', startY);
        connectionLine.setAttribute('x2', startX);
        connectionLine.setAttribute('y2', startY);
        
        // Add the line to the SVG container
        svgContainer.appendChild(connectionLine);
        
        // Add mouse move and mouse up event listeners
        document.addEventListener('mousemove', moveConnection);
        document.addEventListener('mouseup', endConnection);
    }
    
    /**
     * Handle touch start event for mobile devices.
     * @param {TouchEvent} e - The touch event.
     */
    function handleTouchStart(e) {
        e.preventDefault();
        
        isDrawing = true;
        
        // Create a new line element
        connectionLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        connectionLine.setAttribute('class', 'connection-line');
        connectionLine.setAttribute('stroke', '#29b6f6');
        connectionLine.setAttribute('stroke-width', '2');
        
        // Get the starting position (center of the image)
        const imageRect = centralImage.getBoundingClientRect();
        const containerRect = svgContainer.getBoundingClientRect();
        
        const startX = imageRect.left + imageRect.width / 2 - containerRect.left;
        const startY = imageRect.top + imageRect.height / 2 - containerRect.top;
        
        // Set the starting point of the line
        connectionLine.setAttribute('x1', startX);
        connectionLine.setAttribute('y1', startY);
        connectionLine.setAttribute('x2', startX);
        connectionLine.setAttribute('y2', startY);
        
        // Add the line to the SVG container
        svgContainer.appendChild(connectionLine);
        
        // Add touch move and touch end event listeners
        document.addEventListener('touchmove', handleTouchMove);
        document.addEventListener('touchend', handleTouchEnd);
    }
    
    /**
     * Update the connection line as the mouse moves.
     * @param {MouseEvent} e - The mouse event.
     */
    function moveConnection(e) {
        if (!isDrawing || !connectionLine) return;
        
        const containerRect = svgContainer.getBoundingClientRect();
        const mouseX = e.clientX - containerRect.left;
        const mouseY = e.clientY - containerRect.top;
        
        // Update the end point of the line
        connectionLine.setAttribute('x2', mouseX);
        connectionLine.setAttribute('y2', mouseY);
        
        // Check if the mouse is over a word
        checkWordIntersection(e.clientX, e.clientY);
    }
    
    /**
     * Handle touch move event for mobile devices.
     * @param {TouchEvent} e - The touch event.
     */
    function handleTouchMove(e) {
        if (!isDrawing || !connectionLine) return;
        
        const touch = e.touches[0];
        const containerRect = svgContainer.getBoundingClientRect();
        const touchX = touch.clientX - containerRect.left;
        const touchY = touch.clientY - containerRect.top;
        
        // Update the end point of the line
        connectionLine.setAttribute('x2', touchX);
        connectionLine.setAttribute('y2', touchY);
        
        // Check if the touch is over a word
        checkWordIntersection(touch.clientX, touch.clientY);
    }
    
    /**
     * Check if the cursor intersects with a word element.
     * @param {number} clientX - The client X coordinate.
     * @param {number} clientY - The client Y coordinate.
     */
    function checkWordIntersection(clientX, clientY) {
        // Reset previously selected word
        if (selectedWord) {
            selectedWord.classList.remove('selected');
        }
        selectedWord = null;
        
        // Check each word
        words.forEach(word => {
            const wordRect = word.getBoundingClientRect();
            
            if (
                clientX >= wordRect.left &&
                clientX <= wordRect.right &&
                clientY >= wordRect.top &&
                clientY <= wordRect.bottom
            ) {
                selectedWord = word;
                word.classList.add('selected');
            }
        });
    }
    
    /**
     * End the connection and check if it's correct.
     */
    function endConnection() {
        if (!isDrawing) return;
        
        isDrawing = false;
        
        // Remove event listeners
        document.removeEventListener('mousemove', moveConnection);
        document.removeEventListener('mouseup', endConnection);
        
        // Store the current line for use in the response handling
        const currentLine = connectionLine;
        
        // Check if a word was selected
        if (selectedWord) {
            const selectedAnswer = selectedWord.dataset.word;
            const currentWord = selectedWord;
            
            // Send the answer to the server for validation
            fetch('/game/check_answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    game_type: 'relier_images',
                    question_id: questionId,
                    answer: selectedAnswer
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.correct) {
                        // Correct answer
                        currentLine.setAttribute('class', 'connection-line correct');
                        currentWord.classList.add('correct');
                        
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
                        }, 1500);
                    } else {
                        // Incorrect answer
                        currentLine.setAttribute('class', 'connection-line incorrect');
                        currentWord.classList.add('incorrect');
                        
                        // Remove the line and reset the word after animation
                        setTimeout(() => {
                            if (currentLine && currentLine.parentNode) {
                                currentLine.parentNode.removeChild(currentLine);
                            }
                            currentWord.classList.remove('incorrect', 'selected');
                        }, 1000);
                    }
                } else {
                    alert('Erreur: ' + data.message);
                    
                    // Remove the line
                    if (currentLine && currentLine.parentNode) {
                        currentLine.parentNode.removeChild(currentLine);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Une erreur est survenue lors de la validation de votre réponse.');
                
                // Remove the line
                if (currentLine && currentLine.parentNode) {
                    currentLine.parentNode.removeChild(currentLine);
                }
            });
        } else {
            // No word selected, remove the line
            if (currentLine && currentLine.parentNode) {
                currentLine.parentNode.removeChild(currentLine);
            }
        }
        
        // Reset the global variables
        connectionLine = null;
        selectedWord = null;
    }
    
    /**
     * Handle touch end event for mobile devices.
     */
    function handleTouchEnd() {
        if (!isDrawing) return;
        
        isDrawing = false;
        
        // Remove event listeners
        document.removeEventListener('touchmove', handleTouchMove);
        document.removeEventListener('touchend', handleTouchEnd);
        
        // Store the current line for use in the response handling
        const currentLine = connectionLine;
        
        // Check if a word was selected
        if (selectedWord) {
            const selectedAnswer = selectedWord.dataset.word;
            const currentWord = selectedWord;
            
            // Send the answer to the server for validation
            fetch('/game/check_answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    game_type: 'relier_images',
                    question_id: questionId,
                    answer: selectedAnswer
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.correct) {
                        // Correct answer
                        currentLine.setAttribute('class', 'connection-line correct');
                        currentWord.classList.add('correct');
                        
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
                        }, 1500);
                    } else {
                        // Incorrect answer
                        currentLine.setAttribute('class', 'connection-line incorrect');
                        currentWord.classList.add('incorrect');
                        
                        // Remove the line and reset the word after animation
                        setTimeout(() => {
                            if (currentLine && currentLine.parentNode) {
                                currentLine.parentNode.removeChild(currentLine);
                            }
                            currentWord.classList.remove('incorrect', 'selected');
                        }, 1000);
                    }
                } else {
                    alert('Erreur: ' + data.message);
                    
                    // Remove the line
                    if (currentLine && currentLine.parentNode) {
                        currentLine.parentNode.removeChild(currentLine);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Une erreur est survenue lors de la validation de votre réponse.');
                
                // Remove the line
                if (currentLine && currentLine.parentNode) {
                    currentLine.parentNode.removeChild(currentLine);
                }
            });
        } else {
            // No word selected, remove the line
            if (currentLine && currentLine.parentNode) {
                currentLine.parentNode.removeChild(currentLine);
            }
        }
        
        // Reset the global variables
        connectionLine = null;
        selectedWord = null;
    }
}); 