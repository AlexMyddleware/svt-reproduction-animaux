/**
 * Boundary handling for text-à-trous game.
 * Contains implementation of boundary checking.
 */

// Import MAX_VELOCITY constant from physics_calculations.js
// If that doesn't work, define it again here
const BOUNDARY_MAX_VELOCITY = 2.0;

/**
 * Check if any options are outside container boundaries and bounce them.
 */
PhysicsManager.prototype.checkBoundaries = function() {
    const containerRect = this.container.getBoundingClientRect();
    
    this.options.forEach(option => {
        if (option.element.style.display === 'none') return;
        
        const elementRect = option.element.getBoundingClientRect();
        
        // Check horizontal boundaries
        if (elementRect.right > containerRect.right - this.boundaryPadding) {
            // Hitting right boundary
            option.position.x -= (elementRect.right - (containerRect.right - this.boundaryPadding));
            
            // Reverse x velocity (maintain absolute value)
            const currentSpeed = Math.abs(option.velocity.x);
            option.velocity.x = -Math.min(currentSpeed, BOUNDARY_MAX_VELOCITY);
            
            option.element.classList.add('bounce-right');
            setTimeout(() => option.element.classList.remove('bounce-right'), 300);
        } else if (elementRect.left < containerRect.left + this.boundaryPadding) {
            // Hitting left boundary
            option.position.x += ((containerRect.left + this.boundaryPadding) - elementRect.left);
            
            // Reverse x velocity (maintain absolute value)
            const currentSpeed = Math.abs(option.velocity.x);
            option.velocity.x = Math.min(currentSpeed, BOUNDARY_MAX_VELOCITY);
            
            option.element.classList.add('bounce-left');
            setTimeout(() => option.element.classList.remove('bounce-left'), 300);
        }
        
        // Check vertical boundaries
        if (elementRect.bottom > containerRect.bottom - this.boundaryPadding) {
            // Hitting bottom boundary
            option.position.y -= (elementRect.bottom - (containerRect.bottom - this.boundaryPadding));
            
            // Reverse y velocity (maintain absolute value)
            const currentSpeed = Math.abs(option.velocity.y);
            option.velocity.y = -Math.min(currentSpeed, BOUNDARY_MAX_VELOCITY);
            
            option.element.classList.add('bounce-bottom');
            setTimeout(() => option.element.classList.remove('bounce-bottom'), 300);
        } else if (elementRect.top < containerRect.top + this.boundaryPadding) {
            // Hitting top boundary
            option.position.y += ((containerRect.top + this.boundaryPadding) - elementRect.top);
            
            // Reverse y velocity (maintain absolute value)
            const currentSpeed = Math.abs(option.velocity.y);
            option.velocity.y = Math.min(currentSpeed, BOUNDARY_MAX_VELOCITY);
            
            option.element.classList.add('bounce-top');
            setTimeout(() => option.element.classList.remove('bounce-top'), 300);
        }
        
        // Apply updated position
        option.applyPosition();
    });
}; 