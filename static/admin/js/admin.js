// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des tooltips et popovers Bootstrap
    initBootstrapComponents();

    // Gestion des formulaires
    initForms();

    // Gestion des tableaux
    initTables();

    // Gestion des images
    initImageUploads();

    // Gestion des dates
    initDateInputs();

    // Gestion des sélecteurs multiples
    initMultiSelects();

    // Gestion des alertes
    initAlerts();
});

// Initialisation des composants Bootstrap
function initBootstrapComponents() {
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl, {
            trigger: 'hover'
        });
    });

    // Popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function (popoverTriggerEl) {
        new bootstrap.Popover(popoverTriggerEl, {
            trigger: 'click'
        });
    });
}

// Gestion des formulaires
function initForms() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Validation des champs requis
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });

        // Validation en temps réel
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('input', function() {
                validateField(this);
            });
            field.addEventListener('blur', function() {
                validateField(this);
            });
        });

        // Gestion des champs numériques
        const numericInputs = form.querySelectorAll('input[type="number"]');
        numericInputs.forEach(input => {
            input.addEventListener('input', function() {
                validateNumericInput(this);
            });
        });
    });
}

// Validation d'un formulaire
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });

    if (!isValid) {
        showAlert('Veuillez remplir tous les champs obligatoires.', 'danger');
    }

    return isValid;
}

// Validation d'un champ
function validateField(field) {
    const isValid = field.value.trim() !== '';
    const feedback = field.nextElementSibling;
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        if (feedback) feedback.remove();
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        if (!feedback) {
            const feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            feedback.textContent = 'Ce champ est obligatoire';
            field.parentNode.insertBefore(feedback, field.nextSibling);
        }
    }

    return isValid;
}

// Validation des champs numériques
function validateNumericInput(input) {
    const min = parseFloat(input.getAttribute('min'));
    const max = parseFloat(input.getAttribute('max'));
    const value = parseFloat(input.value);

    if (isNaN(value)) {
        input.value = '';
        return;
    }

    if (min !== null && value < min) {
        input.value = min;
    } else if (max !== null && value > max) {
        input.value = max;
    }
}

// Gestion des tableaux
function initTables() {
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        // Tri des colonnes
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.addEventListener('click', function() {
                sortTable(table, this);
            });
        });

        // Recherche
        const searchInput = table.parentElement.querySelector('.table-search');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                filterTable(table, this.value);
            });
        }
    });
}

// Tri d'un tableau
function sortTable(table, header) {
    const column = header.cellIndex;
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const direction = header.classList.contains('asc') ? -1 : 1;
    
    // Toggle la classe de direction
    table.querySelectorAll('th').forEach(th => th.classList.remove('asc', 'desc'));
    header.classList.toggle('asc', direction === 1);
    header.classList.toggle('desc', direction === -1);

    // Tri des lignes
    rows.sort((a, b) => {
        const aValue = a.cells[column].textContent.trim();
        const bValue = b.cells[column].textContent.trim();
        return direction * (aValue > bValue ? 1 : -1);
    });

    // Réorganisation du tableau
    const tbody = table.querySelector('tbody');
    rows.forEach(row => tbody.appendChild(row));
}

// Filtrage d'un tableau
function filterTable(table, searchText) {
    const rows = table.querySelectorAll('tbody tr');
    const searchLower = searchText.toLowerCase();

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchLower) ? '' : 'none';
    });
}

// Gestion des images
function initImageUploads() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept="image/*"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const preview = document.querySelector(`#${this.getAttribute('data-preview')}`);
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.classList.add('fade-in');
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
}

// Gestion des dates
function initDateInputs() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            input.value = new Date().toISOString().split('T')[0];
        }
    });
}

// Gestion des sélecteurs multiples
function initMultiSelects() {
    const multiSelects = document.querySelectorAll('select[multiple]');
    multiSelects.forEach(select => {
        select.addEventListener('change', function() {
            const selectedOptions = Array.from(this.selectedOptions).map(option => option.value);
            const hiddenInput = document.querySelector(`#${this.getAttribute('data-hidden-input')}`);
            if (hiddenInput) {
                hiddenInput.value = JSON.stringify(selectedOptions);
            }
        });
    });
}

// Gestion des alertes
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeButton = alert.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                alert.classList.add('fade');
                setTimeout(() => alert.remove(), 300);
            });
        }
    });
}

// Affichage d'une alerte
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.alert-container') || document.body;
    container.appendChild(alert);
    
    // Suppression automatique après 5 secondes
    setTimeout(() => {
        alert.classList.add('fade');
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

// Export des fonctions utiles
window.admin = {
    showAlert,
    validateForm,
    sortTable,
    filterTable
}; 