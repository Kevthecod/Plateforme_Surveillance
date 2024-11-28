from django.urls import path
from .views import accueil, page_depart, get_postes_data, recevoir_donnees_esp32, login_view, register_view

urlpatterns = [
    path('accueil/', accueil, name='accueil'),  # URL pour la page d'accueil
    path('accueil/page_depart/', page_depart, name='page_depart'),  # URL pour la page départ
    path('api/postes/', get_postes_data, name='get_postes_data'),
    path('api/recevoir-donnees/', recevoir_donnees_esp32, name='recevoir_donnees_esp32'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]
