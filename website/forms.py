from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['foto', 'telefone', 'endereco']