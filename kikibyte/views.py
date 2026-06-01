from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .forms import FormularioContactoForm
from . import basedados


# ── PÁGINA PRINCIPAL ─────────────────────────────────────────────────────────

def index(request):
    servicos       = basedados.servico_ler_todos(apenas_visiveis=True)
    artigos_recentes = basedados.artigo_ler_todos(apenas_publicados=True, limite=3)
    return render(request, 'kikibyte/index.html', {
        'servicos': servicos,
        'artigos_recentes': artigos_recentes,
    })


# ── CONTACTO ─────────────────────────────────────────────────────────────────

def contacto(request):
    if request.method == 'POST':
        form = FormularioContactoForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            basedados.contacto_criar(
                nome=d['nome'],
                email=d['email'],
                assunto=d['assunto'],
                mensagem=d['mensagem'],
                telefone=d.get('telefone'),
            )
            # Regista o log
            basedados.log_criar(
                acao='criar', entidade='formulario_contacto',
                ip_origem=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('kikibyte:contacto_sucesso')
        messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = FormularioContactoForm()
    return render(request, 'kikibyte/index.html',
                  {'form_contacto': form, 'scroll_to': 'contact'})


def contacto_sucesso(request):
    return render(request, 'kikibyte/index.html', {'contacto_enviado': True})


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

def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        utilizador = basedados.utilizador_ler_por_email(email)

        if utilizador and check_password(password, utilizador['password_hash']):
            if not utilizador['ativo']:
                messages.error(request, 'Conta desativada. Contacte o administrador.')
            else:
                # Guarda dados na sessão
                request.session['user_id']        = utilizador['id_utilizador']
                request.session['user_nome']      = utilizador['nome']
                request.session['user_email']     = utilizador['email']
                request.session['user_role']      = utilizador['role_nome']
                request.session['authenticated']  = True

                # Atualiza último login
                basedados.utilizador_atualizar_ultimo_login(utilizador['id_utilizador'])
                basedados.log_criar(
                    acao='login', entidade='utilizador',
                    entidade_id=utilizador['id_utilizador'],
                    utilizador_id=utilizador['id_utilizador'],
                    ip_origem=request.META.get('REMOTE_ADDR')
                )

                role = utilizador['role_nome']
                if role == 'administrador':
                    return redirect('kikibyte:dashboard')
                elif role == 'gestor':
                    return redirect('kikibyte:dashboard')
                else:
                    return redirect('kikibyte:index')
        else:
            messages.error(request, 'Email ou password incorretos.')

    return render(request, 'kikibyte/login.html')


def logout_view(request):
    if request.session.get('authenticated'):
        basedados.log_criar(
            acao='logout', entidade='utilizador',
            entidade_id=request.session.get('user_id'),
            utilizador_id=request.session.get('user_id'),
            ip_origem=request.META.get('REMOTE_ADDR')
        )
    request.session.flush()
    return redirect('kikibyte:index')


# ── DECORADOR de sessão personalizado ────────────────────────────────────────

def session_required(view_func):
    """Substitui @login_required para usar a nossa sessão."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('authenticated'):
            messages.error(request, 'Tens de iniciar sessão para aceder a esta página.')
            return redirect('kikibyte:login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def admin_required(view_func):
    """Apenas administradores."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('authenticated'):
            return redirect('kikibyte:login')
        if request.session.get('user_role') not in ('administrador', 'gestor'):
            messages.error(request, 'Não tens permissão para aceder a esta página.')
            return redirect('kikibyte:index')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── DASHBOARD ────────────────────────────────────────────────────────────────

@admin_required
def dashboard(request):
    total_contactos      = len(basedados.contacto_ler_todos())
    contactos_novos      = len(basedados.contacto_ler_todos(estado='novo'))
    total_clientes       = len(basedados.cliente_ler_todos())
    total_artigos        = len(basedados.artigo_ler_todos(apenas_publicados=False))
    total_servicos       = len(basedados.servico_ler_todos(apenas_visiveis=False))
    total_pedidos        = len(basedados.pedido_ler_todos())
    pedidos_pendentes    = len(basedados.pedido_ler_todos(estado='pendente'))
    ultimos_contactos    = basedados.contacto_ler_todos(estado='novo')[:5]
    ultimos_pedidos      = basedados.pedido_ler_todos(estado='pendente')[:5]
    logs_recentes        = basedados.log_ler_todos(limite=10)

    context = {
        'total_contactos':   total_contactos,
        'contactos_novos':   contactos_novos,
        'total_clientes':    total_clientes,
        'total_artigos':     total_artigos,
        'total_servicos':    total_servicos,
        'total_pedidos':     total_pedidos,
        'pedidos_pendentes': pedidos_pendentes,
        'ultimos_contactos': ultimos_contactos,
        'ultimos_pedidos':   ultimos_pedidos,
        'logs_recentes':     logs_recentes,
    }
    return render(request, 'kikibyte/dashboard.html', context)