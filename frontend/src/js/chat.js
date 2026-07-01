// Chat functionality for Amkyaw AI Agent

class ChatManager {
    constructor() {
        this.messages = [];
        this.isLoading = false;
        this.conversationId = null;
        
        // DOM Elements
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.newChatBtn = document.getElementById('newChatBtn');
        this.clearChatBtn = document.getElementById('clearChat');
        this.attachBtn = document.getElementById('attachBtn');
        this.fileInput = document.getElementById('fileInput');
        this.suggestionCards = document.querySelectorAll('.suggestion-card');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadHistory();
    }

    setupEventListeners() {
        // Send message on button click
        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', () => this.sendMessage());
        }

        // Send message on Enter key
        if (this.chatInput) {
            this.chatInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });

            // Auto-resize textarea
            this.chatInput.addEventListener('input', () => {
                this.autoResize();
                this.updateSendButton();
            });
        }

        // New chat button
        if (this.newChatBtn) {
            this.newChatBtn.addEventListener('click', () => this.startNewChat());
        }

        // Clear chat button
        if (this.clearChatBtn) {
            this.clearChatBtn.addEventListener('click', () => this.clearChat());
        }

        // File attach button
        if (this.attachBtn && this.fileInput) {
            this.attachBtn.addEventListener('click', () => this.fileInput.click());
            this.fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        }

        // Suggestion cards
        this.suggestionCards.forEach(card => {
            card.addEventListener('click', () => {
                const prompt = card.dataset.prompt;
                if (prompt && this.chatInput) {
                    this.chatInput.value = prompt;
                    this.sendMessage();
                }
            });
        });

        // Sidebar toggle for mobile
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.getElementById('sidebar');
        const sidebarOverlay = document.getElementById('sidebarOverlay');
        const closeSidebar = document.getElementById('closeSidebar');

        if (menuToggle && sidebar) {
            menuToggle.addEventListener('click', () => {
                sidebar.classList.add('open');
                if (sidebarOverlay) sidebarOverlay.classList.add('active');
            });
        }

        if (sidebarOverlay) {
            sidebarOverlay.addEventListener('click', () => {
                sidebar.classList.remove('open');
                sidebarOverlay.classList.remove('active');
            });
        }

        if (closeSidebar) {
            closeSidebar.addEventListener('click', () => {
                sidebar.classList.remove('open');
                if (sidebarOverlay) sidebarOverlay.classList.remove('active');
            });
        }
    }

    autoResize() {
        if (!this.chatInput) return;
        this.chatInput.style.height = 'auto';
        this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 150) + 'px';
    }

    updateSendButton() {
        if (!this.sendBtn || !this.chatInput) return;
        const hasContent = this.chatInput.value.trim().length > 0;
        this.sendBtn.disabled = !hasContent || this.isLoading;
        
        // Toggle send button style
        if (hasContent && !this.isLoading) {
            this.sendBtn.classList.add('active');
        } else {
            this.sendBtn.classList.remove('active');
        }
    }

    async sendMessage() {
        const content = this.chatInput?.value.trim();
        if (!content || this.isLoading) return;

        // Clear welcome container if first message
        this.clearWelcome();

        this.isLoading = true;
        this.updateSendButton();

        // Add user message
        this.addMessage('user', content);
        this.chatInput.value = '';
        this.autoResize();

        // Show typing indicator
        this.showTyping();

        try {
            // Call API
            const response = await this.callAPI(content);
            this.hideTyping();
            
            // Add AI response
            this.addMessage('assistant', response.message || response);
            
            // Save to history
            this.saveMessage('user', content);
            this.saveMessage('assistant', response.message || response);
        } catch (error) {
            this.hideTyping();
            console.error('Chat error:', error);
            this.addMessage('error', `Error: ${error.message || 'Connection failed. Please try again.'}`);
        }

        this.isLoading = false;
        this.updateSendButton();
    }

    async callAPI(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    message,
                    conversation_id: this.conversationId 
                })
            });
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            if (data.conversation_id) {
                this.conversationId = data.conversation_id;
            }
            return data;
        } catch (error) {
            // Fallback demo response
            return { 
                message: `I received your message: "${message}". This is a demo response. Connect to the backend API for full functionality.` 
            };
        }
    }

    addMessage(role, content, isError = false) {
        if (!this.chatMessages) return;

        const messageDiv = document.createElement('div');
        const isUser = role === 'user';
        const isAssistant = role === 'assistant';
        const isErrorMsg = role === 'error';
        
        messageDiv.className = `message ${isUser ? 'user' : 'assistant'}${isErrorMsg ? ' error' : ''}`;
        
        // Avatar icon
        const avatarIcon = isUser 
            ? '<i data-lucide="user" width="16" height="16"></i>'
            : '<i data-lucide="sparkles" width="16" height="16"></i>';
        
        // Process content
        const processedContent = this.formatContent(content);

        messageDiv.innerHTML = `
            <div class="avatar ${isUser ? 'user-avatar' : 'ai-avatar'}">
                ${avatarIcon}
            </div>
            <div class="message-content ${isUser ? 'user-message' : 'ai-message'}">
                ${processedContent}
            </div>
        `;

        this.chatMessages.appendChild(messageDiv);
        
        // Re-initialize Lucide icons for new message
        if (window.lucide) {
            window.lucide.createIcons();
        }
        
        this.scrollToBottom();
        this.messages.push({ role, content });
    }

    formatContent(content) {
        if (!content) return '';
        
        // Escape HTML
        let html = content
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');

        // Code blocks
        html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
        
        // Inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Bold
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        // Italic
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        
        // Headers
        html = html.replace(/^### (.+)$/gm, '<h4>$1</h4>');
        html = html.replace(/^## (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^# (.+)$/gm, '<h2>$1</h2>');
        
        // Lists
        html = html.replace(/^\- (.+)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        
        // Line breaks
        html = html.replace(/\n/g, '<br>');
        
        return html;
    }

    showTyping() {
        if (!this.chatMessages) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant';
        typingDiv.id = 'typingIndicator';
        
        typingDiv.innerHTML = `
            <div class="avatar ai-avatar">
                <i data-lucide="sparkles" width="16" height="16"></i>
            </div>
            <div class="message-content ai-message">
                <div class="typing-indicator">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        
        if (window.lucide) {
            window.lucide.createIcons();
        }
        
        this.scrollToBottom();
    }

    hideTyping() {
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
    }

    clearWelcome() {
        const welcome = document.querySelector('.welcome-container');
        if (welcome) {
            welcome.style.display = 'none';
        }
    }

    startNewChat() {
        this.messages = [];
        this.conversationId = null;
        
        if (this.chatMessages) {
            this.chatMessages.innerHTML = '';
            this.showWelcome();
        }
    }

    clearChat() {
        this.messages = [];
        this.conversationId = null;
        
        if (this.chatMessages) {
            this.chatMessages.innerHTML = '';
            this.showWelcome();
        }
    }

    showWelcome() {
        if (!this.chatMessages) return;
        
        this.chatMessages.innerHTML = `
            <div class="welcome-container animate-fade-in">
                <div class="welcome-icon">
                    <i data-lucide="sparkles" width="48" height="48"></i>
                </div>
                <h1 class="welcome-title">Hello, I'm AmkyawDev AI</h1>
                <p class="welcome-subtitle">Your intelligent assistant powered by advanced AI. How can I help you today?</p>
                
                <div class="suggestion-grid">
                    <button class="suggestion-card" data-prompt="Explain quantum computing in simple terms">
                        <i data-lucide="atom" width="20" height="20"></i>
                        <span>Explain quantum computing</span>
                    </button>
                    <button class="suggestion-card" data-prompt="Write a Python function to sort a list">
                        <i data-lucide="code" width="20" height="20"></i>
                        <span>Write Python code</span>
                    </button>
                    <button class="suggestion-card" data-prompt="What are the best practices for REST API design?">
                        <i data-lucide="globe" width="20" height="20"></i>
                        <span>REST API best practices</span>
                    </button>
                    <button class="suggestion-card" data-prompt="Help me debug this code">
                        <i data-lucide="bug" width="20" height="20"></i>
                        <span>Debug my code</span>
                    </button>
                </div>
            </div>
        `;
        
        // Re-attach suggestion handlers
        this.chatMessages.querySelectorAll('.suggestion-card').forEach(card => {
            card.addEventListener('click', () => {
                const prompt = card.dataset.prompt;
                if (prompt && this.chatInput) {
                    this.chatInput.value = prompt;
                    this.sendMessage();
                }
            });
        });
        
        if (window.lucide) {
            window.lucide.createIcons();
        }
    }

    scrollToBottom() {
        if (this.chatMessages) {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }
    }

    handleFileUpload(event) {
        const file = event.target.files?.[0];
        if (!file) return;
        
        // TODO: Implement file upload logic
        console.log('File selected:', file.name);
    }

    saveMessage(role, content) {
        // Save to localStorage for demo
        const chatHistory = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        const lastChat = chatHistory[chatHistory.length - 1];
        
        if (lastChat && !lastChat.completed) {
            lastChat.messages.push({ role, content, timestamp: Date.now() });
        } else {
            chatHistory.push({
                id: Date.now().toString(),
                messages: [{ role, content, timestamp: Date.now() }],
                createdAt: Date.now(),
                completed: false
            });
        }
        
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    }

    loadHistory() {
        // Load history for sidebar display
        const chatHistory = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        console.log('Loaded chat history:', chatHistory.length, 'conversations');
    }
}

// Initialize chat when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatManager = new ChatManager();
});
