from django.contrib import admin
from armazem.models import Produto, Estoque, Localizacao

admin.site.register(Produto)
admin.site.register(Estoque)
admin.site.register(Localizacao)
