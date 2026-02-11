// Compact Beautiful Auth Modal - Perfect Size
function checkAuth() {
    const token = localStorage.getItem('access_token');
    return token ? true : false;
}

function showBeautifulAuthModal(toolName, toolUrl) {
    // Remove any existing modal
    const existingModal = document.getElementById('skillconnect-auth-modal');
    if (existingModal) {
        existingModal.remove();
    }

    // Create compact modal - perfect size
    const modal = document.createElement('div');
    modal.id = 'skillconnect-auth-modal';
    modal.innerHTML = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(6px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: modalFadeIn 0.3s ease;
        ">
            <div style="
                background: white;
                border-radius: 16px;
                padding: 0;
                width: 90%;
                max-width: 380px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
                animation: modalSlideUp 0.4s ease;
                overflow: hidden;
                position: relative;
            ">
                <!-- Close Button -->
                <button onclick="closeAuthModal()" style="
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background: rgba(255, 255, 255, 0.2);
                    border: none;
                    color: white;
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    cursor: pointer;
                    font-size: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.3s ease;
                    z-index: 10;
                " onmouseover="this.style.background='rgba(255,255,255,0.3)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'">
                    ×
                </button>

                <!-- Compact Header -->
                <div style="
                    background: linear-gradient(135deg, var(--primary-teal), var(--coral));
                    padding: 25px 20px 20px;
                    text-align: center;
                    color: white;
                ">
                    <div style="font-size: 32px; margin-bottom: 8px;">💼</div>
                    <h3 style="
                        margin: 0 0 5px 0;
                        font-size: 22px;
                        font-weight: 700;
                        font-family: 'Inter', sans-serif;
                    ">Join SkillConnect</h3>
                    <p style="
                        margin: 0;
                        opacity: 0.9;
                        font-size: 14px;
                    ">Unlock ${toolName}</p>
                </div>

                <!-- Compact Body -->
                <div style="padding: 25px 20px;">
                    <!-- Mini Stats -->
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 20px;
                        background: #f8fafc;
                        padding: 15px;
                        border-radius: 8px;
                        border: 1px solid #e5e7eb;
                    ">
                        <div style="text-align: center; flex: 1;">
                            <div style="font-size: 16px; font-weight: 700; color: var(--primary-teal);">1M+</div>
                            <div style="font-size: 10px; color: var(--gray-600);">JOBS</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div style="font-size: 16px; font-weight: 700; color: var(--primary-teal);">50K+</div>
                            <div style="font-size: 10px; color: var(--gray-600);">COMPANIES</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div style="font-size: 16px; font-weight: 700; color: var(--primary-teal);">5M+</div>
                            <div style="font-size: 10px; color: var(--gray-600);">USERS</div>
                        </div>
                    </div>

                    <!-- Compact Benefits -->
                    <div style="margin-bottom: 20px; font-size: 13px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                            <span style="color: var(--primary-teal); font-weight: 600;">✓</span>
                            <span style="color: var(--gray-700);">Access all career tools</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                            <span style="color: var(--primary-teal); font-weight: 600;">✓</span>
                            <span style="color: var(--gray-700);">Apply to unlimited jobs</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: var(--primary-teal); font-weight: 600;">✓</span>
                            <span style="color: var(--gray-700);">Track applications & alerts</span>
                        </div>
                    </div>

                    <!-- Compact Action Buttons -->
                    <div style="display: flex; flex-direction: column; gap: 8px;">
                        <button onclick="goToRegister('${toolUrl}')" style="
                            background: linear-gradient(135deg, var(--primary-teal), #0891b2);
                            color: white;
                            border: none;
                            padding: 12px 20px;
                            border-radius: 8px;
                            font-size: 14px;
                            font-weight: 600;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            font-family: 'Inter', sans-serif;
                        " onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">
                            🚀 Create Free Account
                        </button>
                        
                        <button onclick="goToLogin('${toolUrl}')" style="
                            background: white;
                            color: var(--primary-teal);
                            border: 1px solid var(--primary-teal);
                            padding: 10px 20px;
                            border-radius: 8px;
                            font-size: 13px;
                            font-weight: 500;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            font-family: 'Inter', sans-serif;
                        " onmouseover="
                            this.style.background='var(--primary-teal)';
                            this.style.color='white';
                        " onmouseout="
                            this.style.background='white';
                            this.style.color='var(--primary-teal)';
                        ">
                            Already have account? Login
                        </button>
                        
                        <button onclick="closeAuthModal()" style="
                            background: none;
                            border: none;
                            color: var(--gray-500);
                            font-size: 12px;
                            cursor: pointer;
                            padding: 8px;
                            transition: color 0.3s ease;
                            font-family: 'Inter', sans-serif;
                            margin-top: 5px;
                        " onmouseover="this.style.color='var(--gray-700)'" onmouseout="this.style.color='var(--gray-500)'">
                            Maybe Later
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Add smooth animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes modalFadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes modalSlideUp {
            from { 
                opacity: 0; 
                transform: translateY(30px) scale(0.95); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0) scale(1); 
            }
        }
        @keyframes modalFadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';

    // Close on background click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeAuthModal();
        }
    });

    return false;
}

function closeAuthModal() {
    const modal = document.getElementById('skillconnect-auth-modal');
    if (modal) {
        modal.style.animation = 'modalFadeOut 0.3s ease-out forwards';
        setTimeout(() => {
            modal.remove();
            document.body.style.overflow = '';
        }, 300);
    }
}

function goToLogin(returnUrl = '') {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    if (returnUrl) {
        localStorage.setItem('return_after_login', returnUrl);
    }
    window.location.href = `login.html?next=${currentPage}`;
}

function goToRegister(returnUrl = '') {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    if (returnUrl) {
        localStorage.setItem('return_after_register', returnUrl);
    }
    window.location.href = `register.html?next=${currentPage}`;
}

// Main blocking functions
function blockTool(toolName, toolUrl) {
    if (checkAuth()) {
        // User logged in - allow access
        window.location.href = toolUrl;
        return true;
    } else {
        // Show beautiful modal
        showBeautifulAuthModal(toolName, toolUrl);
        return false;
    }
}

// For job applications  
function blockJobApply(jobId) {
    if (checkAuth()) {
        // User logged in - allow apply
        window.location.href = `apply-simple.html?job=${jobId}`;
        return true;
    } else {
        // Show beautiful modal for job apply
        showBeautifulAuthModal('job applications', `apply-simple.html?job=${jobId}`);
        return false;
    }
}

console.log('✨ Compact SkillConnect Auth Modal Ready! Perfect Size! 👌');