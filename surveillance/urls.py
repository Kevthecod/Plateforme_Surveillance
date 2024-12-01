from django.urls import path
from .views import accueil, page_depart, get_postes_data, RecevoirDonneesAPIView, login_view, register_view

urlpatterns = [
    path('accueil/', accueil, name='accueil'),  # URL pour la page d'accueil
    path('accueil/page_depart/', page_depart, name='page_depart'),  # URL pour la page départ
    path('api/postes/', get_postes_data, name='get_postes_data'),
    path('api/recevoir-donnees/', RecevoirDonneesAPIView.as_view(), name='recevoir-donnees'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]
