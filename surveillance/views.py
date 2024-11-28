from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import PosteSource, Depart, Transformateur
from .serializers import PosteSourceSerializer, DepartSerializer, TransformateurSerializer, CapteurSerializer


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('page_depart')  # Redirection après connexion
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
            return redirect('page_depart')  # Redirection après inscription
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
    return render(request, 'page_depart.html') 

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

@api_view(['POST'])
def recevoir_donnees_esp32(request):
    if request.method == 'POST':
        # Affiche les données reçues pour le débogage
        print("Données reçues :", request.data)
        
        serializer = CapteurSerializer(data=request.data)
        if serializer.is_valid():
            # Récupérer le code_poste
            code_poste = serializer.validated_data.get('code_poste')
            try:
                # Vérifier si le transformateur existe
                transformateur = Transformateur.objects.get(code_poste=code_poste)
                
                # Mettre à jour uniquement les champs envoyés par l'ESP32
                transformateur.tension_secondaire = serializer.validated_data.get('tension_secondaire')
                transformateur.courant_secondaire = serializer.validated_data.get('courant_secondaire')
                transformateur.temperature = serializer.validated_data.get('temperature')
                transformateur.niveau_huile = serializer.validated_data.get('niveau_huile')
                transformateur.save()
                
                return Response(
                    {"message": "Données mises à jour avec succès."},
                    status=status.HTTP_200_OK
                )
            except Transformateur.DoesNotExist:
                # Si le code_poste n'existe pas
                return Response(
                    {"error": "Le code_poste spécifié n'existe pas."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Affiche les erreurs de validation pour le débogage
            print("Erreurs du serializer :", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Retour si ce n'est pas une requête POST
    return Response({"error": "Méthode non autorisée."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

