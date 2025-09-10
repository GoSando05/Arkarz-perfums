from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Perfume, Marca

def home(request):
    """Vista de la página principal"""
    perfumes_destacados = Perfume.objects.filter(activo=True)[:8]  # Primeros 8 perfumes activos
    marcas = Marca.objects.filter(activo=True)
    
    context = {
        'perfumes': perfumes_destacados,
        'marcas': marcas,
        'titulo': 'Perfumes Árabes - Arkarz Perfums'
    }
    return render(request, 'perfumes/home.html', context)

def productos(request):
    """Vista de la página de productos con filtros"""
    
    # Obtener parámetros de filtro
    marca_id = request.GET.get('marca', '')
    sexo = request.GET.get('sexo', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    busqueda = request.GET.get('q', '')
    
    # Consulta base
    perfumes = Perfume.objects.filter(activo=True)
    
    # Filtros
    if marca_id:
        perfumes = perfumes.filter(marca_id=marca_id)
    
    if sexo:
        perfumes = perfumes.filter(sexo=sexo)
    
    if precio_min:
        try:
            perfumes = perfumes.filter(precio__gte=float(precio_min))
        except ValueError:
            pass
    
    if precio_max:
        try:
            perfumes = perfumes.filter(precio__lte=float(precio_max))
        except ValueError:
            pass
    
    if busqueda:
        perfumes = perfumes.filter(
            Q(nombre__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda) |
            Q(marca__nombre__icontains=busqueda)
        )
    
    # Ordenamiento
    orden = request.GET.get('orden', 'nombre')
    if orden == 'precio_asc':
        perfumes = perfumes.order_by('precio')
    elif orden == 'precio_desc':
        perfumes = perfumes.order_by('-precio')
    elif orden == 'nombre':
        perfumes = perfumes.order_by('nombre')
    elif orden == 'nuevo':
        perfumes = perfumes.order_by('-id')
    
    # Paginación
    paginator = Paginator(perfumes, 12)  # 12 perfumes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener todas las marcas para el filtro
    marcas = Marca.objects.filter(activo=True)
    
    context = {
        'page_obj': page_obj,
        'perfumes': page_obj,
        'marcas': marcas,
        'marca_seleccionada': marca_id,
        'sexo_seleccionado': sexo,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'busqueda': busqueda,
        'orden': orden,
        'total_perfumes': perfumes.count(),
        'titulo': 'Productos - Arkarz Perfums'
    }
    
    return render(request, 'perfumes/productos.html', context)

def detalle_perfume(request, perfume_id):
    """Vista del detalle de un perfume específico"""
    perfume = get_object_or_404(Perfume, id=perfume_id, activo=True)
    
    # Perfumes relacionados (misma marca o mismo sexo)
    perfumes_relacionados = Perfume.objects.filter(
        activo=True
    ).filter(
        Q(marca=perfume.marca) | Q(sexo=perfume.sexo)
    ).exclude(id=perfume.id)[:4]
    
    context = {
        'perfume': perfume,
        'perfumes_relacionados': perfumes_relacionados,
        'titulo': f'{perfume.nombre} - Arkarz Perfums'
    }
    
    return render(request, 'perfumes/detalle.html', context)

def buscar_perfumes_ajax(request):
    """Vista AJAX para búsqueda rápida"""
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if len(query) >= 3:  # Solo buscar si hay al menos 3 caracteres
            perfumes = Perfume.objects.filter(
                Q(nombre__icontains=query) | 
                Q(marca__nombre__icontains=query),
                activo=True
            )[:5]  # Máximo 5 resultados
            
            resultados = []
            for perfume in perfumes:
                resultados.append({
                    'id': perfume.id,
                    'nombre': perfume.nombre,
                    'marca': perfume.marca.nombre,
                    'precio': str(perfume.precio),
                    'imagen': perfume.imagen.url if perfume.imagen else '',
                    'url': f'/perfume/{perfume.id}/'
                })
            
            return JsonResponse({
                'success': True,
                'resultados': resultados
            })
    
    return JsonResponse({'success': False})

def marcas(request):
    """Vista de todas las marcas"""
    marcas = Marca.objects.filter(activo=True).order_by('nombre')
    
    context = {
        'marcas': marcas,
        'titulo': 'Marcas - Arkarz Perfums'
    }
    
    return render(request, 'perfumes/marcas.html', context)

def perfumes_por_marca(request, marca_id):
    """Vista de perfumes filtrados por marca"""
    marca = get_object_or_404(Marca, id=marca_id, activo=True)
    perfumes = Perfume.objects.filter(marca=marca, activo=True)
    
    # Paginación
    paginator = Paginator(perfumes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'marca': marca,
        'page_obj': page_obj,
        'perfumes': page_obj,
        'titulo': f'Perfumes {marca.nombre} - Arkarz Perfums'
    }
    
    return render(request, 'perfumes/productos.html', context)

def contacto(request):
    """Vista de la página de contacto"""
    context = {
        'titulo': 'Contacto - Arkarz Perfums'
    }
    return render(request, 'perfumes/contacto.html', context)
