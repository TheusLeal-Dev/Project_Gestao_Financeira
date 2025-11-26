from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Transações
    path('transacoes/', views.lista_transacoes, name='lista_transacoes'),
    path('nova-transacao/', views.nova_transacao, name='nova_transacao'),
    path('deletar/<int:id>/', views.deletar_transacao, name='deletar_transacao'),

    # Resumos
    path('resumo-anual/', views.resumo_anual, name='resumo_anual'),
    path('resumo-anual/<int:ano>/<int:mes>/', views.resumo_mensal, name='resumo_mensal'),
    path('resumo-anual/mes/<int:mes>/', views.detalhes_mes, name='detalhes_mes'),

    # Registro
    path('registro/', views.registro, name='registro'),
]
