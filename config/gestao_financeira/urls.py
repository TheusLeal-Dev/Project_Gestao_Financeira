from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transacoes/', views.lista_transacoes, name='lista_transacoes'),
    path('transacoes/nova/', views.nova_transacao, name='nova_transacao'),
]