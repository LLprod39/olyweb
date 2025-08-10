document.addEventListener('DOMContentLoaded', function() {
    console.log('OlyWeb Admin JS Initialized');

    // This script is intentionally kept minimal to avoid conflicts with Jazzmin/Bootstrap's built-in JS.
    // The primary goal is to let the CSS handle animations and transitions.

    // A simple function to handle the mobile sidebar toggle, if needed.
    // Jazzmin should handle this by default, but if a custom button is ever added, this is the place for it.
    function initMobileMenu() {
        const toggleButton = document.querySelector('.mobile-menu-toggle'); // Assuming a button with this class exists
        const sidebar = document.querySelector('.main-sidebar');
        const body = document.querySelector('body');

        if (toggleButton && sidebar && body) {
            toggleButton.addEventListener('click', function() {
                body.classList.toggle('sidebar-open');
                // You might also need to toggle classes on the sidebar itself depending on Jazzmin's version
                // For example: sidebar.classList.toggle('collapse-in');
            });
        }
    }

    initMobileMenu();


    // Add any other non-conflicting, necessary JS below.
    // For example, a simple form submission handler to prevent double-clicks.
    function initFormSubmitGuard() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function() {
                const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
                submitButtons.forEach(button => {
                    if (button.disabled) {
                        return;
                    }
                    button.disabled = true;
                    const originalValue = button.value || button.textContent;
                    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Сохранение...';
                    
                    // Re-enable after a short delay in case of validation errors
                    setTimeout(() => {
                        button.disabled = false;
                        button.innerHTML = originalValue;
                    }, 3000);
                });
            });
        });
    }

    initFormSubmitGuard();

});
