from django.contrib import admin
from .models import Poste, Gênero, Banco_De_Imagens

# Register your models here.
@admin.register(Poste)
class Post(admin.ModelAdmin):
    list_display=[
        'Título',
        'Autor',
        'Data_de_Publicação',
        'Data_de_Ultima_Publicação',
    ]
    prepopulated_fields={
        'slug':('Título',)
    }
@admin.register(Gênero)
class Genre(admin.ModelAdmin):
    list_display=[
        "Gênero_ou_Chapéu",
        'slug'
    ]
    prepopulated_fields={
        'slug':('Gênero_ou_Chapéu',)
    }
    list_display_links=None
@admin.register(Banco_De_Imagens)
class Banco_De_Imagens(admin.ModelAdmin):
    list_display=[
        'Nome_da_Imagem',
        'slug',
        'Imagens_Para_Corpo_Da_Matéria',
        
    ]
    list_editable=[
        'Imagens_Para_Corpo_Da_Matéria',
    ]
    prepopulated_fields={
        'slug':('Nome_da_Imagem',)
    }
    
   