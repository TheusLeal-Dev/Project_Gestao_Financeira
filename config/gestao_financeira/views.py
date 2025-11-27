from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from calendar import month_name
from .models import Transacao
from .forms import TransacaoForm
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')


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


# VIEW 5 - Deletar transação
@login_required
def deletar_transacao(request, id):
    transacao = get_object_or_404(Transacao, id=id, usuario=request.user)
    transacao.delete()
    return redirect('dashboard')


# VIEW 6 - Resumo Anual
@login_required
def resumo_anual(request):
    ano_atual = date.today().year
    dados_mensais = []

    meses_nomes = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    for mes in range(1, 13):
        receitas = Transacao.objects.filter(
            usuario=request.user,
            tipo='receita',
            data__year=ano_atual,
            data__month=mes
        ).aggregate(Sum('valor'))['valor__sum'] or 0

        despesas = Transacao.objects.filter(
            usuario=request.user,
            tipo='despesa',
            data__year=ano_atual,
            data__month=mes
        ).aggregate(Sum('valor'))['valor__sum'] or 0

        dados_mensais.append({
            'mes_num': mes,                 # <-- número do mês (1 a 12)
            'mes_nome': meses_nomes[mes-1], # <-- nome do mês
            'receitas': receitas,
            'despesas': despesas,
            'saldo': receitas - despesas
        })

    return render(request, 'resumo_anual.html', {'dados_mensais': dados_mensais})


# VIEW 7 - Resumo Mensal (opcional, caso você use)
@login_required
def resumo_mensal(request, ano, mes):
    transacoes = Transacao.objects.filter(
        usuario=request.user,
        data__year=ano,
        data__month=mes
    ).order_by('-data')

    total_receitas = transacoes.filter(tipo='receita').aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = transacoes.filter(tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_receitas - total_despesas

    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    nome_mes = meses[mes - 1]

    context = {
        'transacoes': transacoes,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'mes': nome_mes,
        'ano': ano
    }

    return render(request, 'resumo_mensal.html', context)


# VIEW 8 - Detalhes do Mês
@login_required
def detalhes_mes(request, mes):
    ano = date.today().year

    transacoes = Transacao.objects.filter(
        usuario=request.user,
        data__month=mes,
        data__year=ano
    ).order_by('-data')

    total_receitas = transacoes.filter(tipo='receita').aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = transacoes.filter(tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_receitas - total_despesas

    nome_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    context = {
        'mes_num': mes,
        'mes_nome': nome_meses.get(mes, "Mês inválido"),
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'transacoes': transacoes
    }

    return render(request, 'detalhes_mes.html', context)
