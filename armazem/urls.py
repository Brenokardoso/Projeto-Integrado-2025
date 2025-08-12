from django.urls import path
from .views import cadastro, buscar_produtos

urlpatterns = [
    path("", view=cadastro, name="cadastro"),
    path("produtos/", view=buscar_produtos, name="produtos"),
]
