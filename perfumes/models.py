from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='marcas/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

class Perfume(models.Model):
    SEXO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
        ('U', 'Unisex'),
    ]
    
    TAMAÑO_CHOICES = [
        ('30ml', '30ml'),
        ('50ml', '50ml'),
        ('100ml', '100ml'),
        ('150ml', '150ml'),
    ]
    
    nombre = models.CharField(max_length=200)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='perfumes')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    tamaño = models.CharField(max_length=10, choices=TAMAÑO_CHOICES, default='100ml')
    precio = models.DecimalField(max_digits=10, decimal_places=3)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='perfumes/')
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.marca.nombre} - {self.nombre} ({self.sexo})"
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Perfume'
        verbose_name_plural = 'Perfumes'
    
    @property
    def disponible(self):
        return self.stock > 0 and self.activo

    @property
    def precio_con_impuesto(self):
        return self.precio * 1.21  # Suponiendo un impuesto del 21%

