// Validación del RFC (México)
          function validateRFC(rfc) {
              const rfcRegex = /^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$/;
              return rfcRegex.test(rfc);
          }

          // Función para mostrar mensajes de error
          function showError(input, message) {
              const formField = input.closest('.mb-3');
              input.classList.add('is-invalid');
              input.classList.remove('is-valid');

              // Buscar o crear el div de feedback
              let feedback = formField.querySelector('.invalid-feedback');
              if (!feedback) {
                  feedback = document.createElement('div');
                  feedback.className = 'invalid-feedback';
                  formField.appendChild(feedback);
              }
              feedback.textContent = message;
          }

          // Función para mostrar mensajes de éxito
          function showSuccess(input, message) {
              const formField = input.closest('.mb-3');
              input.classList.remove('is-invalid');
              input.classList.add('is-valid');

              // Buscar o crear el div de feedback
              let feedback = formField.querySelector('.valid-feedback');
              if (!feedback) {
                  feedback = document.createElement('div');
                  feedback.className = 'valid-feedback';
                  formField.appendChild(feedback);
              }
              feedback.textContent = message;
          }

          // Función para limpiar mensajes
          function clearFeedback(input) {
              const formField = input.closest('.mb-3');
              input.classList.remove('is-invalid', 'is-valid');

              const invalidFeedback = formField.querySelector('.invalid-feedback');
              const validFeedback = formField.querySelector('.valid-feedback');

              if (invalidFeedback) invalidFeedback.remove();
              if (validFeedback) validFeedback.remove();
          }

          // Validación asíncrona de RFC
          async function validateRFCAsync(input) {
              const rfc = input.value.toUpperCase();
              input.value = rfc; // Mantener en mayúsculas

              // Primero validación básica
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

                  showSuccess(input, data.message);
                  return true;
              } catch (error) {
                  console.error('Error validating RFC:', error);
                  showError(input, 'Error al validar RFC');
                  return false;
              }
          }

          // Cuando el DOM esté listo
          document.addEventListener('DOMContentLoaded', function() {
              // Configurar validación de RFC en tiempo real
              const rfcInputs = document.querySelectorAll('input[name$="rfc"]');
              rfcInputs.forEach(input => {
                  let timeoutId;

                  // Validar cuando el usuario deja de escribir
                  input.addEventListener('input', () => {
                      clearTimeout(timeoutId);
                      input.value = input.value.toUpperCase();
                      clearFeedback(input);

                      timeoutId = setTimeout(() => {
                          if (input.value.length >= 12) {
                              validateRFCAsync(input);
                          }
                      }, 500); // Esperar 500ms después de que el usuario deje de escribir
                  });

                  // Validar cuando el campo pierde el foco
                  input.addEventListener('blur', () => {
                      if (input.value.length > 0) {
                          validateRFCAsync(input);
                      }
                  });
              });

              // ... resto del código para otras funcionalidades
          });