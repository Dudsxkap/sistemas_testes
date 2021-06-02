from datetime import date
from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from agendamentos.models import LocalVacinacao, Vacina, GruposAtendimento

Usuario = get_user_model()


class RegisterForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    senha_confirmada = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('nome', 'data_nascimento', 'email', 'is_admin')
        localized_fields = ('data_nascimento',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Usuario.objects.filter(email=email)
        if qs.exists():
            self.add_error('email', "Esse email já foi cadastrado")
        return email

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        senha = cleaned_data.get('senha')
        senha_confirmada = cleaned_data.get('senha_confirmada')
        if senha:
            try:
                password_validation.validate_password(senha, self.instance)
            except ValidationError as error:
                self.add_error('senha', error)
        if senha and senha_confirmada and senha != senha_confirmada:
            self.add_error('senha', "Suas senhas não coincidem")
            self.add_error('senha_confirmada', "Suas senhas não coincidem")
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["senha"])
        if commit:
            usuario.save()
        return usuario


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('nome', 'data_nascimento', 'password', 'email', 'is_active', 'is_admin')


class AutoCadastroUsuario(RegisterForm):
    class Meta(RegisterForm.Meta):
        exclude = ('is_admin',)
        widgets = {
            'data_nascimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control',
                       'placeholder': 'Selecione uma data',
                       'type': 'date'
                       }),
        }


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.cidade


class AgendamentoForm(forms.Form):
    data = forms.CharField(label='Data do agendamento', widget=forms.DateInput(
        format='%Y-%m-%d',
        attrs={'class': 'form-control',
               'placeholder': 'Selecione uma data',
               'type': 'date'
               }))
    cidades_disponiveis = CustomModelChoiceField(label='Cidades disponíveis',
                                                 queryset=LocalVacinacao.objects.all().distinct("cidade"))
    vacinas_disponiveis = forms.ModelChoiceField(label='Vacinas disponíveis',
                                                 queryset=Vacina.objects.all())

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
                                                                   queryset=GruposAtendimento.objects.filter(
                                                                       idade_minima__gte=idade))


class AgendamentosDisponiveisForm(forms.Form):
    def __init__(self, qs, *args, **kwargs):
        super(AgendamentosDisponiveisForm, self).__init__(*args, **kwargs)
        self.fields['agendamentos_disponiveis'] = forms.ModelChoiceField(label='Agendamentos disponíveis',
                                                                         queryset=qs)
