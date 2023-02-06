from django.urls import path
from . import views

urlpatterns = [
    path('figuras/criar_figuras', views.criar_figuras, name="criar_figuras"),
    path('', views.listar_figuras, name="listar_figuras"),
    path('autores/criar_autores', views.criar_autores, name="criar_autores"),
    path('autores/', views.listar_autores, name="listar_autores"),
    path('artigos/criar_artigos', views.criar_artigos, name="criar_artigos"),
    path('artigos/', views.listar_artigos, name="listar_artigos"),
    # endpoints
    path('api/v1/artigos/', views.dados_artigos, name="listar-artigos"),
    path('api/v1/xml/', views.dados_xml, name="carregar-xml"),
]
