// Cyberpunk Enhanced Interactions
class CyberpunkUI {
    constructor() {
        this.init();
    }

    init() {
        this.createMatrixRain();
        this.initParticleEffects();
        this.initGlitchEffects();
        this.initSoundEffects();
        this.initAdvancedAnimations();
        this.initSecurityMonitoring();
    }

    // Matrix Rain Effect
    createMatrixRain() {
        const matrixContainer = document.createElement('div');
        matrixContainer.className = 'matrix-rain';
        document.body.appendChild(matrixContainer);

        const columns = Math.floor(window.innerWidth / 20);
        for (let i = 0; i < columns; i++) {
            const column = document.createElement('div');
            column.className = 'matrix-column';
            column.style.left = (i * 20) + 'px';
            column.style.animationDuration = (5 + Math.random() * 10) + 's';
            column.style.animationDelay = Math.random() * 5 + 's';
            
            // Generate random characters
            const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
            let text = '';
            for (let j = 0; j < 20; j++) {
                text += chars[Math.floor(Math.random() * chars.length)] + '<br>';
            }
            column.innerHTML = text;
            
            matrixContainer.appendChild(column);
        }
    }

    // Enhanced Particle System
    initParticleEffects() {
        const particlesContainer = document.getElementById('particles');
        
        // Interactive particles that follow mouse
        document.addEventListener('mousemove', (e) => {
            if (Math.random() > 0.95) {
                this.createInteractiveParticle(e.clientX, e.clientY);
            }
        });

        // Create data fragments
        setInterval(() => {
            this.createDataFragment();
        }, 2000);
    }

    createInteractiveParticle(x, y) {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = '4px';
        particle.style.height = '4px';
        particle.style.background = 'var(--electric-cyan)';
        particle.style.borderRadius = '50%';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '9999';
        particle.style.boxShadow = '0 0 10px var(--electric-cyan)';
        
        document.body.appendChild(particle);
        
        // Animate particle
        const angle = Math.random() * Math.PI * 2;
        const velocity = 2 + Math.random() * 3;
        let opacity = 1;
        
        const animate = () => {
            const currentX = parseFloat(particle.style.left);
            const currentY = parseFloat(particle.style.top);
            
            particle.style.left = (currentX + Math.cos(angle) * velocity) + 'px';
            particle.style.top = (currentY + Math.sin(angle) * velocity) + 'px';
            opacity -= 0.02;
            particle.style.opacity = opacity;
            
            if (opacity > 0) {
                requestAnimationFrame(animate);
            } else {
                particle.remove();
            }
        };
        
        requestAnimationFrame(animate);
    }

    createDataFragment() {
        const fragment = document.createElement('div');
        fragment.style.position = 'fixed';
        fragment.style.left = Math.random() * window.innerWidth + 'px';
        fragment.style.top = '-20px';
        fragment.style.color = 'var(--neon-green)';
        fragment.style.fontFamily = "'Share Tech Mono', monospace";
        fragment.style.fontSize = '12px';
        fragment.style.pointerEvents = 'none';
        fragment.style.zIndex = '1';
        fragment.style.opacity = '0.7';
        fragment.textContent = Math.random() > 0.5 ? '█' : '▓';
        
        document.body.appendChild(fragment);
        
        // Animate falling
        let y = -20;
        const fall = () => {
            y += 2;
            fragment.style.top = y + 'px';
            
            if (y < window.innerHeight) {
                requestAnimationFrame(fall);
            } else {
                fragment.remove();
            }
        };
        
        requestAnimationFrame(fall);
    }

    // Glitch Effects
    initGlitchEffects() {
        // Random glitch on navigation items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('mouseenter', () => {
                if (Math.random() > 0.8) {
                    this.triggerGlitch(item);
                }
            });
        });

        // Glitch on system errors
        window.addEventListener('error', () => {
            this.triggerGlobalGlitch();
        });
    }

    triggerGlitch(element) {
        element.classList.add('glitch');
        element.setAttribute('data-text', element.textContent);
        
        setTimeout(() => {
            element.classList.remove('glitch');
        }, 500);
    }

    triggerGlobalGlitch() {
        document.body.style.animation = 'glitch 0.3s ease';
        
        setTimeout(() => {
            document.body.style.animation = '';
        }, 300);
    }

    // Sound Effects
    initSoundEffects() {
        // Create audio context for sound effects
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Sound effects mapping
        this.sounds = {
            connect: () => this.playTone(800, 0.1),
            message: () => this.playTone(600, 0.05),
            error: () => this.playTone(200, 0.2),
            success: () => this.playTone(1000, 0.1)
        };
    }

    playTone(frequency, duration) {
        if (!this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }

    // Advanced Animations
    initAdvancedAnimations() {
        // Breathing glow on active elements
        document.querySelectorAll('.status-dot, .lock-icon').forEach(element => {
            element.classList.add('breathing-glow');
        });

        // Scanline effects
        document.querySelectorAll('.message-bubble').forEach(bubble => {
            bubble.classList.add('scanlines');
        });

        // Holographic panels
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.add('holographic');
        });
    }

    // Security Monitoring
    initSecurityMonitoring() {
        this.securityLevel = 100;
        this.threatLevel = 0;
        
        // Simulate security monitoring
        setInterval(() => {
            this.updateSecurityStatus();
        }, 5000);

        // Monitor connection quality
        this.monitorConnection();
    }

    updateSecurityStatus() {
        // Random security events
        const events = [
            { type: 'scan', message: 'Security scan completed' },
            { type: 'encrypt', message: 'Encryption key rotated' },
            { type: 'verify', message: 'Identity verified' },
            { type: 'monitor', message: 'Network monitoring active' }
        ];

        const event = events[Math.floor(Math.random() * events.length)];
        this.logSecurityEvent(event);
    }

    logSecurityEvent(event) {
        console.log(`[SECURITY] ${event.message}`);
        
        // Update security indicators
        const indicators = document.querySelectorAll('.security-badge');
        indicators.forEach(indicator => {
            indicator.classList.add('notification-pulse');
            setTimeout(() => {
                indicator.classList.remove('notification-pulse');
            }, 2000);
        });
    }

    monitorConnection() {
        // Monitor connection quality
        setInterval(() => {
            const quality = Math.random() * 100;
            this.updateConnectionQuality(quality);
        }, 3000);
    }

    updateConnectionQuality(quality) {
        const statusElement = document.querySelector('.status-indicator span:last-child');
        if (statusElement) {
            if (quality > 80) {
                statusElement.textContent = 'Signal: Strong';
            } else if (quality > 50) {
                statusElement.textContent = 'Signal: Medium';
            } else {
                statusElement.textContent = 'Signal: Weak';
            }
        }
    }

    // Enhanced Message Effects
    enhanceMessage(messageElement) {
        // Add typing effect
        const content = messageElement.querySelector('.message-content');
        if (content) {
            this.typewriterEffect(content);
        }

        // Add send animation
        messageElement.classList.add('data-stream');
        
        // Play sound effect
        this.sounds.message();
    }

    typewriterEffect(element) {
        const text = element.textContent;
        element.textContent = '';
        let index = 0;

        const type = () => {
            if (index < text.length) {
                element.textContent += text[index];
                index++;
                setTimeout(type, 20 + Math.random() * 30);
            }
        };

        type();
    }

    // Loading States
    showLoadingState(element) {
        const loader = document.createElement('div');
        loader.className = 'loading-hex';
        loader.style.position = 'absolute';
        loader.style.top = '50%';
        loader.style.left = '50%';
        loader.style.transform = 'translate(-50%, -50%)';
        
        element.style.position = 'relative';
        element.appendChild(loader);
    }

    hideLoadingState(element) {
        const loader = element.querySelector('.loading-hex');
        if (loader) {
            loader.remove();
        }
    }

    // Notification System
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid var(--neon-green);
            border-radius: 8px;
            color: var(--text-primary);
            font-family: 'Share Tech Mono', monospace;
            font-size: 12px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Auto remove
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Terminal Commands
    initTerminal() {
        const terminal = document.createElement('div');
        terminal.className = 'data-terminal';
        terminal.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            width: 300px;
            height: 200px;
            z-index: 1000;
            display: none;
        `;
        
        terminal.innerHTML = `
            <div style="margin-bottom: 10px; color: var(--neon-green);">SECURE TERMINAL v2.0</div>
            <div id="terminalOutput" style="height: 150px; overflow-y: auto; margin-bottom: 10px;"></div>
            <input type="text" id="terminalInput" style="width: 100%; background: transparent; border: none; color: var(--neon-green); outline: none;" placeholder="Enter command...">
        `;
        
        document.body.appendChild(terminal);
        
        // Terminal toggle (Ctrl+`)
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === '`') {
                terminal.style.display = terminal.style.display === 'none' ? 'block' : 'none';
                if (terminal.style.display === 'block') {
                    document.getElementById('terminalInput').focus();
                }
            }
        });
        
        // Terminal command handling
        const terminalInput = document.getElementById('terminalInput');
        const terminalOutput = document.getElementById('terminalOutput');
        
        terminalInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const command = terminalInput.value;
                this.executeTerminalCommand(command, terminalOutput);
                terminalInput.value = '';
            }
        });
    }

    executeTerminalCommand(command, output) {
        const commands = {
            'help': () => 'Available commands: help, status, clear, security, connections',
            'status': () => 'System: ONLINE | Security: ENCRYPTED | Connection: STABLE',
            'clear': () => { output.innerHTML = ''; return ''; },
            'security': () => `Security Level: ${this.securityLevel}% | Threat Level: ${this.threatLevel}`,
            'connections': () => `Active Connections: ${Object.keys(activeUsers || {}).length}`
        };
        
        const outputDiv = document.createElement('div');
        outputDiv.style.marginBottom = '5px';
        outputDiv.innerHTML = `<span style="color: var(--terminal-amber);">$</span> ${command}`;
        
        const response = commands[command.toLowerCase()];
        if (response) {
            const responseDiv = document.createElement('div');
            responseDiv.style.marginBottom = '5px';
            responseDiv.style.color = 'var(--neon-green)';
            responseDiv.textContent = response();
            output.appendChild(responseDiv);
        }
        
        output.appendChild(outputDiv);
        output.scrollTop = output.scrollHeight;
    }
}

// Initialize Cyberpunk UI
let cyberpunkUI;

// Enhanced Socket.IO Integration
class CyberpunkChat {
    constructor() {
        this.socket = io();
        this.currentUser = null;
        this.currentPartner = null;
        this.cyberpunkUI = null;
        this.init();
    }

    init() {
        this.cyberpunkUI = new CyberpunkUI();
        this.setupEventListeners();
        this.setupSocketEvents();
    }

    setupEventListeners() {
        // Enhanced login
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin();
            });
        }

        // Enhanced message sending
        const sendButton = document.getElementById('sendButton');
        const messageInput = document.getElementById('messageInput');
        
        if (sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
        }
        
        if (messageInput) {
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendMessage();
                }
            });
        }

        // Navigation enhancements
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', () => {
                this.handleNavigation(item.dataset.section);
            });
        });
    }

    setupSocketEvents() {
        this.socket.on('connect', () => {
            this.cyberpunkUI.sounds.connect();
            this.cyberpunkUI.showNotification('Connected to secure network', 'success');
        });

        this.socket.on('login_success', (data) => {
            this.currentUser = data.username;
            this.cyberpunkUI.sounds.success();
            this.transitionToMainInterface();
        });

        this.socket.on('login_error', (data) => {
            this.cyberpunkUI.sounds.error();
            this.cyberpunkUI.showNotification('Access denied: ' + data.message, 'error');
            this.triggerErrorState();
        });

        this.socket.on('receive_message', (data) => {
            this.displayEnhancedMessage(data);
            this.cyberpunkUI.sounds.message();
        });
    }

    handleLogin() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        if (username && password) {
            this.cyberpunkUI.showLoadingState(document.querySelector('.login-container'));
            
            this.socket.emit('login', { username, password });
            
            setTimeout(() => {
                this.cyberpunkUI.hideLoadingState(document.querySelector('.login-container'));
            }, 1000);
        }
    }

    sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (message && this.currentUser && this.currentPartner) {
            // Add loading state
            this.cyberpunkUI.showLoadingState(messageInput);
            
            this.socket.emit('send_message', {
                sender: this.currentUser,
                receiver: this.currentPartner,
                message: message
            });
            
            messageInput.value = '';
            this.cyberpunkUI.hideLoadingState(messageInput);
        }
    }

    displayEnhancedMessage(data) {
        const messagesArea = document.getElementById('messagesArea');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${data.sender === this.currentUser ? 'buyer' : (data.is_ai ? 'ai' : 'seller')}`;
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        
        const senderDiv = document.createElement('div');
        senderDiv.className = 'message-sender';
        senderDiv.textContent = data.sender + (data.is_ai ? ' [AI]' : '');
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = data.message;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString();
        
        bubbleDiv.appendChild(senderDiv);
        bubbleDiv.appendChild(contentDiv);
        bubbleDiv.appendChild(timeDiv);
        messageDiv.appendChild(bubbleDiv);
        
        messagesArea.appendChild(messageDiv);
        messagesArea.scrollTop = messagesArea.scrollHeight;
        
        // Enhance with cyberpunk effects
        this.cyberpunkUI.enhanceMessage(messageDiv);
    }

    transitionToMainInterface() {
        const loginModal = document.getElementById('loginModal');
        const mainInterface = document.getElementById('mainInterface');
        
        loginModal.style.animation = 'fadeOut 0.5s ease';
        
        setTimeout(() => {
            loginModal.classList.add('hidden');
            mainInterface.classList.remove('hidden');
            mainInterface.style.animation = 'fadeIn 0.5s ease';
            
            this.loadContacts();
            this.cyberpunkUI.initTerminal();
        }, 500);
    }

    loadContacts() {
        const userRole = this.currentUser.startsWith('buyer') ? 'seller' : 'buyer';
        
        fetch(`/api/contacts/${userRole}`)
            .then(response => response.json())
            .then(data => {
                this.displayContacts(data.users);
            })
            .catch(error => {
                this.cyberpunkUI.showNotification('Failed to load contacts', 'error');
            });
    }

    displayContacts(users) {
        if (users.length > 0) {
            this.currentPartner = users[0];
            document.getElementById('chatPartner').textContent = this.currentPartner;
            
            // Enable input
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            if (messageInput) messageInput.disabled = false;
            if (sendButton) sendButton.disabled = false;
            
            // Join chat room
            this.socket.emit('join_chat', {
                username: this.currentUser,
                partner: this.currentPartner
            });
        }
    }

    handleNavigation(section) {
        this.cyberpunkUI.showNotification(`Navigating to ${section}`, 'info');
        
        // Add navigation animations
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');
    }

    triggerErrorState() {
        const loginContainer = document.querySelector('.login-container');
        loginContainer.classList.add('error-state');
        
        setTimeout(() => {
            loginContainer.classList.remove('error-state');
        }, 500);
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new CyberpunkChat();
});
