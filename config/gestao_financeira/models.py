from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Transacao(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
        ('investimento', 'Investimento'),   # <-- ADICIONADO
    ]

    CATEGORIA_CHOICES = [
        ('salario', 'Salário'),
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('moradia', 'Moradia'),
        ('lazer', 'Lazer'),
        ('outros', 'Outros'),
        ('investimento', 'Investimento'),  # <-- ADICIONADO
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=timezone.now)
    tipo = models.CharField(max_length=12, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
