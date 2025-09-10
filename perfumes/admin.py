# perfumes/admin.py
from django.contrib import admin
from .models import Marca, Perfume

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'total_perfumes')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    list_editable = ('activo',)
    
    def total_perfumes(self, obj):
        return obj.perfumes.count()
    total_perfumes.short_description = 'Total Perfumes'

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'sexo', 'tamaño', 'precio', 'stock', 'activo', 'destacado')
    list_filter = (
        'sexo',           # Filtro por sexo
        'marca',          # Filtro por marca
        'tamaño',         # Filtro por tamaño
        'activo',         # Filtro por estado activo
        'destacado',      # Filtro por destacado
        'fecha_creacion', # Filtro por fecha
    )
    search_fields = ('nombre', 'marca__nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'activo', 'destacado')
    list_per_page = 25
    
    # Campos que se muestran al editar
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'marca', 'sexo', 'tamaño')
        }),
        ('Precio y Stock', {
            'fields': ('precio', 'stock')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'imagen')
        }),
        ('Estado', {
            'fields': ('activo', 'destacado')
        }),
    )
    
    # Filtros personalizados por rango de precio
    def get_list_filter(self, request):
        filters = list(self.list_filter)
        filters.append(PrecioRangeFilter)
        return filters

# Filtro personalizado para rangos de precio
class PrecioRangeFilter(admin.SimpleListFilter):
    title = 'Rango de Precio'
    parameter_name = 'precio_range'
    
    def lookups(self, request, model_admin):
        return (
            ('0-50', '$0 - $50,000'),
            ('50-100', '$50,000 - $100,000'),
            ('100-200', '$100,000 - $200,000'),
            ('200+', 'Más de $200,000'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == '0-50':
            return queryset.filter(precio__gte=0, precio__lt=50000)
        if self.value() == '50-100':
            return queryset.filter(precio__gte=50000, precio__lt=100000)
        if self.value() == '100-200':
            return queryset.filter(precio__gte=100000, precio__lt=200000)
        if self.value() == '200+':
            return queryset.filter(precio__gte=200000)