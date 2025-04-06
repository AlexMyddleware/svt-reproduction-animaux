/**
 * Physics manager for text-à-trous game.
 * Coordinates physics and collision detection for all options.
 */

class PhysicsManager {
    /**
     * Initialize the physics manager.
     * @param {HTMLElement} container - The container element
     */
    constructor(container) {
        this.container = container;
        this.options = [];
        this.running = false;
        this.boundaryPadding = 20;
        this.frameCount = 0;
        this.lastLogTime = 0;
    }

    /**
     * Add an option element to be managed.
     * @param {HTMLElement} element - The option element to manage
     */
    addOption(element) {
        this.options.push(new OptionPhysics(element));
    }

    /**
     * Start the physics simulation.
     */
    start() {
        if (this.running) return;
        
        console.log('Physics manager started');
        this.running = true;
        this.lastTime = performance.now();
        this.lastLogTime = this.lastTime;
        
        // Use RAF for smooth animation
        this.animationFrame = requestAnimationFrame(this.update.bind(this));
    }

    /**
     * Stop the physics simulation.
     */
    stop() {
        if (!this.running) return;
        
        console.log('Physics manager stopped');
        this.running = false;
        
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
            this.animationFrame = null;
        }
    }

    /**
     * Update physics for all options.
     * @param {DOMHighResTimeStamp} currentTime - Current timestamp
     */
    update(currentTime) {
        if (!this.running) return;
        
        // Calculate time delta
        const deltaTime = (currentTime - this.lastTime) / 1000;
        this.lastTime = currentTime;
        
        // Skip if delta time is too high (tab was inactive)
        if (deltaTime > 0.1) {
            console.log('Large time delta detected, skipping update');
            this.animationFrame = requestAnimationFrame(this.update.bind(this));
            return;
        }
        
        // Update physics
        this.updatePositions(deltaTime);
        this.checkCollisions();
        this.checkBoundaries();
        
        // Debugging info
        this.frameCount++;
        if (currentTime - this.lastLogTime > 5000) { // Log every 5 seconds
            console.log(`Physics running at ${Math.round(this.frameCount / 5)} FPS`);
            this.frameCount = 0;
            this.lastLogTime = currentTime;
        }
        
        // Continue animation loop
        this.animationFrame = requestAnimationFrame(this.update.bind(this));
    }

    /**
     * Get managed option by element.
     * @param {HTMLElement} element - The element to find
     * @returns {OptionPhysics|null} - The matching physics object or null
     */
    getOptionByElement(element) {
        return this.options.find(option => option.element === element);
    }
} 