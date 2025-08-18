from django.urls import path
from .views import cadastro, buscar_produtos, editar_produtos, relatorios

urlpatterns = [
    path("", view=cadastro, name="cadastro"),
    path("editar_produtos/", view=editar_produtos, name="editar_produtos"),
    path("buscar_produtos/", view=buscar_produtos, name="buscar_produtos"),
    path("relatorios/", view=relatorios, name="relatorios"),
]
