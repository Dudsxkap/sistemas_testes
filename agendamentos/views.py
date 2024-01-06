import pandas as pd
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import render, redirect
from agendamentos.forms import CadastroCidadaoForm, AgendamentoForm, AgendamentoDisponivelForm
from django.contrib import messages

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date

from agendamentos.models import AgendamentoDisponivel, GrupoAtendimento, Agendamento, Cidadao


def cadastrar_usuario(request):
    form = CadastroCidadaoForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            cidadao = form.save()
            user = cidadao.auth_user
            usuario_autenticado = authenticate(username=user.cpf, password=form.cleaned_data.get("senha"))
            login(request, usuario_autenticado)
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('index')
    return render(request, 'cadastro_usuario.html', locals())


@login_required
def deslogar(request):
    logout(request)
    return redirect('login')


@login_required
def agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.user, request.POST)
        if form.is_valid():
            agendamento_feito = Agendamento.objects.filter(cidadao=request.user)
            if not agendamento_feito.exists():
                qs = AgendamentoDisponivel.objects.filter(vacina_id=form.cleaned_data.get('vacinas_disponiveis').id,
                                                            data=form.cleaned_data.get('data'),
                                                            grupo=form.cleaned_data.get(
                                                                'grupos_disponiveis'),
                                                            local_vacinacao__cidade=form.cleaned_data.get(
                                                                'cidades_disponiveis').cidade,
                                                            num_vagas__gt=0)

                if qs.exists():
                    request.session['data_escolhida'] = form.cleaned_data.get('data')
                    request.session['cidade_escolhida'] = form.cleaned_data.get('cidades_disponiveis').cidade
                    request.session['vacina_escolhida'] = form.cleaned_data.get('vacinas_disponiveis').id
                    request.session['grupo_escolhido'] = form.cleaned_data.get('grupos_disponiveis').id

                    return redirect('agendamentos_disponiveis')
                else:
                    messages.error(request, "Não existem agendamentos disponíveis para esses parâmetros.")
            else:
                messages.error(request, "Você já possui um agendamento!")
    else:
        form = AgendamentoForm(request.user)
    context = {'form': form}
    return render(request, 'agendamento.html', context=context)


@login_required
def agendamentos_disponiveis(request):
    if "data_escolhida" in request.session:
        qs = AgendamentoDisponivel.objects.filter(vacina_id=request.session['vacina_escolhida'],
                                                    data=request.session['data_escolhida'],
                                                    grupo_id=request.session['grupo_escolhido'],
                                                    num_vagas__gt=0,
                                                    local_vacinacao__cidade=request.session['cidade_escolhida'])
        if request.method == 'POST':
            form = AgendamentoDisponivelForm(qs, request.POST)
            if form.is_valid():
                    agendamentos_disp = form.cleaned_data.get('agendamentos_disponiveis')
                    novo_agendamento = Agendamento(agendamento_disponivel=agendamentos_disp,
                                                    cidadao=request.user,
                                                    )
                    with transaction.atomic():
                        novo_agendamento.save()
                        agendamentos_disp.num_vagas -= 1
                        agendamentos_disp.save()

                    request.session.pop('data_escolhida')
                    request.session.pop('cidade_escolhida')
                    request.session.pop('vacina_escolhida')
                    request.session.pop('grupo_escolhido')
                    request.session.modified = True

                    messages.success(request, "Seu agendamento foi concluido com sucesso!")
                    return redirect('meus_agendamentos')
        else:
            form = AgendamentoDisponivelForm(qs)
        context = {'form': form}
        return render(request, 'disponivel.html', context=context)
    else:
        return redirect('index')


@login_required
def meus_agendamentos(request):
    agendamento = Agendamento.objects.filter(cidadao=request.user.cidadao).first()
    dados_agendamento = {}
    if agendamento:
        info = {
            "Data": agendamento.agendamento_disponivel.data.strftime('%d/%m/%Y'),
            "Horário": agendamento.agendamento_disponivel.data.strftime('%H:%M'),
            "Expirado": agendamento.expirado(),
            "Dia da semana": agendamento.agendamento_disponivel.dia_semana(),
            "Estabelecimento de saúde": str(agendamento.agendamento_disponivel.estabelecimento_saude),
        }
    return render(request, 'meus_agendamentos.html', locals())


@login_required
def graficos(request):
    labels = []
    data = []
    cidadaos = Cidadao.objects.all().values('apto_agendamento').annotate(qtd=Count('pk'))
    for cidadao in cidadaos:
        labels.append('Apto' if cidadao['apto_agendamento'] else 'Inapto')
        data.append(cidadao['qtd'])
    return render(request, 'index.html', locals())

