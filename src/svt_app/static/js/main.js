/**
 * Main JavaScript file for Révijouer application.
 * This file contains common functionality used across the application.
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Révijouer application loaded');
    
    // Add event listeners for buttons with confirmation
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}); 