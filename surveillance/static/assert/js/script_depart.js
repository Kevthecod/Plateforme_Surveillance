document.getElementById('liste-postes-toggle').addEventListener('click', function (e) {
    e.preventDefault();

    const postesList = document.getElementById('postes-list');
    const toggleButton = this;

    // Toggle pour le bouton principal
    toggleButton.classList.toggle('active');

    // Vérifie si la liste des postes sources est affichée
    if (getComputedStyle(postesList).display === 'none' || !postesList.hasChildNodes()) {
        postesList.style.opacity = '0';
        postesList.style.display = 'block';
        
        // Récupérer les postes sources de la base de données
        fetch('/api/postes/')
            .then(response => response.json())
            .then(data => {
                // Vider la liste avant de la remplir
                postesList.innerHTML = '';

                data.postes.forEach(poste => {
                    const posteItem = document.createElement('li');
                    posteItem.classList.add('poste-item');
                    posteItem.innerHTML = `
                        <a href="#" class="poste-link" data-poste-id="${poste.id}">
                            ${poste.nom}
                        </a>
                        <ul class="depart-list" style="display: none;"></ul>
                    `;
                    postesList.appendChild(posteItem);
                });

                // Animation d'apparition
                setTimeout(() => {
                    postesList.style.opacity = '1';
                }, 10);

                // Ajouter des gestionnaires d'événements pour chaque poste source
                document.querySelectorAll('.poste-link').forEach(link => {
                    link.addEventListener('click', function (e) {
                        e.preventDefault();
                        
                        // Toggle de la classe active pour l'animation de la flèche
                        this.classList.toggle('active');
                        
                        const posteId = this.getAttribute('data-poste-id');
                        const departList = this.nextElementSibling;

                        // Animation fluide avec opacity
                        if (getComputedStyle(departList).display === 'none') {
                            departList.style.opacity = '0';
                            departList.style.display = 'block';
                            setTimeout(() => {
                                departList.style.opacity = '1';
                            }, 10);

                            // Parcourir les départs du poste source sélectionné
                            const poste = data.postes.find(p => p.id == posteId);
                            departList.innerHTML = '';  // Vider la liste des départs

                            poste.departs.forEach(depart => {
                                const departItem = document.createElement('li');
                                departItem.innerHTML = `
                                    <a href="#" class="depart-link" data-depart-id="${depart.id}">
                                        ${depart.nom}
                                    </a>
                                    <ul class="transformateur-list" style="display: none;"></ul>
                                `;
                                departList.appendChild(departItem);
                            });

                            // Ajouter des gestionnaires d'événements pour chaque départ
                            document.querySelectorAll('.depart-link').forEach(departLink => {
                                departLink.addEventListener('click', function (e) {
                                    e.preventDefault();
                                    
                                    // Toggle de la classe active pour l'animation de la flèche
                                    this.classList.toggle('active');
                                    
                                    const departId = this.getAttribute('data-depart-id');
                                    const transfoList = this.nextElementSibling;

                                    if (getComputedStyle(transfoList).display === 'none') {
                                        transfoList.style.opacity = '0';
                                        transfoList.style.display = 'block';
                                        setTimeout(() => {
                                            transfoList.style.opacity = '1';
                                        }, 10);

                                        // Parcourir les transformateurs du départ sélectionné
                                        const depart = poste.departs.find(d => d.id == departId);
                                        transfoList.innerHTML = '';  // Vider la liste des transformateurs

                                        depart.transformateurs.forEach(transfo => {
                                            const transfoItem = document.createElement('li');
                                            transfoItem.innerHTML = transfo.code_poste;
                                            transfoList.appendChild(transfoItem);
                                        });
                                    } else {
                                        // Animation de fermeture
                                        transfoList.style.opacity = '0';
                                        setTimeout(() => {
                                            transfoList.style.display = 'none';
                                        }, 300);
                                    }
                                });
                            });
                        } else {
                            // Animation de fermeture
                            departList.style.opacity = '0';
                            setTimeout(() => {
                                departList.style.display = 'none';
                            }, 300);
                        }
                    });
                });
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des données :', error);
                postesList.innerHTML = '<li class="error">Erreur lors du chargement des données</li>';
            });
    } else {
        // Animation de fermeture pour la liste principale
        postesList.style.opacity = '0';
        setTimeout(() => {
            postesList.style.display = 'none';
        }, 300);
    }
});