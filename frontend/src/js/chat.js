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
        const isBot = role === 'ai' || role === 'bot';
        messageDiv.className = `message ${isBot ? 'bot' : 'user'}${isError ? ' error' : ''}`;
        
        const avatar = isBot
            ? '<div class="avatar">AI</div>'
            : '<div class="avatar">U</div>';

        // Decode HTML entities first (e.g., &lt;thank&gt; -> <thank>)
        const decodedContent = this.decodeHtmlEntities(content);
        
        // Extract <think> content (thinking process - displayed as processing indicator)
        let thinkContent = '';
        let mainContent = decodedContent;
        
        const thinkMatch = decodedContent.match(/<think>([\s\S]*?)<\/think>/i);
        if (thinkMatch) {
            thinkContent = thinkMatch[1].trim();
            mainContent = decodedContent.replace(/<\/?think>/gi, '');
        }
        
        // Extract <thank> content
        let thankContent = '';
        
        const thankMatch = mainContent.match(/<thank>([\s\S]*?)<\/thank>/i);
        if (thankMatch) {
            thankContent = thankMatch[1].trim();
            mainContent = mainContent.replace(/<\/?thank>/gi, '');
        }

        // Build think indicator if present
        const thinkIndicator = thinkContent ? `
            <div class="think-indicator">
                <div class="think-icon">⚡</div>
                <span class="think-text">Thinking...</span>
            </div>
        ` : '';

        messageDiv.innerHTML = `
            ${avatar}
            <div class="dialog-container">
                ${thinkIndicator}
                ${thankContent ? `<div class="thank-content">${thankContent}</div>` : ''}
                <div class="dialog-box">
                    ${this.formatContentNoThank(mainContent)}
                </div>
                <div class="dialog-arrow"></div>
            </div>
        `;

        this.chatMessages.appendChild(messageDiv);
        Animations.scrollToBottom(this.chatMessages);
        
        this.messages.push({ role, content });
    }
    
    decodeHtmlEntities(text) {
        if (!text) return '';
        return text
            .replace(/&amp;/g, '&')
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/&quot;/g, '"')
            .replace(/&#039;/g, "'")
            .replace(/&#39;/g, "'")
            .replace(/&nbsp;/g, ' ');
    }
    
    formatContentNoThank(content) {
        // Convert markdown-like syntax to HTML (no thank handling)
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

    formatContent(content) {
        // Handle <thank> tags - decode entities and extract content
        let html = this.decodeHtmlEntities(content);
        let thankContent = '';
        
        // Extract content between <thank> tags
        const thankMatch = html.match(/<thank>([\s\S]*?)<\/thank>/i);
        if (thankMatch) {
            thankContent = thankMatch[1].trim();
            html = html.replace(/<\/?thank>/gi, '');
        }
        
        // Escape HTML for main content
        html = Utils.escapeHtml(html);
        
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
        
        // Combine: thank content (no dialog) + main content (with dialog)
        return thankContent ? thankContent + html : html;
    }

    showTyping(skillName = 'thinking') {
        this.isLoading = true;
        this.updateSendButton();
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot';
        typingDiv.id = 'typingIndicator';
        
        const responseText = this.getThinkingText(skillName);
        const skillSVG = this.getSkillSVG(skillName);
        
        typingDiv.innerHTML = `
            <div class="avatar">AI</div>
            <div class="dialog-container">
                <div class="dialog-box skill-active">
                    <div class="skill-animation-container">
                        ${skillSVG}
                    </div>
                    <p class="typing-text mb-0">${responseText}</p>
                </div>
                <div class="dialog-arrow"></div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        Animations.scrollToBottom(this.chatMessages);
    }
    
    getSkillSVG(skillName) {
        const skillLower = (skillName || 'thinking').toLowerCase();
        
        // Skill to SVG mapping
        const svgMap = {
            'search': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" fill="none"/>
                <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="20 22">
                    <animateTransform attributeName="transform" type="rotate" from="0 11 11" to="360 11 11" dur="1.5s" repeatCount="indefinite"/>
                </circle>
                <path d="M21 21L16.5 16.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>`,
            'web': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" fill="none"/>
                <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="20 22">
                    <animateTransform attributeName="transform" type="rotate" from="0 11 11" to="360 11 11" dur="1.5s" repeatCount="indefinite"/>
                </circle>
                <path d="M21 21L16.5 16.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>`,
            'code': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <path d="M16 18L22 12L16 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 6L2 12L8 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 2L12 22" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'programming': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <path d="M16 18L22 12L16 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 6L2 12L8 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 2L12 22" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'read': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke="currentColor" stroke-width="2" fill="none"/>
                <line x1="8" y1="7" x2="16" y2="7" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <animate attributeName="x2" values="8;16;8" dur="1.5s" repeatCount="indefinite"/>
                </line>
            </svg>`,
            'file': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke="currentColor" stroke-width="2" fill="none"/>
                <line x1="8" y1="7" x2="16" y2="7" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <animate attributeName="x2" values="8;16;8" dur="1.5s" repeatCount="indefinite"/>
                </line>
            </svg>`,
            'docs': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke="currentColor" stroke-width="2" fill="none"/>
                <line x1="8" y1="7" x2="16" y2="7" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <animate attributeName="x2" values="8;16;8" dur="1.5s" repeatCount="indefinite"/>
                </line>
            </svg>`,
            'test': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/>
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'deploy': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.5s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'build': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.5s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'security': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" fill="none"/>
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'planning': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2" fill="none" opacity="0.3"/>
                <line x1="3" y1="9" x2="21" y2="9" stroke="currentColor" stroke-width="2"/>
                <line x1="9" y1="21" x2="9" y2="9" stroke="currentColor" stroke-width="2">
                    <animate attributeName="y1" values="21;9;21" dur="2s" repeatCount="indefinite"/>
                </line>
            </svg>`,
            'analyze': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none" opacity="0.3"/>
                <path d="M12 3C8 3 5 8 5 12" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <animate attributeName="d" values="M12 3C8 3 5 8 5 12;M12 3C16 3 19 8 19 12;M12 3C8 3 5 8 5 12" dur="2s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'telegram': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="8" cy="10" r="1" fill="currentColor">
                    <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite"/>
                </circle>
            </svg>`,
            'browser': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/>
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="30 56">
                    <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="2s" repeatCount="indefinite"/>
                </circle>
            </svg>`,
            'scrap': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/>
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="30 56">
                    <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="2s" repeatCount="indefinite"/>
                </circle>
            </svg>`,
            'database': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <ellipse cx="12" cy="5" rx="9" ry="3" stroke="currentColor" stroke-width="2" fill="none"/>
                <path d="M21 5V19C21 20.66 16.97 22 12 22C7.03 22 3 20.66 3 19V5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M21 12V19C21 20.66 16.97 22 12 22C7.03 22 3 20.66 3 19V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
                <path d="M3 5V12C3 13.66 7.03 15 12 15C16.97 15 21 13.66 21 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity="0.5">
                    <animate attributeName="opacity" values="0.3;0.7;0.3" dur="1.5s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'db': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <ellipse cx="12" cy="5" rx="9" ry="3" stroke="currentColor" stroke-width="2" fill="none"/>
                <path d="M21 5V19C21 20.66 16.97 22 12 22C7.03 22 3 20.66 3 19V5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M21 12V19C21 20.66 16.97 22 12 22C7.03 22 3 20.66 3 19V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
                <path d="M3 5V12C3 13.66 7.03 15 12 15C16.97 15 21 13.66 21 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity="0.5">
                    <animate attributeName="opacity" values="0.3;0.7;0.3" dur="1.5s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'processing': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none" opacity="0.3"/>
                <path d="M12 3C8 3 5 8 5 12" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            'thinking': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="skill-icon">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none" opacity="0.3"/>
                <path d="M12 3C8 3 5 8 5 12" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
                </path>
            </svg>`
        };
        
        // Find matching SVG
        for (const [key, svg] of Object.entries(svgMap)) {
            if (skillLower.includes(key)) {
                return svg;
            }
        }
        
        // Default thinking SVG
        return svgMap['thinking'];
    }
    
    getThinkingText(skillName) {
        const skillLower = skillName.toLowerCase();
        
        if (skillLower.includes('search') || skillLower.includes('web')) {
            return 'Searching the web...';
        } else if (skillLower.includes('code') || skillLower.includes('programming')) {
            return 'Writing code...';
        } else if (skillLower.includes('read') || skillLower.includes('file') || skillLower.includes('docs')) {
            return 'Reading documents...';
        } else if (skillLower.includes('test')) {
            return 'Running tests...';
        } else if (skillLower.includes('deploy') || skillLower.includes('build')) {
            return 'Building...';
        } else if (skillLower.includes('security')) {
            return 'Analyzing security...';
        } else if (skillLower.includes('planning') || skillLower.includes('analyze')) {
            return 'Analyzing...';
        } else if (skillLower.includes('telegram')) {
            return 'Sending to Telegram...';
        } else if (skillLower.includes('browser') || skillLower.includes('scrap')) {
            return 'Browsing websites...';
        } else {
            return 'Hello! How can I assist you today?';
        }
    }
    
    async getSkillAnimationSVG(skill) {
        const skillLower = skill.toLowerCase();
        
        // Animation paths for each skill type
        const animationMap = {
            'search': '/images/animations/search.svg',
            'web': '/images/animations/search.svg',
            'code': '/images/animations/typing.svg',
            'programming': '/images/animations/typing.svg',
            'read': '/images/animations/reading.svg',
            'file': '/images/animations/reading.svg',
            'docs': '/images/animations/reading.svg',
            'test': '/images/animations/processing.svg',
            'deploy': '/images/animations/processing.svg',
            'build': '/images/animations/processing.svg',
            'security': '/images/animations/security.svg',
            'planning': '/images/animations/processing.svg',
            'analyze': '/images/animations/processing.svg',
            'telegram': '/images/animations/success.svg',
            'browser': '/images/animations/search.svg',
            'scrap': '/images/animations/search.svg'
        };
        
        // Find matching animation
        let animationPath = '/images/animations/thinking.svg';
        for (const [key, path] of Object.entries(animationMap)) {
            if (skillLower.includes(key)) {
                animationPath = path;
                break;
            }
        }
        
        // Return SVG as inline with small size
        return this.loadSVGAnimation(animationPath);
    }
    
    async loadSVGAnimation(path) {
        try {
            const response = await fetch(path);
            if (response.ok) {
                const svgText = await response.text();
                // Wrap and make small
                return `<div class="skill-animation">${svgText.replace(/<svg/, '<svg width="32" height="32"')}</div>`;
            }
        } catch (e) {
            console.warn('Could not load SVG:', path);
        }
        // Fallback to inline SVG (small)
        return `<div class="skill-animation">${this.getThinkingSVGSmall()}</div>`;
    }
    
    getThinkingSVGSmall() {
        return `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" class="skill-svg">
            <circle cx="12" cy="12" r="10" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
            <path d="M12 6C8.686 6 6 8.686 6 12" stroke="#2563eb" stroke-width="2" stroke-linecap="round">
                <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
            </path>
        </svg>`;
    }
    
    getSearchSVGSmall() {
        return `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" class="skill-svg">
            <circle cx="10" cy="10" r="6" stroke="#2563eb" stroke-width="2" fill="none"/>
            <circle cx="10" cy="10" r="6" stroke="#2563eb" stroke-width="2" fill="none" stroke-dasharray="10 28">
                <animateTransform attributeName="transform" type="rotate" from="0 10 10" to="360 10 10" dur="1.5s" repeatCount="indefinite"/>
            </circle>
            <line x1="14" y1="14" x2="20" y2="20" stroke="#2563eb" stroke-width="2" stroke-linecap="round"/>
        </svg>`;
    }
    
    getCodeSVGSmall() {
        return `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" class="skill-svg">
            <path d="M16 18L22 12L16 6" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M8 6L2 12L8 18" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`;
    }
    
    getReadingSVGSmall() {
        return `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" class="skill-svg">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="#2563eb" stroke-width="2" stroke-linecap="round"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke="#2563eb" stroke-width="2" fill="none"/>
            <line x1="8" y1="7" x2="16" y2="7" stroke="#2563eb" stroke-width="2" stroke-linecap="round">
                <animate attributeName="x2" values="8;16;8" dur="1.5s" repeatCount="indefinite"/>
            </line>
        </svg>`;
    }
    
    getTestingSVGSmall() {
        return `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" class="skill-svg">
            <path d="M9 12L11 14L15 10" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite"/>
            </path>
            <circle cx="12" cy="12" r="8" stroke="#2563eb" stroke-width="2" fill="none"/>
        </svg>`;
    }
    
    getDeploySVGSmall() {
        return `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" class="skill-svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`;
    }
    
    getSecuritySVGSmall() {
        return `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" class="skill-svg">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="#2563eb" stroke-width="2" fill="none"/>
            <path d="M9 12L11 14L15 10" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"/>
            </path>
        </svg>`;
    }
    
    getPlanningSVGSmall() {
        return `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" class="skill-svg">
            <rect x="3" y="3" width="18" height="18" rx="2" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
            <line x1="3" y1="9" x2="21" y2="9" stroke="#2563eb" stroke-width="2"/>
            <line x1="9" y1="21" x2="9" y2="9" stroke="#2563eb" stroke-width="2"/>
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
