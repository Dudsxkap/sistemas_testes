from django.contrib import admin
from agendamentos.models import Agendamento, AgendamentoDisponivel, EstabelecimentoSaude, GrupoAtendimento
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

Usuario = get_user_model()

admin.site.unregister(Group)

admin.site.site_header = 'Administração do site VacinAÇÃO'
admin.site.site_title = 'Administração do site VacinAÇÃO'


"""class UsuarioAdmin(BaseUserAdmin):
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


class GrupoAtendimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade_minima')
    list_filter = ('nome', 'idade_minima')


class EstabelecimentoSaudeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'logradouro', 'bairro', 'cidade')
    list_filter = ('logradouro', 'bairro', 'cidade')


class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('nome_cidadao', 'nome_grupo', 'data_agendamento', 'horario_agendamento', 'status')
    list_filter = ('status',)


class AgendamentoDisponivelAdmin(admin.ModelAdmin):
    list_display = ('nome_local', 'nome_vacina', 'data', 'horario', 'num_vagas')
    list_filter = ('data', 'horario')


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Agendamento, AgendamentoAdmin)
admin.site.register(AgendamentoDisponivel, AgendamentoDisponivelAdmin)
admin.site.register(EstabelecimentoSaude, EstabelecimentoSaudeAdmin)
admin.site.register(GrupoAtendimento, GrupoAtendimentoAdmin)"""
