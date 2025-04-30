# example/views.py
from datetime import datetime

from django.shortcuts import render
from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Arrecadacao, Arrecadacao_eletrodomestico, Arrecadacao_alimento, Vestuario, Eletrodomestico, Alimento, Tamanho, Genero, Arrecadador

def adicionar_doacao(request):
    quantidade = 0
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        quantidade = int(request.POST.get('quantidade', 0))

        if tipo == 'vestuario':
            vestuario_id = request.POST.get('vestuario')
            tamanho_id = request.POST.get('tamanho')
            genero_id = request.POST.get('genero')

            vestuario = Vestuario.objects.get(id=vestuario_id)
            tamanho = Tamanho.objects.get(id=tamanho_id)
            genero = Genero.objects.get(id=genero_id)


            # Criação da doação incluindo o arrecadador
            Arrecadacao.objects.create(
                vestuario=vestuario,
                tamanho=tamanho,
                genero=genero,
                quantidade=quantidade,
            )


        elif tipo == 'eletrodomestico':
            eletro_id = request.POST.get('eletrodomestico')
            eletro = Eletrodomestico.objects.get(id=eletro_id)
            Arrecadacao_eletrodomestico.objects.create(eletrodomestico=eletro, quantidade=quantidade)

        elif tipo == 'alimento':
            alimento_id = request.POST.get('alimento')
            alimento = Alimento.objects.get(id=alimento_id)
            Arrecadacao_alimento.objects.create(alimento=alimento, quantidade=quantidade)

        # Retorna a quantidade como contexto para o JavaScript manipular
        return render(request, 'adicionar_doacao.html', {'quantidade': quantidade, 'doacao_realizada': True})

    context = {
        'vestuarios': Vestuario.objects.all(),
        'tamanhos': Tamanho.objects.all(),
        'generos': Genero.objects.all(),
        'eletrodomesticos': Eletrodomestico.objects.all(),
        'alimentos': Alimento.objects.all(),
    }
    return render(request, 'adicionar_doacao.html', context)

def soma_quantidade_arrecadacao(request):
    # Calcula a soma da quantidade de arrecadação
    soma = Arrecadacao.objects.aggregate(soma_quantidade=Sum('quantidade'))['soma_quantidade'] or 0
    context = {'soma_quantidade': soma}
    return render(request, 'index.html', context)

def soma_quantidade_eletrodomestico(request):
    # Calcula a soma da quantidade de eletrodomésticos
    soma = Arrecadacao_eletrodomestico.objects.aggregate(soma_quantidade_eletrodomestico=Sum('quantidade'))['soma_quantidade_eletrodomestico'] or 0
    context = {'soma_quantidade_eletrodomestico': soma}
    return render(request, 'index.html', context)



def index(request):
    # Soma das quantidades de vestuário
    soma_quantidade = Arrecadacao.objects.aggregate(total=Sum('quantidade'))['total'] or 0

    # Soma das quantidades de eletrodomésticos
    soma_quantidade_eletrodomestico = Arrecadacao_eletrodomestico.objects.aggregate(total=Sum('quantidade'))['total'] or 0

    # Soma das quantidades de alimentos
    soma_quantidade_alimento = Arrecadacao_alimento.objects.aggregate(total=Sum('quantidade'))['total'] or 0

    context = {
        'soma_quantidade': soma_quantidade,
        'soma_quantidade_eletrodomestico': soma_quantidade_eletrodomestico,
        'soma_quantidade_alimento': soma_quantidade_alimento,
    }
    return render(request, 'index.html', context)

def cadastrar_arrecadador(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        Arrecadador.objects.create(nome=nome, cep=cep, bairro=bairro, cidade=cidade)
        return redirect('index')  # Redireciona para a página inicial após o cadastro
    return render(request, 'adicionar_arrecadador.html')
