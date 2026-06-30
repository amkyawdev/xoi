// Animation utilities for Amkyaw AI Agent

const Animations = {
    // Initialize staggered animations
    initStaggeredAnimations(container, selector = '.stagger-item') {
        const items = document.querySelectorAll(selector);
        items.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
            item.classList.add('animate-fade-in-up');
        });
    },

    // Show loading overlay
    showLoading(text = 'Thinking...') {
        const overlay = document.getElementById('loadingOverlay');
        const loadingText = document.getElementById('loadingText');
        if (overlay) {
            overlay.classList.add('active');
            if (loadingText) loadingText.textContent = text;
        }
    },

    // Hide loading overlay
    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) overlay.classList.remove('active');
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
    }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Animations;
}
