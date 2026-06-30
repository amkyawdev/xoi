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
        messageDiv.className = `message ${role}${isError ? ' error' : ''}`;
        
        const avatar = role === 'ai' 
            ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"></path><path d="M2 17l10 5 10-5"></path><path d="M2 12l10 5 10-5"></path></svg>'
            : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>';

        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
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
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message ai';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5"></path>
                    <path d="M2 12l10 5 10-5"></path>
                </svg>
            </div>
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
