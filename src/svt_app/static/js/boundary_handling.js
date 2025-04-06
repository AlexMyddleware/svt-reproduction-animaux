/**
 * Boundary handling for text-à-trous game.
 * Contains implementation of boundary checking.
 */

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
            option.velocity.x = -Math.abs(option.velocity.x);
            option.element.classList.add('bounce-right');
            setTimeout(() => option.element.classList.remove('bounce-right'), 300);
        } else if (elementRect.left < containerRect.left + this.boundaryPadding) {
            // Hitting left boundary
            option.position.x += ((containerRect.left + this.boundaryPadding) - elementRect.left);
            option.velocity.x = Math.abs(option.velocity.x);
            option.element.classList.add('bounce-left');
            setTimeout(() => option.element.classList.remove('bounce-left'), 300);
        }
        
        // Check vertical boundaries
        if (elementRect.bottom > containerRect.bottom - this.boundaryPadding) {
            // Hitting bottom boundary
            option.position.y -= (elementRect.bottom - (containerRect.bottom - this.boundaryPadding));
            option.velocity.y = -Math.abs(option.velocity.y);
            option.element.classList.add('bounce-bottom');
            setTimeout(() => option.element.classList.remove('bounce-bottom'), 300);
        } else if (elementRect.top < containerRect.top + this.boundaryPadding) {
            // Hitting top boundary
            option.position.y += ((containerRect.top + this.boundaryPadding) - elementRect.top);
            option.velocity.y = Math.abs(option.velocity.y);
            option.element.classList.add('bounce-top');
            setTimeout(() => option.element.classList.remove('bounce-top'), 300);
        }
        
        // Apply updated position
        option.applyPosition();
    });
}; 