from datetime import date

from localflavor.br.forms import BRCPFField
from django import forms

from agendamentos.models import User, Cidadao, GrupoAtendimento
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
                    'type': 'date'
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


class AgendamentoForm(forms.Form):
    data = forms.CharField(label='Data do agendamento', widget=forms.DateInput(
        format='%Y-%m-%d',
        attrs={'class': 'form-control',
               'placeholder': 'Selecione uma data',
               'type': 'date'
               }))

    def __init__(self, usuario, *args, **kwargs):
        super(AgendamentoForm, self).__init__(*args, **kwargs)
        self.usuario = usuario
        data_nascimento = self.usuario.data_nascimento
        data_atual = date.today()
        try:
            data_nascimento = data_nascimento.replace(year=data_atual.year)
        except ValueError:
            data_nascimento = data_nascimento.replace(year=data_atual.year,
                                                      month=data_nascimento.month + 1, day=1)
        idade = 0
        if data_nascimento > data_atual:
            idade = data_atual.year - data_nascimento.year - 1
        else:
            idade = data_atual.year - data_nascimento.year
        self.fields['grupos_disponiveis'] = forms.ModelChoiceField(label='Grupos disponíveis',
                                                                   queryset=GrupoAtendimento.objects.filter(
                                                                       idade_minima__gte=idade))


class AgendamentoDisponivelForm(forms.Form):
    def __init__(self, qs, *args, **kwargs):
        super(AgendamentoDisponivelForm, self).__init__(*args, **kwargs)
        self.fields['agendamentos_disponiveis'] = forms.ModelChoiceField(label='Agendamentos disponíveis',
                                                                         queryset=qs)
