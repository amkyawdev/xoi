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

    async login(email, password) {
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
