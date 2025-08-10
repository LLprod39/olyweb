// Мобильные улучшения для Evall Clan

document.addEventListener('DOMContentLoaded', function() {
    
    // Улучшение навигации для мобильных устройств
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Закрытие меню при клике на ссылку
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    navbarCollapse.classList.remove('show');
                }
            });
        });
    }
    
    // Улучшение форм для мобильных устройств
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(control => {
        // Увеличение размера шрифта при фокусе на мобильных
        control.addEventListener('focus', function() {
            if (window.innerWidth <= 768) {
                this.style.fontSize = '16px'; // Предотвращает зум на iOS
            }
        });
        
        // Возврат к нормальному размеру при потере фокуса
        control.addEventListener('blur', function() {
            if (window.innerWidth <= 768) {
                this.style.fontSize = '';
            }
        });
    });
    
    // Улучшение кнопок для touch устройств
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        // Добавление активного состояния для touch
        button.addEventListener('touchstart', function() {
            this.classList.add('active');
        });
        
        button.addEventListener('touchend', function() {
            this.classList.remove('active');
        });
        
        // Предотвращение двойного клика
        button.addEventListener('click', function(e) {
            if (this.classList.contains('disabled')) {
                e.preventDefault();
                return;
            }
            
            this.classList.add('disabled');
            setTimeout(() => {
                this.classList.remove('disabled');
            }, 1000);
        });
    });
    
    // Улучшение карточек для мобильных
    const cards = document.querySelectorAll('.card, .news-card, .stats-card');
    cards.forEach(card => {
        // Добавление haptic feedback для touch устройств
        card.addEventListener('touchstart', function() {
            if ('vibrate' in navigator) {
                navigator.vibrate(10);
            }
        });
    });
    
    // Улучшение поиска для мобильных
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        // Автофокус на поиск при открытии на мобильных
        if (window.innerWidth <= 768) {
            searchInput.addEventListener('focus', function() {
                setTimeout(() => {
                    this.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 300);
            });
        }
    }
    
    // Улучшение пагинации для мобильных
    const paginationLinks = document.querySelectorAll('.pagination-btn');
    paginationLinks.forEach(link => {
        link.addEventListener('touchstart', function() {
            if ('vibrate' in navigator) {
                navigator.vibrate(5);
            }
        });
    });
    
    // Обработка изменения ориентации экрана
    window.addEventListener('orientationchange', function() {
        setTimeout(() => {
            window.dispatchEvent(new Event('resize'));
        }, 100);
    });
    
    // Обработка изменения размера окна
    window.addEventListener('resize', function() {
        const isMobile = window.innerWidth <= 768;
        document.body.classList.toggle('mobile', isMobile);
        document.body.classList.toggle('desktop', !isMobile);
    });
    
    // Инициализация мобильного состояния
    const isMobile = window.innerWidth <= 768;
    document.body.classList.toggle('mobile', isMobile);
    document.body.classList.toggle('desktop', !isMobile);
    
    console.log('Мобильные улучшения загружены для Evall Clan');
}); 