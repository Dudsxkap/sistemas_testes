from django.contrib import admin
from agendamentos.models import User, Agendamento, AgendamentoDisponivel, EstabelecimentoSaude, GrupoAtendimento, \
    Cidadao
from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.site_header = 'Administração do site'
admin.site.site_title = 'Administração do site'


class EstabelecimentoSaudeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnes',)
    search_fields = ('nome', 'cnes',)
    list_filter = ('nome', 'cnes',)


admin.site.register(User)
admin.site.register(Cidadao)
admin.site.register(Agendamento)
admin.site.register(AgendamentoDisponivel)
admin.site.register(EstabelecimentoSaude, EstabelecimentoSaudeAdmin)
admin.site.register(GrupoAtendimento)
