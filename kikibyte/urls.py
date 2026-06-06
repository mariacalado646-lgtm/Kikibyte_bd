from django.urls import path
from . import views

app_name = 'kikibyte'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard),
    path('contacto/', views.contacto, name='contacto'),
    path('contacto/sucesso/', views.contacto_sucesso, name='contacto_sucesso'),
    path('artigos/', views.artigos_lista, name='artigos_lista'),
    path('artigos/<int:artigo_id>/', views.artigo_detalhe, name='artigo_detalhe'),
    path('dashboard/documentos/upload/', views.documento_upload, name='documento_upload'),
    path('dashboard/documentos/<int:documento_id>/download/', views.documento_download, name='documento_download'),
    path('dashboard/documentos/<int:documento_id>/ver/', views.documento_visualizar, name='documento_visualizar'),
    path('dashboard/clientes/novo/', views.cliente_novo, name='cliente_novo'),
    path('dashboard/clientes/editar/<int:cliente_id>/', views.cliente_editar, name='cliente_editar'),
    path('dashboard/clientes/eliminar/<int:cliente_id>/', views.cliente_eliminar, name='cliente_eliminar'),
    path('dashboard/documentos/eliminar/<int:documento_id>/', views.documento_eliminar, name='documento_eliminar'),
]