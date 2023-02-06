from django.contrib import admin

from .models import Artigo, Figura, Autor

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Figura)
class FiguraAdmin(admin.ModelAdmin):
    list_display = (
        'rotulo',
        'legenda',
        'imagem'
    )

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo_do_periodico',
        'titulo_do_artigo',
        'volume',
        'numero',
        'ano_de_publicacao'
    )
