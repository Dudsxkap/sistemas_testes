from django.urls import path
from django.contrib.auth import views as auth_views
from agendamentos.forms import UserLoginForm
from agendamentos import views
from .views import IndexView, DadosJSONView


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('cadastro/', views.cadastro_usuario_view, name='cadastro_usuario'),
    path('logout/', views.deslogar, name='logout'),
    path('teste/', views.teste, name='teste'),
    path('agendamento/', views.agendamento, name='agendamento'),
    path('agendamentos_disponiveis/', views.agendamentos_disponiveis, name='agendamentos_disponiveis'),
    path('meus_agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),

]
urlpatterns += [
    path('', IndexView.as_view(), name='index'),
    path('dados/', DadosJSONView.as_view(), name='dados'),
]