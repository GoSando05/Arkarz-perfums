from django.urls import path
from . import views

app_name = 'perfumes'

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    
    # Productos
    path('productos/', views.productos, name='productos'),
    
    # Detalle del perfume
    path('perfume/<int:perfume_id>/', views.detalle_perfume, name='detalle_perfume'),
    
    # Marcas
    path('marcas/', views.marcas, name='marcas'),
    path('marca/<int:marca_id>/', views.perfumes_por_marca, name='perfumes_por_marca'),
    
    # Búsqueda AJAX
    path('buscar/', views.buscar_perfumes_ajax, name='buscar_ajax'),
    
    # Contacto
    path('contacto/', views.contacto, name='contacto'),
]