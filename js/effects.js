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
