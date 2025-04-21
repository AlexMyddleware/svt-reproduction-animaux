// Folder management functionality
function initializeFolderManagement() {
    // Add fold all button to the toolbar
    const toolbarActions = document.querySelector('.toolbar-actions');
    const foldAllButton = document.createElement('button');
    foldAllButton.className = 'toolbar-button';
    foldAllButton.id = 'fold-all-btn';
    foldAllButton.textContent = 'Plier tout';
    toolbarActions.insertBefore(foldAllButton, toolbarActions.firstChild);

    // Add fold button to each folder
    document.querySelectorAll('.folder-name').forEach(folderName => {
        const folderActions = folderName.querySelector('.folder-actions');
        const foldButton = document.createElement('button');
        foldButton.className = 'action-button fold-folder';
        foldButton.textContent = 'Plier';
        folderActions.insertBefore(foldButton, folderActions.firstChild);
    });

    // Handle fold all button click
    document.getElementById('fold-all-btn').addEventListener('click', function() {
        const isAnyFolderExpanded = Array.from(document.querySelectorAll('.folder-content'))
            .some(content => !content.classList.contains('collapsed'));

        document.querySelectorAll('.folder-content').forEach(content => {
            if (isAnyFolderExpanded) {
                content.classList.add('collapsed');
                content.previousElementSibling.classList.add('collapsed');
            } else {
                content.classList.remove('collapsed');
                content.previousElementSibling.classList.remove('collapsed');
            }
        });

        // Update button text
        this.textContent = isAnyFolderExpanded ? 'Déplier tout' : 'Plier tout';
    });

    // Handle individual folder fold buttons
    document.querySelectorAll('.fold-folder').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const folderNode = this.closest('.folder-node');
            const folderContent = folderNode.querySelector('.folder-content');
            const isFolded = folderContent.classList.contains('collapsed');

            folderContent.classList.toggle('collapsed');
            folderNode.querySelector('.folder-name').classList.toggle('collapsed');
            this.textContent = isFolded ? 'Plier' : 'Déplier';
        });
    });

    // Handle folder deletion
    document.querySelectorAll('.folder-node .delete-button').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.stopPropagation();
            const path = this.closest('.folder-node').dataset.path;
            
            if (confirm('Êtes-vous sûr de vouloir supprimer ce dossier et tout son contenu ?')) {
                try {
                    const response = await fetch('/game/delete_folder', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ path: path })
                    });
                    
                    const result = await response.json();
                    if (result.success) {
                        // Remove the folder node from the DOM
                        this.closest('.folder-node').remove();
                    } else {
                        alert(result.message || 'Une erreur est survenue lors de la suppression du dossier');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Une erreur est survenue lors de la suppression du dossier');
                }
            }
        });
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeFolderManagement); 