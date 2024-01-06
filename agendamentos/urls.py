from django.urls import path
from django.contrib.auth import views as auth_views
from agendamentos import views


urlpatterns = [
    path('', views.graficos, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.deslogar, name="logout"),
    path('cadastro/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('agendamento/', views.agendamento, name='agendamento'),
    path('meus_agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
]
