// JavaScript для темной темы админ панели OlyWeb

document.addEventListener('DOMContentLoaded', function() {
    // Добавляем плавные переходы для всех элементов
    const style = document.createElement('style');
    style.textContent = `
        * {
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }
    `;
    document.head.appendChild(style);

    // Улучшаем интерактивность карточек
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Улучшаем кнопки
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Добавляем анимацию для статистических карточек
    const statCards = document.querySelectorAll('.border-left-primary, .border-left-success, .border-left-info, .border-left-warning');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Улучшаем таблицы
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Добавляем подсветку активных элементов
    const activeElements = document.querySelectorAll('.active, .current-app, .current-model');
    activeElements.forEach(element => {
        element.style.boxShadow = '0 0 0 2px rgba(99, 102, 241, 0.3)';
    });

    // Улучшаем формы
    const formControls = document.querySelectorAll('.form-control, .form-select');
    formControls.forEach(control => {
        control.addEventListener('focus', function() {
            this.style.boxShadow = '0 0 0 3px rgba(99, 102, 241, 0.2)';
        });
        
        control.addEventListener('blur', function() {
            this.style.boxShadow = 'none';
        });
    });

    // Добавляем анимацию загрузки
    const loadingAnimation = `
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .loading {
            animation: pulse 2s infinite;
        }
    `;
    
    const loadingStyle = document.createElement('style');
    loadingStyle.textContent = loadingAnimation;
    document.head.appendChild(loadingStyle);

    // Улучшаем уведомления
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Добавляем кнопку закрытия
        if (!alert.querySelector('.close')) {
            const closeBtn = document.createElement('button');
            closeBtn.type = 'button';
            closeBtn.className = 'btn-close btn-close-white';
            closeBtn.setAttribute('data-bs-dismiss', 'alert');
            closeBtn.setAttribute('aria-label', 'Close');
            alert.appendChild(closeBtn);
        }
    });

    // Добавляем плавную прокрутку
    const smoothScroll = document.createElement('style');
    smoothScroll.textContent = `
        html {
            scroll-behavior: smooth;
        }
    `;
    document.head.appendChild(smoothScroll);

    // Улучшаем модальные окна
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            this.style.animation = 'fadeIn 0.3s ease-out';
        });
    });

    // Добавляем подсветку для важных элементов
    const importantElements = document.querySelectorAll('.text-danger, .text-warning');
    importantElements.forEach(element => {
        element.style.fontWeight = '600';
    });

    // Улучшаем навигацию
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(4px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });

    // Добавляем индикатор загрузки для форм
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('input[type="submit"], button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Отправка...';
            }
        });
    });

    // Улучшаем пагинацию
    const paginationLinks = document.querySelectorAll('.page-link');
    paginationLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Добавляем тултипы для иконок
    const icons = document.querySelectorAll('.fas, .far, .fab');
    icons.forEach(icon => {
        if (icon.title) {
            icon.style.cursor = 'help';
        }
    });

    // Улучшаем фильтры
    const filters = document.querySelectorAll('.filter');
    filters.forEach(filter => {
        filter.addEventListener('mouseenter', function() {
            this.style.borderColor = 'var(--primary)';
        });
        
        filter.addEventListener('mouseleave', function() {
            this.style.borderColor = 'var(--dark-border)';
        });
    });

    console.log('Темная тема админ панели OlyWeb загружена успешно!');
});
