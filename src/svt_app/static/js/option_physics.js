/**
 * Physics system for text-à-trous game options.
 * Manages option movement, velocity and position.
 */

class OptionPhysics {
    /**
     * Initialize the physics system for an option element.
     * @param {HTMLElement} element - The option element
     */
    constructor(element) {
        this.element = element;
        this.position = { x: 0, y: 0 };
        this.velocity = { 
            x: (Math.random() * 2 - 1) * 2,  // -2 to 2 range
            y: (Math.random() * 2 - 1) * 2   // -2 to 2 range
        };
        
        // Make sure velocity is not too low
        if (Math.abs(this.velocity.x) < 0.5) {
            this.velocity.x = this.velocity.x > 0 ? 0.5 : -0.5;
        }
        if (Math.abs(this.velocity.y) < 0.5) {
            this.velocity.y = this.velocity.y > 0 ? 0.5 : -0.5;
        }
        
        this.lastCollisionTime = 0;
        
        // Add random speed burst at start
        const speedMultiplier = 1 + Math.random();
        this.velocity.x *= speedMultiplier;
        this.velocity.y *= speedMultiplier;

        // Initialize position from current transform
        this.updatePositionFromElement();
        console.log(`Physics initialized for element with velocity: (${this.velocity.x.toFixed(2)}, ${this.velocity.y.toFixed(2)})`);
    }

    /**
     * Update the position based on element's current transform.
     */
    updatePositionFromElement() {
        // Get computed transform
        const transform = window.getComputedStyle(this.element).transform;
        
        // If we have a transform matrix, extract translation values
        if (transform && transform !== 'none') {
            const matrix = transform.match(/matrix.*\((.+)\)/);
            if (matrix && matrix[1]) {
                const values = matrix[1].split(', ');
                if (values.length >= 6) {
                    // Standard transform matrix - last two values are translation
                    this.position.x = parseFloat(values[4]);
                    this.position.y = parseFloat(values[5]);
                    console.log(`Extracted position from matrix: (${this.position.x}, ${this.position.y})`);
                    return;
                }
            }
        }
        
        // If no transform matrix or couldn't parse it, try to extract from transform attribute
        const transformAttr = this.element.style.transform;
        if (transformAttr && transformAttr.includes('translate')) {
            const translateMatch = transformAttr.match(/translate\(([^,]+)px,\s*([^)]+)px\)/);
            if (translateMatch && translateMatch.length >= 3) {
                this.position.x = parseFloat(translateMatch[1]);
                this.position.y = parseFloat(translateMatch[2]);
                console.log(`Extracted position from translate: (${this.position.x}, ${this.position.y})`);
                return;
            }
        }
        
        // Fallback to getBoundingClientRect if transform can't be parsed
        const rect = this.element.getBoundingClientRect();
        const parentRect = this.element.offsetParent?.getBoundingClientRect() || { left: 0, top: 0 };
        this.position.x = rect.left - parentRect.left;
        this.position.y = rect.top - parentRect.top;
        console.log(`Using fallback position: (${this.position.x}, ${this.position.y})`);
    }

    /**
     * Apply current position to the element.
     */
    applyPosition() {
        this.element.style.transform = `translate(${this.position.x}px, ${this.position.y}px)`;
    }

    /**
     * Reverse velocity for bounce effect.
     * @param {string} axis - The axis to reverse ('x', 'y', or 'both')
     */
    bounce(axis = 'both') {
        const now = Date.now();
        // Prevent too frequent bounces
        if (now - this.lastCollisionTime < 500) return;
        
        if (axis === 'x' || axis === 'both') this.velocity.x *= -1;
        if (axis === 'y' || axis === 'both') this.velocity.y *= -1;
        this.lastCollisionTime = now;
    }
} 