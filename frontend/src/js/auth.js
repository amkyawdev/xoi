// Authentication functionality for Amkyaw AI Agent

class Auth {
    constructor() {
        this.token = null;
        this.user = null;
        this.init();
    }

    init() {
        this.loadUser();
    }

    loadUser() {
        this.token = Utils.getStorage('authToken');
        this.user = Utils.getStorage('user');
        
        if (this.token && this.user) {
            this.updateUI();
        }
    }

    updateUI() {
        const userAvatar = document.querySelector('.user-avatar');
        const userName = document.querySelector('.user-name');
        
        if (userAvatar && this.user) {
            userAvatar.textContent = this.user.name?.charAt(0).toUpperCase() || 'U';
        }
        if (userName && this.user) {
            userName.textContent = this.user.name || 'User';
        }
    }

    // Validate email format
    validateEmail(email) {
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!pattern.test(email)) {
            return { valid: false, message: 'Please enter a valid email address' };
        }
        return { valid: true };
    }

    // Validate password strength
    validatePassword(password) {
        if (password.length < 8) {
            return { valid: false, message: 'Password must be at least 8 characters' };
        }
        if (!/[A-Z]/.test(password)) {
            return { valid: false, message: 'Password must contain at least one uppercase letter' };
        }
        if (!/[a-z]/.test(password)) {
            return { valid: false, message: 'Password must contain at least one lowercase letter' };
        }
        if (!/\d/.test(password)) {
            return { valid: false, message: 'Password must contain at least one digit' };
        }
        return { valid: true };
    }

    // Validate username
    validateUsername(username) {
        if (username.length < 2) {
            return { valid: false, message: 'Username must be at least 2 characters' };
        }
        if (username.length > 50) {
            return { valid: false, message: 'Username must be at most 50 characters' };
        }
        if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
            return { valid: false, message: 'Username can only contain letters, numbers, underscores, and hyphens' };
        }
        return { valid: true };
    }

    async login(email, password) {
        // Validate email
        const emailValidation = this.validateEmail(email);
        if (!emailValidation.valid) {
            Utils.showToast(emailValidation.message, 'error');
            return { success: false, error: emailValidation.message };
        }

        // Validate password exists
        if (!password) {
            Utils.showToast('Please enter your password', 'error');
            return { success: false, error: 'Password required' };
        }

        try {
            const response = await Utils.apiRequest('/api/auth/login', {
                method: 'POST',
                body: { email, password }
            });

            this.token = response.token;
            this.user = response.user;

            Utils.setStorage('authToken', this.token);
            Utils.setStorage('user', this.user);

            this.updateUI();
            Utils.showToast('Login successful!', 'success');
            
            return { success: true };
        } catch (error) {
            Utils.showToast(error.message || 'Login failed', 'error');
            return { success: false, error };
        }
    }

    async register(name, email, password) {
        // Validate username
        const usernameValidation = this.validateUsername(name);
        if (!usernameValidation.valid) {
            Utils.showToast(usernameValidation.message, 'error');
            return { success: false, error: usernameValidation.message };
        }

        // Validate email
        const emailValidation = this.validateEmail(email);
        if (!emailValidation.valid) {
            Utils.showToast(emailValidation.message, 'error');
            return { success: false, error: emailValidation.message };
        }

        // Validate password
        const passwordValidation = this.validatePassword(password);
        if (!passwordValidation.valid) {
            Utils.showToast(passwordValidation.message, 'error');
            return { success: false, error: passwordValidation.message };
        }

        try {
            const response = await Utils.apiRequest('/api/auth/register', {
                method: 'POST',
                body: { name, email, password }
            });

            this.token = response.token;
            this.user = response.user;

            Utils.setStorage('authToken', this.token);
            Utils.setStorage('user', this.user);

            this.updateUI();
            Utils.showToast('Registration successful!', 'success');
            
            return { success: true };
        } catch (error) {
            Utils.showToast(error.message || 'Registration failed', 'error');
            return { success: false, error };
        }
    }

    async resetPassword(email) {
        // Validate email
        const emailValidation = this.validateEmail(email);
        if (!emailValidation.valid) {
            Utils.showToast(emailValidation.message, 'error');
            return { success: false, error: emailValidation.message };
        }

        try {
            await Utils.apiRequest('/api/auth/reset', {
                method: 'POST',
                body: { email }
            });

            Utils.showToast('Password reset email sent!', 'success');
            return { success: true };
        } catch (error) {
            Utils.showToast(error.message || 'Reset failed', 'error');
            return { success: false, error };
        }
    }

    logout() {
        this.token = null;
        this.user = null;
        
        Utils.removeStorage('authToken');
        Utils.removeStorage('user');
        
        // Redirect to login or home
        window.location.href = '/src/pages/login.html';
    }

    isAuthenticated() {
        return !!this.token;
    }

    getToken() {
        return this.token;
    }

    getUser() {
        return this.user;
    }
}

// Initialize auth when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.auth = new Auth();
});
