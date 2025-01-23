document.addEventListener('DOMContentLoaded', function() {
    const showMoreBtn = document.getElementById('show-more-comments');
    const remainingComments = document.getElementById('remaining-comments');
    const showMoreContainer = document.getElementById('show-more-container');

    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', function() {
            if (remainingComments) {
                // Get all comments from the hidden container
                const comments = remainingComments.innerHTML;
                
                // Insert the comments before the "Show More" button container
                const commentsContainer = document.getElementById('comments-container');
                commentsContainer.insertAdjacentHTML('beforeend', comments);
                
                // Remove the "Show More" button container
                showMoreContainer.remove();
                
                // Remove the hidden comments container
                remainingComments.remove();
            }
        });
    }
});
