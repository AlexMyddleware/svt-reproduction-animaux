/**
 * Effects toggle functionality for text-à-trous game.
 * Handles enabling/disabling visual collision effects.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the effects toggle
    initEffectsToggle();
});

/**
 * Initialize effects toggle and event listeners.
 */
function initEffectsToggle() {
    const effectsToggle = document.getElementById('effects-toggle');
    
    if (!effectsToggle) return;
    
    // Load saved preference if available
    try {
        const effectsEnabled = localStorage.getItem('texte_trous_effects');
        if (effectsEnabled !== null) {
            const enabled = effectsEnabled === 'true';
            effectsToggle.checked = enabled;
            applyEffectsState(enabled);
        }
    } catch (e) {
        console.log('Could not load effects preference');
    }
    
    // Add event listener for toggle changes
    effectsToggle.addEventListener('change', function(e) {
        const enabled = e.target.checked;
        applyEffectsState(enabled);
        
        // Try to save the preference if localStorage is available
        try {
            localStorage.setItem('texte_trous_effects', String(enabled));
        } catch (e) {
            console.log('Could not save effects preference');
        }
    });
}

// file for color picker


// function to change the color of the option, takes the hex code as a parameter
function changeColor(hex) {
    console.log('Applying color:', hex);
    const options = document.querySelectorAll('.option');
    options.forEach(option => {
        option.style.setProperty('color', hex, 'important');
    });
    
    // Save the color preference
    try {
        localStorage.setItem('texte_trous_color', hex);
    } catch (e) {
        console.log('Could not save color preference');
    }
}

// Initialize color picker functionality
document.addEventListener('DOMContentLoaded', function() {
    const colorPicker = document.getElementById('color-picker');
    const applyColorBtn = document.querySelector('.color-apply-btn');
    
    if (colorPicker && applyColorBtn) {
        // Load saved color preference if available
        try {
            const savedColor = localStorage.getItem('texte_trous_color');
            if (savedColor) {
                colorPicker.value = savedColor;
                changeColor(savedColor);
            }
        } catch (e) {
            console.log('Could not load color preference');
        }

        // Apply color when button is clicked
        applyColorBtn.addEventListener('click', function() {
            const selectedColor = colorPicker.value;
            changeColor(selectedColor);
        });

        // Optional: Preview color changes in real-time
        colorPicker.addEventListener('input', function() {
            changeColor(this.value);
        });
    }
});

/**
 * Apply the effects state by adding or removing a class to the document body.
 * @param {boolean} enabled - Whether effects are enabled
 */
function applyEffectsState(enabled) {
    if (enabled) {
        document.body.classList.remove('effects-disabled');
        console.log('Collision effects enabled');
    } else {
        document.body.classList.add('effects-disabled');
        console.log('Collision effects disabled');
    }
    
    // Store global state for other scripts to check
    window.TEXTE_TROUS_EFFECTS_ENABLED = enabled;
}

/**
 * Check if effects are currently enabled.
 * @returns {boolean} - Whether effects are enabled
 */
function areEffectsEnabled() {
    return window.TEXTE_TROUS_EFFECTS_ENABLED !== false;
} 