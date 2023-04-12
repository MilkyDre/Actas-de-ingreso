from collections import Counter
from io import BytesIO
from itertools import cycle
from django.db import models
from PIL import Image, ImageDraw
from multiselectfield import MultiSelectField
from rest_framework import serializers
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from qrcode import make as qr_make
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import qrcode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.core.validators import validate_integer
from django.core.files.uploadedfile import InMemoryUploadedFile




RUT_REGEX = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){2})\-([\dkK])$')

def validate_rut(value):
    if not RUT_REGEX.match(value):
        raise ValidationError('RUT inválido')
    rut, dv = value.split('-')
    rut = rut.replace('.', '')
    if dv.lower() == 'k':
        dv = '10'
    rut = int(rut)
    dv = int(dv)
    m = 0
    for i, c in enumerate(reversed(str(rut))):
        m += int(c) * (2 + i % 6)
    if dv != 11 - m % 11:
        raise ValidationError('RUT inválido')

# Create your models here.
class Departamento(models.Model):
    id_departamento = models.CharField(max_length=6, primary_key=True, unique=True)
    nombre_departamento = models.CharField(max_length=50)

    def __str__(self):
        return self.id_departamento + ' - ' + self.nombre_departamento
    
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        db_table = "Departamento"

class Equipo(models.Model):
    serial = models.CharField(max_length=50, primary_key=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    codigo_qr = models.ImageField(upload_to='media/codigos_qr', null=True, blank=True)
    tipo_equipo = [
        ('PC','PC'),
        ('Laptop','Laptop'),
        ('Impresora','Impresora'),
        ('Monitor','Monitor'),
        ('Otro','Otro'),
    ]
    tipo = models.CharField(max_length=50, choices=tipo_equipo)
    depto = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    estado_choices = [
        ('Activo','Activo'),
        ('Inactivo','Inactivo'),
    ]
    estado = models.CharField(max_length=50, choices=estado_choices)

    def __str__(self):
        return self.serial + ' - ' + self.modelo
    

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        db_table = "Equipo"


class Funcionario(models.Model):
    rut_funcionario = models.CharField(max_length=12,
                                                      help_text="el rut debe ser con puntos y guión",primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=8)
    email = models.EmailField(validators=[validate_email], 
                              help_text="Ingrese un email válido con dominio @municoquimbo.cl")

    def clean(self):
        super().clean()
        if self.email:
            if not self.email.endswith('@municoquimbo.cl'):
                raise ValidationError('El email debe tener el dominio @municoquimbo.cl')
            

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)
    
    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"
        db_table = "Funcionario"
    
class Tecnico(models.Model):
    rut_tecnico = models.CharField(max_length=12, validators=[validate_rut], primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(validators=[validate_email])

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)
    
    class Meta:
        verbose_name = "Tecnico"
        verbose_name_plural = "Tecnicos"
        db_table = "Tecnico"
      
class Ingreso(models.Model):
    id_ingreso = models.AutoField(primary_key=True)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)
    descripcion_problema = models.CharField(max_length=50)
    
    ESTADO = [
        ('En espera','En espera'),
        ('En reparacion','En reparacion'),
        ('Reparado','Reparado'),
        ('No reparado', 'No reparado')
    ]
    estado_equipo = models.CharField(max_length=50, choices=ESTADO, default='En espera')
    
    P_CHOICES = (
        ('No Aplica','No Aplica'),
        ('Mouse','Mouse'),
        ('Teclado','Teclado'),
        ('Cable de poder','Cable de poder'),
        ('Cargador','Cargador'),
        ('Cable de USB','Cable de USB'),
        ('Pantalla','Pantalla'),
    )

    perifericos = MultiSelectField(choices = P_CHOICES, max_length=100, blank=True, null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    #llaves foraneas
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    fecha_salida = models.DateTimeField(blank=True, null=True)
    descripcion_reparacion = models.CharField(max_length=50, blank=True, null=True)

    @receiver(pre_save, sender='Actas.Ingreso')
    def actualizar_fecha_salida(sender, instance, **kwargs):
        if instance.estado_equipo == 'Reparado' and not instance.fecha_salida:
            instance.fecha_salida = timezone.now()
            instance.descripcion_reparacion = "Sin descripción"

    @receiver(post_save, sender='Actas.Ingreso')
    def guardar_cambio_estado(sender, instance, **kwargs):
        if instance.estado_equipo == 'Reparado' and not instance.fecha_salida:
            instance.fecha_salida = timezone.now()
            instance.descripcion_reparacion = "Sin descripción"
            instance.save()

    def asignar_tecnico(self):
        tecnicos = Tecnico.objects.annotate(num_ingresos=Counter('ingreso')).order_by('num_ingresos')
        for tecnico in tecnicos:
            if tecnico.num_ingresos < settings.MAX_INGRESOS_POR_TECNICO:
                self.tecnico = tecnico
                self.asignado_a = tecnico.pk
                self.save()
                return True
        return False
    
    def change_status(self):
        if self.estado_equipo == 'En espera':
            asignado = self.asignar_tecnico()
            if asignado:
                # Enviamos un correo electrónico al técnico asignado
                subject = 'Nueva solicitud de ingreso asignada'
                message = render_to_string('email_template.html', {'ingreso': self})
                plain_message = strip_tags(message)
                from_email = settings.EMAIL_HOST_USER
                to_email = self.tecnico.email
                send_mail(subject, plain_message, from_email, [to_email], html_message=message)
            else:
                # No hay técnicos disponibles para asignar
                pass
        elif self.estado_equipo == 'Reparado':
            # Enviamos un correo electrónico al funcionario
            subject = 'Equipo listo para entrega'
            message = render_to_string('email_template.html', {'ingreso': self})
            plain_message = strip_tags(message)
            from_email = settings.EMAIL_HOST_USER
            to_email = self.funcionario.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=message)
        elif self.estado_equipo == 'En reparación':
            # Asignamos la fecha de entrada
            self.fecha_entrada = timezone.now()
            self.save()
        elif self.estado_equipo == 'No reparado':
            # Asignamos la fecha de rechazo
            self.fecha_salida = timezone.now()
            self.save()

    def equipo_estado_class(self):
        if self.estado_equipo == 'En espera':
            return 'en-espera'
        elif self.estado_equipo == 'Reparado':
            return 'reparado'
        elif self.estado_equipo == 'En reparación':
            return 'en-reparacion'
        elif self.estado_equipo == 'No reparado':
            return 'no-reparado'

    def __str__(self):
        return str(self.id_ingreso)
    
    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"
        db_table = "Ingreso"
