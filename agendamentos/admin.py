from django.contrib import admin
from agendamentos.models import Agendamentos, SalasAgendamento, AgendamentosDisponiveis, Sala, LocalVacinacao, Vacina, \
    GruposAtendimento

admin.site.site_header = 'Administração do site VacinAÇÃO'
admin.site.site_title = 'Administração do site VacinAÇÃO'


class VacinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'fabricante')
    list_filter = ('nome', 'fabricante')


class GruposAtendimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade_minima')
    list_filter = ('nome', 'idade_minima')


class LocalVacinacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'logradouro', 'bairro', 'cidade')
    list_filter = ('logradouro', 'bairro', 'cidade')


class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nome_local')
    list_filter = ('nome',)


class SalasAgendamentoAdmin(admin.ModelAdmin):
    list_display = ('nome_sala', 'data_agendamento', 'horario_agendamento', 'numero_vagas')


class AgendamentosAdmin(admin.ModelAdmin):
    list_display = ('nome_cidadao', 'nome_grupo', 'data_agendamento', 'horario_agendamento', 'status')
    list_filter = ('status',)


class AgendamentosDisponiveisAdmin(admin.ModelAdmin):
    list_display = ('nome_vacina', 'data', 'horario')
    list_filter = ('data', 'horario')


# Talvez colocar cidadao depois
admin.site.register(Agendamentos, AgendamentosAdmin)
admin.site.register(SalasAgendamento, SalasAgendamentoAdmin)
admin.site.register(AgendamentosDisponiveis, AgendamentosDisponiveisAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(LocalVacinacao, LocalVacinacaoAdmin)
admin.site.register(Vacina, VacinaAdmin)
admin.site.register(GruposAtendimento, GruposAtendimentoAdmin)
