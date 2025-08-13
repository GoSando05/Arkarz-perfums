from django.contrib import admin
from .models import Categoria, Perfume

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'precio_descuento', 'genero', 'stock', 'activo']
    list_filter = ['categoria', 'genero', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'precio_descuento', 'stock', 'activo']
    fields = ['nombre', 'categoria', 'descripcion', 'precio', 'precio_descuento', 'genero', 'tamano_ml', 'stock', 'activo', 'imagen']