from django.shortcuts import render


def cadastro(request):
    data = {"data": [1, 2, 3, 4, 5, 6, 7, 8]}
    nome = request.POST.get("data_validade")
    print(nome or "Vazio")
    return render(request=request, template_name="cadastro.html", context=data)
