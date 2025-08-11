from django.db import models


class Produto(models.Model):
    nome = models.CharField(verbose_name="Nome", max_length=100, null=True, blank=True)
    categoria = models.IntegerField(
        choices=[(0, "Bebida"), (1, "Comida"), (2, "Outros")],
        null=True,
        blank=True,
    )
    data_validade = models.DateField(
        verbose_name="Data de validade", blank=True, null=True
    )
    codigo_identificador = models.IntegerField(
        verbose_name="Código Indentificador",
        null=True,
        blank=True,
    )
    valor = models.PositiveIntegerField(
        verbose_name="Valor do produto", blank=True, null=True
    )

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome}"


class Estoque(models.Model):
    produto = models.ForeignKey(
        to=Produto,
        on_delete=models.DO_NOTHING,
        related_name="estoque",
    )
    quantidade = models.IntegerField(verbose_name="Quantidade", null=True, blank=True)
    localizacao = models.ForeignKey(
        to="Localizacao",
        on_delete=models.DO_NOTHING,
        related_name="estoque",
        verbose_name="Localizacao",
    )
    ultima_movimentacao = models.DateField(
        verbose_name="Data de movimentacao", blank=True, null=True
    )

    class Meta:
        ordering = ["produto__nome"]

    def __str__(self):
        return f"{self.produto.nome} - {self.localizacao}"


class Localizacao(models.Model):
    corredor = models.CharField(verbose_name="Corredor", blank=True, null=True)
    prateleira = models.IntegerField(verbose_name="Prateleira", null=True, blank=True)

    class Meta:
        ordering = ["corredor"]

    def __str__(self):
        return f"{self.corredor}"
