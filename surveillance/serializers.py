from rest_framework import serializers
from .models import PosteSource, Depart, Transformateur, HistoriqueDonnees

class PosteSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosteSource
        fields = '__all__'

class DepartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depart
        fields = '__all__'

class TransformateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformateur
        fields = '__all__'

class DernieresDonneesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueDonnees
        fields = [
            'timestamp', 
            'pression_interne', 
            'courant_secondaire_I1', 
            'courant_secondaire_I2',    
            'courant_secondaire_I3', 
            'temperature', 
            'niveau_huile',
            'alerte', 
            'message'
        ]

class CapteurSerializer(serializers.ModelSerializer):
    dernieres_donnees = serializers.SerializerMethodField()

    class Meta:
        model = Transformateur
        fields = [
            'code_poste', 
            'puissance',
            'depart',
            'dernieres_donnees',  # Les données dynamiques les plus récentes
        ]

    def get_dernieres_donnees(self, obj):
        derniere_entree = obj.historique.order_by('-timestamp').first()  # Récupère la plus récente
        if derniere_entree:
            return DernieresDonneesSerializer(derniere_entree).data
        return None  # Si aucune donnée n'existe encore


# class CapteurSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transformateur
#         fields = [
#             'code_poste', 
#             'tension_secondaire', 
#             'courant_secondaire', 
#             'temperature', 
#             'niveau_huile',
#             'timestamp'  
#         ]
 

# class HistoriqueDonneesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HistoriqueDonnees
#         fields = '__all__'