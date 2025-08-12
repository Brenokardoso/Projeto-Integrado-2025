from django.shortcuts import render
from .models import Produto, Localizacao, Estoque
import datetime


def cadastro(request):
    objetos = {
        "produto_cadastro": [],
        "localizacao_cadastro": [],
        "estoque_cadastro": [],
    }
    nome = request.POST.get("nome")
    categoria = request.POST.get("categoria")
    data_validade = request.POST.get("data_validade")
    codigo_identificador = request.POST.get("codigo_identificador")
    valor = request.POST.get("valor")

    corredor = request.POST.get("corredor")
    prateleira = request.POST.get("prateleira")

    quantidade = request.POST.get("quantidade")
    data_atual = datetime.datetime.now()

    item_produto, created_prod = Produto.objects.update_or_create(
        nome=nome,
        codigo_identificador=codigo_identificador,
        defaults={
            "nome": nome,
            "categoria": categoria,
            "data_validade": data_validade,
            "codigo_identificador": codigo_identificador,
            "valor": valor,
        },
    )

    item_localizacao, created_loc = Localizacao.objects.update_or_create(
        corredor=corredor,
        prateleira=prateleira,
        defaults={"corredor": corredor, "prateleira": prateleira},
    )

    if created_prod and created_loc:
        item_produto.save()
        item_localizacao.save()
        objetos["produto_cadastro"].append(item_produto)
        objetos["localizacao_cadastro"].append(item_localizacao)

        item_estoque, created_estoque = Estoque.objects.update_or_create(
            produto=item_produto,
            defaults={
                "quantidade": quantidade,
                "produto": item_produto,
                "localizacao": item_localizacao,
                "ultima_movimentacao": data_atual,
            },
        )
        item_estoque.save()
        objetos["estoque_cadastro"].append(item_estoque)

    return render(request=request, template_name="cadastro.html", context=objetos)


def buscar_produtos(request):
    produtos = None
    localizacoes = Localizacao.objects.all()
    lista_itens = {"produtos": produtos, "localizacoes": localizacoes}
    estoques = Estoque.objects.all()

    if request.method == "POST":
        produtos = Produto.objects.all().order_by("nome").exclude(nome__isnull=True)
        lista_itens = {
            "produtos": produtos,
            "localizacoes": localizacoes,
            "estoques": estoques,
            "produtos_estoques": zip(produtos, estoques),
        }

    return render(request=request, template_name="cadastro.html", context=lista_itens)


def editar_produtos(request, name):
    if request.method == "POST":
        nome_produto = request.POST.get("nome_produto")
        Produto.objects.filter(nome__icontains=nome_produto)
        return render(
            request,
            template_name="cadastro.html",
            context={"produto_encontrado": nome_produto},
        )
