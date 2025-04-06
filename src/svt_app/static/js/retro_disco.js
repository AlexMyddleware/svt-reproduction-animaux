/**
 * Retro Disco Theme JavaScript - Far Cry 3: Blood Dragon inspired
 * Handles sound effects, animations, and score tracking for the main menu
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Retro Disco Theme loaded');
    
    // Create audio elements
    const clickSound = new Audio();
    clickSound.src = '/static/audio/click.mp3';
    clickSound.volume = 0.4;
    
    const scoreUpSound = new Audio();
    scoreUpSound.src = '/static/audio/score-up.mp3';
    scoreUpSound.volume = 0.5;
    
    // Get score elements
    const texteTrousScore = document.getElementById('texte-trous-score');
    const relierImagesScore = document.getElementById('relier-images-score');
    
    // Store initial scores to check for changes
    let initialScores = {
        texteTrous: texteTrousScore ? parseInt(texteTrousScore.textContent) : 0,
        relierImages: relierImagesScore ? parseInt(relierImagesScore.textContent) : 0
    };
    
    // Add scanlines effect to body
    const scanlines = document.createElement('div');
    scanlines.className = 'scanlines';
    document.body.appendChild(scanlines);
    
    // Add click sound and bounce animation to menu buttons
    const menuButtons = document.querySelectorAll('.menu-button');
    menuButtons.forEach(button => {
        // Add click sound
        button.addEventListener('click', function(e) {
            // Play click sound (clone it to allow overlapping sounds)
            const soundClone = clickSound.cloneNode();
            soundClone.play();
            
            // If it's a button with a form submit, we add a small delay to hear the sound
            if (this.tagName === 'BUTTON' && !this.classList.contains('no-delay')) {
                e.preventDefault();
                setTimeout(() => {
                    this.form ? this.form.submit() : null;
                }, 200);
            }
        });
        
        // Add hover bounce animation
        button.addEventListener('mouseenter', function() {
            this.style.animation = 'bounce 0.5s ease infinite';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.animation = '';
        });
    });
    
    // Function to check if a score is a multiple of 5
    function isMultipleOfFive(score) {
        return score > 0 && score % 5 === 0;
    }
    
    // Function to update scores and add effects for multiples of 5
    function updateScoreDisplay() {
        if (texteTrousScore) {
            const currentScore = parseInt(texteTrousScore.textContent);
            if (currentScore !== initialScores.texteTrous) {
                if (isMultipleOfFive(currentScore) && currentScore > initialScores.texteTrous) {
                    texteTrousScore.classList.add('score-flash');
                    scoreUpSound.play();
                    setTimeout(() => {
                        texteTrousScore.classList.remove('score-flash');
                    }, 1500);
                }
                initialScores.texteTrous = currentScore;
            }
        }
        
        if (relierImagesScore) {
            const currentScore = parseInt(relierImagesScore.textContent);
            if (currentScore !== initialScores.relierImages) {
                if (isMultipleOfFive(currentScore) && currentScore > initialScores.relierImages) {
                    relierImagesScore.classList.add('score-flash');
                    scoreUpSound.play();
                    setTimeout(() => {
                        relierImagesScore.classList.remove('score-flash');
                    }, 1500);
                }
                initialScores.relierImages = currentScore;
            }
        }
    }
    
    // Check for score updates when the page loads
    updateScoreDisplay();
    
    // Handle the reset scores button
    const resetScoresButton = document.querySelector('button[onclick="resetScores()"]');
    if (resetScoresButton) {
        resetScoresButton.onclick = null; // Remove the inline onclick
        resetScoresButton.addEventListener('click', function() {
            // Play click sound
            clickSound.play();
            
            fetch('/game/reset_scores', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Reload the page to show updated scores
                    setTimeout(() => {
                        window.location.reload();
                    }, 300);
                } else {
                    alert('Une erreur est survenue lors de la réinitialisation des scores.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Une erreur est survenue lors de la réinitialisation des scores.');
            });
        });
    }
}); 