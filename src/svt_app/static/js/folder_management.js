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
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeFolderManagement); 