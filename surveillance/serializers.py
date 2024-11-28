from rest_framework import serializers
from .models import PosteSource, Depart, Transformateur

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

class CapteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformateur
        fields = [
            'code_poste', 
            'tension_secondaire', 
            'courant_secondaire', 
            'temperature', 
            'niveau_huile',
            'timestamp'  
        ]