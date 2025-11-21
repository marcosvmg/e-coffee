from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Pagina(models.Model):
    nome_do_site = models.CharField(max_length=100)
    logo_do_site = models.ImageField(upload_to='logos/')
    texto_chamada = models.TextField()
    texto_sobre = models.TextField()
    imagem_sobre = models.ImageField(upload_to='sobre/')
    endereco = models.CharField(max_length=255)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_do_site

    class Meta:
        verbose_name = 'Página Institucional'
        verbose_name_plural = 'Páginas Institucionais'

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    estoque = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='produtos/')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.nome}"

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto = models.ImageField(upload_to='perfis/', null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Sinais para criar/atualizar o perfil automaticamente quando um User é criado
@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)
    else:
        PerfilUsuario.objects.get_or_create(user=instance)