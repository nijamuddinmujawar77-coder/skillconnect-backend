// Beautiful Auth Modal - Matches SkillConnect Style
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

    // Create modal with your website's style
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
            backdrop-filter: blur(8px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: modalFadeIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        ">
            <div style="
                background: white;
                border-radius: 20px;
                padding: 0;
                max-width: 450px;
                width: 90%;
                box-shadow: 0 25px 80px rgba(0, 0, 0, 0.15);
                animation: modalSlideUp 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                overflow: hidden;
                position: relative;
            ">
                <!-- Header with gradient like your website -->
                <div style="
                    background: linear-gradient(135deg, var(--primary-teal), var(--coral));
                    padding: 30px;
                    text-align: center;
                    color: white;
                    position: relative;
                ">
                    <div style="
                        position: absolute;
                        top: 15px;
                        right: 15px;
                        background: rgba(255, 255, 255, 0.2);
                        border: none;
                        color: white;
                        width: 35px;
                        height: 35px;
                        border-radius: 50%;
                        cursor: pointer;
                        font-size: 18px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        transition: all 0.3s ease;
                    " onclick="closeAuthModal()" onmouseover="this.style.background='rgba(255,255,255,0.3)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'">
                        ×
                    </div>
                    
                    <div style="font-size: 48px; margin-bottom: 15px;">
                        �
                    </div>
                    <h2 style="
                        margin: 0 0 10px 0;
                        font-size: 28px;
                        font-weight: 800;
                        font-family: 'Inter', sans-serif;
                    ">Join SkillConnect</h2>
                    <p style="
                        margin: 0;
                        opacity: 0.9;
                        font-size: 16px;
                        font-weight: 500;
                    ">Unlock ${toolName} and advance your career</p>
                </div>

                <!-- Body Content -->
                <div style="padding: 35px;">
                    <!-- Stats matching your website style -->
                    <div style="
                        display: grid;
                        grid-template-columns: repeat(3, 1fr);
                        gap: 20px;
                        margin-bottom: 30px;
                        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
                        padding: 20px;
                        border-radius: 12px;
                        border: 1px solid #e5e7eb;
                    ">
                        <div style="text-align: center;">
                            <div style="
                                font-size: 20px;
                                font-weight: 800;
                                color: var(--primary-teal);
                                font-family: 'Inter', sans-serif;
                            ">1M+</div>
                            <div style="
                                font-size: 11px;
                                color: var(--gray-600);
                                font-weight: 600;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                            ">Jobs</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="
                                font-size: 20px;
                                font-weight: 800;
                                color: var(--primary-teal);
                                font-family: 'Inter', sans-serif;
                            ">50K+</div>
                            <div style="
                                font-size: 11px;
                                color: var(--gray-600);
                                font-weight: 600;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                            ">Companies</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="
                                font-size: 20px;
                                font-weight: 800;
                                color: var(--primary-teal);
                                font-family: 'Inter', sans-serif;
                            ">5M+</div>
                            <div style="
                                font-size: 11px;
                                color: var(--gray-600);
                                font-weight: 600;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                            ">Users</div>
                        </div>
                    </div>

                    <!-- Benefits -->
                    <div style="margin-bottom: 30px;">
                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 12px;
                            margin-bottom: 15px;
                            padding: 12px;
                            background: #f0f9ff;
                            border-radius: 10px;
                            border-left: 3px solid var(--primary-teal);
                        ">
                            <div style="
                                width: 40px;
                                height: 40px;
                                background: linear-gradient(135deg, var(--primary-teal), #0891b2);
                                border-radius: 8px;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                                font-size: 16px;
                                flex-shrink: 0;
                            ">✓</div>
                            <div style="color: var(--gray-700); font-size: 14px; font-weight: 500;">
                                Access all premium career tools
                            </div>
                        </div>
                        
                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 12px;
                            margin-bottom: 15px;
                            padding: 12px;
                            background: #f0f9ff;
                            border-radius: 10px;
                            border-left: 3px solid var(--primary-teal);
                        ">
                            <div style="
                                width: 40px;
                                height: 40px;
                                background: linear-gradient(135deg, var(--primary-teal), #0891b2);
                                border-radius: 8px;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                                font-size: 16px;
                                flex-shrink: 0;
                            ">✓</div>
                            <div style="color: var(--gray-700); font-size: 14px; font-weight: 500;">
                                Apply to unlimited job positions
                            </div>
                        </div>
                        
                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 12px;
                            margin-bottom: 15px;
                            padding: 12px;
                            background: #f0f9ff;
                            border-radius: 10px;
                            border-left: 3px solid var(--primary-teal);
                        ">
                            <div style="
                                width: 40px;
                                height: 40px;
                                background: linear-gradient(135deg, var(--primary-teal), #0891b2);
                                border-radius: 8px;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                                font-size: 16px;
                                flex-shrink: 0;
                            ">✓</div>
                            <div style="color: var(--gray-700); font-size: 14px; font-weight: 500;">
                                Track applications & get job alerts
                            </div>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div style="display: flex; flex-direction: column; gap: 12px;">
                        <button onclick="goToRegister('${toolUrl}')" style="
                            background: linear-gradient(135deg, var(--primary-teal), #0891b2);
                            color: white;
                            border: none;
                            padding: 15px 25px;
                            border-radius: 12px;
                            font-size: 16px;
                            font-weight: 600;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            box-shadow: 0 4px 15px rgba(13, 148, 136, 0.2);
                            font-family: 'Inter', sans-serif;
                        " onmouseover="
                            this.style.transform='translateY(-2px)';
                            this.style.boxShadow='0 8px 25px rgba(13, 148, 136, 0.3)';
                        " onmouseout="
                            this.style.transform='translateY(0)';
                            this.style.boxShadow='0 4px 15px rgba(13, 148, 136, 0.2)';
                        ">
                            🚀 Create Free Account
                        </button>
                        
                        <button onclick="goToLogin('${toolUrl}')" style="
                            background: white;
                            color: var(--primary-teal);
                            border: 2px solid var(--primary-teal);
                            padding: 15px 25px;
                            border-radius: 12px;
                            font-size: 16px;
                            font-weight: 600;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            font-family: 'Inter', sans-serif;
                        " onmouseover="
                            this.style.background='var(--primary-teal)';
                            this.style.color='white';
                            this.style.transform='translateY(-1px)';
                        " onmouseout="
                            this.style.background='white';
                            this.style.color='var(--primary-teal)';
                            this.style.transform='translateY(0)';
                        ">
                            Already have an account? Login
                        </button>
                        
                        <button onclick="closeAuthModal()" style="
                            background: none;
                            border: none;
                            color: var(--gray-500);
                            font-size: 14px;
                            cursor: pointer;
                            padding: 12px;
                            transition: color 0.3s ease;
                            font-family: 'Inter', sans-serif;
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
                transform: translateY(50px) scale(0.95); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0) scale(1); 
            }
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

// Add fade out animation
const fadeOutStyle = document.createElement('style');
fadeOutStyle.textContent = `
    @keyframes modalFadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(fadeOutStyle);

console.log('✨ Beautiful SkillConnect Auth Modal Ready!');