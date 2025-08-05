// AI News Research Hub - Frontend Application JavaScript

class ResearchApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeFeatherIcons();
        this.setupAutoRefresh();
        this.setupFormValidation();
    }

    setupEventListeners() {
        // Refresh button functionality
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="refresh"]') || 
                e.target.closest('[data-action="refresh"]')) {
                this.refreshPage();
            }
        });

        // Form submission handling
        document.addEventListener('submit', (e) => {
            if (e.target.matches('#research-form')) {
                this.handleResearchSubmission(e);
            }
        });

        // Auto-refresh toggle
        const autoRefreshToggle = document.getElementById('auto-refresh-toggle');
        if (autoRefreshToggle) {
            autoRefreshToggle.addEventListener('change', (e) => {
                this.toggleAutoRefresh(e.target.checked);
            });
        }
    }

    initializeFeatherIcons() {
        if (typeof feather !== 'undefined') {
            feather.replace();
            
            // Re-initialize icons when content is dynamically updated
            const observer = new MutationObserver(() => {
                feather.replace();
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
    }

    setupAutoRefresh() {
        // Check if we're on a project status page
        const projectStatus = document.querySelector('[data-project-status]');
        if (projectStatus) {
            const status = projectStatus.dataset.projectStatus;
            const projectId = projectStatus.dataset.projectId;
            
            // Only auto-refresh for active projects
            if (status && !['completed', 'error', 'stopped'].includes(status)) {
                this.startAutoRefresh(projectId);
            }
        }
    }

    startAutoRefresh(projectId) {
        this.autoRefreshInterval = setInterval(() => {
            this.checkProjectStatus(projectId);
        }, 30000); // Check every 30 seconds
    }

    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
    }

    toggleAutoRefresh(enabled) {
        if (enabled) {
            const projectStatus = document.querySelector('[data-project-status]');
            if (projectStatus) {
                this.startAutoRefresh(projectStatus.dataset.projectId);
            }
        } else {
            this.stopAutoRefresh();
        }
    }

    async checkProjectStatus(projectId) {
        try {
            const response = await fetch(`/api/project/${projectId}/status`);
            if (!response.ok) throw new Error('Status check failed');
            
            const data = await response.json();
            const currentStatus = document.querySelector('[data-project-status]')?.dataset.projectStatus;
            
            // If status changed, reload the page
            if (data.status !== currentStatus) {
                window.location.reload();
            } else {
                // Update progress if available
                this.updateProgress(data.progress);
            }
        } catch (error) {
            console.warn('Failed to check project status:', error);
        }
    }

    updateProgress(progressData) {
        if (!progressData) return;
        
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar && progressData.total_progress !== undefined) {
            const progress = Math.round(progressData.total_progress);
            progressBar.style.width = `${progress}%`;
            progressBar.textContent = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);
        }

        // Update counters
        this.updateCounter('[data-counter="analysts"]', progressData.analysts_created);
        this.updateCounter('[data-counter="interviews-scheduled"]', progressData.interviews_scheduled);
        this.updateCounter('[data-counter="interviews-completed"]', progressData.interviews_completed);
    }

    updateCounter(selector, value) {
        const element = document.querySelector(selector);
        if (element && value !== undefined) {
            element.textContent = value;
        }
    }

    refreshPage() {
        // Add loading indicator
        const refreshBtn = document.querySelector('[data-action="refresh"]');
        if (refreshBtn) {
            const originalContent = refreshBtn.innerHTML;
            refreshBtn.innerHTML = '<i data-feather="loader" class="me-2"></i>Refreshing...';
            refreshBtn.disabled = true;
            
            // Refresh icons and reload
            setTimeout(() => {
                window.location.reload();
            }, 500);
        } else {
            window.location.reload();
        }
    }

    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    validateForm(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        
        inputs.forEach(input => {
            const value = input.value.trim();
            const errorElement = input.parentNode.querySelector('.invalid-feedback');
            
            if (!value) {
                this.showFieldError(input, 'This field is required');
                isValid = false;
            } else if (input.type === 'email' && !this.isValidEmail(value)) {
                this.showFieldError(input, 'Please enter a valid email address');
                isValid = false;
            } else {
                this.clearFieldError(input);
            }
        });
        
        return isValid;
    }

    showFieldError(input, message) {
        input.classList.add('is-invalid');
        let errorElement = input.parentNode.querySelector('.invalid-feedback');
        
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            input.parentNode.appendChild(errorElement);
        }
        
        errorElement.textContent = message;
    }

    clearFieldError(input) {
        input.classList.remove('is-invalid');
        const errorElement = input.parentNode.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.remove();
        }
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    handleResearchSubmission(e) {
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const topicInput = form.querySelector('textarea[name="topic"]');
        
        if (!topicInput || !topicInput.value.trim()) {
            this.showFieldError(topicInput, 'Please enter a research topic');
            e.preventDefault();
            return;
        }
        
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i data-feather="loader" class="me-2"></i>Starting Research...';
        }
    }

    // Utility methods
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }

    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showNotification('Copied to clipboard!', 'success');
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.researchApp = new ResearchApp();
});

// Export for use in other scripts
window.ResearchApp = ResearchApp;

// Additional utility functions
window.utils = {
    formatBytes: (bytes, decimals = 2) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    },
    
    debounce: (func, wait, immediate) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    },
    
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};
