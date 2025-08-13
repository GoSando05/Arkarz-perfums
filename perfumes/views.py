from django.shortcuts import render, get_object_or_404
from .models import Perfume, Categoria

def home(request):
    # Mostrar los perfumes más recientes
    productos_destacados = Perfume.objects.filter(activo=True)[:8]
    categorias = Categoria.objects.all()
    
    context = {
        'productos_destacados': productos_destacados,
        'categorias': categorias,
    }
    return render(request, 'perfumes/home.html', context)

def productos(request):
    productos = Perfume.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    
    context = {
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, 'perfumes/productos.html', context)
