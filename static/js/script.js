/* ========================================
   AUTISM SPECTRUM DISORDER DETECTION SYSTEM
   JavaScript Interactions
   ======================================== */

// ========================================
// GLOBAL VARIABLES
// ========================================
let uploadedFileName = '';

// ========================================
// DOM READY
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// ========================================
// INITIALIZE APPLICATION
// ========================================
function initializeApp() {
    // Highlight active navigation link
    highlightActiveNav();
    
    // Setup form validations
    setupFormValidation();
    
    // Setup file upload
    setupFileUpload();
    
    // Setup smooth scrolling
    setupSmoothScroll();
    
    // Setup mobile menu toggle
    setupMobileMenu();
    
    // Auto-hide alerts
    autoHideAlerts();
}

// ========================================
// NAVIGATION HIGHLIGHTING
// ========================================
function highlightActiveNav() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href.replace('/', ''))) {
            link.classList.add('active');
        }
    });
}

// ========================================
// MOBILE MENU TOGGLE
// ========================================
function setupMobileMenu() {
    // Create mobile menu toggle button if it doesn't exist
    const navContainer = document.querySelector('.nav-container');
    if (!navContainer) return;
    
    const existingToggle = document.querySelector('.mobile-toggle');
    if (existingToggle) return; // Already exists
    
    const mobileToggle = document.createElement('button');
    mobileToggle.classList.add('mobile-toggle');
    mobileToggle.innerHTML = '☰';
    mobileToggle.style.cssText = `
        display: none;
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: var(--primary-color);
    `;
    
    // Show on mobile
    if (window.innerWidth <= 768) {
        mobileToggle.style.display = 'block';
    }
    
    navContainer.appendChild(mobileToggle);
    
    mobileToggle.addEventListener('click', function() {
        const navMenu = document.querySelector('.nav-menu');
        if (navMenu) {
            navMenu.classList.toggle('active');
        }
    });
}

// ========================================
// FORM VALIDATION
// ========================================
function setupFormValidation() {
    // Register Form Validation
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', validateRegisterForm);
    }
    
    // Login Form Validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', validateLoginForm);
    }
    
    // Upload Form Validation
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', validateUploadForm);
    }
}

// ========================================
// REGISTER FORM VALIDATION
// ========================================
function validateRegisterForm(e) {
    // Clear previous errors
    clearErrors();
    
    let isValid = true;
    
    // Get form values
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const mobile = document.getElementById('mobile').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Username validation
    if (username === '') {
        showError('username', 'Username is required');
        isValid = false;
    } else if (username.length < 3) {
        showError('username', 'Username must be at least 3 characters');
        isValid = false;
    }
    
    // Email validation
    if (email === '') {
        showError('email', 'Email is required');
        isValid = false;
    } else if (!isValidEmail(email)) {
        showError('email', 'Please enter a valid email address');
        isValid = false;
    }
    
    // Mobile validation
    if (mobile === '') {
        showError('mobile', 'Mobile number is required');
        isValid = false;
    } else if (!isValidMobile(mobile)) {
        showError('mobile', 'Please enter a valid 10-digit mobile number');
        isValid = false;
    }
    
    // Password validation
    if (password === '') {
        showError('password', 'Password is required');
        isValid = false;
    } else if (password.length < 6) {
        showError('password', 'Password must be at least 6 characters');
        isValid = false;
    }
    
    // Confirm password validation
    if (confirmPassword === '') {
        showError('confirmPassword', 'Please confirm your password');
        isValid = false;
    } else if (password !== confirmPassword) {
        showError('confirmPassword', 'Passwords do not match');
        isValid = false;
    }
    
    if (!isValid) {
        e.preventDefault();
        return false;
    }
    
    return true;
}

// ========================================
// LOGIN FORM VALIDATION
// ========================================
function validateLoginForm(e) {
    clearErrors();
    
    let isValid = true;
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    
    if (email === '') {
        showError('email', 'Email is required');
        isValid = false;
    } else if (!isValidEmail(email)) {
        showError('email', 'Please enter a valid email address');
        isValid = false;
    }
    
    if (password === '') {
        showError('password', 'Password is required');
        isValid = false;
    }
    
    if (!isValid) {
        e.preventDefault();
        return false;
    }
    
    return true;
}

// ========================================
// UPLOAD FORM VALIDATION
// ========================================
function validateUploadForm(e) {
    clearErrors();
    
    const fileInput = document.getElementById('csvFile');
    
    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        showAlert('Please select a CSV file to upload', 'error');
        e.preventDefault();
        return false;
    }
    
    const file = fileInput.files[0];
    const fileName = file.name;
    const fileExtension = fileName.split('.').pop().toLowerCase();
    
    if (fileExtension !== 'csv') {
        showAlert('Only CSV files are allowed', 'error');
        e.preventDefault();
        return false;
    }
    
    // Check file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    if (file.size > maxSize) {
        showAlert('File size must be less than 10MB', 'error');
        e.preventDefault();
        return false;
    }
    
    return true;
}

// ========================================
// VALIDATION HELPERS
// ========================================
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidMobile(mobile) {
    const mobileRegex = /^[0-9]{10}$/;
    return mobileRegex.test(mobile);
}

function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    // Add error class to input
    field.classList.add('error');
    field.style.borderColor = 'var(--danger-color)';
    
    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.classList.add('error-message');
    errorDiv.style.cssText = 'color: var(--danger-color); font-size: 0.85rem; margin-top: 0.25rem;';
    errorDiv.textContent = message;
    
    // Insert error message after the field
    field.parentNode.appendChild(errorDiv);
}

function clearErrors() {
    // Remove error classes
    const errorFields = document.querySelectorAll('.error');
    errorFields.forEach(field => {
        field.classList.remove('error');
        field.style.borderColor = '';
    });
    
    // Remove error messages
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(msg => msg.remove());
}

// ========================================
// FILE UPLOAD HANDLING
// ========================================
function setupFileUpload() {
    const fileInput = document.getElementById('csvFile');
    const fileLabel = document.querySelector('.file-upload-label');
    
    if (fileInput && fileLabel) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'No file chosen';
            uploadedFileName = fileName;
            
            // Update label to show selected file
            const fileNameDisplay = document.querySelector('.file-name');
            if (fileNameDisplay) {
                fileNameDisplay.textContent = fileName;
            } else {
                const fileNameEl = document.createElement('div');
                fileNameEl.classList.add('file-name');
                fileNameEl.textContent = fileName;
                fileLabel.appendChild(fileNameEl);
            }
        });
    }
}

// ========================================
// SMOOTH SCROLL
// ========================================
function setupSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ========================================
// ALERT SYSTEM
// ========================================
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.classList.add('alert', `alert-${type}`);
    alertDiv.textContent = message;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.3s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

// ========================================
// DATASET PREVIEW
// ========================================
function previewDataset(data) {
    const previewContainer = document.getElementById('dataPreview');
    if (!previewContainer) return;
    
    // Create table
    let tableHTML = '<div class="table-wrapper"><table class="data-table"><thead><tr>';
    
    // Add headers
    const headers = Object.keys(data[0]);
    headers.forEach(header => {
        tableHTML += `<th>${header}</th>`;
    });
    tableHTML += '</tr></thead><tbody>';
    
    // Add rows (limit to 10 for preview)
    const previewRows = data.slice(0, 10);
    previewRows.forEach(row => {
        tableHTML += '<tr>';
        headers.forEach(header => {
            tableHTML += `<td>${row[header]}</td>`;
        });
        tableHTML += '</tr>';
    });
    
    tableHTML += '</tbody></table></div>';
    tableHTML += `<p class="text-center mt-3">Showing ${previewRows.length} of ${data.length} records</p>`;
    
    previewContainer.innerHTML = tableHTML;
}

// ========================================
// CHART RENDERING (Simple Bar Chart)
// ========================================
function renderResultChart(positiveCount, negativeCount) {
    const chartContainer = document.getElementById('resultChart');
    if (!chartContainer) return;
    
    const total = positiveCount + negativeCount;
    const positivePercent = (positiveCount / total) * 100;
    const negativePercent = (negativeCount / total) * 100;
    
    const chartHTML = `
        <div style="display: flex; gap: 1rem; align-items: end; height: 250px; justify-content: center;">
            <div style="text-align: center;">
                <div style="
                    width: 100px;
                    height: ${positivePercent * 2}px;
                    background: linear-gradient(to top, var(--danger-color), var(--warning-color));
                    border-radius: 8px 8px 0 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                ">
                    ${positiveCount}
                </div>
                <p style="margin-top: 0.5rem; font-weight: 600;">ASD Detected</p>
            </div>
            <div style="text-align: center;">
                <div style="
                    width: 100px;
                    height: ${negativePercent * 2}px;
                    background: linear-gradient(to top, var(--accent-color), var(--primary-color));
                    border-radius: 8px 8px 0 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                ">
                    ${negativeCount}
                </div>
                <p style="margin-top: 0.5rem; font-weight: 600;">No ASD</p>
            </div>
        </div>
    `;
    
    chartContainer.innerHTML = chartHTML;
}

// ========================================
// UTILITY FUNCTIONS
// ========================================
function showLoading() {
    const spinner = document.createElement('div');
    spinner.classList.add('spinner');
    spinner.id = 'loadingSpinner';
    
    const container = document.querySelector('.container');
    if (container) {
        container.appendChild(spinner);
    }
}

function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.remove();
    }
}

// ========================================
// PASSWORD TOGGLE VISIBILITY
// ========================================
function togglePasswordVisibility(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.type = field.type === 'password' ? 'text' : 'password';
    }
}
