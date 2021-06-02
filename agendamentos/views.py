from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from agendamentos.forms import AutoCadastroUsuario, AgendamentoForm, AgendamentosDisponiveisForm
from django.contrib import messages
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from chartjs.views.pie import HighChartPieView
from random import randint

from agendamentos.models import AgendamentosDisponiveis, GruposAtendimento, Agendamentos


class IndexView(TemplateView):
    template_name = 'index.html'


class DadosJSONView(BaseLineChartView):
    # eixox
    def get_labels(self):
        labels = [
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]
        return labels

    def get_providers(self):
        # datasets
        datasets = [
            "P1",
        ]
        return datasets

    def get_data(self):
        # retorna datasets pro plto, cada linha representa um dataset, cada coluna um label
        # quantidade de dados precisa ser datasets/labels: 12 labrl=12 colunas, 4 data 4 linha
        dados = []
        for l in range(1):
            for c in range(12):
                dado = [
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                    randint(1, 200),
                ]
            dados.append(dado)
        return dados


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
    qs = AgendamentosDisponiveis.objects.filter(vacina_id=request.session['vacina_escolhida'],
                                                data=request.session['data_escolhida'],
                                                num_vagas__gt=0,
                                                local_vacinacao__cidade=request.session['cidade_escolhida'])
    if request.method == 'POST':
        form = AgendamentosDisponiveisForm(qs, request.POST)
        if form.is_valid():
                grupo = GruposAtendimento.objects.get(id=request.session['grupo_escolhido'])
                agendamentos_disp = form.cleaned_data.get('agendamentos_disponiveis')
                novo_agendamento = Agendamentos(agendamento_disponivel=agendamentos_disp,
                                                cidadao=request.user,
                                                grupo=grupo
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
                return redirect('index')
    else:
        form = AgendamentosDisponiveisForm(qs)
    context = {'form': form}
    return render(request, 'disponivel.html', context=context)


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
                'Grupo de Atendimento': dados.grupo,
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
