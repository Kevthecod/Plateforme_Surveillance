// Chargement du composant formulaire
document.addEventListener('DOMContentLoaded', async () => {
    try {
      const response = await fetch('src/components/login/login-form.html');
      const formHtml = await response.text();
      document.getElementById('login-form-container').innerHTML = formHtml;
      
      initializeFormValidation();
    } catch (error) {
      console.error('Erreur lors du chargement du formulaire:', error);
    }
  });
  
  // Initialisation de la validation du formulaire
  function initializeFormValidation() {
    const form = document.querySelector('form');
    
    if (form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        
        form.classList.add('was-validated');
      });
    }
  }