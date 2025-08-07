from django.urls import path
from .views import cadastro

urlpatterns = [
    path("", view=cadastro, name="cadastro"),
]
