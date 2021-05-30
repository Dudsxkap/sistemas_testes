from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

Usuario = get_user_model()


class RegisterForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    senha_confirmada = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('nome', 'data_nascimento', 'email', 'is_admin')

    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs = Usuario.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Esse email já foi cadastrado')
        return email

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        senha = cleaned_data.get('senha')
        senha_confirmada = cleaned_data.get('senha_confirmada')
        if senha and senha_confirmada and senha != senha_confirmada:
            raise forms.ValidationError("Suas senhas não coincidem")
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
