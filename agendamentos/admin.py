from django.contrib import admin
from agendamentos.models import Agendamentos, SalasAgendamento, AgendamentosDisponiveis, Sala, LocalVacinacao, Vacina, \
    GruposAtendimento
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from agendamentos.forms import RegisterForm, UserAdminChangeForm

Usuario = get_user_model()

admin.site.unregister(Group)

admin.site.site_header = 'Administração do site VacinAÇÃO'
admin.site.site_title = 'Administração do site VacinAÇÃO'


class UsuarioAdmin(BaseUserAdmin):
    add_form = RegisterForm
    form = UserAdminChangeForm

    list_display = ('nome', 'email', 'data_nascimento', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('nome', 'email', 'data_nascimento', 'password')}),
        ('Permissões', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome', 'data_nascimento', 'email', 'senha', 'senha_confirmada', 'is_admin')}
         ),
    )
    search_fields = ['nome', 'email']
    ordering = ['nome', 'email']
    filter_horizontal = ()


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


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Agendamentos, AgendamentosAdmin)
admin.site.register(SalasAgendamento, SalasAgendamentoAdmin)
admin.site.register(AgendamentosDisponiveis, AgendamentosDisponiveisAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(LocalVacinacao, LocalVacinacaoAdmin)
admin.site.register(Vacina, VacinaAdmin)
admin.site.register(GruposAtendimento, GruposAtendimentoAdmin)
