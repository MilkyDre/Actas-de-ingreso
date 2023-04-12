from django.contrib import admin

# Register your models here.
from .models import *

class EquipoAdmin(admin.ModelAdmin):
    list_display = ('serial', 'marca', 'modelo', 'tipo', 'estado', 'depto')
    list_filter = ('serial', 'marca', 'modelo', 'tipo', 'estado', 'depto')
    search_fields = ('serial', 'marca', 'modelo', 'tipo', 'estado', 'depto')

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id_departamento', 'nombre_departamento')
    list_filter = ('id_departamento', 'nombre_departamento')
    search_fields = ('id_departamento', 'nombre_departamento')

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('rut_funcionario', 'nombre', 'apellido', 'telefono', 'email')
    list_filter = ('rut_funcionario', 'nombre', 'apellido', 'telefono', 'email')
    search_fields = ('rut_funcionario', 'nombre', 'apellido', 'telefono', 'email')

class IngresoAdmin(admin.ModelAdmin):
    list_display = ('descripcion_problema', 'perifericos', 'fecha_ingreso', 'equipo', 'estado_equipo', 'fecha_salida', 'descripcion_reparacion', 'funcionario', 'tecnico')
    list_filter = ('descripcion_problema', 'perifericos', 'fecha_ingreso', 'equipo', 'estado_equipo', 'fecha_salida', 'descripcion_reparacion', 'funcionario', 'tecnico')
    search_fields = ('descripcion_problema', 'perifericos', 'fecha_ingreso', 'equipo', 'estado_equipo', 'fecha_salida', 'descripcion_reparacion', 'funcionario', 'tecnico')

class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('rut_tecnico', 'nombre')
    list_filter = ('rut_tecnico', 'nombre')
    search_fields = ('rut_tecnico', 'nombre')



admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Tecnico, TecnicoAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Funcionario,FuncionarioAdmin)
admin.site.register(Ingreso, IngresoAdmin)