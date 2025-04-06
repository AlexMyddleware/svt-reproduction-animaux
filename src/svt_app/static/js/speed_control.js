/**
 * Speed control functionality for text-à-trous game.
 * Handles the speed slider and updates game speed.
 */

// Default reference speed value
const DEFAULT_SPEED = 120;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the speed control
    initSpeedControl();
});

/**
 * Initialize speed control slider and event listeners.
 */
function initSpeedControl() {
    const speedSlider = document.getElementById('speed-slider');
    const speedValue = document.getElementById('speed-value');
    const speedPercentage = document.getElementById('speed-percentage');
    
    if (!speedSlider || !speedValue) return;
    
    // Set initial value
    window.TEXTE_TROUS_SPEED = parseInt(speedSlider.value);
    updateSpeedLabel(speedSlider.value);
    
    // Add event listener for slider changes
    speedSlider.addEventListener('input', function(e) {
        const newSpeed = parseInt(e.target.value);
        window.TEXTE_TROUS_SPEED = newSpeed;
        updateSpeedLabel(newSpeed);
        
        // Apply the speed change immediately if the physics is running
        if (window.gamePhysicsManager) {
            console.log(`Speed changed to ${newSpeed}`);
        }
        
        // Try to save the preference if localStorage is available
        try {
            localStorage.setItem('texte_trous_speed', newSpeed);
        } catch (e) {
            console.log('Could not save speed preference');
        }
    });
    
    // Load saved preference if available
    try {
        const savedSpeed = localStorage.getItem('texte_trous_speed');
        if (savedSpeed) {
            const parsedSpeed = parseInt(savedSpeed);
            speedSlider.value = parsedSpeed;
            window.TEXTE_TROUS_SPEED = parsedSpeed;
            updateSpeedLabel(parsedSpeed);
        }
    } catch (e) {
        console.log('Could not load speed preference');
    }
}

/**
 * Update the speed label text based on the speed value.
 * @param {number} speed - The speed value
 */
function updateSpeedLabel(speed) {
    const speedValue = document.getElementById('speed-value');
    const speedPercentage = document.getElementById('speed-percentage');
    
    if (!speedValue) return;
    
    // Calculate percentage compared to default
    const percentage = Math.round((speed / DEFAULT_SPEED) * 100);
    
    // Update percentage display
    if (speedPercentage) {
        speedPercentage.textContent = `(${percentage}%)`;
        
        // Apply color based on percentage
        if (percentage <= 50) {
            speedPercentage.style.color = '#6495ED'; // Blue
        } else if (percentage <= 100) {
            speedPercentage.style.color = '#4CAF50'; // Green
        } else if (percentage <= 250) {
            speedPercentage.style.color = '#FF9800'; // Orange
        } else {
            speedPercentage.style.color = '#FF5252'; // Red
        }
    }
    
    // Set the text label
    if (speed <= 40) {
        speedValue.textContent = 'Très lent';
        speedValue.style.color = '#6495ED'; // Cornflower blue
    } else if (speed <= 80) {
        speedValue.textContent = 'Lent';
        speedValue.style.color = '#4169E1'; // Royal blue
    } else if (speed <= 160) {
        speedValue.textContent = 'Normal';
        speedValue.style.color = '#4CAF50'; // Green
    } else if (speed <= 280) {
        speedValue.textContent = 'Rapide';
        speedValue.style.color = '#FF9800'; // Orange
    } else if (speed <= 400) {
        speedValue.textContent = 'Très rapide';
        speedValue.style.color = '#FF5252'; // Red
    } else {
        speedValue.textContent = 'Extrême';
        speedValue.style.color = '#B71C1C'; // Dark red
    }
} 