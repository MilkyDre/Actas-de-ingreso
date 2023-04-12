from django import forms

from Actas.views import *
from .models import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from multiselectfield import MultiSelectField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field


class departamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['id_departamento', 'nombre_departamento']
        widgets = {
            'id_departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_departamento': forms.TextInput(attrs={'class': 'form-control'}),
        }

class equipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'
        widgets = {
            'serial': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'depto': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        
        }
        
class funcionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['rut_funcionario', 'nombre', 'apellido', 'telefono', 'email']
        widgets = {
            'rut_funcionario': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class tecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = '__all__'
        widgets = {
            'rut_tecnico': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),   
        }

class ingresoForm(forms.ModelForm):
    perifericos = forms.MultipleChoiceField(choices=Ingreso.P_CHOICES, widget=forms.CheckboxSelectMultiple())
    funcionario = forms.ModelChoiceField(queryset=Funcionario.objects.all())
    equipo = forms.ModelChoiceField(queryset=Equipo.objects.all())
    tecnico = forms.ModelChoiceField(queryset=Tecnico.objects.all())

    class Meta:
        model = Ingreso
        fields = '__all__'
        widgets = {
            'descripcion_problema': forms.TextInput(attrs={'class': 'form-control'}),
            'perifericos': forms.CheckboxSelectMultiple(),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'equipo': forms.Select(attrs={'class': 'form-control'}),
            'estado_equipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'descripcion_reparacion': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

