document.getElementById('startButton').addEventListener('click', function () {
    const authSection = document.getElementById('authSection');
    authSection.style.display = 'block';
});


// function showPostes(departId) {
//     // Cacher toutes les sections de postes
//     var sections = document.querySelectorAll('.postes-section');
//     sections.forEach(function(section) {
//         section.style.display = 'none';
//     });

//     // Afficher la section correspondante au départ cliqué
//     var selectedSection = document.getElementById(departId);
//     if (selectedSection) {
//         selectedSection.style.display = 'block';
//     }

//     // Gérer l'état actif des liens dans le sidebar
//     var links = document.querySelectorAll('.nav-link');
//     links.forEach(function(link) {
//         link.classList.remove('active');
//     });
//     event.target.classList.add('active');
// }


    // Fonction pour générer l'arborescence




// function toggleDepart(id) {
//     var element = document.getElementById(id);
//     if (element.style.display === "none") {
//         element.style.display = "block";
//     } else {
//         element.style.display = "none";
//     }
// }

// function toggleTransformateur(id) {
//     var element = document.getElementById(id);
//     if (element.style.display === "none") {
//         element.style.display = "block";
//     } else {
//         element.style.display = "none";
//     }
// }
