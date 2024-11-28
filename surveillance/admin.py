from django.contrib import admin
from .models import PosteSource, Depart, Transformateur

class DepartInline(admin.TabularInline):
    model = Depart
    extra = 1

class TransformateurInline(admin.TabularInline):
    model = Transformateur
    extra = 1
    fields = ['code_poste', 'puissance', 'caracteristiques']  # Remplacer nom par code_poste

@admin.register(PosteSource)
class PosteSourceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'localisation']  # Les champs pour PosteSource restent inchangés
    inlines = [DepartInline]

@admin.register(Depart)
class DepartAdmin(admin.ModelAdmin):
    inlines = [TransformateurInline]
    list_display = ['nom', 'get_poste_source_nom']

    def get_poste_source_nom(self, obj):
        return obj.poste_source.nom
    get_poste_source_nom.short_description = 'Poste Source'

@admin.register(Transformateur)
class TransformateurAdmin(admin.ModelAdmin):
    list_display = ['code_poste', 'puissance', 'depart']  # Mettre à jour ici
    fields = ['code_poste', 'puissance', 'depart', 'caracteristiques']  # Mettre à jour ici
