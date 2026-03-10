from django.db import models

# Create your models here.
class Autor(models.Model):
    nombre=models.CharField(max_length=100)
    apellido=models.CharField(max_length=100)
    fecha_nacimiento=models.DateField()
    nacionalidad = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    
class libro (models.Model) :
    GENEROS= [
        ('ficcion','ficcion'),
        ("no_ficcion","no_ficcion"),
        ("fantasia","fantasia"),
        ("ciencia","ciencia"),
        ("historia","historia"),
    ]  
    titulo=models.CharField(max_length=200)
    autor=models.ForeignKey(Autor,on_delete=models.CASCADE)
    isbn= models.CharField(max_length=20)
    fecha_nacimiento=models.DateField()
    genero=models.CharField(max_length=20,choices=GENEROS)
    paginas=models.PositiveBigIntegerField()
    disponible=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.titulo}"
    
class prestamo(models.Model):
    libro=models.ForeignKey(libro,on_delete=models.CASCADE)
    fecha_prestamo=models.DateField()
    fecha_devolucion=models.DateField()
    usuario= models.ForeignKey("auth.User",on_delete=models.CASCADE)
    devuelto = models.BooleanField(default=False)
    def __str__(self):
        return f"Prestamo de {self.libro.titulo} el {self.user.username}"
    
    
    