from django.urls import path
from .views import cadastro,listar_produtos

urlpatterns = [
    path("", view=cadastro, name="cadastro"),
    path("produtos/", view=listar_produtos, name="produtos"),

]
