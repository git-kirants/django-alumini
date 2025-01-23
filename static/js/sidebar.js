document.addEventListener('DOMContentLoaded', function() {
    // Mobile sidebar toggle
    const sidebar = document.getElementById('sidebar');
    const openSidebarButton = document.getElementById('openSidebar');
    const closeSidebarButton = document.getElementById('closeSidebar');

    if (sidebar && openSidebarButton && closeSidebarButton) {
        openSidebarButton.addEventListener('click', () => {
            sidebar.classList.remove('-translate-x-full');
        });

        closeSidebarButton.addEventListener('click', () => {
            sidebar.classList.add('-translate-x-full');
        });

        // Close sidebar on mobile when clicking outside
        document.addEventListener('click', (e) => {
            if (window.innerWidth < 768 && 
                !sidebar.contains(e.target) && 
                !openSidebarButton.contains(e.target)) {
                sidebar.classList.add('-translate-x-full');
            }
        });
    }
});
