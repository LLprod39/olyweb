// Main site scripts from base.html
document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов
    const elements = document.querySelectorAll('.card, .stats-card, .news-card');
    elements.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('fade-in-up');
        }, index * 100);
    });

    // Анимация для секций
    const sections = document.querySelectorAll('section');
    sections.forEach((section, index) => {
        if (index % 2 === 0) {
            section.classList.add('slide-in-left');
        } else {
            section.classList.add('slide-in-right');
        }
    });

    // Плавная прокрутка для якорных ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Анимация при скролле
    function animateOnScroll() {
        const elements = document.querySelectorAll('.card, .stats-card, .news-card');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;

            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('fade-in-up');
            }
        });
    }

    window.addEventListener('scroll', animateOnScroll);

    // Создание плавающих элементов
    function createFloatingElements() {
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            const floatingContainer = document.createElement('div');
            floatingContainer.className = 'floating-elements';

            for (let i = 0; i < 5; i++) {
                const element = document.createElement('div');
                element.className = 'floating-element';
                element.innerHTML = ['⚔️', '🛡️', '👑', '⚜️', '🔮'][i];
                element.style.left = Math.random() * 100 + '%';
                element.style.top = Math.random() * 100 + '%';
                element.style.animationDelay = Math.random() * 2 + 's';
                element.style.fontSize = (Math.random() * 2 + 1) + 'rem';
                floatingContainer.appendChild(element);
            }

            heroSection.appendChild(floatingContainer);
        }
    }

    createFloatingElements();

    // Mobile scripts from mobile.js
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler && navbarCollapse) {
        // Закрытие меню при клике на ссылку
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 992) { // Bootstrap's lg breakpoint
                    navbarCollapse.classList.remove('show');
                }
            });
        });
    }

    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(control => {
        control.addEventListener('focus', function() {
            if (window.innerWidth <= 768) {
                this.style.fontSize = '16px'; // Prevents zoom on iOS
            }
        });

        control.addEventListener('blur', function() {
            if (window.innerWidth <= 768) {
                this.style.fontSize = '';
            }
        });
    });

    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('touchstart', function() {
            this.classList.add('active');
        }, { passive: true });

        button.addEventListener('touchend', function() {
            this.classList.remove('active');
        }, { passive: true });
    });

    console.log('Main site JS loaded');
});
