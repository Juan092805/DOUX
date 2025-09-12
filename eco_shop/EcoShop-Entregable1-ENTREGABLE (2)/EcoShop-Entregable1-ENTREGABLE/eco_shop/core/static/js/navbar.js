// navbar.js - Funcionalidad para el navbar de EcoShop

document.addEventListener('DOMContentLoaded', function() {
    // Toggle del formulario de búsqueda
    const searchToggle = document.querySelector('.search-toggle');
    const searchForm = document.querySelector('.search-form');
    
    if (searchToggle && searchForm) {
        searchToggle.addEventListener('click', function(e) {
            e.preventDefault();
            searchForm.classList.toggle('active');
            
            // Si el formulario se muestra, enfocar el input
            if (searchForm.classList.contains('active')) {
                const searchInput = searchForm.querySelector('.search-input');
                if (searchInput) {
                    searchInput.focus();
                }
            }
        });
        
        // Cerrar búsqueda al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (!searchToggle.contains(e.target) && !searchForm.contains(e.target)) {
                searchForm.classList.remove('active');
            }
        });
        
        // Prevenir que el formulario se cierre al hacer clic dentro
        searchForm.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
});
