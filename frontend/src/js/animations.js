// Animation utilities for Amkyaw AI Agent

const Animations = {
    // Animation states
    currentAnimation: 'thinking',
    
    // Animation SVG paths
    animations: {
        thinking: '/images/animations/thinking.svg',
        reading: '/images/animations/reading.svg',
        search: '/images/animations/search.svg',
        waiting: '/images/animations/waiting.svg',
        typing: '/images/animations/typing.svg',
        processing: '/images/animations/processing.svg',
        success: '/images/animations/success.svg'
    },

    // Initialize staggered animations
    initStaggeredAnimations(container, selector = '.stagger-item') {
        const items = document.querySelectorAll(selector);
        items.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
            item.classList.add('animate-fade-in-up');
        });
    },

    // Show loading overlay with animation
    showLoading(text = 'Thinking...', animationType = 'thinking') {
        const overlay = document.getElementById('loadingOverlay');
        const loadingText = document.getElementById('loadingText');
        const loadingAnimation = document.getElementById('loadingAnimation');
        
        if (overlay) {
            this.currentAnimation = animationType;
            overlay.classList.add('active');
            
            if (loadingText) loadingText.textContent = text;
            
            // Set animation SVG
            if (loadingAnimation) {
                loadingAnimation.innerHTML = this.getAnimationSVG(animationType);
            }
        }
    },

    // Hide loading overlay
    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.remove('active');
            // Show success animation briefly
            setTimeout(() => {
                const loadingAnimation = document.getElementById('loadingAnimation');
                if (loadingAnimation) {
                    loadingAnimation.innerHTML = this.getAnimationSVG('success');
                }
            }, 100);
        }
    },

    // Get animation SVG by type
    getAnimationSVG(type) {
        const svgMap = {
            thinking: `<svg width="60" height="60" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="20" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
                <path d="M24 8C15.163 8 8 15.163 8 24" stroke="#2563eb" stroke-width="2" stroke-linecap="round">
                    <animateTransform attributeName="transform" type="rotate" from="0 24 24" to="360 24 24" dur="1s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            reading: `<svg width="60" height="60" viewBox="0 0 48 48" fill="none">
                <rect x="8" y="8" width="32" height="32" rx="4" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
                <line x1="14" y1="18" x2="34" y2="18" stroke="#2563eb" stroke-width="2" stroke-linecap="round">
                    <animate attributeName="x2" values="14;34;14" dur="1.5s" repeatCount="indefinite"/>
                </line>
                <line x1="14" y1="24" x2="28" y2="24" stroke="#2563eb" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
                <line x1="14" y1="30" x2="32" y2="30" stroke="#2563eb" stroke-width="2" stroke-linecap="round" opacity="0.4"/>
            </svg>`,
            search: `<svg width="60" height="60" viewBox="0 0 48 48" fill="none">
                <circle cx="20" cy="20" r="12" stroke="#2563eb" stroke-width="2" fill="none"/>
                <circle cx="20" cy="20" r="12" stroke="#2563eb" stroke-width="2" fill="none" stroke-dasharray="20 56">
                    <animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="1.5s" repeatCount="indefinite"/>
                </circle>
                <line x1="29" y1="29" x2="40" y2="40" stroke="#2563eb" stroke-width="3" stroke-linecap="round"/>
            </svg>`,
            waiting: `<svg width="60" height="60" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="18" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.2"/>
                <circle cx="24" cy="24" r="18" stroke="#2563eb" stroke-width="2" fill="none" stroke-linecap="round" stroke-dasharray="80 200">
                    <animateTransform attributeName="transform" type="rotate" from="0 24 24" to="360 24 24" dur="2s" repeatCount="indefinite"/>
                </circle>
                <circle cx="24" cy="24" r="4" fill="#2563eb">
                    <animate attributeName="opacity" values="1;0.3;1" dur="1s" repeatCount="indefinite"/>
                </circle>
            </svg>`,
            typing: `<svg width="60" height="60" viewBox="0 0 48 48" fill="none">
                <rect x="6" y="12" width="36" height="24" rx="4" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.3"/>
                <rect x="6" y="12" width="36" height="24" rx="4" stroke="#2563eb" stroke-width="2" fill="none"/>
                <circle cx="12" cy="24" r="3" fill="#2563eb">
                    <animate attributeName="opacity" values="1;0.2;1" dur="0.6s" repeatCount="indefinite" calcMode="discrete"/>
                </circle>
                <circle cx="22" cy="24" r="3" fill="#2563eb">
                    <animate attributeName="opacity" values="0.2;1;0.2" dur="0.6s" repeatCount="indefinite" calcMode="discrete"/>
                </circle>
                <circle cx="32" cy="24" r="3" fill="#2563eb">
                    <animate attributeName="opacity" values="0.2;0.2;1" dur="0.6s" repeatCount="indefinite" calcMode="discrete"/>
                </circle>
            </svg>`,
            processing: `<svg width="60" height="60" viewBox="0 0 48 48" fill="none">
                <rect x="8" y="8" width="32" height="32" rx="8" stroke="#2563eb" stroke-width="2" fill="none" opacity="0.2"/>
                <rect x="8" y="8" width="32" height="32" rx="8" stroke="#2563eb" stroke-width="2" fill="none">
                    <animate attributeName="stroke-dasharray" values="0 150;150 0" dur="1.5s" repeatCount="indefinite"/>
                </rect>
                <path d="M16 24L22 30L32 18" stroke="#2563eb" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="0.6">
                    <animate attributeName="opacity" values="0.6;1;0.6" dur="1s" repeatCount="indefinite"/>
                </path>
            </svg>`,
            success: `<svg width="60" height="60" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="18" stroke="#22c55e" stroke-width="2" fill="none" opacity="0.2"/>
                <circle cx="24" cy="24" r="18" stroke="#22c55e" stroke-width="2" fill="none" stroke-dasharray="113">
                    <animate attributeName="stroke-dashoffset" from="113" to="0" dur="0.5s" fill="freeze"/>
                </circle>
                <path d="M15 24L21 30L33 18" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <animate attributeName="stroke-dasharray" from="0 50" to="25 0" dur="0.3s" begin="0.3s" fill="freeze"/>
                </path>
            </svg>`
        };
        return svgMap[type] || svgMap.thinking;
    },

    // Change loading animation
    setAnimation(type) {
        const loadingAnimation = document.getElementById('loadingAnimation');
        if (loadingAnimation) {
            loadingAnimation.innerHTML = this.getAnimationSVG(type);
            this.currentAnimation = type;
        }
    },

    // Typewriter effect
    typewriter(element, text, speed = 30) {
        return new Promise((resolve) => {
            let i = 0;
            element.textContent = '';
            
            function type() {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                } else {
                    resolve();
                }
            }
            type();
        });
    },

    // Fade out element
    fadeOut(element, duration = 300) {
        element.style.transition = `opacity ${duration}ms ease`;
        element.style.opacity = '0';
        setTimeout(() => element.remove(), duration);
    },

    // Fade in element
    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.display = 'block';
        requestAnimationFrame(() => {
            element.style.transition = `opacity ${duration}ms ease`;
            element.style.opacity = '1';
        });
    },

    // Slide in from direction
    slideIn(element, direction = 'left', duration = 300) {
        const transforms = {
            left: 'translateX(-30px)',
            right: 'translateX(30px)',
            up: 'translateY(-30px)',
            down: 'translateY(30px)'
        };
        
        element.style.transform = transforms[direction];
        element.style.opacity = '0';
        element.style.transition = `transform ${duration}ms ease, opacity ${duration}ms ease`;
        
        requestAnimationFrame(() => {
            element.style.transform = 'translate(0)';
            element.style.opacity = '1';
        });
    },

    // Pulse animation
    pulse(element, scale = 1.05) {
        element.style.transition = 'transform 0.2s ease';
        element.style.transform = `scale(${scale})`;
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 200);
    },

    // Shake animation
    shake(element) {
        element.classList.add('animate-shake');
        setTimeout(() => element.classList.remove('animate-shake'), 500);
    },

    // Bounce animation
    bounce(element) {
        element.classList.add('animate-bounce');
        setTimeout(() => element.classList.remove('animate-bounce'), 1000);
    },

    // Typing dots animation for loading
    showTypingDots(container) {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
        container.appendChild(typingDiv);
        return typingDiv;
    },

    // Remove typing dots
    removeTypingDots(typingDiv) {
        if (typingDiv && typingDiv.parentNode) {
            typingDiv.parentNode.removeChild(typingDiv);
        }
    },

    // Scroll to bottom smoothly
    scrollToBottom(container, smooth = true) {
        container.scrollTo({
            top: container.scrollHeight,
            behavior: smooth ? 'smooth' : 'auto'
        });
    },

    // Parallax effect
    parallax(element, speed = 0.5) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    },

    // Intersection Observer for scroll animations
    observeReveal(elements, callback) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    if (callback) callback(entry.target);
                }
            });
        }, { threshold: 0.1 });

        elements.forEach(el => observer.observe(el));
    },

    // Confetti animation
    confetti(container = document.body) {
        const colors = ['#2563eb', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6'];
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: ${Math.random() * 100}vw;
                top: -10px;
                opacity: ${Math.random() + 0.5};
                animation: confetti-fall ${2 + Math.random() * 2}s linear forwards;
            `;
            container.appendChild(confetti);
            setTimeout(() => confetti.remove(), 4000);
        }
    },

    // Glitch effect
    glitch(element) {
        element.style.animation = 'none';
        setTimeout(() => {
            element.style.animation = 'glitch 0.3s ease';
        }, 10);
    },

    // Ripple effect
    ripple(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        ripple.style.cssText = `
            position: absolute;
            width: 20px;
            height: 20px;
            background: rgba(37, 99, 235, 0.4);
            border-radius: 50%;
            left: ${event.clientX - rect.left}px;
            top: ${event.clientY - rect.top}px;
            transform: scale(0);
            animation: ripple-effect 0.6s ease-out;
        `;
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Animations;
}
