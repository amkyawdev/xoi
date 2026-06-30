// Settings Manager for Amkyaw AI Agent

class SettingsManager {
    constructor() {
        this.storageKey = 'amkyaw_settings';
        this.settings = this.getDefaultSettings();
        this.load();
    }

    getDefaultSettings() {
        return {
            theme: 'light',
            language: 'my',
            notifications: true,
            soundEffects: true,
            autoSave: true,
            aiModel: 'mixtral-8x7b-32768',
            temperature: 0.7,
            maxTokens: 4096,
            streamResponses: true,
            showTimestamps: true,
            compactMode: false
        };
    }

    load() {
        const saved = localStorage.getItem(this.storageKey);
        if (saved) {
            try {
                this.settings = { ...this.getDefaultSettings(), ...JSON.parse(saved) };
            } catch (e) {
                this.settings = this.getDefaultSettings();
            }
        }
    }

    save() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.settings));
    }

    get(key) {
        return this.settings[key];
    }

    set(key, value) {
        this.settings[key] = value;
        this.save();
    }

    getAll() {
        return { ...this.settings };
    }

    reset() {
        this.settings = this.getDefaultSettings();
        this.save();
    }

    async syncWithServer() {
        try {
            const response = await fetch('/api/settings', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            });
            
            if (response.ok) {
                const serverSettings = await response.json();
                this.settings = { ...this.settings, ...serverSettings };
                this.save();
            }
        } catch (error) {
            console.error('Failed to sync settings:', error);
        }
    }

    async updateServer() {
        try {
            await fetch('/api/settings', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                },
                body: JSON.stringify(this.settings)
            });
        } catch (error) {
            console.error('Failed to update server:', error);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.settingsManager = new SettingsManager();
});
