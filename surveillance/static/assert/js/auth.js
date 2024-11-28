document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScript chargé'); // Vérifie si le fichier est chargé correctement

    const startButton = document.getElementById('startButton'); // Bouton "Commencer"
    const authSection = document.getElementById('authSection'); // Section d'authentification

    if (startButton && authSection) {
        startButton.addEventListener('click', function () {
            console.log('Bouton cliqué'); // Pour déboguer
            authSection.style.display = 'block'; // Affiche la section d'authentification
            startButton.textContent = 'Bienvenue'; // Change le texte du bouton
            startButton.disabled = true; // Optionnel : Désactive le bouton après le clic
        });
    } else {
        console.error('Bouton ou section introuvable');
    }
});
