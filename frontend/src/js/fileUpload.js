// File Upload Handler for Amkyaw AI Agent

class FileUploadHandler {
    constructor() {
        this.uploadBtn = document.getElementById('upload-btn');
        this.fileInput = document.getElementById('file-input');
        this.uploadPreview = document.getElementById('upload-preview');
        this.fileName = document.getElementById('file-name');
        this.removeFileBtn = document.getElementById('remove-file-btn');
        this.currentFile = null;
        
        this.init();
    }

    init() {
        if (this.uploadBtn && this.fileInput) {
            this.uploadBtn.addEventListener('click', () => this.fileInput.click());
            this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }
        
        if (this.removeFileBtn) {
            this.removeFileBtn.addEventListener('click', () => this.removeFile());
        }
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.currentFile = file;
            this.showPreview(file);
        }
    }

    showPreview(file) {
        if (this.uploadPreview && this.fileName) {
            this.uploadPreview.classList.remove('d-none');
            this.uploadPreview.classList.add('show');
            this.fileName.textContent = file.name;
        }
    }

    removeFile() {
        this.currentFile = null;
        if (this.fileInput) this.fileInput.value = '';
        if (this.uploadPreview) {
            this.uploadPreview.classList.add('d-none');
            this.uploadPreview.classList.remove('show');
        }
    }

    async uploadFile() {
        if (!this.currentFile) return null;

        const formData = new FormData();
        formData.append('file', this.currentFile);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Upload failed');

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Upload error:', error);
            return null;
        }
    }

    getFile() {
        return this.currentFile;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.fileUploadHandler = new FileUploadHandler();
});
