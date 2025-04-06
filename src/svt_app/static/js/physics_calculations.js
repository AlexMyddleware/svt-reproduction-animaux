/**
 * Physics calculations for text-à-trous game.
 * Contains implementation of physics methods.
 */

// Configure game speed here - higher values = faster movement
const GAME_SPEED = 120; // Default: 120 pixels per second

// Maximum velocity to prevent excessive acceleration
const MAX_VELOCITY = 2.5;

/**
 * Update positions of all options based on their velocities.
 * @param {number} deltaTime - Time elapsed since last update in seconds
 */
PhysicsManager.prototype.updatePositions = function(deltaTime) {
    // Limit delta time to avoid huge jumps if browser tab was inactive
    const cappedDelta = Math.min(deltaTime, 0.05);
    
    // Adjust for smoother movement - use configured speed factor
    const speedFactor = window.TEXTE_TROUS_SPEED || GAME_SPEED;
    
    let firstUpdate = false;
    if (!this.hasLoggedFirstUpdate) {
        console.log(`Updating positions with delta time: ${cappedDelta.toFixed(4)}, speed factor: ${speedFactor}`);
        this.hasLoggedFirstUpdate = true;
        firstUpdate = true;
    }
    
    this.options.forEach((option, index) => {
        // Skip if the option is hidden
        if (option.element.style.display === 'none') return;
        
        // Update position based on velocity
        const oldX = option.position.x;
        const oldY = option.position.y;
        
        option.position.x += option.velocity.x * speedFactor * cappedDelta;
        option.position.y += option.velocity.y * speedFactor * cappedDelta;
        
        // Log first movement for debugging
        if (firstUpdate && index === 0) {
            console.log(`First option moved from (${oldX.toFixed(1)},${oldY.toFixed(1)}) to (${option.position.x.toFixed(1)},${option.position.y.toFixed(1)})`);
            console.log(`Velocity: (${option.velocity.x.toFixed(2)},${option.velocity.y.toFixed(2)})`);
        }
        
        // Apply the new position to the DOM element
        option.applyPosition();
    });
};

/**
 * Check for collisions between all options.
 */
PhysicsManager.prototype.checkCollisions = function() {
    for (let i = 0; i < this.options.length; i++) {
        for (let j = i + 1; j < this.options.length; j++) {
            const optionA = this.options[i];
            const optionB = this.options[j];
            
            // Skip if either element is hidden (used already)
            if (optionA.element.style.display === 'none' || 
                optionB.element.style.display === 'none') {
                continue;
            }
            
            if (checkCollision(optionA.element, optionB.element)) {
                // Calculate collision response
                const dx = optionA.position.x - optionB.position.x;
                const dy = optionA.position.y - optionB.position.y;
                
                // Calculate collision normal and distance
                const distance = Math.sqrt(dx * dx + dy * dy);
                const nx = dx / (distance || 1); // Normalized x component
                const ny = dy / (distance || 1); // Normalized y component
                
                // Calculate relative velocity
                const vx = optionA.velocity.x - optionB.velocity.x;
                const vy = optionA.velocity.y - optionB.velocity.y;
                
                // Calculate velocity along the normal
                const velocityAlongNormal = vx * nx + vy * ny;
                
                // Get element rectangles for separation and spark effect
                const elementA = optionA.element.getBoundingClientRect();
                const elementB = optionB.element.getBoundingClientRect();
                
                // Calculate half sizes
                const halfWidthA = elementA.width / 2;
                const halfHeightA = elementA.height / 2;
                const halfWidthB = elementB.width / 2;
                const halfHeightB = elementB.height / 2;
                
                // Calculate centers
                const centerAx = elementA.left + halfWidthA;
                const centerAy = elementA.top + halfHeightA;
                const centerBx = elementB.left + halfWidthB;
                const centerBy = elementB.top + halfHeightB;
                
                // Only separate if moving toward each other
                if (velocityAlongNormal < 0) {
                    // Simple bounce: reverse velocities along normal
                    // Reduced bounce factor to prevent excessive acceleration
                    const bounce = 1.0; // No energy increase (was 1.1)
                    
                    // Save original velocities for debugging
                    const origVelAx = optionA.velocity.x;
                    const origVelAy = optionA.velocity.y;
                    const origVelBx = optionB.velocity.x;
                    const origVelBy = optionB.velocity.y;
                    
                    // Apply impulse along the normal
                    optionA.velocity.x -= velocityAlongNormal * nx * bounce;
                    optionA.velocity.y -= velocityAlongNormal * ny * bounce;
                    optionB.velocity.x += velocityAlongNormal * nx * bounce;
                    optionB.velocity.y += velocityAlongNormal * ny * bounce;
                    
                    // Cap maximum velocity to prevent excessive acceleration
                    optionA.velocity.x = Math.min(Math.max(optionA.velocity.x, -MAX_VELOCITY), MAX_VELOCITY);
                    optionA.velocity.y = Math.min(Math.max(optionA.velocity.y, -MAX_VELOCITY), MAX_VELOCITY);
                    optionB.velocity.x = Math.min(Math.max(optionB.velocity.x, -MAX_VELOCITY), MAX_VELOCITY);
                    optionB.velocity.y = Math.min(Math.max(optionB.velocity.y, -MAX_VELOCITY), MAX_VELOCITY);
                    
                    // Ensure minimum velocity after collision
                    const minVelocity = 0.3;
                    if (Math.abs(optionA.velocity.x) < minVelocity) optionA.velocity.x = (optionA.velocity.x > 0 ? 1 : -1) * minVelocity;
                    if (Math.abs(optionA.velocity.y) < minVelocity) optionA.velocity.y = (optionA.velocity.y > 0 ? 1 : -1) * minVelocity;
                    if (Math.abs(optionB.velocity.x) < minVelocity) optionB.velocity.x = (optionB.velocity.x > 0 ? 1 : -1) * minVelocity;
                    if (Math.abs(optionB.velocity.y) < minVelocity) optionB.velocity.y = (optionB.velocity.y > 0 ? 1 : -1) * minVelocity;
                    
                    // Calculate overlap
                    const overlapX = halfWidthA + halfWidthB - Math.abs(centerAx - centerBx);
                    const overlapY = halfHeightA + halfHeightB - Math.abs(centerAy - centerBy);
                    
                    // Apply separation if there's overlap
                    if (overlapX > 0 && overlapY > 0) {
                        // Move each option half the distance in opposite directions
                        const separationX = overlapX * nx * 1.1; // 10% extra to ensure separation
                        const separationY = overlapY * ny * 1.1;
                        
                        optionA.position.x += separationX * 0.5;
                        optionA.position.y += separationY * 0.5;
                        optionB.position.x -= separationX * 0.5;
                        optionB.position.y -= separationY * 0.5;
                        
                        // Apply the new positions
                        optionA.applyPosition();
                        optionB.applyPosition();
                    }
                }
                
                // Only add visual effects if they're enabled
                if (window.TEXTE_TROUS_EFFECTS_ENABLED !== false) {
                    // Add a visual effect
                    optionA.element.classList.add('bounce');
                    optionB.element.classList.add('bounce');
                    
                    // Add additional collision-flash class for extra visibility
                    optionA.element.classList.add('collision-flash');
                    optionB.element.classList.add('collision-flash');
                    
                    // Create a collision spark effect at the point of impact
                    createCollisionSpark(
                        (centerAx + centerBx) / 2, 
                        (centerAy + centerBy) / 2
                    );
                    
                    setTimeout(() => {
                        optionA.element.classList.remove('bounce');
                        optionB.element.classList.remove('bounce');
                        optionA.element.classList.remove('collision-flash');
                        optionB.element.classList.remove('collision-flash');
                    }, 300);
                }
            }
        }
    }
}; 