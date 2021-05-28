from django.contrib import admin
from agendamentos.models import Agendamentos, SalasAgendamento, AgendamentosDisponiveis, Sala, LocalVacinacao, Vacina, \
    GruposAtendimento#, Cidadao
# Talvez colocar cidadao depois
admin.site.register(Agendamentos)
admin.site.register(SalasAgendamento)
admin.site.register(AgendamentosDisponiveis)
admin.site.register(Sala)
admin.site.register(LocalVacinacao)
admin.site.register(Vacina)
admin.site.register(GruposAtendimento)

