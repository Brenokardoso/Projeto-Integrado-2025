from django.urls import path
from .views import cadastro, buscar_produtos, editar_produtos

urlpatterns = [
    path("", view=cadastro, name="cadastro"),
    path("produtos/", view=buscar_produtos, name="produtos"),
    path("editar_produtos/", view=editar_produtos, name="editar_produtos"),
]
