from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorías"

class Perfume(models.Model):
    GENERO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
        ('U', 'Unisex'),
    ]
    
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=3)
    precio_descuento = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    tamano_ml = models.PositiveIntegerField(help_text="Tamaño en mililitros")
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='perfumes/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    def precio_con_descuento(self):
        return self.precio_descuento if self.precio_descuento else self.precio
    
    def tiene_descuento(self):
        return self.precio_descuento is not None
