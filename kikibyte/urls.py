from django.urls import path
from . import views

app_name = 'kikibyte'

urlpatterns = [
    path('', views.index, name='index'),
    path('contacto/', views.contacto, name='contacto'),
    path('contacto/sucesso/', views.contacto_sucesso, name='contacto_sucesso'),
    path('artigos/', views.artigos_lista, name='artigos_lista'),
    path('artigos/<int:artigo_id>/', views.artigo_detalhe, name='artigo_detalhe'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]