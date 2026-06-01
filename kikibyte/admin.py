from django.contrib import admin
from .models import (
    Empresa, Role, Cliente, Utilizador, Pagina,
    CategoriaArtigo, Artigo, FormularioContacto,
    Servico, Pedido, Mensagem, Documento,
    Relatorio, Notificacao, LogAtividade
)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'ativo']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'ativo']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'setor', 'telefone', 'ativo']
    search_fields = ['nome', 'email', 'nif']
    list_filter = ['ativo', 'setor']

@admin.register(Utilizador)
class UtilizadorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'role', 'ativo', 'ultimo_login']
    search_fields = ['nome', 'email']
    list_filter = ['ativo', 'role']

@admin.register(CategoriaArtigo)
class CategoriaArtigoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'estado', 'autor', 'created_at']
    search_fields = ['titulo', 'resumo']
    list_filter = ['estado', 'categoria']

@admin.register(FormularioContacto)
class FormularioContactoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'assunto', 'estado', 'data_envio']
    list_filter = ['estado']
    search_fields = ['nome', 'email', 'assunto']

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'visivel_site', 'ativo']
    list_filter = ['visivel_site', 'ativo']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'cliente', 'servico', 'estado', 'prioridade', 'data_criacao']
    list_filter = ['estado', 'prioridade']
    search_fields = ['titulo']

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'utilizador', 'lida', 'created_at']
    list_filter = ['lida']

@admin.register(LogAtividade)
class LogAtividadeAdmin(admin.ModelAdmin):
    list_display = ['acao', 'entidade', 'entidade_id', 'utilizador', 'ip_origem', 'created_at']
    list_filter = ['acao', 'entidade']
    readonly_fields = ['acao','entidade','entidade_id','utilizador','cliente',
                       'ip_origem','user_agent','antes','depois','created_at']