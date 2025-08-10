// Динамические исправления для админ панели - Полная перезапись

document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin fixes loaded');
    applyFixes();
    applyMobileFixes();
    
    // Повторное применение через небольшую задержку
    setTimeout(function() {
        applyFixes();
        applyMobileFixes();
    }, 100);
    
    // Повторное применение после полной загрузки
    setTimeout(function() {
        applyFixes();
        applyMobileFixes();
    }, 500);
});

window.addEventListener('resize', function() {
    applyFixes();
    applyMobileFixes();
});

// Применение исправлений каждые 2 секунды для динамического контента
setInterval(function() {
    applyFixes();
    applyMobileFixes();
}, 2000);

function applyFixes() {
    console.log('Applying admin fixes...');
    
    // КРИТИЧЕСКИЕ исправления для основного контента
    const content = document.getElementById('content');
    if (content) {
        console.log('Fixing #content element');
        content.style.position = 'relative';
        content.style.left = '0';
        content.style.right = 'auto';
        content.style.top = 'auto';
        content.style.bottom = 'auto';
        content.style.transform = 'none';
        content.style.width = 'calc(100vw - 280px)';
        content.style.maxWidth = 'none';
        content.style.minWidth = 'calc(100vw - 280px)';
        content.style.marginLeft = '280px';
        content.style.marginRight = '0';
        content.style.marginTop = '70px';
        content.style.marginBottom = '0';
        content.style.padding = '2rem';
        content.style.boxSizing = 'border-box';
        content.style.display = 'block';
        content.style.float = 'none';
        content.style.clear = 'none';
    }

    // Принудительное исправление всех контейнеров
    const containers = document.querySelectorAll('.container-fluid');
    containers.forEach(function(element) {
        element.style.position = 'relative';
        element.style.left = '0';
        element.style.right = 'auto';
        element.style.top = 'auto';
        element.style.bottom = 'auto';
        element.style.transform = 'none';
        element.style.width = '100%';
        element.style.maxWidth = 'none';
        element.style.minWidth = '100%';
        element.style.padding = '0';
        element.style.margin = '0';
        element.style.boxSizing = 'border-box';
        element.style.display = 'block';
        element.style.float = 'none';
        element.style.clear = 'none';
    });

    // Принудительное исправление всех строк
    const rows = document.querySelectorAll('.row');
    rows.forEach(function(element) {
        element.style.position = 'relative';
        element.style.left = '0';
        element.style.right = 'auto';
        element.style.top = 'auto';
        element.style.bottom = 'auto';
        element.style.transform = 'none';
        element.style.width = '100%';
        element.style.maxWidth = 'none';
        element.style.minWidth = '100%';
        element.style.margin = '0';
        element.style.padding = '0';
        element.style.boxSizing = 'border-box';
        element.style.display = 'flex';
        element.style.flexWrap = 'wrap';
        element.style.float = 'none';
        element.style.clear = 'none';
    });

    // Исправления для всех колонок Bootstrap
    const columns = document.querySelectorAll('.col-1, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-10, .col-11, .col-12, .col-sm-1, .col-sm-2, .col-sm-3, .col-sm-4, .col-sm-5, .col-sm-6, .col-sm-7, .col-sm-8, .col-sm-9, .col-sm-10, .col-sm-11, .col-sm-12, .col-md-1, .col-md-2, .col-md-3, .col-md-4, .col-md-5, .col-md-6, .col-md-7, .col-md-8, .col-md-9, .col-md-10, .col-md-11, .col-md-12, .col-lg-1, .col-lg-2, .col-lg-3, .col-lg-4, .col-lg-5, .col-lg-6, .col-lg-7, .col-lg-8, .col-lg-9, .col-lg-10, .col-lg-11, .col-lg-12, .col-xl-1, .col-xl-2, .col-xl-3, .col-xl-4, .col-xl-5, .col-xl-6, .col-xl-7, .col-xl-8, .col-xl-9, .col-xl-10, .col-xl-11, .col-xl-12');
    columns.forEach(function(element) {
        element.style.position = 'relative';
        element.style.left = '0';
        element.style.right = 'auto';
        element.style.top = 'auto';
        element.style.bottom = 'auto';
        element.style.transform = 'none';
        element.style.boxSizing = 'border-box';
        element.style.padding = '0 1rem';
        element.style.margin = '0';
        element.style.float = 'none';
        element.style.clear = 'none';
    });

    // Исправления для карточек и других элементов
    const cards = document.querySelectorAll('.card, .card-body, .card-header, .card-footer');
    cards.forEach(function(element) {
        element.style.position = 'relative';
        element.style.left = '0';
        element.style.right = 'auto';
        element.style.top = 'auto';
        element.style.bottom = 'auto';
        element.style.transform = 'none';
        element.style.boxSizing = 'border-box';
        element.style.margin = '0';
        element.style.float = 'none';
        element.style.clear = 'none';
        
        if (element.classList.contains('card')) {
            element.style.width = '100%';
            element.style.maxWidth = 'none';
            element.style.minWidth = '100%';
            element.style.margin = '0 0 1rem 0';
        }
        
        if (element.classList.contains('card-body')) {
            element.style.width = '100%';
            element.style.maxWidth = 'none';
            element.style.minWidth = '100%';
        }
    });

    // Исправления для flexbox элементов
    const flexElements = document.querySelectorAll('.d-flex, .justify-content-between, .align-items-center');
    flexElements.forEach(function(element) {
        element.style.position = 'relative';
        element.style.left = '0';
        element.style.right = 'auto';
        element.style.top = 'auto';
        element.style.bottom = 'auto';
        element.style.transform = 'none';
        element.style.boxSizing = 'border-box';
        element.style.margin = '0';
        element.style.float = 'none';
        element.style.clear = 'none';
        element.style.width = '100%';
        element.style.maxWidth = 'none';
        element.style.minWidth = '100%';
        
        if (element.classList.contains('d-flex')) {
            element.style.display = 'flex';
        }
        
        if (element.classList.contains('justify-content-between')) {
            element.style.justifyContent = 'space-between';
        }
        
        if (element.classList.contains('align-items-center')) {
            element.style.alignItems = 'center';
        }
    });

    // Исправления для заголовков и кнопок
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6, .btn, .btn-group');
    headings.forEach(function(element) {
        element.style.position = 'relative';
        element.style.left = '0';
        element.style.right = 'auto';
        element.style.top = 'auto';
        element.style.bottom = 'auto';
        element.style.transform = 'none';
        element.style.boxSizing = 'border-box';
        element.style.margin = '0';
        element.style.float = 'none';
        element.style.clear = 'none';
    });

    // Исправления для всех остальных элементов
    const allElements = document.querySelectorAll('#content p, #content div, #content span, #content a');
    allElements.forEach(function(element) {
        element.style.position = 'relative';
        element.style.left = '0';
        element.style.right = 'auto';
        element.style.top = 'auto';
        element.style.bottom = 'auto';
        element.style.transform = 'none';
        element.style.boxSizing = 'border-box';
        element.style.margin = '0';
        element.style.float = 'none';
        element.style.clear = 'none';
    });

    // Принудительное удаление всех ограничений ширины
    const allContentElements = document.querySelectorAll('#content *');
    allContentElements.forEach(function(element) {
        element.style.maxWidth = 'none';
        element.style.boxSizing = 'border-box';
    });

    // Предотвращение горизонтального скролла
    document.documentElement.style.overflowX = 'hidden';
    document.body.style.overflowX = 'hidden';
    document.documentElement.style.boxSizing = 'border-box';
    document.body.style.boxSizing = 'border-box';
    document.documentElement.style.width = '100%';
    document.body.style.width = '100%';
    document.documentElement.style.maxWidth = 'none';
    document.body.style.maxWidth = 'none';
    document.documentElement.style.margin = '0';
    document.body.style.margin = '0';
    document.documentElement.style.padding = '0';
    document.body.style.padding = '0';
}

function applyMobileFixes() {
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        console.log('Applying mobile fixes...');
        
        const content = document.getElementById('content');
        if (content) {
            content.style.marginLeft = '0';
            content.style.width = '100vw';
            content.style.minWidth = '100vw';
            content.style.maxWidth = 'none';
            content.style.padding = '1rem';
        }

        const containers = document.querySelectorAll('.container-fluid, .row');
        containers.forEach(function(element) {
            element.style.width = '100%';
            element.style.maxWidth = 'none';
            element.style.minWidth = '100%';
            element.style.padding = '0';
            element.style.margin = '0';
            element.style.boxSizing = 'border-box';
        });

        const columns = document.querySelectorAll('.col-1, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-10, .col-11, .col-12, .col-sm-1, .col-sm-2, .col-sm-3, .col-sm-4, .col-sm-5, .col-sm-6, .col-sm-7, .col-sm-8, .col-sm-9, .col-sm-10, .col-sm-11, .col-sm-12, .col-md-1, .col-md-2, .col-md-3, .col-md-4, .col-md-5, .col-md-6, .col-md-7, .col-md-8, .col-md-9, .col-md-10, .col-md-11, .col-md-12, .col-lg-1, .col-lg-2, .col-lg-3, .col-lg-4, .col-lg-5, .col-lg-6, .col-lg-7, .col-lg-8, .col-lg-9, .col-lg-10, .col-lg-11, .col-lg-12, .col-xl-1, .col-xl-2, .col-xl-3, .col-xl-4, .col-xl-5, .col-xl-6, .col-xl-7, .col-xl-8, .col-xl-9, .col-xl-10, .col-xl-11, .col-xl-12');
        columns.forEach(function(element) {
            element.style.flex = '0 0 100%';
            element.style.maxWidth = '100%';
            element.style.width = '100%';
            element.style.padding = '0.5rem';
            element.style.marginBottom = '1rem';
        });
    }
}
