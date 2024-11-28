from django.db import models

class PosteSource(models.Model):
    nom = models.CharField(max_length=100)
    localisation = models.CharField(max_length=255)
    capacite = models.CharField(max_length=100)  # Capacité en MW ou autre unité

    def __str__(self):
        return self.nom

class Depart(models.Model):
    nom = models.CharField(max_length=100)
    poste_source = models.ForeignKey(PosteSource, on_delete=models.CASCADE, related_name='departs')
    capacite = models.CharField(max_length=50)  # Capacité du départ

    def __str__(self):
        return f"{self.nom} ({self.poste_source.nom})"
    


class Transformateur(models.Model):
    code_poste = models.CharField(max_length=100, unique=True)  
    puissance = models.CharField(max_length=100)  # Puissance en W ou autre unité
    depart = models.ForeignKey('Depart', on_delete=models.CASCADE, related_name="transformateurs")
    caracteristiques = models.TextField(blank=True, null=True)
    
    # Champs pour les données envoyées par l'ESP32
    tension_secondaire = models.FloatField(blank=True, null=True)
    courant_secondaire = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    niveau_huile = models.FloatField(blank=True, null=True)

    # Nouveau champ pour suivre la date et l'heure des mises à jour
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code_poste

# Ancien modèle Transformateur
# class Transformateur(models.Model):
#     code_poste = models.CharField(max_length=100, unique=True)  
#     puissance = models.CharField(max_length=100)  # Puissance en W ou autre unité()
#     depart = models.ForeignKey('Depart', on_delete=models.CASCADE, related_name="transformateurs")
#     caracteristiques = models.TextField(blank=True, null=True)
    
#     # Champs pour les données envoyées par l'ESP32
#     tension_secondaire = models.FloatField(blank=True, null=True)
#     courant_secondaire = models.FloatField(blank=True, null=True)
#     temperature = models.FloatField(blank=True, null=True)
#     niveau_huile = models.FloatField(blank=True, null=True)

#     def __str__(self):
#         return self.code_poste


    



