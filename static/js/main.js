// Main JavaScript for Game Dev Encyclopedia

// Smooth scroll to top button
document.addEventListener('DOMContentLoaded', function() {
    // If we arrived here after a filter change, remove the suppression flag and class
    try {
        if (sessionStorage.getItem('suppressAnimations') === '1') {
            sessionStorage.removeItem('suppressAnimations');
            // Remove the class on next tick to keep initial paint without animations
            setTimeout(() => document.documentElement.classList.remove('no-animations'), 0);
        }
    } catch (e) {
        // ignore storage errors
    }
    
    // Form validation
    const gameForm = document.getElementById('gameForm');
    if (gameForm) {
        gameForm.addEventListener('submit', function(e) {
            const title = document.querySelector('input[name="title"]');
            const releaseYear = document.querySelector('input[name="release_year"]');
            const description = document.querySelector('textarea[name="description"]');
            
            let errors = [];
            
            // Title validation
            if (title && title.value.trim().length < 2) {
                errors.push('Название игры должно содержать минимум 2 символа');
            }
            
            // Release year validation
            if (releaseYear) {
                const year = parseInt(releaseYear.value);
                const currentYear = new Date().getFullYear();
                if (year < 1950 || year > currentYear + 5) {
                    errors.push(`Год выпуска должен быть между 1950 и ${currentYear + 5}`);
                }
            }
            
            // Description validation
            if (description && description.value.trim().length < 10) {
                errors.push('Описание должно содержать минимум 10 символов');
            }
            
            // Show errors if any
            if (errors.length > 0) {
                e.preventDefault();
                alert('Ошибки формы:\n\n' + errors.join('\n'));
            }
        });
    }
    
    // Filter form auto-submit
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        const filterSelects = filterForm.querySelectorAll('.filter-select');
        
        filterSelects.forEach(select => {
            select.addEventListener('change', function() {
                // Add loading indicator
                const submitBtn = filterForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="loading"></span> Загрузка...';
                }
                // Suppress animations on next page load so filtering doesn't look like reload animation
                try { sessionStorage.setItem('suppressAnimations', '1'); } catch (e) {}
                filterForm.submit();
            });
        });

        // Also handle explicit submit button clicks
        filterForm.addEventListener('submit', function() {
            try { sessionStorage.setItem('suppressAnimations', '1'); } catch (e) {}
        });
    }
    
    // Add animation delay to game cards
    const gameCards = document.querySelectorAll('.game-card');
    gameCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });
    
    // Image lazy loading fallback
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Dynamic search filter (client-side for better UX)
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const gameCards = document.querySelectorAll('.game-card');
            
            gameCards.forEach(card => {
                const title = card.querySelector('h3 a').textContent.toLowerCase();
                const studio = card.querySelector('.game-studio')?.textContent.toLowerCase() || '';
                
                if (title.includes(searchTerm) || studio.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Confirm delete with custom styling
    const deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Only confirm if not on the confirm page
            if (!window.location.pathname.includes('delete')) {
                if (!confirm('Вы уверены, что хотите удалить эту игру?')) {
                    e.preventDefault();
                }
            }
        });
    });
    
    // Add hover effect to platform badges
    const platformBadges = document.querySelectorAll('.platform-badge, .platform-badge-large');
    platformBadges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(2deg)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 5000);
    });
    
    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('no-loading')) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading"></span> Загрузка...';
            }
        });
    });
    
    // API endpoint test button (optional)
    const apiTestBtn = document.getElementById('apiTestBtn');
    if (apiTestBtn) {
        apiTestBtn.addEventListener('click', async function() {
            try {
                const response = await fetch('/api/games/');
                const data = await response.json();
                console.log('API Response:', data);
                alert(`API работает! Найдено игр: ${data.count}`);
            } catch (error) {
                console.error('API Error:', error);
                alert('Ошибка при обращении к API');
            }
        });
    }
    
    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals/forms
        if (e.key === 'Escape') {
            const activeElement = document.activeElement;
            if (activeElement && activeElement.tagName !== 'BODY') {
                activeElement.blur();
            }
        }
    });
    
    // Console welcome message
    console.log('%c🎮 Энциклопедия Разработки Игр', 'font-size: 24px; color: #6366f1; font-weight: bold;');
    console.log('%cAPI Endpoints:', 'font-size: 14px; color: #8b5cf6; font-weight: bold;');
    console.log('- GET /api/games/ - Список всех игр');
    console.log('- GET /api/games/<id>/ - Детали игры');
});

// Utility function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Utility function to truncate text
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

// Export for use in other scripts
window.GameEncyclopedia = {
    formatDate,
    truncateText
};
