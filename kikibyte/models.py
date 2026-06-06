from django.db import models


class Empresa(models.Model):
    id_empresa    = models.BigAutoField(primary_key=True)
    nome          = models.CharField(max_length=150)
    nif           = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email         = models.CharField(max_length=150, null=True, blank=True)
    telefone      = models.CharField(max_length=20, null=True, blank=True)
    website       = models.CharField(max_length=255, null=True, blank=True)
    descricao     = models.TextField(null=True, blank=True)
    missao        = models.TextField(null=True, blank=True)
    visao         = models.TextField(null=True, blank=True)
    valores       = models.TextField(null=True, blank=True)
    logo_base64   = models.TextField(null=True, blank=True)
    ativo         = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'empresa'
        managed  = False

    def __str__(self):
        return self.nome


class Role(models.Model):
    id_role    = models.BigAutoField(primary_key=True)
    nome       = models.CharField(max_length=50, unique=True)
    descricao  = models.TextField(null=True, blank=True)
    ativo      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role'
        managed  = False

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    id_cliente  = models.BigAutoField(primary_key=True)
    empresa     = models.ForeignKey(Empresa, on_delete=models.SET_NULL,
                                    null=True, blank=True, db_column='empresa_id')
    nome        = models.CharField(max_length=150)
    nif         = models.CharField(max_length=20, unique=True, null=True, blank=True)
    setor       = models.CharField(max_length=100, null=True, blank=True)
    email       = models.CharField(max_length=150, null=True, blank=True)
    telefone    = models.CharField(max_length=20, null=True, blank=True)
    morada      = models.TextField(null=True, blank=True)
    foto_base64 = models.TextField(null=True, blank=True)
    ativo       = models.BooleanField(default=True)
    CONFORMIDADE = [
        ('conforme',       'Conforme'),
        ('em_avaliacao',   'Em Avaliação'),
        ('com_pendencias', 'Com Pendências'),
    ]
    estado_conformidade = models.CharField(
        max_length=30,
        choices=CONFORMIDADE,
        default='em_avaliacao')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cliente'
        managed  = False

    def __str__(self):
        return self.nome


class Utilizador(models.Model):
    id_utilizador      = models.BigAutoField(primary_key=True)
    empresa            = models.ForeignKey(Empresa, on_delete=models.SET_NULL,
                                           null=True, blank=True, db_column='empresa_id')
    cliente            = models.ForeignKey(Cliente, on_delete=models.SET_NULL,
                                           null=True, blank=True, db_column='cliente_id')
    role               = models.ForeignKey(Role, on_delete=models.RESTRICT,
                                           db_column='role_id')
    nome               = models.CharField(max_length=150)
    email              = models.CharField(max_length=150, unique=True)
    password_hash      = models.TextField()
    foto_perfil_base64 = models.TextField(null=True, blank=True)
    ativo              = models.BooleanField(default=True)
    ultimo_login       = models.DateTimeField(null=True, blank=True)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'utilizador'
        managed  = False

    def __str__(self):
        return self.email


class Pagina(models.Model):
    ESTADO = [('rascunho','Rascunho'),('publicado','Publicado'),('arquivado','Arquivado')]
    id_pagina          = models.BigAutoField(primary_key=True)
    titulo             = models.CharField(max_length=200)
    slug               = models.CharField(max_length=200, unique=True)
    resumo             = models.TextField(null=True, blank=True)
    conteudo           = models.TextField(null=True, blank=True)
    imagem_capa_base64 = models.TextField(null=True, blank=True)
    estado             = models.CharField(max_length=20, choices=ESTADO, default='rascunho')
    seo_title          = models.CharField(max_length=200, null=True, blank=True)
    seo_description    = models.CharField(max_length=255, null=True, blank=True)
    published_at       = models.DateTimeField(null=True, blank=True)
    created_by         = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                           null=True, blank=True,
                                           related_name='paginas_criadas', db_column='created_by')
    updated_by         = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                           null=True, blank=True,
                                           related_name='paginas_atualizadas', db_column='updated_by')
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pagina'
        managed  = False

    def __str__(self):
        return self.titulo


class CategoriaArtigo(models.Model):
    id_categoria = models.BigAutoField(primary_key=True)
    nome         = models.CharField(max_length=100, unique=True)
    slug         = models.CharField(max_length=120, unique=True)

    class Meta:
        db_table = 'categoria_artigo'
        managed  = False

    def __str__(self):
        return self.nome


class Artigo(models.Model):
    ESTADO = [('rascunho','Rascunho'),('publicado','Publicado'),('arquivado','Arquivado')]
    id_artigo          = models.BigAutoField(primary_key=True)
    categoria          = models.ForeignKey(CategoriaArtigo, on_delete=models.SET_NULL,
                                           null=True, blank=True, db_column='id_categoria')
    titulo             = models.CharField(max_length=200)
    slug               = models.CharField(max_length=200, unique=True)
    resumo             = models.TextField(null=True, blank=True)
    conteudo           = models.TextField()
    imagem_capa_base64 = models.TextField(null=True, blank=True)
    estado             = models.CharField(max_length=20, choices=ESTADO, default='rascunho')
    autor              = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                           null=True, blank=True, db_column='autor_id')
    published_at       = models.DateTimeField(null=True, blank=True)
    seo_title          = models.CharField(max_length=200, null=True, blank=True)
    seo_description    = models.CharField(max_length=255, null=True, blank=True)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'artigo'
        managed  = False

    def __str__(self):
        return self.titulo


class FormularioContacto(models.Model):
    ESTADO = [('novo','Novo'),('em_tratamento','Em Tratamento'),
              ('respondido','Respondido'),('arquivado','Arquivado')]
    id_contacto_form = models.BigAutoField(primary_key=True)
    nome             = models.CharField(max_length=150)
    email            = models.CharField(max_length=150)
    telefone         = models.CharField(max_length=20, null=True, blank=True)
    assunto          = models.CharField(max_length=200)
    mensagem         = models.TextField()
    estado           = models.CharField(max_length=20, choices=ESTADO, default='novo')
    tratado_por      = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                         null=True, blank=True, db_column='tratado_por')
    data_envio       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'formulario_contacto'
        managed  = False

    def __str__(self):
        return f"{self.nome} — {self.assunto}"


class Servico(models.Model):
    id_servico    = models.BigAutoField(primary_key=True)
    nome          = models.CharField(max_length=150, unique=True)
    descricao     = models.TextField(null=True, blank=True)
    imagem_base64 = models.TextField(null=True, blank=True)
    visivel_site  = models.BooleanField(default=True)
    ativo         = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'servico'
        managed  = False

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    ESTADO = [('pendente','Pendente'),('em_analise','Em Análise'),
              ('em_execucao','Em Execução'),('aguarda_cliente','Aguarda Cliente'),
              ('concluido','Concluído'),('cancelado','Cancelado')]
    PRIORIDADE = [('baixa','Baixa'),('normal','Normal'),('alta','Alta')]
    id_pedido    = models.BigAutoField(primary_key=True)
    cliente      = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='cliente_id')
    servico      = models.ForeignKey(Servico, on_delete=models.SET_NULL,
                                     null=True, blank=True, db_column='servico_id')
    criado_por   = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='pedidos_criados', db_column='criado_por')
    atribuido_a  = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='pedidos_atribuidos', db_column='atribuido_a')
    titulo       = models.CharField(max_length=200)
    descricao    = models.TextField(null=True, blank=True)
    estado       = models.CharField(max_length=30, choices=ESTADO, default='pendente')
    prioridade   = models.CharField(max_length=20, choices=PRIORIDADE, default='normal')
    TIPO = [
        ('pedido',       'Pedido'),
        ('incidente',    'Incidente de Segurança'),
        ('auditoria',    'Auditoria'),
        ('consultoria',  'Consultoria'),
    ]
    tipo         = models.CharField(max_length=30, choices=TIPO, default='pedido')
    anexo_base64 = models.TextField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_fecho = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'pedido'
        managed = False

    def __str__(self):
        return self.titulo
class Mensagem(models.Model):
    id_mensagem     = models.BigAutoField(primary_key=True)
    pedido          = models.ForeignKey(Pedido, on_delete=models.CASCADE, db_column='pedido_id')
    remetente       = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                        null=True, blank=True, db_column='remetente_id')
    mensagem        = models.TextField()
    anexo_base64    = models.TextField(null=True, blank=True)
    visivel_cliente = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mensagem'
        managed  = False


class Documento(models.Model):
    id_documento    = models.BigAutoField(primary_key=True)
    cliente         = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='cliente_id')
    pedido          = models.ForeignKey(Pedido, on_delete=models.SET_NULL,
                                        null=True, blank=True, db_column='pedido_id')
    uploaded_by     = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                        null=True, blank=True, db_column='uploaded_by')
    titulo          = models.CharField(max_length=200)
    tipo_documento  = models.CharField(max_length=50)
    ficheiro_base64 = models.TextField()
    mime_type       = models.CharField(max_length=100, null=True, blank=True)
    tamanho_bytes   = models.BigIntegerField(null=True, blank=True)
    sensivel        = models.BooleanField(default=True)
    visivel_cliente = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'documento'
        managed  = False


class DocumentoPartilha(models.Model):
    PERMISSAO = [('leitura','Leitura'),('download','Download')]
    id_partilha   = models.BigAutoField(primary_key=True)
    documento     = models.ForeignKey(Documento, on_delete=models.CASCADE, db_column='documento_id')
    utilizador    = models.ForeignKey(Utilizador, on_delete=models.CASCADE, db_column='utilizador_id')
    permissao     = models.CharField(max_length=20, choices=PERMISSAO, default='leitura')
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'documento_partilha'
        managed  = False


class Relatorio(models.Model):
    id_relatorio      = models.BigAutoField(primary_key=True)
    cliente           = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='cliente_id')
    pedido            = models.ForeignKey(Pedido, on_delete=models.SET_NULL,
                                          null=True, blank=True, db_column='pedido_id')
    criado_por        = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                          null=True, blank=True, db_column='criado_por')
    titulo            = models.CharField(max_length=200)
    tipo_relatorio    = models.CharField(max_length=50)
    ficheiro_base64   = models.TextField()
    mime_type         = models.CharField(max_length=100, null=True, blank=True)
    versao            = models.CharField(max_length=20, null=True, blank=True)
    publicado_cliente = models.BooleanField(default=False)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'relatorio'
        managed  = False


class Notificacao(models.Model):
    id_notificacao = models.BigAutoField(primary_key=True)
    utilizador     = models.ForeignKey(Utilizador, on_delete=models.CASCADE, db_column='utilizador_id')
    titulo         = models.CharField(max_length=200)
    mensagem       = models.TextField()
    lida           = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notificacao'
        managed  = False


class LogAtividade(models.Model):
    id_log        = models.BigAutoField(primary_key=True)
    utilizador    = models.ForeignKey(Utilizador, on_delete=models.SET_NULL,
                                      null=True, blank=True, db_column='utilizador_id')
    cliente       = models.ForeignKey(Cliente, on_delete=models.SET_NULL,
                                      null=True, blank=True, db_column='cliente_id')
    acao          = models.CharField(max_length=50)
    entidade      = models.CharField(max_length=50)
    entidade_id   = models.BigIntegerField(null=True, blank=True)
    ip_origem     = models.CharField(max_length=45, null=True, blank=True)
    user_agent    = models.TextField(null=True, blank=True)
    antes         = models.JSONField(null=True, blank=True)
    depois        = models.JSONField(null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log_atividade'
        managed  = False