from django.contrib import admin
from .models import Pagina, Produto, Contato, Pedido, PerfilUsuario

@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ('nome_do_site', 'email', 'whatsapp', 'atualizado_em')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estoque', 'preco', 'atualizado_em')
    search_fields = ('nome',)

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'criado_em')
    readonly_fields = ('nome', 'email', 'mensagem', 'criado_em')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'produto', 'quantidade', 'total', 'data')
    list_filter = ('data',)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone', 'endereco')