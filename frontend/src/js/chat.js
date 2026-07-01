// Chat functionality for Amkyaw AI Agent

class ChatManager {
    constructor() {
        this.messages = [];
        this.isLoading = false;
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.newChatBtn = document.getElementById('new-chat-btn');
        
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
            console.error('Chat error:', error);
            this.addMessage('ai', `Error: ${error.message || 'Connection failed. Please try again.'}`, true);
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
            ? '<img src="/images/admin.svg" alt="AI" width="36" height="36" class="rounded-circle flex-shrink-0" />'
            : '<div class="rounded-circle flex-shrink-0 d-flex align-items-center justify-content-center bg-light text-secondary fw-bold" style="width:36px;height:36px;font-size:14px;">U</div>';

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
        
        // Show typing indicator in chat
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <img src="/images/admin.svg" alt="AI" width="36" height="36" class="rounded-circle flex-shrink-0" />
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
        
        // Remove typing indicator from chat
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
    }

    startNewChat() {
        this.messages = [];
        this.chatMessages.innerHTML = '';
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
