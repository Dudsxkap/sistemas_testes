from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

from agendamentos.decorators import cidadao_required, apto_agendamento_required
from agendamentos.forms import CadastroCidadaoForm, AgendamentoForm
from django.contrib import messages

from agendamentos.models import Cidadao
from agendamentos.utils import strftime_local


def index(request):
    return render(request, 'index.html', locals())


def cadastrar_usuario(request):
    form = CadastroCidadaoForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            cidadao = form.save()
            user = cidadao.auth_user
            usuario_autenticado = authenticate(username=user.cpf, password=form.cleaned_data.get("senha"))
            login(request, usuario_autenticado)
            msg = 'Você não está apto para realizar agendamentos de teste.'
            if cidadao.apto_agendamento:
                msg = 'Você está apto para realizar agendamentos de teste.'
            messages.success(request, f'Usuário cadastrado com sucesso! {msg}')
            return redirect('index')
    return render(request, 'cadastro_usuario.html', locals())


@login_required
def deslogar(request):
    logout(request)
    return redirect('index')


@cidadao_required()
@apto_agendamento_required()
def agendamento(request):
    if request.user.cidadao.get_agendamento():
        messages.error(request, "Você já possui um agendamento!")
        return redirect('meus_agendamentos')

    form = AgendamentoForm(request.user.cidadao, request.POST or None)
    if request.POST:
        if form.is_valid():
            agendamento = form.save()
            messages.success(request, "Seu agendamento foi concluído com sucesso!")
            return redirect('meus_agendamentos')

    return render(request, 'agendamento.html', locals())


@cidadao_required()
@apto_agendamento_required()
def meus_agendamentos(request):
    agendamento = request.user.cidadao.get_agendamento()
    dados_agendamento = {}
    if agendamento:
        dados_agendamento = {
            "Data": strftime_local(agendamento.agendamento_disponivel.data, '%d/%m/%Y'),
            "Horário": strftime_local(agendamento.agendamento_disponivel.data, '%H:%M'),
            "Expirado": agendamento.expirado(),
            "Dia da semana": agendamento.agendamento_disponivel.dia_semana(),
            "Estabelecimento de saúde": str(agendamento.agendamento_disponivel.estabelecimento_saude),
        }
    return render(request, 'meus_agendamentos.html', locals())


@cidadao_required()
def graficos(request):
    if not request.user.is_staff:
        return redirect('index')

    labels = []
    data = []
    cidadaos = Cidadao.objects.all().values('apto_agendamento').annotate(qtd=Count('pk'))
    for cidadao in cidadaos:
        labels.append('Apto' if cidadao['apto_agendamento'] else 'Inapto')
        data.append(cidadao['qtd'])
    return render(request, 'graficos.html', locals())

