from django.contrib import admin
from .models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'valor', 'data', 'tipo', 'categoria', 'usuario']
    list_filter = ['tipo', 'categoria', 'data']