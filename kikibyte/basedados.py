"""
basedados.py — Funções CRUD com SQL puro para o KikiByte
Tabelas: empresa, role, cliente, utilizador, pagina,
         categoria_artigo, artigo, formulario_contacto,
         servico, pedido, mensagem, documento, relatorio,
         notificacao, log_atividade
"""
from django.db import connection


def _query(sql, params=None, fetchall=False, fetchone=False):
    """Executa SQL e devolve resultados como dicionários."""
    with connection.cursor() as c:
        c.execute(sql, params or [])
        if fetchall:
            cols = [col[0] for col in c.description]
            return [dict(zip(cols, row)) for row in c.fetchall()]
        if fetchone:
            row = c.fetchone()
            if row:
                cols = [col[0] for col in c.description]
                return dict(zip(cols, row))
            return None
        return c.rowcount


# ── EMPRESA ──────────────────────────────────────────────────────────────────

def empresa_ler():
    """Devolve os dados da empresa (é apenas uma)."""
    return _query("SELECT * FROM empresa WHERE ativo = TRUE LIMIT 1", fetchone=True)

def empresa_criar(nome, nif=None, email=None, telefone=None, website=None,
                  descricao=None, missao=None, visao=None, valores=None):
    sql = """
        INSERT INTO empresa (nome, nif, email, telefone, website,
                             descricao, missao, visao, valores)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    return _query(sql, [nome, nif, email, telefone, website,
                        descricao, missao, visao, valores])

def empresa_atualizar(id_empresa, nome, nif=None, email=None, telefone=None,
                      website=None, descricao=None, missao=None, visao=None, valores=None):
    sql = """
        UPDATE empresa SET nome=%s, nif=%s, email=%s, telefone=%s, website=%s,
               descricao=%s, missao=%s, visao=%s, valores=%s, updated_at=NOW()
        WHERE id_empresa=%s
    """
    return _query(sql, [nome, nif, email, telefone, website,
                        descricao, missao, visao, valores, id_empresa])


# ── ROLE ─────────────────────────────────────────────────────────────────────

def role_ler_todos():
    return _query("SELECT * FROM role WHERE ativo = TRUE ORDER BY nome", fetchall=True)

def role_ler_por_id(id_role):
    return _query("SELECT * FROM role WHERE id_role=%s", [id_role], fetchone=True)

def role_ler_por_nome(nome):
    return _query("SELECT * FROM role WHERE nome=%s", [nome], fetchone=True)


# ── CLIENTE ──────────────────────────────────────────────────────────────────

def cliente_criar(nome, email=None, nif=None, setor=None,
                  telefone=None, morada=None, empresa_id=None):
    sql = """
        INSERT INTO cliente (nome, email, nif, setor, telefone, morada, empresa_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    return _query(sql, [nome, email, nif, setor, telefone, morada, empresa_id])

def cliente_ler_todos(apenas_ativos=True):
    if apenas_ativos:
        return _query("SELECT * FROM cliente WHERE ativo=TRUE ORDER BY nome", fetchall=True)
    return _query("SELECT * FROM cliente ORDER BY nome", fetchall=True)

def cliente_ler_por_id(id_cliente):
    return _query("SELECT * FROM cliente WHERE id_cliente=%s", [id_cliente], fetchone=True)

def cliente_ler_por_email(email):
    return _query("SELECT * FROM cliente WHERE email=%s", [email], fetchone=True)

def cliente_atualizar(id_cliente, nome, email=None, nif=None,
                      setor=None, telefone=None, morada=None, ativo=True):
    sql = """
        UPDATE cliente SET nome=%s, email=%s, nif=%s, setor=%s,
               telefone=%s, morada=%s, ativo=%s, updated_at=NOW()
        WHERE id_cliente=%s
    """
    return _query(sql, [nome, email, nif, setor, telefone, morada, ativo, id_cliente])

def cliente_eliminar(id_cliente):
    return _query("DELETE FROM cliente WHERE id_cliente=%s", [id_cliente])


# ── UTILIZADOR ───────────────────────────────────────────────────────────────

def utilizador_criar(nome, email, password_hash, role_id,
                     empresa_id=None, cliente_id=None):
    sql = """
        INSERT INTO utilizador (nome, email, password_hash, role_id,
                                empresa_id, cliente_id)
        VALUES (%s,%s,%s,%s,%s,%s)
    """
    return _query(sql, [nome, email, password_hash, role_id, empresa_id, cliente_id])

def utilizador_ler_todos(apenas_ativos=True):
    sql = """
        SELECT u.*, r.nome AS role_nome
        FROM utilizador u
        JOIN role r ON u.role_id = r.id_role
        {}
        ORDER BY u.nome
    """.format("WHERE u.ativo=TRUE" if apenas_ativos else "")
    return _query(sql, fetchall=True)

def utilizador_ler_por_id(id_utilizador):
    sql = """
        SELECT u.*, r.nome AS role_nome
        FROM utilizador u
        JOIN role r ON u.role_id = r.id_role
        WHERE u.id_utilizador=%s
    """
    return _query(sql, [id_utilizador], fetchone=True)

def utilizador_ler_por_email(email):
    sql = """
        SELECT u.*, r.nome AS role_nome
        FROM utilizador u
        JOIN role r ON u.role_id = r.id_role
        WHERE u.email=%s
    """
    return _query(sql, [email], fetchone=True)

def utilizador_atualizar_ultimo_login(id_utilizador):
    return _query(
        "UPDATE utilizador SET ultimo_login=NOW(), updated_at=NOW() WHERE id_utilizador=%s",
        [id_utilizador])

def utilizador_atualizar(id_utilizador, nome, email, role_id, ativo):
    sql = """
        UPDATE utilizador SET nome=%s, email=%s, role_id=%s, ativo=%s, updated_at=NOW()
        WHERE id_utilizador=%s
    """
    return _query(sql, [nome, email, role_id, ativo, id_utilizador])

def utilizador_eliminar(id_utilizador):
    return _query("DELETE FROM utilizador WHERE id_utilizador=%s", [id_utilizador])


# ── CATEGORIA ARTIGO ─────────────────────────────────────────────────────────

def categoria_criar(nome, slug):
    return _query(
        "INSERT INTO categoria_artigo (nome, slug) VALUES (%s,%s)",
        [nome, slug])

def categoria_ler_todas():
    return _query("SELECT * FROM categoria_artigo ORDER BY nome", fetchall=True)

def categoria_ler_por_id(id_categoria):
    return _query(
        "SELECT * FROM categoria_artigo WHERE id_categoria=%s",
        [id_categoria], fetchone=True)

def categoria_eliminar(id_categoria):
    return _query(
        "DELETE FROM categoria_artigo WHERE id_categoria=%s", [id_categoria])


# ── ARTIGO ───────────────────────────────────────────────────────────────────

def artigo_criar(titulo, slug, conteudo, id_categoria=None,
                 resumo=None, autor_id=None, estado='rascunho'):
    sql = """
        INSERT INTO artigo (titulo, slug, conteudo, id_categoria,
                            resumo, autor_id, estado, published_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s, CASE WHEN %s='publicado' THEN NOW() ELSE NULL END)
    """
    return _query(sql, [titulo, slug, conteudo, id_categoria,
                        resumo, autor_id, estado, estado])

def artigo_ler_todos(apenas_publicados=True, limite=None):
    sql = """
        SELECT a.*, c.nome AS categoria_nome
        FROM artigo a
        LEFT JOIN categoria_artigo c ON a.id_categoria = c.id_categoria
        {}
        ORDER BY a.created_at DESC
        {}
    """.format(
        "WHERE a.estado='publicado'" if apenas_publicados else "",
        f"LIMIT {int(limite)}" if limite else ""
    )
    return _query(sql, fetchall=True)

def artigo_ler_por_id(id_artigo):
    sql = """
        SELECT a.*, c.nome AS categoria_nome
        FROM artigo a
        LEFT JOIN categoria_artigo c ON a.id_categoria = c.id_categoria
        WHERE a.id_artigo=%s
    """
    return _query(sql, [id_artigo], fetchone=True)

def artigo_ler_por_categoria(id_categoria):
    sql = """
        SELECT a.*, c.nome AS categoria_nome
        FROM artigo a
        LEFT JOIN categoria_artigo c ON a.id_categoria = c.id_categoria
        WHERE a.id_categoria=%s AND a.estado='publicado'
        ORDER BY a.created_at DESC
    """
    return _query(sql, [id_categoria], fetchall=True)

def artigo_atualizar(id_artigo, titulo, slug, conteudo, id_categoria,
                     resumo, estado):
    sql = """
        UPDATE artigo
        SET titulo=%s, slug=%s, conteudo=%s, id_categoria=%s,
            resumo=%s, estado=%s, updated_at=NOW(),
            published_at = CASE WHEN %s='publicado' AND published_at IS NULL
                           THEN NOW() ELSE published_at END
        WHERE id_artigo=%s
    """
    return _query(sql, [titulo, slug, conteudo, id_categoria,
                        resumo, estado, estado, id_artigo])

def artigo_eliminar(id_artigo):
    return _query("DELETE FROM artigo WHERE id_artigo=%s", [id_artigo])


# ── FORMULÁRIO DE CONTACTO ───────────────────────────────────────────────────

def contacto_criar(nome, email, assunto, mensagem, telefone=None):
    sql = """
        INSERT INTO formulario_contacto (nome, email, telefone, assunto, mensagem)
        VALUES (%s,%s,%s,%s,%s)
    """
    return _query(sql, [nome, email, telefone, assunto, mensagem])

def contacto_ler_todos(estado=None):
    if estado:
        return _query(
            "SELECT * FROM formulario_contacto WHERE estado=%s ORDER BY data_envio DESC",
            [estado], fetchall=True)
    return _query(
        "SELECT * FROM formulario_contacto ORDER BY data_envio DESC",
        fetchall=True)

def contacto_ler_por_id(id_contacto):
    return _query(
        "SELECT * FROM formulario_contacto WHERE id_contacto_form=%s",
        [id_contacto], fetchone=True)

def contacto_atualizar_estado(id_contacto, estado, tratado_por=None):
    sql = """
        UPDATE formulario_contacto
        SET estado=%s, tratado_por=%s
        WHERE id_contacto_form=%s
    """
    return _query(sql, [estado, tratado_por, id_contacto])

def contacto_eliminar(id_contacto):
    return _query(
        "DELETE FROM formulario_contacto WHERE id_contacto_form=%s", [id_contacto])


# ── SERVIÇO ──────────────────────────────────────────────────────────────────

def servico_criar(nome, descricao=None, visivel_site=True, ativo=True):
    sql = """
        INSERT INTO servico (nome, descricao, visivel_site, ativo)
        VALUES (%s,%s,%s,%s)
    """
    return _query(sql, [nome, descricao, visivel_site, ativo])

def servico_ler_todos(apenas_visiveis=True):
    if apenas_visiveis:
        return _query(
            "SELECT * FROM servico WHERE visivel_site=TRUE AND ativo=TRUE ORDER BY nome",
            fetchall=True)
    return _query("SELECT * FROM servico ORDER BY nome", fetchall=True)

def servico_ler_por_id(id_servico):
    return _query("SELECT * FROM servico WHERE id_servico=%s", [id_servico], fetchone=True)

def servico_atualizar(id_servico, nome, descricao, visivel_site, ativo):
    sql = """
        UPDATE servico SET nome=%s, descricao=%s, visivel_site=%s, ativo=%s
        WHERE id_servico=%s
    """
    return _query(sql, [nome, descricao, visivel_site, ativo, id_servico])

def servico_eliminar(id_servico):
    return _query("DELETE FROM servico WHERE id_servico=%s", [id_servico])


# ── PEDIDO ───────────────────────────────────────────────────────────────────

def pedido_criar(cliente_id, titulo, descricao=None,
                 servico_id=None, criado_por=None, prioridade='normal'):
    sql = """
        INSERT INTO pedido (cliente_id, titulo, descricao, servico_id,
                            criado_por, prioridade)
        VALUES (%s,%s,%s,%s,%s,%s)
    """
    return _query(sql, [cliente_id, titulo, descricao, servico_id, criado_por, prioridade])

def pedido_ler_todos(estado=None):
    base = """
        SELECT p.*, c.nome AS cliente_nome, s.nome AS servico_nome
        FROM pedido p
        LEFT JOIN cliente c ON p.cliente_id = c.id_cliente
        LEFT JOIN servico s ON p.servico_id = s.id_servico
    """
    if estado:
        return _query(base + " WHERE p.estado=%s ORDER BY p.data_criacao DESC",
                      [estado], fetchall=True)
    return _query(base + " ORDER BY p.data_criacao DESC", fetchall=True)

def pedido_ler_por_cliente(cliente_id):
    sql = """
        SELECT p.*, s.nome AS servico_nome
        FROM pedido p
        LEFT JOIN servico s ON p.servico_id = s.id_servico
        WHERE p.cliente_id=%s ORDER BY p.data_criacao DESC
    """
    return _query(sql, [cliente_id], fetchall=True)

def pedido_ler_por_id(id_pedido):
    sql = """
        SELECT p.*, c.nome AS cliente_nome, s.nome AS servico_nome
        FROM pedido p
        LEFT JOIN cliente c ON p.cliente_id = c.id_cliente
        LEFT JOIN servico s ON p.servico_id = s.id_servico
        WHERE p.id_pedido=%s
    """
    return _query(sql, [id_pedido], fetchone=True)

def pedido_atualizar_estado(id_pedido, estado, atribuido_a=None):
    sql = """
        UPDATE pedido SET estado=%s, atribuido_a=%s,
               data_fecho = CASE WHEN %s IN ('concluido','cancelado') THEN NOW() ELSE NULL END
        WHERE id_pedido=%s
    """
    return _query(sql, [estado, atribuido_a, estado, id_pedido])

def pedido_eliminar(id_pedido):
    return _query("DELETE FROM pedido WHERE id_pedido=%s", [id_pedido])


# ── MENSAGEM ─────────────────────────────────────────────────────────────────

def mensagem_criar(pedido_id, mensagem, remetente_id=None,
                   visivel_cliente=True, anexo_base64=None):
    sql = """
        INSERT INTO mensagem (pedido_id, mensagem, remetente_id,
                              visivel_cliente, anexo_base64)
        VALUES (%s,%s,%s,%s,%s)
    """
    return _query(sql, [pedido_id, mensagem, remetente_id,
                        visivel_cliente, anexo_base64])

def mensagem_ler_por_pedido(pedido_id, incluir_internas=False):
    base = """
        SELECT m.*, u.nome AS remetente_nome
        FROM mensagem m
        LEFT JOIN utilizador u ON m.remetente_id = u.id_utilizador
        WHERE m.pedido_id=%s
    """
    if not incluir_internas:
        base += " AND m.visivel_cliente=TRUE"
    return _query(base + " ORDER BY m.created_at ASC", [pedido_id], fetchall=True)

def mensagem_eliminar(id_mensagem):
    return _query("DELETE FROM mensagem WHERE id_mensagem=%s", [id_mensagem])


# ── DOCUMENTO ────────────────────────────────────────────────────────────────

def documento_criar(cliente_id, titulo, tipo_documento, ficheiro_base64,
                    mime_type=None, tamanho_bytes=None, pedido_id=None,
                    uploaded_by=None, sensivel=True, visivel_cliente=False):
    sql = """
        INSERT INTO documento (cliente_id, titulo, tipo_documento, ficheiro_base64,
                               mime_type, tamanho_bytes, pedido_id, uploaded_by,
                               sensivel, visivel_cliente)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    return _query(sql, [cliente_id, titulo, tipo_documento, ficheiro_base64,
                        mime_type, tamanho_bytes, pedido_id, uploaded_by,
                        sensivel, visivel_cliente])

def documento_ler_por_cliente(cliente_id, visivel_cliente=None):
    base = "SELECT * FROM documento WHERE cliente_id=%s"
    if visivel_cliente is not None:
        base += f" AND visivel_cliente={'TRUE' if visivel_cliente else 'FALSE'}"
    return _query(base + " ORDER BY created_at DESC", [cliente_id], fetchall=True)

def documento_ler_por_id(id_documento):
    return _query(
        "SELECT * FROM documento WHERE id_documento=%s", [id_documento], fetchone=True)

def documento_eliminar(id_documento):
    return _query("DELETE FROM documento WHERE id_documento=%s", [id_documento])


# ── RELATÓRIO ────────────────────────────────────────────────────────────────

def relatorio_criar(cliente_id, titulo, tipo_relatorio, ficheiro_base64,
                    mime_type=None, versao=None, pedido_id=None,
                    criado_por=None, publicado_cliente=False):
    sql = """
        INSERT INTO relatorio (cliente_id, titulo, tipo_relatorio, ficheiro_base64,
                               mime_type, versao, pedido_id, criado_por, publicado_cliente)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    return _query(sql, [cliente_id, titulo, tipo_relatorio, ficheiro_base64,
                        mime_type, versao, pedido_id, criado_por, publicado_cliente])

def relatorio_ler_por_cliente(cliente_id, apenas_publicados=False):
    base = "SELECT * FROM relatorio WHERE cliente_id=%s"
    if apenas_publicados:
        base += " AND publicado_cliente=TRUE"
    return _query(base + " ORDER BY created_at DESC", [cliente_id], fetchall=True)

def relatorio_ler_por_id(id_relatorio):
    return _query(
        "SELECT * FROM relatorio WHERE id_relatorio=%s", [id_relatorio], fetchone=True)

def relatorio_eliminar(id_relatorio):
    return _query("DELETE FROM relatorio WHERE id_relatorio=%s", [id_relatorio])


# ── NOTIFICAÇÃO ──────────────────────────────────────────────────────────────

def notificacao_criar(utilizador_id, titulo, mensagem):
    sql = """
        INSERT INTO notificacao (utilizador_id, titulo, mensagem)
        VALUES (%s,%s,%s)
    """
    return _query(sql, [utilizador_id, titulo, mensagem])

def notificacao_ler_por_utilizador(utilizador_id, apenas_nao_lidas=False):
    base = "SELECT * FROM notificacao WHERE utilizador_id=%s"
    if apenas_nao_lidas:
        base += " AND lida=FALSE"
    return _query(base + " ORDER BY created_at DESC", [utilizador_id], fetchall=True)

def notificacao_marcar_lida(id_notificacao):
    return _query(
        "UPDATE notificacao SET lida=TRUE WHERE id_notificacao=%s", [id_notificacao])

def notificacao_marcar_todas_lidas(utilizador_id):
    return _query(
        "UPDATE notificacao SET lida=TRUE WHERE utilizador_id=%s", [utilizador_id])

def notificacao_eliminar(id_notificacao):
    return _query(
        "DELETE FROM notificacao WHERE id_notificacao=%s", [id_notificacao])


# ── LOG DE ATIVIDADE ─────────────────────────────────────────────────────────

def log_criar(acao, entidade, entidade_id=None, utilizador_id=None,
              cliente_id=None, ip_origem=None, antes=None, depois=None):
    import json
    sql = """
        INSERT INTO log_atividade (acao, entidade, entidade_id, utilizador_id,
                                   cliente_id, ip_origem, antes, depois)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    return _query(sql, [
        acao, entidade, entidade_id, utilizador_id, cliente_id, ip_origem,
        json.dumps(antes) if antes else None,
        json.dumps(depois) if depois else None,
    ])

def log_ler_todos(limite=100):
    sql = """
        SELECT l.*, u.nome AS utilizador_nome
        FROM log_atividade l
        LEFT JOIN utilizador u ON l.utilizador_id = u.id_utilizador
        ORDER BY l.created_at DESC
        LIMIT %s
    """
    return _query(sql, [limite], fetchall=True)