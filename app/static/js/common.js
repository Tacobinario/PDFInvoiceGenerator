// Validación del RFC (México)
function validateRFC(rfc) {
    const rfcRegex = /^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$/;
    return rfcRegex.test(rfc);
}

// Función para mostrar mensajes de error
function showError(input, message) {
    const formField = input.closest('.mb-3');
    input.classList.add('is-invalid');

    // Buscar o crear el div de feedback
    let feedback = formField.querySelector('.invalid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        formField.appendChild(feedback);
    }
    feedback.textContent = message;
}

// Función para limpiar errores
function clearError(input) {
    const formField = input.closest('.mb-3');
    input.classList.remove('is-invalid');
    const feedback = formField.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.remove();
    }
}

// Validación asíncrona de RFC
async function validateRFCAsync(input) {
    const rfc = input.value.toUpperCase();

    if (!validateRFC(rfc)) {
        showError(input, 'Formato de RFC inválido');
        return false;
    }

    try {
        const response = await fetch('/api/validate_rfc', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rfc: rfc })
        });

        const data = await response.json();

        if (!data.valid) {
            showError(input, data.message);
            return false;
        }

        clearError(input);
        return true;
    } catch (error) {
        console.error('Error validating RFC:', error);
        showError(input, 'Error al validar RFC');
        return false;
    }
}

// Preview de imagen
function setupImagePreview(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);

    if (!input || !preview) return;

    input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            showError(input, 'Por favor seleccione una imagen válida');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            const img = preview.querySelector('img') || document.createElement('img');
            img.src = e.target.result;
            img.classList.add('img-thumbnail');
            img.style.maxHeight = '150px';
            if (!preview.contains(img)) {
                preview.appendChild(img);
            }
        };
        reader.readAsDataURL(file);
    });
}

// Cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Configurar preview de imagen para el logo de la empresa
    setupImagePreview('logo', 'logo-preview');

    // Validación de RFC en tiempo real
    const rfcInputs = document.querySelectorAll('input[name$="rfc"]');
    rfcInputs.forEach(input => {
        input.addEventListener('blur', () => validateRFCAsync(input));
        input.addEventListener('input', () => {
            input.value = input.value.toUpperCase();
            clearError(input);
        });
    });
});