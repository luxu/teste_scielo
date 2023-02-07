from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_figuras, name="listar_figuras"),
    # endpoints
    path('api/v1/artigos/', views.dados_artigos, name="listar-artigos"),
    path('api/v1/xml/', views.dados_xml, name="carregar-xml"),
]
