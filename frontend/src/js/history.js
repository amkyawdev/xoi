// History Manager for Amkyaw AI Agent

class HistoryManager {
    constructor() {
        this.historyList = document.getElementById('history-list');
        this.storageKey = 'amkyaw_history';
        this.init();
    }

    init() {
        this.renderHistory();
        
        // Toggle history button
        const historyToggle = document.getElementById('history-toggle');
        if (historyToggle) {
            historyToggle.addEventListener('click', () => {
                const offcanvas = new bootstrap.Offcanvas(document.getElementById('historyOffcanvas'));
                offcanvas.show();
            });
        }
    }

    getHistory() {
        const data = localStorage.getItem(this.storageKey);
        return data ? JSON.parse(data) : [];
    }

    saveHistory(history) {
        localStorage.setItem(this.storageKey, JSON.stringify(history));
    }

    addToHistory(conversation) {
        const history = this.getHistory();
        history.unshift({
            id: Date.now().toString(),
            title: conversation.title || 'New Chat',
            messages: conversation.messages || [],
            createdAt: new Date().toISOString()
        });
        
        // Keep only last 50 conversations
        if (history.length > 50) {
            history.pop();
        }
        
        this.saveHistory(history);
        this.renderHistory();
    }

    deleteFromHistory(id) {
        const history = this.getHistory().filter(h => h.id !== id);
        this.saveHistory(history);
        this.renderHistory();
    }

    clearHistory() {
        this.saveHistory([]);
        this.renderHistory();
    }

    renderHistory() {
        if (!this.historyList) return;
        
        const history = this.getHistory();
        
        if (history.length === 0) {
            this.historyList.innerHTML = `
                <li class="list-group-item text-muted text-center">
                    <i class="fas fa-inbox me-2"></i>No history yet.
                </li>
            `;
            return;
        }

        this.historyList.innerHTML = history.map(item => `
            <li class="list-group-item d-flex justify-content-between align-items-start py-3">
                <div class="ms-2 me-auto">
                    <div class="fw-semibold">${this.escapeHtml(item.title)}</div>
                    <small class="text-muted">${this.formatDate(item.createdAt)}</small>
                </div>
                <button class="btn btn-sm btn-outline-danger delete-history" data-id="${item.id}">
                    <i class="fas fa-trash"></i>
                </button>
            </li>
        `).join('');

        // Add delete handlers
        this.historyList.querySelectorAll('.delete-history').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.deleteFromHistory(btn.dataset.id);
            });
        });

        // Add click handlers to load conversation
        this.historyList.querySelectorAll('li').forEach((li, index) => {
            if (history[index]) {
                li.style.cursor = 'pointer';
                li.addEventListener('click', () => {
                    this.loadConversation(history[index]);
                });
            }
        });
    }

    loadConversation(conversation) {
        // Emit event to load conversation in chat
        window.dispatchEvent(new CustomEvent('loadConversation', { 
            detail: conversation 
        }));
        
        // Close offcanvas
        const offcanvas = bootstrap.Offcanvas.getInstance(document.getElementById('historyOffcanvas'));
        if (offcanvas) offcanvas.hide();
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        if (diff < 604800000) return `${Math.floor(diff / 86400000)}d ago`;
        
        return date.toLocaleDateString();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.historyManager = new HistoryManager();
});
