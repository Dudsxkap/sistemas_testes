from dateutil.relativedelta import relativedelta
from django.conf import settings
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from localflavor.br.models import BRCPFField


class UserManager(BaseUserManager):
    def create_user(self, cpf, password):
        user = self.model(cpf=cpf)
        user.password = make_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, cpf, password=None):
        user = self.create_user(cpf=cpf, password=password)
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser):
    cpf = BRCPFField(verbose_name="CPF", unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, verbose_name="Administrador")

    USERNAME_FIELD = "cpf"

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Cidadao(models.Model):
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    grupos_atendimento = models.ManyToManyField('GrupoAtendimento', verbose_name='Grupos de atendimento')
    teve_covid = models.BooleanField(verbose_name="Teve COVID-19 nos últimos 30 dias?")
    apto_agendamento = models.BooleanField(verbose_name="Está apto para agendamento?")
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cidadao")

    def __str__(self):
        return self.nome

    def is_apto_agendamento(self):
        nome_grupos_excluidos = ['População Privada de Liberdade', 'Pessoas com Deficiência Institucionalizadas',
                                 'Pessoas ACAMADAS de 80 anos ou mais']

        if (
                self.idade >= 18 and not self.teve_covid and
                not self.grupos_atendimento.filter(nome__in=nome_grupos_excluidos).exists()
        ):
            return True
        return False

    @property
    def idade(self):
        idade = relativedelta(datetime.now().date(), self.data_nascimento)
        return idade.years


class GrupoAtendimento(models.Model):
    nome = models.CharField(max_length=200)
    codigo_si_pni = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Grupo de Atendimento"
        verbose_name_plural = "Grupos de Atendimento"


class EstabelecimentoSaude(models.Model):
    nome = models.CharField(max_length=200)
    cnes = models.CharField(verbose_name="CNES", max_length=200)

    def __str__(self):
        return f"{self.cnes} - {self.nome}"

    class Meta:
        verbose_name = "Estabelecimento de Saúde"
        verbose_name_plural = "Estabelecimentos de Saúde"


class AgendamentoDisponivel(models.Model):
    data = models.DateField()
    horario = models.TimeField(verbose_name="Horário")
    num_vagas = models.IntegerField(verbose_name="Número de vagas")
    idade_inicial = models.IntegerField(verbose_name="Idade inicial")
    idade_final = models.IntegerField(verbose_name="Idade final")
    estabelecimento_saude = models.ForeignKey(
        "EstabelecimentoSaude",
        verbose_name="Estabelecimento de Saúde",
        on_delete=models.CASCADE,
        related_name="agendamento_disponivel"
    )

    def __str__(self):
        return f"{self.data} {self.horario} - {self.estabelecimento_saude} - {self.num_vagas} vagas"

    class Meta:
        verbose_name = "Agendamentos Disponíveis"
        verbose_name_plural = "Agendamentos Disponíveis"


class Agendamento(models.Model):
    agendamento_disponivel = models.ForeignKey(AgendamentoDisponivel, verbose_name="Agendamento",
                                               on_delete=models.CASCADE)
    cidadao = models.OneToOneField(Cidadao, verbose_name="Cidadão", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cidadao} - {self.agendamento_disponivel}"

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
