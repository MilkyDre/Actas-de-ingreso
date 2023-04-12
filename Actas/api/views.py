from rest_framework.viewsets import ModelViewSet
from Actas.models import *
from Actas.api.serializers import IngresoSerializer, DepartamentoSerializer, FuncionarioSerializer, EquipoSerializer

class IngresoApiViewSet(ModelViewSet):
    queryset = Ingreso.objects.all()
    serializer_class = IngresoSerializer

class DepartamentoApiViewSet(ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class FuncionarioApiViewSet(ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

class EquipoApiViewSet(ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
