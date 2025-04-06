/**
 * Initialization code for the text-à-trous game physics system.
 * Sets up the physics manager and collision detection.
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Physics init starting');
    // Delay the physics initialization slightly to ensure DOM is fully ready
    setTimeout(initPhysics, 300); // Increased delay for better DOM readiness
});

/**
 * Initialize the physics system for the game.
 */
function initPhysics() {
    const optionsContainer = document.querySelector('.options-container');
    if (!optionsContainer) {
        console.error('Options container not found');
        return;
    }
    
    console.log('Creating physics manager');
    // Create the physics manager
    const physicsManager = new PhysicsManager(optionsContainer);
    
    // Get all option elements
    const options = document.querySelectorAll('.option');
    console.log(`Found ${options.length} options`);
    
    if (options.length === 0) {
        console.error('No option elements found');
        return;
    }
    
    // Force the container to have a specific size if too small
    if (optionsContainer.clientHeight < 200) {
        optionsContainer.style.minHeight = '300px';
        console.log('Increasing container height to ensure space for options');
    }
    
    // Calculate container center
    const containerRect = optionsContainer.getBoundingClientRect();
    const centerX = containerRect.width / 2;
    const centerY = containerRect.height / 2;
    console.log(`Container size: ${containerRect.width}x${containerRect.height}, center: (${centerX}, ${centerY})`);
    
    // Initialize with random positions around the center
    options.forEach((option, index) => {
        // Remove any existing CSS positioning/animation
        option.style.animation = 'none';
        option.style.position = 'absolute';
        option.style.left = '0';
        option.style.top = '0';
        option.style.margin = '0';
        
        // Calculate a position around a circle
        const angleStep = (2 * Math.PI) / options.length;
        const angle = index * angleStep + (Math.random() * 0.5 - 0.25); // Add slight randomness
        
        // Use a radius that's appropriate for the container size
        const radius = Math.min(centerX, centerY) * 0.7;
        
        // Calculate initial position
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;
        
        console.log(`Option ${index}: Positioning at angle ${(angle * 180 / Math.PI).toFixed(0)}°, radius ${radius.toFixed(0)}px, position (${x.toFixed(0)}, ${y.toFixed(0)})`);
        
        // Set transform explicitly 
        option.style.transform = `translate(${x}px, ${y}px)`;
        
        // Create a temporary style to force position recalculation
        const tempDisplay = option.style.display;
        option.style.display = 'none';
        
        // Force layout recalculation
        void option.offsetHeight;
        
        // Restore display
        option.style.display = tempDisplay;
        
        // Add to physics system
        option.classList.add('physics-controlled');
        physicsManager.addOption(option);
    });
    
    // Store physics manager for global access
    window.gamePhysicsManager = physicsManager;
    
    // Start physics with a small delay to ensure positions are applied
    setTimeout(() => {
        console.log('Starting physics simulation');
        physicsManager.start();
        
        // Force the first few frames to ensure movement
        let forceFrames = 5;
        const forceUpdate = () => {
            if (forceFrames-- > 0) {
                physicsManager.options.forEach(option => {
                    // Apply position again to ensure it took effect
                    option.applyPosition();
                });
                setTimeout(forceUpdate, 50);
            }
        };
        forceUpdate();
    }, 100);
    
    // Debug check after 1 second
    setTimeout(() => {
        if (physicsManager.options.length > 0) {
            // Log some velocities and positions
            physicsManager.options.forEach((option, i) => {
                console.log(`Option ${i}: pos=(${option.position.x.toFixed(1)}, ${option.position.y.toFixed(1)}), vel=(${option.velocity.x.toFixed(1)}, ${option.velocity.y.toFixed(1)})`);
            });
        }
    }, 1000);
} 