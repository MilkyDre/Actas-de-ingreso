from rest_framework.routers import DefaultRouter
from Actas.api.views import IngresoApiViewSet, DepartamentoApiViewSet, FuncionarioApiViewSet, EquipoApiViewSet

router = DefaultRouter()

router.register(r'ingresos', IngresoApiViewSet, basename='ingresos')
router.register(r'departamentos', DepartamentoApiViewSet, basename='departamentos')
router.register(r'funcionarios', FuncionarioApiViewSet, basename='funcionarios')
router.register(r'equipos', EquipoApiViewSet, basename='equipos')
