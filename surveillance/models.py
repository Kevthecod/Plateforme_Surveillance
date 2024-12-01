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
    code_poste = models.CharField(max_length=50, unique=True)
    puissance = models.FloatField(null=True, blank=True)
    depart = models.ForeignKey('Depart', on_delete=models.CASCADE, related_name="transformateurs")
    caracteristiques = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Transformateur {self.code_poste}"


class HistoriqueDonnees(models.Model):
    transformateur = models.ForeignKey(Transformateur, on_delete=models.CASCADE, related_name="historique")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    pression_interne = models.FloatField()
    courant_secondaire_I1 = models.FloatField()  # Courant pour la phase 1
    courant_secondaire_I2 = models.FloatField(null=True)  # Courant pour la phase 2
    courant_secondaire_I3 = models.FloatField(null=True)  # Courant pour la phase 3
    temperature = models.FloatField()
    niveau_huile = models.FloatField()
    alerte = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.transformateur.code_poste} - {self.timestamp}"

# class Transformateur(models.Model):
#     code_poste = models.CharField(max_length=100, unique=True)  
#     puissance = models.CharField(max_length=100)  # Puissance en W ou autre unité
#     depart = models.ForeignKey('Depart', on_delete=models.CASCADE, related_name="transformateurs")
#     caracteristiques = models.TextField(blank=True, null=True)
    
#     # Champs pour les données envoyées par l'ESP32
#     tension_secondaire = models.FloatField(blank=True, null=True)
#     courant_secondaire = models.FloatField(blank=True, null=True)
#     temperature = models.FloatField(blank=True, null=True)
#     niveau_huile = models.FloatField(blank=True, null=True)

#     # Nouveau champ pour suivre la date et l'heure des mises à jour
#     timestamp = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.code_poste

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


    



