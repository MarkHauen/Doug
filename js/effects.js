// Subtle visual effects for the DOUG website

document.addEventListener('DOMContentLoaded', () => {
    // Typing effect for tagline
    initTypingEffect();
    
    // Random glitch effect
    initGlitchEffect();
    
    // Parallax on hero portal
    initParallax();
    
    // Smooth scroll for anchor links
    initSmoothScroll();
    
    // Reading settings (font/size)
    initReadingSettings();
});

// Typing effect
function initTypingEffect() {
    const typingElement = document.querySelector('.typing-text');
    if (!typingElement) return;
    
    const text = typingElement.textContent;
    typingElement.textContent = '';
    
    let i = 0;
    const typeSpeed = 50;
    
    function type() {
        if (i < text.length) {
            typingElement.textContent += text.charAt(i);
            i++;
            setTimeout(type, typeSpeed);
        }
    }
    
    // Start typing after a short delay
    setTimeout(type, 1000);
}

// Random glitch effect on title
function initGlitchEffect() {
    const glitchElements = document.querySelectorAll('.glitch');
    
    glitchElements.forEach(element => {
        setInterval(() => {
            if (Math.random() > 0.95) {
                element.style.animation = 'none';
                element.offsetHeight; // Trigger reflow
                element.style.animation = null;
            }
        }, 100);
    });
}

// Parallax effect for portal rings
function initParallax() {
    const portal = document.querySelector('.hell-portal');
    if (!portal) return;
    
    document.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth / 2 - e.clientX) / 50;
        const y = (window.innerHeight / 2 - e.clientY) / 50;
        
        portal.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
    });
}

// Smooth scroll
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Add some random flicker to status values
function initStatusFlicker() {
    const statValues = document.querySelectorAll('.stat-value');
    
    statValues.forEach(stat => {
        setInterval(() => {
            if (Math.random() > 0.9) {
                stat.style.opacity = '0.5';
                setTimeout(() => {
                    stat.style.opacity = '1';
                }, 50);
            }
        }, 200);
    });
}

// Initialize status flicker
initStatusFlicker();

// Hamburger menu functionality
function initNavMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navOverlay = document.querySelector('.nav-overlay');
    
    if (!navToggle || !navMenu) return;
    
    function toggleMenu() {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        if (navOverlay) navOverlay.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    }
    
    function closeMenu() {
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
        if (navOverlay) navOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    navToggle.addEventListener('click', toggleMenu);
    if (navOverlay) navOverlay.addEventListener('click', closeMenu);
    
    // Close menu when clicking a link
    navMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMenu);
    });
    
    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            closeMenu();
        }
    });
}

// Initialize nav menu
initNavMenu();

// Initialize reading settings
initReadingSettings();

// Reading settings (font family and size)
function initReadingSettings() {
    const storyText = document.querySelector('.story-text');
    const settingsContainer = document.querySelector('.reading-settings');
    
    if (!storyText || !settingsContainer) return;
    
    // Load saved preferences
    const savedFont = localStorage.getItem('doug-reading-font') || 'serif';
    const savedSize = localStorage.getItem('doug-reading-size') || 'medium';
    
    // Apply saved preferences
    applyFont(savedFont);
    applySize(savedSize);
    
    // Set active buttons
    updateActiveButtons('font', savedFont);
    updateActiveButtons('size', savedSize);
    
    // Font buttons
    settingsContainer.querySelectorAll('.setting-btn[data-font]').forEach(btn => {
        btn.addEventListener('click', () => {
            const font = btn.dataset.font;
            applyFont(font);
            updateActiveButtons('font', font);
            localStorage.setItem('doug-reading-font', font);
        });
    });
    
    // Size buttons
    settingsContainer.querySelectorAll('.setting-btn[data-size]').forEach(btn => {
        btn.addEventListener('click', () => {
            const size = btn.dataset.size;
            applySize(size);
            updateActiveButtons('size', size);
            localStorage.setItem('doug-reading-size', size);
        });
    });
    
    function applyFont(font) {
        storyText.classList.remove('font-serif', 'font-sans', 'font-mono', 'font-modern');
        storyText.classList.add(`font-${font}`);
    }
    
    function applySize(size) {
        storyText.classList.remove('size-small', 'size-medium', 'size-large');
        storyText.classList.add(`size-${size}`);
    }
    
    function updateActiveButtons(type, value) {
        const attr = type === 'font' ? 'data-font' : 'data-size';
        settingsContainer.querySelectorAll(`.setting-btn[${attr}]`).forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute(attr) === value);
        });
    }
}

// Console easter egg
console.log(`
%c██╗  ██╗███████╗██╗     ██╗         ██╗███╗   ██╗ ██████╗
%c██║  ██║██╔════╝██║     ██║         ██║████╗  ██║██╔════╝
%c███████║█████╗  ██║     ██║         ██║██╔██╗ ██║██║     
%c██╔══██║██╔══╝  ██║     ██║         ██║██║╚██╗██║██║     
%c██║  ██║███████╗███████╗███████╗    ██║██║ ╚████║╚██████╗
%c╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝    ╚═╝╚═╝  ╚═══╝ ╚═════╝

%cWelcome to Hell Inc. Your soul has been logged.
Employee Handbook Section 2.1: Debugging in Hell voids your warranty.
`, 
'color: #ff2a2a', 
'color: #ff4444', 
'color: #ff6b35', 
'color: #f7931e', 
'color: #ff6b35', 
'color: #ff4444',
'color: #00ffff; font-style: italic;'
);

