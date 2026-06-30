// Chat functionality for Amkyaw AI Agent

class ChatManager {
    constructor() {
        this.messages = [];
        this.isLoading = false;
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.newChatBtn = document.getElementById('newChatBtn');
        
        this.init();
    }

    init() {
        this.loadHistory();
        this.setupEventListeners();
        this.updateSendButton();
    }

    setupEventListeners() {
        // Send message on button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());

        // Send message on Enter key
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

        // New chat button
        this.newChatBtn.addEventListener('click', () => this.startNewChat());

        // Load history on click
        document.querySelectorAll('.history-item').forEach(item => {
            item.addEventListener('click', () => this.loadChat(item.dataset.id));
        });
    }

    autoResize() {
        this.chatInput.style.height = 'auto';
        this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 200) + 'px';
    }

    updateSendButton() {
        this.sendBtn.disabled = !this.chatInput.value.trim() || this.isLoading;
    }

    async sendMessage() {
        const content = this.chatInput.value.trim();
        if (!content || this.isLoading) return;

        // Add user message
        this.addMessage('user', content);
        this.chatInput.value = '';
        this.autoResize();
        this.updateSendButton();

        // Show typing indicator
        this.showTyping();

        try {
            // Call API
            const response = await this.callAPI(content);
            this.hideTyping();
            
            // Add AI response
            this.addMessage('ai', response.message);
            
            // Save to history
            this.saveMessage('user', content);
            this.saveMessage('ai', response.message);
        } catch (error) {
            this.hideTyping();
            this.addMessage('ai', `Sorry, I encountered an error: ${error.message}`, true);
        }
    }

    async callAPI(message) {
        const response = await Utils.apiRequest('/api/chat', {
            method: 'POST',
            body: { message }
        });
        return response;
    }

    addMessage(role, content, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role === 'user' ? 'user' : 'bot'}${isError ? ' error' : ''}`;
        
        const avatar = role === 'ai' || role === 'bot'
            ? '<img src="/public/images/admin.png" alt="AI" width="36" height="36" class="rounded-circle flex-shrink-0" />'
            : '<img src="/public/images/user.png" alt="User" width="36" height="36" class="rounded-circle flex-shrink-0" />';

        messageDiv.innerHTML = `
            ${avatar}
            <div class="message-content">${this.formatContent(content)}</div>
        `;

        this.chatMessages.appendChild(messageDiv);
        Animations.scrollToBottom(this.chatMessages);
        
        this.messages.push({ role, content });
    }

    formatContent(content) {
        // Convert markdown-like syntax to HTML
        let html = Utils.escapeHtml(content);
        
        // Code blocks
        html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
        
        // Inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Bold
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        // Italic
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        
        // Line breaks
        html = html.replace(/\n/g, '<br>');
        
        return html;
    }

    showTyping() {
        this.isLoading = true;
        this.updateSendButton();
        
        // Show loading overlay
        const overlay = document.getElementById('loadingOverlay');
        const animationEl = document.getElementById('loadingAnimation');
        const textEl = document.getElementById('loadingText');
        
        if (overlay && animationEl) {
            // Set thinking animation
            animationEl.innerHTML = `
                <svg width="80" height="80" viewBox="0 0 48 48" fill="none">
                    <circle cx="24" cy="24" r="20" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
                    <path d="M24 8C15.163 8 8 15.163 8 24" stroke="#2563eb" stroke-width="2" stroke-linecap="round">
                        <animateTransform attributeName="transform" type="rotate" from="0 24 24" to="360 24 24" dur="1s" repeatCount="indefinite"/>
                    </path>
                </svg>
            `;
            if (textEl) textEl.textContent = 'Thinking...';
            overlay.classList.add('show');
        }
        
        // Also show typing in chat
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <img src="/public/images/admin.png" alt="AI" width="36" height="36" class="rounded-circle flex-shrink-0" />
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        Animations.scrollToBottom(this.chatMessages);
    }

    hideTyping() {
        this.isLoading = false;
        this.updateSendButton();
        
        // Hide loading overlay
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) overlay.classList.remove('show');
        
        // Remove typing indicator from chat
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
    }

    startNewChat() {
        this.messages = [];
        this.chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                        <path d="M2 17l10 5 10-5"></path>
                        <path d="M2 12l10 5 10-5"></path>
                    </svg>
                </div>
                <h3>Welcome to Amkyaw AI</h3>
                <p>Your intelligent assistant ready to help</p>
            </div>
        `;
    }

    saveMessage(role, content) {
        const chatHistory = Utils.getStorage('chatHistory', []);
        const lastChat = chatHistory[chatHistory.length - 1];
        
        if (lastChat && !lastChat.completed) {
            lastChat.messages.push({ role, content, timestamp: Date.now() });
        } else {
            chatHistory.push({
                id: Utils.generateId(),
                messages: [{ role, content, timestamp: Date.now() }],
                createdAt: Date.now(),
                completed: false
            });
        }
        
        Utils.setStorage('chatHistory', chatHistory);
    }

    loadHistory() {
        const chatHistory = Utils.getStorage('chatHistory', []);
        // Can be used to populate history sidebar
    }

    loadChat(chatId) {
        const chatHistory = Utils.getStorage('chatHistory', []);
        const chat = chatHistory.find(c => c.id === chatId);
        
        if (chat) {
            this.chatMessages.innerHTML = '';
            chat.messages.forEach(msg => {
                this.addMessage(msg.role, msg.content);
            });
            this.messages = chat.messages;
        }
    }
}

// Initialize chat when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatManager = new ChatManager();
});
