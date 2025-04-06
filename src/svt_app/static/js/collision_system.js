/**
 * Collision detection and bounce system for text-à-trous game.
 * Handles detecting and resolving collisions between orbiting options.
 */

/**
 * Check if two elements are colliding.
 * @param {HTMLElement} el1 - First element
 * @param {HTMLElement} el2 - Second element
 * @returns {boolean} - True if elements are colliding
 */
function checkCollision(el1, el2) {
    const rect1 = el1.getBoundingClientRect();
    const rect2 = el2.getBoundingClientRect();
    
    return !(
        rect1.right < rect2.left || 
        rect1.left > rect2.right || 
        rect1.bottom < rect2.top || 
        rect1.top > rect2.bottom
    );
}

/**
 * Handle collision between two elements by changing their orbits.
 * @param {HTMLElement} el1 - First element
 * @param {HTMLElement} el2 - Second element
 */
function handleCollision(el1, el2) {
    // Get current orbit parameters
    const getOrbitParams = (el) => ({
        x: parseFloat(el.style.getPropertyValue('--orbit-x') || '100px'),
        y: parseFloat(el.style.getPropertyValue('--orbit-y') || '100px'),
        duration: parseFloat(el.style.getPropertyValue('--orbit-duration') || '8s'),
        delay: parseFloat(el.style.getPropertyValue('--orbit-delay') || '0s'),
        direction: el.style.animationDirection
    });
    
    // Switch orbit parameters or adjust them
    const params1 = getOrbitParams(el1);
    const params2 = getOrbitParams(el2);
    
    // Swap direction and slightly modify orbit parameters
    el1.style.animationDirection = params1.direction === 'normal' ? 'reverse' : 'normal';
    el2.style.animationDirection = params2.direction === 'normal' ? 'reverse' : 'normal';
} 