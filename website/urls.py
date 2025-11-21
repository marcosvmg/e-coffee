from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('cadastro/', views.cadastrar_usuario, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('comprar/<int:produto_id>/', views.comprar_produto, name='comprar'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('historico/', views.historico_pedidos, name='historico'),
]