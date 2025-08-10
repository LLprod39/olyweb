// Админка OlyWeb - Современный JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('Админка OlyWeb загружена!');

    // Инициализация всех компонентов
    initAnimations();
    initSidebar();
    initTables();
    initForms();
    initButtons();
    initModals();
    initTooltips();
    initSearch();
    initNotifications();
    initMobileMenu();

    // Анимации появления элементов
    function initAnimations() {
        const elements = document.querySelectorAll('.card, .module, .table, .alert');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('fade-in-up');
                    }, index * 50);
                }
            });
        }, { threshold: 0.1 });

        elements.forEach(el => observer.observe(el));
    }

    // Улучшенная боковая панель
    function initSidebar() {
        const sidebar = document.querySelector('#nav-sidebar');
        const sidebarLinks = document.querySelectorAll('#nav-sidebar .module a');
        
        if (!sidebar) return;

        // Подсветка активной ссылки
        const currentPath = window.location.pathname;
        sidebarLinks.forEach(link => {
            if (link.href && link.href.includes(currentPath)) {
                link.classList.add('active');
            }
        });

        // Плавная прокрутка в сайдбаре
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Добавляем индикатор загрузки
                const loadingIndicator = document.createElement('div');
                loadingIndicator.className = 'loading-indicator';
                loadingIndicator.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                loadingIndicator.style.cssText = `
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: var(--secondary-bg);
                    color: var(--text-primary);
                    padding: 1rem 2rem;
                    border-radius: var(--border-radius);
                    border: 1px solid var(--border-color);
                    z-index: 9999;
                    box-shadow: var(--shadow-lg);
                `;
                document.body.appendChild(loadingIndicator);

                // Убираем индикатор через 1 секунду
                setTimeout(() => {
                    if (loadingIndicator.parentNode) {
                        loadingIndicator.parentNode.removeChild(loadingIndicator);
                    }
                }, 1000);
            });
        });

        // Анимация при наведении на модули
        const modules = document.querySelectorAll('#nav-sidebar .module');
        modules.forEach(module => {
            module.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = 'var(--shadow-xl)';
            });
            
            module.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'var(--shadow-md)';
            });
        });
    }

    // Улучшенные таблицы
    function initTables() {
        const tables = document.querySelectorAll('.table, .results');
        
        tables.forEach(table => {
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                row.addEventListener('mouseenter', function() {
                    this.style.transform = 'scale(1.01)';
                    this.style.backgroundColor = 'var(--tertiary-bg)';
                });
                
                row.addEventListener('mouseleave', function() {
                    this.style.transform = 'scale(1)';
                    this.style.backgroundColor = '';
                });
            });

            // Добавляем возможность сортировки
            const headers = table.querySelectorAll('thead th');
            headers.forEach(header => {
                if (header.textContent.trim() && !header.querySelector('a')) {
                    header.style.cursor = 'pointer';
                    header.addEventListener('click', function() {
                        sortTable(table, Array.from(headers).indexOf(this));
                    });
                }
            });
        });
    }

    // Функция сортировки таблицы
    function sortTable(table, columnIndex) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.sort((a, b) => {
            const aText = a.cells[columnIndex]?.textContent.trim() || '';
            const bText = b.cells[columnIndex]?.textContent.trim() || '';
            return aText.localeCompare(bText, 'ru');
        });
        
        rows.forEach(row => tbody.appendChild(row));
    }

    // Улучшенные формы
    function initForms() {
        const forms = document.querySelectorAll('form');
        const inputs = document.querySelectorAll('input, textarea, select');
        
        // Анимация фокуса для полей ввода
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'translateY(-1px)';
                this.parentElement.style.boxShadow = 'var(--shadow-md)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'translateY(0)';
                this.parentElement.style.boxShadow = 'none';
            });
        });

        // Улучшенная отправка форм
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const submitButton = this.querySelector('input[type="submit"], button[type="submit"]');
                if (submitButton) {
                    const originalText = submitButton.value || submitButton.textContent;
                    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Сохранение...';
                    submitButton.disabled = true;
                    
                    // Восстанавливаем текст через 3 секунды (на случай ошибки)
                    setTimeout(() => {
                        if (submitButton.disabled) {
                            submitButton.innerHTML = originalText;
                            submitButton.disabled = false;
                        }
                    }, 3000);
                }
            });
        });
    }

    // Улучшенные кнопки
    function initButtons() {
        const buttons = document.querySelectorAll('.btn, .object-tools a, input[type="submit"]');
        
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-1px)';
                this.style.boxShadow = 'var(--shadow-lg)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '';
            });

            // Эффект нажатия
            button.addEventListener('mousedown', function() {
                this.style.transform = 'translateY(0)';
            });
            
            button.addEventListener('mouseup', function() {
                this.style.transform = 'translateY(-1px)';
            });
        });
    }

    // Улучшенные модальные окна
    function initModals() {
        const modals = document.querySelectorAll('.modal');
        
        modals.forEach(modal => {
            modal.addEventListener('show.bs.modal', function() {
                const content = this.querySelector('.modal-content');
                content.style.transform = 'scale(0.8)';
                content.style.opacity = '0';
            });
            
            modal.addEventListener('shown.bs.modal', function() {
                const content = this.querySelector('.modal-content');
                content.style.transition = 'all 0.3s ease';
                content.style.transform = 'scale(1)';
                content.style.opacity = '1';
            });
        });
    }

    // Улучшенные подсказки
    function initTooltips() {
        const tooltipElements = document.querySelectorAll('[title]');
        
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', function(e) {
                const tooltip = document.createElement('div');
                tooltip.className = 'custom-tooltip';
                tooltip.textContent = this.getAttribute('title');
                tooltip.style.cssText = `
                    position: absolute;
                    background: var(--tertiary-bg);
                    color: var(--text-primary);
                    padding: 0.5rem 1rem;
                    border-radius: var(--border-radius-sm);
                    border: 1px solid var(--border-color);
                    box-shadow: var(--shadow-lg);
                    z-index: 1000;
                    font-size: 0.875rem;
                    pointer-events: none;
                    max-width: 200px;
                    word-wrap: break-word;
                `;
                
                document.body.appendChild(tooltip);
                
                const rect = this.getBoundingClientRect();
                tooltip.style.left = rect.left + 'px';
                tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
                
                this.addEventListener('mouseleave', function() {
                    if (tooltip.parentNode) {
                        tooltip.parentNode.removeChild(tooltip);
                    }
                }, { once: true });
            });
        });
    }

    // Улучшенный поиск
    function initSearch() {
        const searchInputs = document.querySelectorAll('input[type="search"], .search-input');
        
        searchInputs.forEach(input => {
            input.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                const table = this.closest('.content').querySelector('.table, .results');
                
                if (table) {
                    const rows = table.querySelectorAll('tbody tr');
                    rows.forEach(row => {
                        const text = row.textContent.toLowerCase();
                        if (text.includes(searchTerm)) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    });
                }
            });
        });
    }

    // Улучшенные уведомления
    function initNotifications() {
        const alerts = document.querySelectorAll('.alert, .messagelist li');
        
        alerts.forEach(alert => {
            // Добавляем иконку к алертам
            if (!alert.querySelector('i')) {
                const icon = document.createElement('i');
                icon.className = 'fas fa-info-circle me-2';
                alert.insertBefore(icon, alert.firstChild);
            }
            
            // Анимация появления
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            
            setTimeout(() => {
                alert.style.transition = 'all 0.3s ease';
                alert.style.opacity = '1';
                alert.style.transform = 'translateY(0)';
            }, 100);

            // Автоматическое скрытие через 5 секунд
            setTimeout(() => {
                alert.style.transition = 'all 0.3s ease';
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 300);
            }, 5000);
        });
    }

    // Мобильное меню
    function initMobileMenu() {
        const sidebar = document.querySelector('#nav-sidebar');
        const toggleButton = document.createElement('button');
        toggleButton.innerHTML = '<i class="fas fa-bars"></i>';
        toggleButton.className = 'mobile-menu-toggle';
        toggleButton.style.cssText = `
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 1001;
            background: var(--gradient-primary);
            color: var(--text-inverse);
            border: none;
            border-radius: var(--border-radius-sm);
            padding: 0.75rem;
            cursor: pointer;
            display: none;
            box-shadow: var(--shadow-lg);
        `;

        document.body.appendChild(toggleButton);

        toggleButton.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            this.innerHTML = sidebar.classList.contains('show') ? 
                '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
        });

        // Показываем кнопку только на мобильных устройствах
        function checkMobile() {
            if (window.innerWidth <= 768) {
                toggleButton.style.display = 'block';
            } else {
                toggleButton.style.display = 'none';
                sidebar.classList.remove('show');
            }
        }

        window.addEventListener('resize', checkMobile);
        checkMobile();

        // Закрываем меню при клике вне его
        document.addEventListener('click', function(e) {
            if (!sidebar.contains(e.target) && !toggleButton.contains(e.target)) {
                sidebar.classList.remove('show');
                toggleButton.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });
    }

    // Добавляем индикатор загрузки для всех ссылок
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'A' && e.target.href && !e.target.href.includes('#')) {
            const loadingOverlay = document.createElement('div');
            loadingOverlay.className = 'loading-overlay';
            loadingOverlay.innerHTML = `
                <div class="loading-spinner">
                    <i class="fas fa-spinner fa-spin"></i>
                    <p>Загрузка...</p>
                </div>
            `;
            loadingOverlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
            `;
            
            const spinner = loadingOverlay.querySelector('.loading-spinner');
            spinner.style.cssText = `
                background: var(--secondary-bg);
                color: var(--text-primary);
                padding: 2rem;
                border-radius: var(--border-radius);
                text-align: center;
                border: 1px solid var(--border-color);
                box-shadow: var(--shadow-xl);
            `;
            
            document.body.appendChild(loadingOverlay);
            
            // Убираем оверлей через 2 секунды
            setTimeout(() => {
                if (loadingOverlay.parentNode) {
                    loadingOverlay.parentNode.removeChild(loadingOverlay);
                }
            }, 2000);
        }
    });

    // Добавляем горячие клавиши
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K для поиска
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], .search-input');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape для закрытия модальных окон
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const closeButton = modal.querySelector('.btn-close, [data-bs-dismiss="modal"]');
                if (closeButton) {
                    closeButton.click();
                }
            });
        }
    });

    // Добавляем анимацию для статистических карточек
    const statCards = document.querySelectorAll('.border-left-primary, .border-left-success, .border-left-info, .border-left-warning');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
            this.style.boxShadow = 'var(--shadow-xl)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'var(--shadow-md)';
        });
    });

    // Добавляем анимацию для иконок
    const icons = document.querySelectorAll('.fas, .far, .fab');
    icons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.color = 'var(--accent-primary)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.color = '';
        });
    });

    // Добавляем контекстное меню для таблиц
    const tables = document.querySelectorAll('.table, .results');
    tables.forEach(table => {
        table.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            
            const contextMenu = document.createElement('div');
            contextMenu.className = 'context-menu';
            contextMenu.innerHTML = `
                <div class="context-menu-item" data-action="copy">Копировать</div>
                <div class="context-menu-item" data-action="export">Экспорт</div>
                <div class="context-menu-item" data-action="print">Печать</div>
            `;
            contextMenu.style.cssText = `
                position: fixed;
                background: var(--secondary-bg);
                border: 1px solid var(--border-color);
                border-radius: var(--border-radius-sm);
                padding: 0.5rem 0;
                z-index: 1000;
                box-shadow: var(--shadow-lg);
                min-width: 150px;
            `;
            
            contextMenu.style.left = e.pageX + 'px';
            contextMenu.style.top = e.pageY + 'px';
            
            document.body.appendChild(contextMenu);
            
            // Убираем контекстное меню при клике
            document.addEventListener('click', function() {
                if (contextMenu.parentNode) {
                    contextMenu.parentNode.removeChild(contextMenu);
                }
            }, { once: true });
        });
    });

    console.log('Все компоненты админки инициализированы!');
});
