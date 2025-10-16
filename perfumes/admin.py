from django.contrib import admin
from .models import Marca, Perfume, Calificacion

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'total_perfumes')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    list_editable = ('activo',)
    
    def total_perfumes(self, obj):
        return obj.perfumes.count()
    total_perfumes.short_description = 'Total Perfumes'


class CalificacionInline(admin.TabularInline):
    model = Calificacion
    extra = 0
    readonly_fields = ['fecha', 'ip_usuario']
    fields = ['puntuacion', 'comentario', 'ip_usuario', 'fecha']


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'sexo', 'tamaño', 'precio', 'stock', 'activo', 'destacado', 'calificacion_promedio', 'total_calificaciones')
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
    inlines = [CalificacionInline]
    
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
    
    def calificacion_promedio(self, obj):
        return f"{obj.calificacion_promedio} ⭐"
    calificacion_promedio.short_description = 'Calificación'
    
    def total_calificaciones(self, obj):
        return obj.total_calificaciones
    total_calificaciones.short_description = 'Nº Calificaciones'


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


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['perfume', 'puntuacion', 'ip_usuario', 'fecha', 'tiene_comentario']
    list_filter = ['puntuacion', 'fecha']
    search_fields = ['perfume__nombre', 'comentario', 'ip_usuario']
    readonly_fields = ['fecha']
    date_hierarchy = 'fecha'
    
    def tiene_comentario(self, obj):
        return '✓' if obj.comentario else '✗'
    tiene_comentario.short_description = 'Comentario'