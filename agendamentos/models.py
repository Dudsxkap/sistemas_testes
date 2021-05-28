from django.db import models

# Create your models here.
class Cidadao(models.Model):
    nome = models.CharField(max_length=200, help_text='Digite seu nome completo.')
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    email = models.EmailField(max_length=254, help_text="Digite seu email.")
    senha = models.CharField(max_length=50, help_text='Digite sua senha.')

    def __str__(self):
        """String for representing the Model object."""
        return self.nome

    class Meta:
        verbose_name = "Cidadãos"
        verbose_name_plural = "Cidadãos"


class GruposAtendimento(models.Model):
    nome = models.CharField(max_length=200, help_text='Digite o nome do grupo de atendimento.')
    idade_minima = models.IntegerField(verbose_name="Idade mínima")

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.nome} com idade mínima {self.idade_minima}'

    class Meta:
        verbose_name = "Grupos de Atendimento"
        verbose_name_plural = "Grupos de Atendimento"


class Vacina(models.Model):
    nome = models.CharField(max_length=200, help_text='Digite o nome da vacina.')
    fabricante = models.CharField(max_length=200, help_text='Digite o nome do fabricante da vacina.')

    def __str__(self):
        """String for representing the Model object."""
        return f'Vacina {self.nome} ({self.fabricante})'

    class Meta:
        verbose_name = "Vacinas"
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
        verbose_name = "Locais de vacinação"
        verbose_name_plural = "Locais de vacinação"

class Sala(models.Model):
    id_local = models.ForeignKey(LocalVacinacao, verbose_name="Local de Vacinação", on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, help_text='Digite o nome da sala.')

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.nome} no local {self.id_local.nome}'

    class Meta:
        verbose_name = "Salas"
        verbose_name_plural = "Salas"


class AgendamentosDisponiveis(models.Model):
    id_vacina = models.ForeignKey(Vacina,verbose_name="Vacina" ,on_delete=models.CASCADE)
    horario = models.DateTimeField(verbose_name="Horário")


    def __str__(self):
        """String for representing the Model object."""
        return f'Agendamento disponível da vacina {self.id_vacina.nome} em {self.horario}'

    class Meta:
        verbose_name = "Agendamentos Disponíveis"
        verbose_name_plural = "Agendamentos Disponíveis"


class SalasAgendamento(models.Model):
    id_sala = models.ForeignKey(Sala,verbose_name="Sala", on_delete=models.CASCADE)
    id_agendamento_disponivel = models.ForeignKey(AgendamentosDisponiveis,verbose_name="Agendamento Disponível" ,on_delete=models.CASCADE)
    numero_vagas = models.IntegerField(verbose_name="Número de vagas")

    def __str__(self):
        """String for representing the Model object."""
        return f'Agendamento da sala {self.id_sala.nome} em {self.id_agendamento_disponivel.horario}'

    class Meta:
        verbose_name = "Agendamentos por Sala"
        verbose_name_plural = "Agendamentos por Sala"


class Agendamentos(models.Model):
    id_agendamento = models.ForeignKey(AgendamentosDisponiveis, verbose_name="Agendamento", on_delete=models.CASCADE)
    id_cidadao = models.OneToOneField(Cidadao, verbose_name="Nome do Cidadão", on_delete=models.CASCADE)
    id_grupo = models.ForeignKey(GruposAtendimento, verbose_name="Grupo de Atendimento", on_delete=models.CASCADE)

    status_disponiveis=(('a',"Agendado"),('c',"Cancelado"),('v',"Vacinado"))

    status = models.CharField(verbose_name="Status do agendamento", max_length=200, choices=status_disponiveis,
                              help_text='Digite o status do agendamento.')

    def __str__(self):
        """String for representing the Model object."""
        return f'Agendamento de {self.id_cidadao.nome}, grupo {self.id_grupo.nome} em {self.id_agendamento.horario} '

    class Meta:
        verbose_name = "Agendamentos feitos"
        verbose_name_plural = "Agendamentos feitos"
