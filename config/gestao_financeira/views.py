# gestao_financeira/views.py - TODAS AS 3 VIEWS JUNTAS NUM ÚNICO ARQUIVO

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from .models import Transacao
from .forms import TransacaoForm


# VIEW 1 - Registro de usuário
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})


# VIEW 2 - Dashboard principal
@login_required
def dashboard(request):
    hoje = date.today()
    transacoes_mes = Transacao.objects.filter(
        usuario=request.user,
        data__month=hoje.month,
        data__year=hoje.year
    )

    total_receitas = transacoes_mes.filter(tipo='receita').aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = transacoes_mes.filter(tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_receitas - total_despesas

    ultimas_transacoes = Transacao.objects.filter(usuario=request.user).order_by('-data')[:5]

    context = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'ultimas_transacoes': ultimas_transacoes,
    }

    return render(request, 'dashboard.html', context)


# VIEW 3 - Lista de transações
@login_required
def lista_transacoes(request):
    transacoes = Transacao.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'lista_transacoes.html', {'transacoes': transacoes})


# VIEW 4 - Nova transação
@login_required
def nova_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user
            transacao.save()
            messages.success(request, 'Transação cadastrada com sucesso!')
            return redirect('dashboard')
    else:
        form = TransacaoForm()

    return render(request, 'nova_transacao.html', {'form': form})