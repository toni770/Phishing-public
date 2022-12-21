from django.db import models

# Create your models here.
class Empresas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.nombre

class Correos(models.Model):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField(max_length=50)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)

    def __str__(self):
        return self.correo
    
class Plantillas(models.Model):
    id = models.AutoField(primary_key=True)
    servicio = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()


    def __str__(self):
        return self.servicio
    
class Status_Mail(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False)
    num_open = models.IntegerField(default=0)
    fecha = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
    

class Status_Web(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False)
    num_open = models.IntegerField(default=0)
    fecha = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)    
    
class Intentos(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=20, null=True, blank=True)
    contraseña = models.CharField(max_length=25, null=True, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    servicio = models.ForeignKey(Plantillas, on_delete=models.CASCADE)
    mail_status_id = models.ForeignKey(Status_Mail, on_delete=models.CASCADE)
    web_status_id = models.ForeignKey(Status_Web, on_delete=models.CASCADE)
    correo = models.ForeignKey(Correos, on_delete=models.CASCADE)               

    def __str__(self):
        return str(self.id)
    
