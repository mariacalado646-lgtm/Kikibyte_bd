from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib import messages
from .forms import FormularioContactoForm
from . import basedados


# ── PÁGINA PRINCIPAL ─────────────────────────────────────────────────────────

# ── CONTACTO ─────────────────────────────────────────────────────────────────

def contacto(request):
    return redirect('kikibyte:dashboard')


def contacto_sucesso(request):
    return redirect('kikibyte:dashboard')


# ── ARTIGOS ──────────────────────────────────────────────────────────────────

def artigos_lista(request):
    id_categoria = request.GET.get('categoria')
    if id_categoria:
        artigos = basedados.artigo_ler_por_categoria(id_categoria)
    else:
        artigos = basedados.artigo_ler_todos(apenas_publicados=True)
    categorias = basedados.categoria_ler_todas()
    return render(request, 'kikibyte/artigos.html', {
        'artigos': artigos,
        'categorias': categorias,
        'categoria_ativa': id_categoria,
    })


def artigo_detalhe(request, artigo_id):
    artigo = basedados.artigo_ler_por_id(artigo_id)
    if not artigo:
        from django.http import Http404
        raise Http404("Artigo não encontrado")
    return render(request, 'kikibyte/artigo_detalhe.html', {'artigo': artigo})


# ── AUTENTICAÇÃO (usa tabela utilizador) ─────────────────────────────────────

def documento_upload(request):
    clientes = basedados.cliente_ler_todos(apenas_ativos=False)
    pedidos_abertos = basedados.pedido_ler_todos(estado='pendente') + \
                      basedados.pedido_ler_todos(estado='em_execucao')

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        tipo_documento = request.POST.get('tipo_documento', '').strip() or 'Documento'
        cliente_id = request.POST.get('cliente_id')
        visivel_cliente = request.POST.get('visivel_cliente') == 'on'
        pedido_id = request.POST.get('pedido_id') or None
        tempo_resolucao = request.POST.get('tempo_resolucao') or None
        ficheiro = request.FILES.get('ficheiro')

        if not titulo or not cliente_id:
            messages.error(request, 'Preencha o título e escolha um cliente.')
        else:
            if ficheiro:
                import base64
                ficheiro_base64 = base64.b64encode(ficheiro.read()).decode('utf-8')
                mime_type = ficheiro.content_type
                tamanho_bytes = ficheiro.size
            else:
                ficheiro_base64 = 'VGhpcyBpcyBhIGRlbW8gZG9jdW1lbnQgc3RyZWFtLg=='
                mime_type = 'application/pdf'
                tamanho_bytes = 1024

            basedados.documento_criar(
                cliente_id=int(cliente_id),
                titulo=titulo,
                tipo_documento=tipo_documento,
                ficheiro_base64=ficheiro_base64,
                mime_type=mime_type,
                tamanho_bytes=tamanho_bytes,
                pedido_id=int(pedido_id) if pedido_id else None,
                visivel_cliente=visivel_cliente,
                sensivel=False,
            )

            # Se foi escolhido um pedido + tempo de resolução, marca como concluído
            if pedido_id and tempo_resolucao:
                basedados._query(
                    """UPDATE pedido
                       SET estado='concluido',
                           data_fecho = data_criacao + (%s || ' hours')::interval
                       WHERE id_pedido=%s""",
                    [tempo_resolucao, pedido_id]
                )

            messages.success(request, 'Documento criado com sucesso.')
            return redirect(reverse('kikibyte:dashboard') + '?tab=documentos')

    return render(request, 'kikibyte/documento_upload.html', {
        'clientes': clientes,
        'pedidos_abertos': pedidos_abertos,
    })


def documento_download(request, documento_id):
    documento = basedados.documento_ler_por_id(documento_id)
    if not documento:
        raise Http404('Documento não encontrado')

    import base64
    import mimetypes

    content = documento.get('ficheiro_base64', '')
    try:
        body = base64.b64decode(content)
    except Exception:
        body = content.encode('utf-8')

    mime_type = documento.get('mime_type') or 'application/octet-stream'
    extensao = mimetypes.guess_extension(mime_type) or ''
    if extensao == '.jpe':
        extensao = '.jpg'

    nome_ficheiro = documento.get('titulo', 'documento').replace(' ', '_') + extensao

    response = HttpResponse(body, content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename="{nome_ficheiro}"'
    return response


def documento_visualizar(request, documento_id):
    documento = basedados.documento_ler_por_id(documento_id)
    if not documento:
        raise Http404('Documento não encontrado')

    mime_type = documento.get('mime_type') or ''
    if mime_type.startswith('image/'):
        categoria = 'imagem'
    elif mime_type == 'application/pdf':
        categoria = 'pdf'
    else:
        categoria = 'outro'

    return render(request, 'kikibyte/documento_visualizar.html', {
        'documento': documento,
        'categoria': categoria,
    })


def cliente_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip() or None
        nif = request.POST.get('nif', '').strip() or None
        setor = request.POST.get('setor', '').strip() or None
        telefone = request.POST.get('telefone', '').strip() or None
        morada = request.POST.get('morada', '').strip() or None

        if not nome:
            messages.error(request, 'Preencha o nome da empresa para continuar.')
        else:
            basedados.cliente_criar(
                nome=nome,
                email=email,
                nif=nif,
                setor=setor,
                telefone=telefone,
                morada=morada,
                empresa_id=None,
            )
            messages.success(request, 'Cliente criado com sucesso.')
            return redirect(reverse('kikibyte:dashboard') + '?tab=clientes')

    return render(request, 'kikibyte/cliente_form.html', {
        'selected_tab': 'clientes',
    })


def cliente_editar(request, cliente_id):
    cliente = basedados.cliente_ler_por_id(cliente_id)
    if not cliente:
        raise Http404('Cliente não encontrado')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip() or None
        nif = request.POST.get('nif', '').strip() or None
        setor = request.POST.get('setor', '').strip() or None
        telefone = request.POST.get('telefone', '').strip() or None
        morada = request.POST.get('morada', '').strip() or None

        if not nome:
            messages.error(request, 'Preencha o nome da empresa para continuar.')
        else:
            basedados.cliente_atualizar(
                id_cliente=cliente_id,
                nome=nome,
                email=email,
                nif=nif,
                setor=setor,
                telefone=telefone,
                morada=morada,
                ativo=True,
            )
            messages.success(request, 'Cliente atualizado com sucesso.')
            return redirect(reverse('kikibyte:dashboard') + '?tab=clientes')

    return render(request, 'kikibyte/cliente_form.html', {
        'selected_tab': 'clientes',
        'cliente': cliente,
    })


def seed_demo_dashboard_data():
    clientes = basedados.cliente_ler_todos(apenas_ativos=False)
    if not clientes:
        basedados.cliente_criar(
            nome='SecuriBank',
            email='demo1@securibyte.pt',
            nif='503214561',
            setor='Financeiro',
            telefone='219000111',
            morada='Rua Demo 1'
        )
        basedados.cliente_criar(
            nome='AuditPro',
            email='demo2@securibyte.pt',
            nif='503214562',
            setor='Consultoria',
            telefone='219000222',
            morada='Avenida Inovação 45'
        )
        clientes = basedados.cliente_ler_todos(apenas_ativos=False)

    documentos = basedados.documento_ler_todos()
    if not documentos and clientes:
        first_client = clientes[0]
        second_client = clientes[1] if len(clientes) > 1 else clientes[0]
        basedados.documento_criar(
            cliente_id=first_client['id_cliente'],
            titulo='Relatório NIS2',
            tipo_documento='Relatório',
            ficheiro_base64='demo-document-1',
            mime_type='application/pdf',
            tamanho_bytes=1024,
            pedido_id=None,
            uploaded_by=None,
            sensivel=False,
            visivel_cliente=False
        )
        basedados.documento_criar(
            cliente_id=second_client['id_cliente'],
            titulo='Plano de Continuidade',
            tipo_documento='Plano',
            ficheiro_base64='demo-document-2',
            mime_type='application/pdf',
            tamanho_bytes=2048,
            pedido_id=None,
            uploaded_by=None,
            sensivel=False,
            visivel_cliente=False
        )
        documentos = basedados.documento_ler_todos()

    return clientes, documentos


# ── DASHBOARD ────────────────────────────────────────────────────────────────
def dashboard(request):
    selected_tab = request.GET.get('tab', 'dashboard')

    # Métricas base
    total_contactos   = len(basedados.contacto_ler_todos())
    contactos_novos   = len(basedados.contacto_ler_todos(estado='novo'))
    total_clientes    = len(basedados.cliente_ler_todos())
    total_artigos     = len(basedados.artigo_ler_todos(apenas_publicados=False))
    total_pedidos     = len(basedados.pedido_ler_todos())
    pedidos_pendentes = len(basedados.pedido_ler_todos(estado='pendente'))

    # ── 5 Requisitos obrigatórios ──────────────────────────────
    conformidade_dados   = basedados.dash_clientes_por_conformidade()
    top5_incidentes      = basedados.dash_top5_clientes_incidentes()
    docs_por_mes         = basedados.dash_documentos_por_cliente_mes()
    utilizadores_perfil  = basedados.dash_utilizadores_por_perfil()
    pedidos_stats        = basedados.dash_pedidos_estado_e_tempo_medio()

    # Formata conformidade como dicionário para acesso fácil no template
    conformidade_map = {
        row['estado_conformidade']: row['total']
        for row in conformidade_dados
    }

    context = {
        # Contexto da aba selecionada
        'selected_tab': selected_tab,

        # Métricas base
        'total_contactos':   total_contactos,
        'contactos_novos':   contactos_novos,
        'total_clientes':    total_clientes,
        'total_artigos':     total_artigos,
        'total_pedidos':     total_pedidos,
        'pedidos_pendentes': pedidos_pendentes,

        # Requisito 1
        'conformidade_dados':    conformidade_dados,
        'conf_conforme':         conformidade_map.get('conforme', 0),
        'conf_em_avaliacao':     conformidade_map.get('em_avaliacao', 0),
        'conf_com_pendencias':   conformidade_map.get('com_pendencias', 0),

        # Requisito 2
        'top5_incidentes':       top5_incidentes,

        # Requisito 3
        'docs_por_mes':          docs_por_mes[:10],  # últimos 10 registos

        # Requisito 4
        'utilizadores_perfil':   utilizadores_perfil,

        # Requisito 5
        'pedidos_por_estado':    pedidos_stats['por_estado'],
        'pedidos_tempo_medio':   pedidos_stats['tempo_medio'],
    }

    page_titles = {
        'dashboard': 'Visão Geral',
        'clientes': 'Clientes',
        'documentos': 'Documentos',
        'pedidos': 'Pedidos de Acesso',
        'noticias': 'Notícias',
    }
    page_subtitles = {
        'dashboard': 'Visão geral da gestão de clientes e documentos',
        'clientes': 'Gerencie a base de clientes e contacte as empresas registadas.',
        'documentos': 'Revise e organize todos os documentos carregados pelos clientes.',
        'pedidos': 'Acompanhe os pedidos de acesso e incidentes pendentes.',
        'noticias': 'Gerencie os artigos e notícias do portal.',
    }
    page_icons = {
        'dashboard': '📊',
        'clientes': '👥',
        'documentos': '📄',
        'pedidos': '📝',
        'noticias': '📰',
    }

    if selected_tab not in page_titles:
        selected_tab = 'dashboard'

    context.update({
        'selected_tab': selected_tab,
        'page_title': page_titles[selected_tab],
        'page_subtitle': page_subtitles[selected_tab],
        'page_icon': page_icons[selected_tab],
    })

    clientes = basedados.cliente_ler_todos(apenas_ativos=False)
    documentos = basedados.documento_ler_todos()
    if not clientes or not documentos:
        clientes, documentos = seed_demo_dashboard_data()

    context.update({
        'clientes_list': clientes,
        'clientes': clientes,
        'documentos': documentos,
        'pedidos': basedados.pedido_ler_todos(),
        'contactos': basedados.contacto_ler_todos(),
        'artigos': basedados.artigo_ler_todos(apenas_publicados=False),
    })
    return render(request, 'kikibyte/dashboard.html', context)


def cliente_eliminar(request, cliente_id):
    if request.method == 'POST':
        basedados.cliente_eliminar(cliente_id)
        messages.success(request, 'Cliente eliminado com sucesso.')
    return redirect(reverse('kikibyte:dashboard') + '?tab=clientes')


def documento_eliminar(request, documento_id):
    if request.method == 'POST':
        basedados.documento_eliminar(documento_id)
        messages.success(request, 'Documento eliminado com sucesso.')
    return redirect(reverse('kikibyte:dashboard') + '?tab=documentos')