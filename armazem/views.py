from django.shortcuts import render
from .models import Produto, Localizacao, Estoque
import datetime


def cadastro(request):
    todos_produtos = Produto.objects.all()
    created_prod = False
    created_loc = False
    objetos = {
        "produto_cadastro": [],
        "localizacao_cadastro": [],
        "estoque_cadastro": [],
        "todos_produtos": todos_produtos,
        "flag": True,
        "menu": False,
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

    if nome is not None:
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

    if corredor is not None:
        item_localizacao, created_loc = Localizacao.objects.update_or_create(
            corredor=corredor,
            prateleira=prateleira,
            defaults={
                "corredor": corredor,
                "prateleira": prateleira,
            },
        )

    if created_prod and created_loc:
        item_produto.save()
        item_localizacao.save()
        objetos["produto_cadastro"].append(item_produto)
        objetos["localizacao_cadastro"].append(item_localizacao)

        item_estoque, _ = Estoque.objects.update_or_create(
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

    return render(
        request=request,
        template_name="cadastro.html",
        context=objetos,
    )


def buscar_produtos(request):
    query = request.GET.get("item", "")
    query_loc = request.GET.get("loc", "")

    localizacoes = Localizacao.objects.all()
    estoques = Estoque.objects.all().exclude(quantidade__isnull=True)

    if query:
        produtos = Produto.objects.filter(nome__icontains=query).order_by("nome")

    elif query_loc:
        produtos = Produto.objects.filter(
            estoque__localizacao__corredor__icontains=query_loc
        ) | Produto.objects.filter(
            estoque__localizacao__prateleira__icontains=query_loc
        )
        produtos = produtos.distinct().order_by("nome")

    else:
        produtos = Produto.objects.all().order_by("nome").exclude(nome__isnull=True)

    lista_itens = {
        "produtos": produtos,
        "localizacoes": localizacoes,
        "estoques": estoques,
        "produtos_estoques": zip(produtos, estoques),
        "query": query,
        "query_loc": query_loc,
    }

    return render(
        request=request,
        template_name="buscar_produtos.html",
        context=lista_itens,
    )


def editar_produtos(request):
    escolha_produto = Produto.objects.all()
    web_produto = request.POST.get("escolha_produto")
    if web_produto is not None:
        produto_update = Produto.objects.get(pk=web_produto)
        estoque_update = Estoque.objects.get(produto=produto_update)
        localizacao_update = Localizacao.objects.get(estoque_localizacao=estoque_update)

        nome = request.POST.get("nome")
        categoria = request.POST.get("categoria")
        data_validade = request.POST.get("data_validade")
        codigo_identificador = request.POST.get("codigo_identificador")
        valor = request.POST.get("valor")

        corredor = request.POST.get("corredor")
        prateleira = request.POST.get("prateleira")

        quantidade = request.POST.get("quantidade")
        data_atual = datetime.datetime.now()

        produto_update.nome = nome
        produto_update.categoria = categoria
        produto_update.data_validade = data_validade
        produto_update.codigo_identificador = codigo_identificador
        produto_update.valor = valor
        produto_update.save()

        estoque_update.quantidade = quantidade
        estoque_update.ultima_movimentacao = data_atual
        estoque_update.save()

        localizacao_update.corredor = corredor
        localizacao_update.prateleira = prateleira
        localizacao_update.save()

        print(f"{nome}-{quantidade}")

    return render(
        request,
        template_name="editar.html",
        context={
            "todos_produtos": web_produto,
            "escolha_produto": escolha_produto,
        },
    )


def relatorios(request):
    estoque_baixo = Estoque.objects.filter(quantidade__lte=5)
    excesso_estoque = Estoque.objects.filter(quantidade__gte=100)
    movimentacoes = Estoque.objects.exclude(ultima_movimentacao__isnull=True).order_by(
        "-ultima_movimentacao"
    )

    contexto = {
        "estoque_baixo": estoque_baixo,
        "excesso_estoque": excesso_estoque,
        "movimentacoes": movimentacoes,
    }

    return render(request, template_name="relatorios.html", context=contexto)
