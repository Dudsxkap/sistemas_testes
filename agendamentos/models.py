from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


Cidadao = settings.AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def create_user(self, email, nome, data_nascimento, password=None):
        user = self.model(
            email=self.normalize_email(email),
            nome=nome,
            data_nascimento=data_nascimento
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nome, data_nascimento, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            nome=nome,
            data_nascimento=data_nascimento,
            password=password
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nome = models.CharField(verbose_name="Nome completo", max_length=200)
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(verbose_name="Administrador", default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nome', 'data_nascimento']

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.nome

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['nome', 'email']


class GruposAtendimento(models.Model):
    nome = models.CharField(max_length=200, help_text='Digite o nome do grupo de atendimento.')
    idade_minima = models.IntegerField(verbose_name="Idade mínima")

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.nome} com idade mínima {self.idade_minima}'

    class Meta:
        ordering = ['nome', 'idade_minima']
        verbose_name = "Grupo de Atendimento"
        verbose_name_plural = "Grupos de Atendimento"


class Vacina(models.Model):
    nome = models.CharField(max_length=200, help_text='Digite o nome da vacina.')
    fabricante = models.CharField(max_length=200, help_text='Digite o nome do fabricante da vacina.')

    def __str__(self):
        """String for representing the Model object."""
        return f'Vacina {self.nome} ({self.fabricante})'

    class Meta:
        ordering = ['nome', 'fabricante']
        verbose_name = "Vacina"
        verbose_name_plural = "Vacinas"


class LocalVacinacao(models.Model):
    nome = models.CharField(max_length=200, help_text='Digite o nome do local.')
    logradouro = models.CharField(max_length=200, help_text='Digite o logradouro.')
    bairro = models.CharField(max_length=200, help_text='Digite o bairro.')
    cidade = models.CharField(max_length=200, help_text='Digite a cidade.')
    cnes = models.CharField(verbose_name="CNES", max_length=200, help_text='Digite o CNES.')

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.nome} na {self.logradouro}, bairro {self.bairro} em {self.cidade} '

    class Meta:
        ordering = ['cidade', 'bairro', 'logradouro', 'nome']
        verbose_name = "Local de Vacinação"
        verbose_name_plural = "Locais de Vacinação"


class Sala(models.Model):
    id_local = models.ForeignKey(LocalVacinacao, verbose_name="Local de Vacinação", on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, help_text='Digite o nome da sala.')

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.nome} no local {self.id_local.nome}'

    def nome_local(self):
        return self.id_local.nome

    nome_local.short_description = "Local"

    class Meta:
        ordering = ['nome']
        verbose_name = "Sala"
        verbose_name_plural = "Salas"


class AgendamentosDisponiveis(models.Model):
    id_vacina = models.ForeignKey(Vacina, verbose_name="Vacina", on_delete=models.CASCADE)
    horario = models.TimeField(verbose_name="Horário")
    data = models.DateField()

    def __str__(self):
        """String for representing the Model object."""
        return f'Agendamento disponível da vacina {self.id_vacina.nome} na data {self.data} às {self.horario}'

    def nome_vacina(self):
        return self.id_vacina.nome

    nome_vacina.short_description = "Vacina"

    class Meta:
        ordering = ['data', 'horario']
        verbose_name = "Agendamentos Disponíveis"
        verbose_name_plural = "Agendamentos Disponíveis"


class SalasAgendamento(models.Model):
    id_sala = models.ForeignKey(Sala, verbose_name="Sala", on_delete=models.CASCADE)
    id_agendamento_disponivel = models.ForeignKey(AgendamentosDisponiveis, verbose_name="Agendamento Disponível",
                                                  on_delete=models.CASCADE)
    numero_vagas = models.IntegerField(verbose_name="Número de Vagas")

    def __str__(self):
        """String for representing the Model object."""
        return f'Agendamento da sala {self.id_sala.nome} na data {self.id_agendamento_disponivel.data} às ' \
               f'{self.id_agendamento_disponivel.horario}'

    def nome_sala(self):
        return self.id_sala.nome

    nome_sala.short_description = "Sala"

    def data_agendamento(self):
        return self.id_agendamento_disponivel.data

    data_agendamento.short_description = "Data"

    def horario_agendamento(self):
        return self.id_agendamento_disponivel.horario

    horario_agendamento.short_description = "Horário"

    class Meta:
        ordering = ['-numero_vagas']
        verbose_name = "Agendamentos por Sala"
        verbose_name_plural = "Agendamentos por Sala"


class Agendamentos(models.Model):
    id_agendamento_disponivel = models.ForeignKey(AgendamentosDisponiveis, verbose_name="Agendamento",
                                                  on_delete=models.CASCADE)
    id_cidadao = models.OneToOneField(Cidadao, verbose_name="Nome do Cidadão", on_delete=models.CASCADE)
    id_grupo = models.ForeignKey(GruposAtendimento, verbose_name="Grupo de Atendimento", on_delete=models.CASCADE)

    status_disponiveis = (('a', "Agendado"), ('c', "Cancelado"), ('v', "Vacinado"))

    status = models.CharField(verbose_name="Status do agendamento", max_length=200, choices=status_disponiveis,
                              help_text='Digite o status do agendamento.')

    def __str__(self):
        """String for representing the Model object."""
        return f'Agendamento de {self.id_cidadao.nome}, grupo {self.id_grupo.nome} na data ' \
               f'{self.id_agendamento_disponivel.data} em {self.id_agendamento_disponivel.horario} '

    def nome_cidadao(self):
        return self.id_cidadao.nome
    id_cidadao.short_description = "Cidadão"

    def data_agendamento(self):
        return self.id_agendamento_disponivel.data

    data_agendamento.short_description = "Data"

    def horario_agendamento(self):
        return self.id_agendamento_disponivel.horario

    horario_agendamento.short_description = "Horário"

    def nome_grupo(self):
        return self.id_grupo.nome

    nome_grupo.short_description = "Grupo de atendimento"

    class Meta:
        ordering = ['status']
        verbose_name = "Agendamentos Feitos"
        verbose_name_plural = "Agendamentos Feitos"
