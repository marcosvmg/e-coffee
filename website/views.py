from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pagina, Produto, Contato, Pedido, PerfilUsuario
from .forms import UserUpdateForm, PerfilUpdateForm

def index(request):
    pagina_dados = Pagina.objects.first()
    produtos = Produto.objects.all()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')

        if nome and email and mensagem:
            Contato.objects.create(nome=nome, email=email, mensagem=mensagem)
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Preencha todos os campos do formulário.')

    context = {
        'pagina': pagina_dados,
        'produtos': produtos,
    }
    return render(request, 'index.html', context)

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario) 
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('index')
    else:
        form = UserCreationForm()
    
    return render(request, 'cadastro.html', {'form': form})

@login_required
def comprar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))
        
        if quantidade > produto.estoque:
            messages.error(request, f'Estoque insuficiente. Apenas {produto.estoque} disponíveis.')
        elif quantidade < 1:
             messages.error(request, 'A quantidade deve ser no mínimo 1.')
        else:
            total = produto.preco * quantidade
            
            Pedido.objects.create(
                usuario=request.user,
                produto=produto,
                quantidade=quantidade,
                total=total
            )
            
            produto.estoque -= quantidade
            produto.save()
            
            messages.success(request, 'Compra realizada com sucesso!')
            return redirect('historico')

    return render(request, 'compra.html', {'produto': produto})

@login_required
def perfil_usuario(request):
    PerfilUsuario.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Informações atualizadas com sucesso!')
            return redirect('perfil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=request.user.perfil)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'perfil.html', context)

@login_required
def historico_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'historico.html', {'pedidos': pedidos})