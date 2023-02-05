from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def cadastro(request): 
    # Redirecionar para a home e evitar o acesso ao login/cadastro de usuarios logados
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')

    
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    # Se receber dados do form, processe os dados recebidos
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Validações dos campos do form
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
            return render(request, 'cadastro.html')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Digite duas senhas iguais!')
            return render(request, 'cadastro.html')

        # Cria um usuario
        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
            return render(request, 'cadastro.html')

        # Em caso de erro no BD
        except:
            messages.add_message(request, constants.ERROR, 'Erro ao tentar cadastrar')
            return render(request, 'cadastro.html')

def logar(request):
    # Redirecionar para a home e evitar o acesso ao login/cadastro de usuarios logados
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')

    if request.method == 'GET':
        return render(request, 'login.html')

    # Se receber dados do form, processe os dados recebidos
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        # Cheque a autenticidade do usuario
        user = authenticate(username=nome, password=senha)
        if user is not None:
            login(request, user)
            return redirect('/divulgar/novo_pet')
        else:
           messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos') 
           return render(request, 'login.html')

def sair(request):
    # Logout do usuario
    logout(request)
    return redirect('/')
