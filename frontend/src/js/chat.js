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

    showTyping(skillName = 'thinking') {
        this.isLoading = true;
        this.updateSendButton();
        
        // Get animation SVG based on skill/action
        const animationSvg = this.getSkillAnimationSVG(skillName);
        
        // Show typing indicator in chat
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-message';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <img src="/images/admin.svg" alt="AI" width="36" height="36" class="rounded-circle flex-shrink-0" />
            <div class="message-content">
                ${animationSvg}
                <p class="skill-text mb-0 mt-1">Using ${skillName}...</p>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        Animations.scrollToBottom(this.chatMessages);
    }
    
    getSkillAnimationSVG(skill) {
        const skillLower = skill.toLowerCase();
        
        // Map skills to animations
        if (skillLower.includes('search') || skillLower.includes('web')) {
            return `<div class="skill-animation">${this.getSearchSVG()}</div>`;
        } else if (skillLower.includes('code') || skillLower.includes('programming')) {
            return `<div class="skill-animation">${this.getCodeSVG()}</div>`;
        } else if (skillLower.includes('read') || skillLower.includes('file') || skillLower.includes('docs')) {
            return `<div class="skill-animation">${this.getReadingSVG()}</div>`;
        } else if (skillLower.includes('test')) {
            return `<div class="skill-animation">${this.getTestingSVG()}</div>`;
        } else if (skillLower.includes('deploy') || skillLower.includes('build')) {
            return `<div class="skill-animation">${this.getDeploySVG()}</div>`;
        } else if (skillLower.includes('security')) {
            return `<div class="skill-animation">${this.getSecuritySVG()}</div>`;
        } else if (skillLower.includes('planning') || skillLower.includes('analyze')) {
            return `<div class="skill-animation">${this.getPlanningSVG()}</div>`;
        } else {
            // Default thinking animation
            return `<div class="skill-animation">${this.getThinkingSVG()}</div>`;
        }
    }
    
    getThinkingSVG() {
        return `<svg width="40" height="40" viewBox="0 0 48 48" fill="none" class="skill-svg">
            <circle cx="24" cy="24" r="20" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
            <path d="M24 8C15.163 8 8 15.163 8 24" stroke="#2563eb" stroke-width="2" stroke-linecap="round">
                <animateTransform attributeName="transform" type="rotate" from="0 24 24" to="360 24 24" dur="1s" repeatCount="indefinite"/>
            </path>
        </svg>`;
    }
    
    getSearchSVG() {
        return `<svg width="40" height="40" viewBox="0 0 48 48" fill="none" class="skill-svg">
            <circle cx="20" cy="20" r="12" stroke="#2563eb" stroke-width="2" fill="none"/>
            <circle cx="20" cy="20" r="12" stroke="#2563eb" stroke-width="2" fill="none" stroke-dasharray="20 56">
                <animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="1.5s" repeatCount="indefinite"/>
            </circle>
            <line x1="29" y1="29" x2="40" y2="40" stroke="#2563eb" stroke-width="3" stroke-linecap="round"/>
        </svg>`;
    }
    
    getCodeSVG() {
        return `<svg width="40" height="40" viewBox="0 0 48 48" fill="none" class="skill-svg">
            <rect x="4" y="8" width="40" height="32" rx="4" stroke="#2563eb" stroke-width="2" fill="none"/>
            <path d="M16 18L10 24L16 30" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M32 18L38 24L32 30" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="28" y1="16" x2="20" y2="32" stroke="#2563eb" stroke-width="2" stroke-linecap="round">
                <animate attributeName="opacity" values="1;0.3;1" dur="1s" repeatCount="indefinite"/>
            </line>
        </svg>`;
    }
    
    getReadingSVG() {
        return `<svg width="40" height="40" viewBox="0 0 48 48" fill="none" class="skill-svg">
            <rect x="8" y="8" width="32" height="32" rx="4" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
            <line x1="14" y1="18" x2="34" y2="18" stroke="#2563eb" stroke-width="2" stroke-linecap="round">
                <animate attributeName="x2" values="14;34;14" dur="1.5s" repeatCount="indefinite"/>
            </line>
            <line x1="14" y1="24" x2="28" y2="24" stroke="#2563eb" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
            <line x1="14" y1="30" x2="32" y2="30" stroke="#2563eb" stroke-width="2" stroke-linecap="round" opacity="0.4"/>
        </svg>`;
    }
    
    getTestingSVG() {
        return `<svg width="40" height="40" viewBox="0 0 48 48" fill="none" class="skill-svg">
            <path d="M8 12L24 6L40 12V36L24 42L8 36V12Z" stroke="#2563eb" stroke-width="2" fill="none"/>
            <path d="M8 12L24 18L40 12" stroke="#2563eb" stroke-width="2" fill="none"/>
            <path d="M24 18V42" stroke="#2563eb" stroke-width="2">
                <animate attributeName="stroke-dasharray" values="0 30;30 0" dur="1s" repeatCount="indefinite"/>
            </path>
        </svg>`;
    }
    
    getDeploySVG() {
        return `<svg width="40" height="40" viewBox="0 0 48 48" fill="none" class="skill-svg">
            <path d="M24 4L8 20V44H40V20L24 4Z" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
            <path d="M24 44V24" stroke="#2563eb" stroke-width="2">
                <animate attributeName="d" values="M24 44V24;M24 20V44;M24 44V24" dur="1.5s" repeatCount="indefinite"/>
            </path>
            <path d="M16 36L24 28L32 36" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite"/>
            </path>
        </svg>`;
    }
    
    getSecuritySVG() {
        return `<svg width="40" height="40" viewBox="0 0 48 48" fill="none" class="skill-svg">
            <path d="M24 4L8 12V24C8 33 15 42 24 44C33 42 40 33 40 24V12L24 4Z" stroke="#2563eb" stroke-width="2" fill="none"/>
            <path d="M16 24L22 30L32 18" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"/>
            </path>
        </svg>`;
    }
    
    getPlanningSVG() {
        return `<svg width="40" height="40" viewBox="0 0 48 48" fill="none" class="skill-svg">
            <rect x="6" y="8" width="36" height="36" rx="4" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
            <line x1="6" y1="18" x2="42" y2="18" stroke="#2563eb" stroke-width="2"/>
            <rect x="12" y="24" width="8" height="8" fill="#2563eb" opacity="0.6">
                <animate attributeName="opacity" values="0.6;1;0.6" dur="1s" repeatCount="indefinite"/>
            </rect>
            <rect x="24" y="24" width="8" height="8" fill="#2563eb" opacity="0.4">
                <animate attributeName="opacity" values="0.4;0.8;0.4" dur="1.2s" repeatCount="indefinite"/>
            </rect>
        </svg>`;
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
