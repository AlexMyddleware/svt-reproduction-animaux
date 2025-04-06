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