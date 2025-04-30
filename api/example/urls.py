from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('adicionar_doacao/', views.adicionar_doacao, name='adicionar_doacao'),
    path('cadastrar_arrecadador/', views.cadastrar_arrecadador, name='cadastrar_arrecadador'),
    path('arrecadacao/', views.soma_quantidade_arrecadacao, name='soma_arrecadacao'),
    path('arrecadacao_eletrodomestico/', views.soma_quantidade_eletrodomestico, name='soma_quantidade_eletrodomestico'),
    #path('pontos/', views.pontos, name='pontos'),
]
