import pandas as pd
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from agendamentos.forms import AutoCadastroUsuario, AgendamentoForm, AgendamentosDisponiveisForm
from django.contrib import messages

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date

from agendamentos.models import AgendamentosDisponiveis, GruposAtendimento, Agendamentos, Vacina


def cadastro_usuario_view(request):
    if request.method == 'POST':
        form = AutoCadastroUsuario(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario_autenticado = authenticate(username=usuario.email, password=form.cleaned_data.get("senha"))
            login(request, usuario_autenticado)
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('index')
    else:
        form = AutoCadastroUsuario()
    context = {'form': form}
    return render(request, 'cadastro_usuario.html', context=context)


def teste(request):
    return render(request, 'teste.html')


@login_required
def deslogar(request):
    logout(request)
    return redirect('login')


@login_required
def agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.user, request.POST)
        if form.is_valid():
            agendamento_feito = Agendamentos.objects.filter(cidadao=request.user)
            if not agendamento_feito.exists():
                qs = AgendamentosDisponiveis.objects.filter(vacina_id=form.cleaned_data.get('vacinas_disponiveis').id,
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
        qs = AgendamentosDisponiveis.objects.filter(vacina_id=request.session['vacina_escolhida'],
                                                    data=request.session['data_escolhida'],
                                                    grupo_id=request.session['grupo_escolhido'],
                                                    num_vagas__gt=0,
                                                    local_vacinacao__cidade=request.session['cidade_escolhida'])
        if request.method == 'POST':
            form = AgendamentosDisponiveisForm(qs, request.POST)
            if form.is_valid():
                    agendamentos_disp = form.cleaned_data.get('agendamentos_disponiveis')
                    novo_agendamento = Agendamentos(agendamento_disponivel=agendamentos_disp,
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
            form = AgendamentosDisponiveisForm(qs)
        context = {'form': form}
        return render(request, 'disponivel.html', context=context)
    else:
        return redirect('index')


@login_required
def meus_agendamentos(request):
    query = Agendamentos.objects.filter(cidadao=request.user)
    info = {}
    if query.exists():
        dados = query[0]
        controle = "1"
        info = {
                'Nome': request.user.nome,
                'Data': dados.agendamento_disponivel.data,
                'Horário': dados.agendamento_disponivel.horario,
                'Grupo de Atendimento': dados.agendamento_disponivel.grupo,
                'Cidade': dados.agendamento_disponivel.local_vacinacao.cidade,
                'Bairro': dados.agendamento_disponivel.local_vacinacao.bairro,
                'Logradouro': dados.agendamento_disponivel.local_vacinacao.logradouro,
                'Local de Vacinação': dados.agendamento_disponivel.local_vacinacao.nome,
                }
    else:
        controle = "0"
    context = {
        'controle': controle,
        'info': info
    }
    return render(request, 'meus_agendamentos.html', context=context)

def graficos(request):
    labels = []
    values = []

    queryset = Vacina.objects.order_by().values_list('fabricante', flat=True).distinct()
    for fabricante_vacina in queryset:
        numero_vacinas = Agendamentos.objects.filter(
            agendamento_disponivel__vacina__fabricante=fabricante_vacina).count()
        if numero_vacinas > 0:
            labels.append(fabricante_vacina)
            values.append(numero_vacinas)

    doughnut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    layout_doughnut = {
        'height': 420,
        'width': 560,
    }

    doughnut.update_layout(title='Agendamentos de vacinação por fabricante')

    plot_doughnut = plot({'data': doughnut, 'layout': layout_doughnut}, output_type='div')

    labels = []
    values = []
    datas = []
    data_atual = date.today()

    for i in range(6, -1, -1):
        datas.append(data_atual - timedelta(days=i))

    for dia in datas:
        labels.append(dia.strftime('%d/%m'))
        data_de_agendamento = Agendamentos.objects.filter(
            data_realizado=dia).count()
        values.append(data_de_agendamento)

    bar = go.Bar(x=labels, y=values)

    layout_bar = {
        'title': 'Agendamentos realizados nos últimos 7 dias',
        'height': 420,
        'width': 560,
    }

    plot_bar = plot({'data': bar, 'layout': layout_bar}, output_type='div')

    context = {
        'plot_doughnut': plot_doughnut,
        'plot_bar': plot_bar
    }

    return render(request, 'index.html', context=context)
