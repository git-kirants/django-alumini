document.querySelector('textarea').addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

function toggleReplies() {
    const olderReplies = document.getElementById('olderReplies');
    const viewMoreBtn = document.getElementById('viewMoreBtn');
    const isHidden = olderReplies.classList.contains('hidden');
    
    if (isHidden) {
        olderReplies.classList.remove('hidden');
        viewMoreBtn.innerHTML = '<i class="fas fa-chevron-up mr-2"></i>Hide Previous Replies';
    } else {
        olderReplies.classList.add('hidden');
        viewMoreBtn.innerHTML = '<i class="fas fa-chevron-down mr-2"></i>View Previous Replies';
    }
}
