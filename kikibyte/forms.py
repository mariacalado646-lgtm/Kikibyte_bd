from django import forms
from .models import (FormularioContacto, Artigo, CategoriaArtigo,
                     Servico, Cliente, Utilizador, Pedido, Empresa)


class FormularioContactoForm(forms.ModelForm):
    nome = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'João Silva'}),
        label='Nome Completo *'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'joao@empresa.pt'}),
        label='Email *'
    )
    telefone = forms.CharField(
        required=False, max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+351 912 345 678'}),
        label='Telefone'
    )
    assunto = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Assunto da mensagem'}),
        label='Assunto *'
    )
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 5,
                                     'placeholder': 'Como podemos ajudar?'}),
        label='Mensagem *'
    )

    class Meta:
        model  = FormularioContacto
        fields = ['nome', 'email', 'telefone', 'assunto', 'mensagem']


class ArtigoForm(forms.ModelForm):
    class Meta:
        model  = Artigo
        fields = ['titulo', 'slug', 'categoria', 'resumo', 'conteudo', 'estado',
                  'seo_title', 'seo_description']
        widgets = {
            'titulo':          forms.TextInput(attrs={'class': 'form-input'}),
            'slug':            forms.TextInput(attrs={'class': 'form-input'}),
            'categoria':       forms.Select(attrs={'class': 'form-input'}),
            'resumo':          forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'conteudo':        forms.Textarea(attrs={'class': 'form-input', 'rows': 10}),
            'estado':          forms.Select(attrs={'class': 'form-input'}),
            'seo_title':       forms.TextInput(attrs={'class': 'form-input'}),
            'seo_description': forms.TextInput(attrs={'class': 'form-input'}),
        }


class CategoriaArtigoForm(forms.ModelForm):
    class Meta:
        model  = CategoriaArtigo
        fields = ['nome', 'slug']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
        }


class ServicoForm(forms.ModelForm):
    class Meta:
        model  = Servico
        fields = ['nome', 'descricao', 'visivel_site', 'ativo']
        widgets = {
            'nome':      forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model  = Cliente
        fields = ['nome', 'nif', 'setor', 'email', 'telefone', 'morada', 'ativo']
        widgets = {
            'nome':     forms.TextInput(attrs={'class': 'form-input'}),
            'nif':      forms.TextInput(attrs={'class': 'form-input'}),
            'setor':    forms.TextInput(attrs={'class': 'form-input'}),
            'email':    forms.EmailInput(attrs={'class': 'form-input'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'morada':   forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }


class UtilizadorForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        label='Password'
    )

    class Meta:
        model  = Utilizador
        fields = ['nome', 'email', 'role', 'ativo']
        widgets = {
            'nome':  forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'role':  forms.Select(attrs={'class': 'form-input'}),
        }


class PedidoForm(forms.ModelForm):
    class Meta:
        model  = Pedido
        fields = ['cliente', 'servico', 'titulo', 'descricao', 'prioridade']
        widgets = {
            'cliente':   forms.Select(attrs={'class': 'form-input'}),
            'servico':   forms.Select(attrs={'class': 'form-input'}),
            'titulo':    forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'prioridade':forms.Select(attrs={'class': 'form-input'}),
        }


class EmpresaForm(forms.ModelForm):
    class Meta:
        model  = Empresa
        fields = ['nome', 'nif', 'email', 'telefone', 'website',
                  'descricao', 'missao', 'visao', 'valores']
        widgets = {
            'nome':     forms.TextInput(attrs={'class': 'form-input'}),
            'nif':      forms.TextInput(attrs={'class': 'form-input'}),
            'email':    forms.EmailInput(attrs={'class': 'form-input'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'website':  forms.URLInput(attrs={'class': 'form-input'}),
            'descricao':forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'missao':   forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'visao':    forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'valores':  forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }