from datetime import datetime

from django.db import transaction
from localflavor.br.forms import BRCPFField
from django import forms

from agendamentos.models import User, Cidadao, AgendamentoDisponivel, Agendamento
from agendamentos.utils import digits


class CadastroCidadaoForm(forms.ModelForm):
    cpf = BRCPFField(label='CPF')
    senha = forms.CharField(widget=forms.PasswordInput)
    senha_confirmada = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput)

    class Meta:
        model = Cidadao
        fields = ['cpf', 'nome', 'data_nascimento', 'grupos_atendimento', 'teve_covid', 'senha', 'senha_confirmada']
        widgets = {
            'data_nascimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Selecione uma data',
                    'type': 'date',
                    'max': datetime.now().date(),
                }
            ),
        }

    def clean_cpf(self):
        cpf = digits(self.cleaned_data.get('cpf'))
        qs = User.objects.filter(cpf=cpf)
        if qs.exists():
            self.add_error('cpf', "Esse CPF já foi cadastrado.")
        return cpf

    def clean(self):
        senha = self.cleaned_data.get("senha")
        senha_confirmada = self.cleaned_data.get("senha_confirmada")
        if senha and senha_confirmada and senha != senha_confirmada:
            self.add_error("senha", "Suas senhas não coincidem.")
            self.add_error("senha_confirmada", "Suas senhas não coincidem.")
        return self.cleaned_data

    def save(self, commit=True):
        cpf = self.cleaned_data.get("cpf")
        senha = self.cleaned_data.get("senha")
        grupos_atendimento = self.cleaned_data.get('grupos_atendimento')

        cidadao = super().save(commit=False)
        usuario = User.objects.create_user(cpf, senha)
        cidadao.auth_user = usuario
        cidadao.save()
        cidadao.grupos_atendimento.add(*grupos_atendimento)
        cidadao.apto_agendamento = cidadao.is_apto_agendamento()
        cidadao.save()
        return cidadao


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['agendamento_disponivel']

    def __init__(self, cidadao, *args, **kwargs):
        super(AgendamentoForm, self).__init__(*args, **kwargs)
        self.cidadao = cidadao
        idade = self.cidadao.idade
        self.fields['agendamento_disponivel'] = forms.ModelChoiceField(
            label='Agendamentos disponíveis',
            queryset=AgendamentoDisponivel.objects.filter(
                idade_inicial__lte=idade, idade_final__gte=idade, data__gt=datetime.now(),
                num_vagas__gt=0
            ).order_by('data')
        )

    @transaction.atomic()
    def save(self, commit=True):
        agendamento_disponivel = self.cleaned_data.get('agendamento_disponivel')

        agendamento = super().save(commit=False)
        agendamento.cidadao = self.cidadao
        if commit:
            agendamento.save()
            agendamento_disponivel.num_vagas -= 1
            agendamento_disponivel.save()
        return agendamento
