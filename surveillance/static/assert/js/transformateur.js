class TransformateursManager {
    constructor(transformateursData) {
        this.transformateursData = transformateursData;
        this.currentDepartId = null;
        this.currentDepartNom = null;
        this.currentTransformateur = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.querySelectorAll('.depart-button').forEach(button => {
            button.addEventListener('click', event => {
                const departId = button.dataset.departId;
                const departNom = button.dataset.departNom;
                this.showTransformateurs(departId, departNom);
            });
        });
    }

    createBreadcrumb() {
        const breadcrumb = document.createElement('div');
        breadcrumb.className = 'breadcrumb';
        
        const items = [];
        
        // Accueil
        items.push(`<span class="breadcrumb-item"><a onclick="transformateursManager.resetView()">Accueil</a></span>`);
        
        // Départ
        if (this.currentDepartNom) {
            items.push(`<span class="breadcrumb-item"><a onclick="transformateursManager.showTransformateurs('${this.currentDepartId}', '${this.currentDepartNom}')">${this.currentDepartNom}</a></span>`);
        }
        
        // Transformateur
        if (this.currentTransformateur) {
            items.push(`<span class="breadcrumb-item active">${this.currentTransformateur.code}</span>`);
        }
        
        breadcrumb.innerHTML = items.join('');
        return breadcrumb;
    }

    resetView() {
        this.currentDepartId = null;
        this.currentDepartNom = null;
        this.currentTransformateur = null;
        
        const container = document.getElementById('content-container');
        container.innerHTML = '';
        
        const title = document.createElement('h1');
        title.id = 'section-title';
        title.textContent = 'Sélectionnez un départ';
        
        const transformateursDiv = document.createElement('div');
        transformateursDiv.id = 'transformateurs-container';
        transformateursDiv.className = 'transformateurs';
        transformateursDiv.innerHTML = '<p>Aucun transformateur à afficher.</p>';
        
        container.appendChild(this.createBreadcrumb());
        container.appendChild(title);
        container.appendChild(transformateursDiv);
    }

    showTransformateurs(departId, departNom) {
        this.currentDepartId = departId;
        this.currentDepartNom = departNom;
        this.currentTransformateur = null;
        
        const transformateurs = this.transformateursData[departId] || [];
        const container = document.getElementById('content-container');
        container.innerHTML = '';
        
        const title = document.createElement('h1');
        title.id = 'section-title';
        title.textContent = `Transformateurs pour le départ : ${departNom}`;
        
        const transformateursDiv = document.createElement('div');
        transformateursDiv.className = 'transformateurs';
        
        container.appendChild(this.createBreadcrumb());
        container.appendChild(title);
        container.appendChild(transformateursDiv);

        if (transformateurs.length > 0) {
            transformateurs.forEach(transformateur => {
                const button = document.createElement('button');
                button.innerText = transformateur.code;
                button.onclick = () => this.showTransformateurDetails(transformateur);
                transformateursDiv.appendChild(button);
            });
        } else {
            transformateursDiv.innerHTML = '<p>Aucun transformateur à afficher.</p>';
        }
    }

    showTransformateurDetails(transformateur) {
        this.currentTransformateur = transformateur;
        
        const container = document.getElementById('content-container');
        container.innerHTML = '';
        
        container.appendChild(this.createBreadcrumb());

        const detailsDiv = document.createElement('div');
        detailsDiv.className = 'transformateur-details';
        
        const title = document.createElement('h2');
        title.textContent = `Détails du transformateur ${transformateur.code}`;
        detailsDiv.appendChild(title);

        const infoGrid = document.createElement('div');
        infoGrid.className = 'info-grid';

        // Exemple de données à afficher (à adapter selon vos données réelles)
        const infos = [
            { title: 'Code', value: transformateur.code },
            { title: 'Puissance', value: transformateur.puissance || 'Non spécifiée' },
            { title: 'État', value: transformateur.etat || 'Non spécifié' },
            { title: 'Localisation', value: transformateur.localisation || 'Non spécifiée' },
            { title: 'Date d\'installation', value: transformateur.dateInstallation || 'Non spécifiée' },
            { title: 'Dernière maintenance', value: transformateur.derniereMaintenance || 'Non spécifiée' }
        ];

        infos.forEach(info => {
            const card = document.createElement('div');
            card.className = 'info-card';
            card.innerHTML = `
                <h3>${info.title}</h3>
                <p>${info.value}</p>
            `;
            infoGrid.appendChild(card);
        });

        detailsDiv.appendChild(infoGrid);
        container.appendChild(detailsDiv);
    }

    // showTransformateurDetails(id) {
    //     const container = document.getElementById('transformateurs-container');
    //     const transformateur = this.transformateursData[id];
    //     container.innerHTML = `
    //         <div class="card">
    //             <h3>${transformateur.code}</h3>
    //             <p>Puissance : ${transformateur.puissance}</p>
    //             <p>État : ${transformateur.etat}</p>
    //         </div>`;
    // }
    
}