// Main application controller for Amkyaw AI Agent

class App {
    constructor() {
        this.init();
    }

    init() {
        this.setupSidebar();
        this.setupKeyboardShortcuts();
        this.initAnimations();
    }

    setupSidebar() {
        // Sidebar navigation active state
        const navLinks = document.querySelectorAll('.sidebar-nav-item');
        const currentPath = window.location.pathname;
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href.replace('./', '').replace('.html', ''))) {
                link.classList.add('active');
            }
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Cmd/Ctrl + K to focus chat input
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                const chatInput = document.getElementById('chatInput');
                if (chatInput) chatInput.focus();
            }

            // Cmd/Ctrl + N for new chat
            if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
                e.preventDefault();
                const newChatBtn = document.getElementById('newChatBtn');
                if (newChatBtn) newChatBtn.click();
            }
        });
    }

    initAnimations() {
        // Add fade-in animation to main content
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.classList.add('animate-fade-in');
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
    
    // Initialize Lucide icons
    if (window.lucide) {
        window.lucide.createIcons();
    }
});
