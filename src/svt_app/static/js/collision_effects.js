/**
 * Visual effects for collisions in text-à-trous game.
 * Creates sparks and other visual effects during collisions.
 */

/**
 * Create a visual spark effect at the collision point.
 * @param {number} x - X coordinate of the collision point
 * @param {number} y - Y coordinate of the collision point
 */
function createCollisionSpark(x, y) {
    // Create a container for the spark effect
    const spark = document.createElement('div');
    spark.className = 'collision-spark';
    document.body.appendChild(spark);
    
    // Position the spark at the collision point
    spark.style.left = `${x}px`;
    spark.style.top = `${y}px`;
    
    // Create multiple particles for the spark effect
    const particleCount = 12;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'spark-particle';
        
        // Random angle distribution in a circle
        const angle = (i / particleCount) * Math.PI * 2;
        
        // Set directional properties as CSS variables
        particle.style.setProperty('--x', Math.cos(angle));
        particle.style.setProperty('--y', Math.sin(angle));
        
        // Random color for each particle
        const colors = ['var(--neon-pink)', 'var(--neon-blue)', 'var(--neon-green)', 'var(--neon-purple)'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        particle.style.backgroundColor = color;
        particle.style.boxShadow = `0 0 10px ${color}`;
        
        // Random size for each particle
        const size = 4 + Math.random() * 8;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Random delay for each particle
        particle.style.animationDelay = `${Math.random() * 0.2}s`;
        
        spark.appendChild(particle);
    }
    
    // Add a flash effect at the collision point
    const flash = document.createElement('div');
    flash.className = 'collision-flash-center';
    spark.appendChild(flash);
    
    // Remove the spark effect after animation completes
    setTimeout(() => {
        spark.style.opacity = '0';
        setTimeout(() => {
            if (document.body.contains(spark)) {
                document.body.removeChild(spark);
            }
        }, 300);
    }, 500);
} 