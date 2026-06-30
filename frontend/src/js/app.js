// Main application controller for Amkyaw AI Agent

class App {
    constructor() {
        this.currentPage = 'chat';
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupTheme();
        this.setupKeyboardShortcuts();
        this.initAnimations();
    }

    setupNavigation() {
        // Handle navigation active states
        const navItems = document.querySelectorAll('.nav-item');
        const currentPath = window.location.pathname;

        navItems.forEach(item => {
            if (item.getAttribute('href') === currentPath) {
                item.classList.add('active');
            }

            item.addEventListener('click', (e) => {
                navItems.forEach(nav => nav.classList.remove('active'));
                e.target.classList.add('active');
            });
        });
    }

    setupTheme() {
        // Check for saved theme preference
        const savedTheme = Utils.getStorage('theme', 'light');
        document.documentElement.setAttribute('data-theme', savedTheme);
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

            // Escape to close modals/overlays
            if (e.key === 'Escape') {
                const overlay = document.getElementById('loadingOverlay');
                if (overlay && overlay.classList.contains('active')) {
                    Animations.hideLoading();
                }
            }
        });
    }

    initAnimations() {
        // Initialize staggered animations on page load
        const animatedElements = document.querySelectorAll('.stagger-item');
        if (animatedElements.length > 0) {
            Animations.initStaggeredAnimations(animatedElements[0].parentElement);
        }
    }

    // Page-specific initialization
    initPage(page) {
        switch (page) {
            case 'chat':
                this.initChatPage();
                break;
            case 'docs':
                this.initDocsPage();
                break;
            case 'skills':
                this.initSkillsPage();
                break;
        }
    }

    initChatPage() {
        // Additional chat page initialization
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.focus();
        }
    }

    initDocsPage() {
        // Initialize docs navigation highlighting
        const docsNav = document.querySelector('.docs-nav');
        if (docsNav) {
            const links = docsNav.querySelectorAll('a');
            links.forEach(link => {
                link.addEventListener('click', () => {
                    links.forEach(l => l.classList.remove('active'));
                    link.classList.add('active');
                });
            });
        }
    }

    initSkillsPage() {
        // Initialize skill cards
        const skillCards = document.querySelectorAll('.skill-card');
        skillCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                Animations.pulse(card, 1.02);
            });
        });
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
    
    // Determine current page
    const path = window.location.pathname;
    if (path.includes('docs')) {
        window.app.initPage('docs');
    } else if (path.includes('skills')) {
        window.app.initPage('skills');
    } else {
        window.app.initPage('chat');
    }
});
