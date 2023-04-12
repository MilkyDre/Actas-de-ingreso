from rest_framework.serializers import ModelSerializer
from Actas.models import *

class IngresoSerializer(ModelSerializer):
    class Meta:
        model = Ingreso
        fields = '__all__'
class DepartamentoSerializer(ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class FuncionarioSerializer(ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'

class EquipoSerializer(ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'