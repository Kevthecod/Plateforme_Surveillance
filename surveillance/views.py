from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import HistoriqueDonnees, PosteSource, Depart, Transformateur
from .serializers import PosteSourceSerializer, DepartSerializer, TransformateurSerializer, CapteurSerializer, DernieresDonneesSerializer



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirection après connexion
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte l'utilisateur après inscription
            return redirect('dashboard')  # Redirection après inscription
        else:
            messages.error(request, "Erreur lors de l'inscription. Vérifiez les champs.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class PostesSourceViewSet(viewsets.ModelViewSet):
    queryset = PosteSource.objects.all()
    serializer_class = PosteSourceSerializer

class DepartViewSet(viewsets.ModelViewSet):
    queryset = Depart.objects.all()
    serializer_class = DepartSerializer

class TransformateurViewSet(viewsets.ModelViewSet):
    queryset = Transformateur.objects.all()
    serializer_class = TransformateurSerializer


def accueil(request, *args, **kwargs):
    return render(request, 'index.html')

@login_required
def page_depart(request):
    return render(request, 'dashboard.html') 

@api_view(['GET'])
def get_postes_data(request):
    postes_sources = PosteSource.objects.prefetch_related('departs__transformateurs').all()
    
    # Construire les données en JSON
    data = []
    for poste in postes_sources:
        poste_data = {
            'id': poste.id,
            'nom': poste.nom,
            'departs': []
        }
        for depart in poste.departs.all():
            depart_data = {
                'id': depart.id,
                'nom': depart.nom,
                'transformateurs': []
            }
            for transformateur in depart.transformateurs.all():
                transformateur_data = {
                    'id': transformateur.id,
                    'code_poste': transformateur.code_poste,
                }
                depart_data['transformateurs'].append(transformateur_data)
            poste_data['departs'].append(depart_data)
        data.append(poste_data)
    
    return JsonResponse({'postes': data})

def verifier_anomalies(data):
    anomalies = []
    
    if data.get('temperature') > 70:
        anomalies.append("Température élevée (> 70°C).")
    if data.get('niveau_huile') < 20:
        anomalies.append("Faible niveau d'huile (< 20%).")
    if data.get('pression_interne') < 210 or data.get('pression_interne') > 250:
        anomalies.append("Tension secondaire hors plage normale (210-250 V).")
    for phase in ['I1', 'I2', 'I3']:
        if data.get(f'courant_secondaire_{phase}') > 50:  # Exemple : seuil de 50 A
            anomalies.append(f"Courant secondaire {phase} élevé (> 50 A).")
    
    alerte = len(anomalies) > 0
    message = " | ".join(anomalies) if anomalies else None
    
    return alerte, message


class RecevoirDonneesAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        # Récupérer les données envoyées
        data = request.data

        if not all(key in data for key in ['code_poste', 'pression_interne', 'courant_secondaire_I1', 'courant_secondaire_I2', 'courant_secondaire_I3', 'temperature', 'niveau_huile']):
            return Response(
                {"detail": "Données manquantes dans la requête."},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        try:
            # Vérifier si le transformateur existe
            transformateur = Transformateur.objects.get(code_poste=data.get('code_poste'))
        except Transformateur.DoesNotExist:
            return Response(
                {"detail": "Transformateur introuvable avec ce code_poste."},
                status=status.HTTP_404_NOT_FOUND
            )
        alerte, message = verifier_anomalies(data)
        # Enregistrer les données dans HistoriqueDonnees
        HistoriqueDonnees.objects.create(
            transformateur=transformateur,
            pression_interne=data.get('pression_interne'),
            courant_secondaire_I1=data.get('courant_secondaire_I1'),
            courant_secondaire_I2=data.get('courant_secondaire_I2'),
            courant_secondaire_I3=data.get('courant_secondaire_I3'),
            temperature=data.get('temperature'),
            niveau_huile=data.get('niveau_huile'),
            alerte=alerte,
            message=message
        )

        return Response(
            {"detail": "Données enregistrées avec succès."},
            status=status.HTTP_201_CREATED
        )
    

def dashboard_view(request):
    postes_sources = PosteSource.objects.prefetch_related('departs__transformateurs').all()

    # Construire les données JSON pour les départs et transformateurs
    transformateurs_data = {
        depart.id: [
            {"id": transformateur.id, "code": transformateur.code_poste}
            for transformateur in depart.transformateurs.all()
        ]
        for poste in postes_sources
        for depart in poste.departs.all()
    }

    context = {
        "postes_sources": postes_sources,
        "transformateurs_data": json.dumps(transformateurs_data)  # Sérialisation JSON
    }
    return render(request, "dashboard.html", context)
