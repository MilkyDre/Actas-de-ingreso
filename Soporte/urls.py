from django.contrib import admin
from django.urls import path, include
from Actas.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from Actas.api.router import router


app_name = 'Actas'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path ('accounts/', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/',login_required(logout_view), name='logout'),
    path('ingresos_list/', ingresos_list, name='ingresos_list'),
    path('ingresos_update/<int:id>/', ingresos_update, name='ingresos_update'),
    path('ingresos_delete/<int:id>/', ingresos_delete, name='ingresos_delete'),
    path('ingresos_create/', ingresos_create, name='ingresos_create'),
    path('ingresos_search/', ingresos_search, name='ingresos_search'),
    path('equipos_list/', equipos_list, name='equipos_list'),
    path('equipos_create/', equipos_create, name='equipos_create'),
    path('equipos_edit/<str:id>/', equipos_edit, name='equipos_edit' ),
    path('equipo_delete/<str:id>/', equipos_delete, name='equipos_delete'),
    path('equipo_detail/<str:serial>/', equipo_detail, name='equipo_detail'),
    path('departamentos_search/', departamentos_search, name='departamentos_search'),  
    path('departamentos_list', departamentos_list, name='departamentos_list'),
    path('departamentos_create/', departamentos_create, name='departamentos_create'),
    path('departamentos_edit/<str:id>/', departamentos_edit, name='departamentos_edit'),
    path('departamentos_delete/<str:id>/', departamentos_delete, name='departamentos_delete'),
    path('funcionarios_list/', funcionarios_list, name='funcionarios_list'),
    path('funcionarios_create/', funcionarios_create, name='funcionarios_create'),
    path('funcionarios_edit/<str:id>/', funcionarios_edit, name='funcionarios_edit'),
    path('funcionarios_delete/<str:id>/', funcionarios_delete, name='funcionarios_delete'),
    path('tecnicos_list/', tecnicos_list, name='tecnicos_list'),
    path('tecnicos_create/', tecnicos_create, name='tecnicos_create'),
    path('tecnicos_edit/<str:id>/', tecnicos_edit, name='tecnicos_edit'),
    path('tecnicos_delete/<str:id>/', tecnicos_delete, name='tecnicos_delete'),
    path('export_to_excel/', export_to_excel, name='export_to_excel'),
    path('grafico-ingresos/', grafico_ingresos, name='grafico_ingresos'),
    path('grafico_tecnicos/', grafico_tecnicos, name='grafico_tecnicos'),
    path('scan_qr/', scan_qr, name='scan_qr'),
    path('mantenimiento/', mantenimiento, name='mantenimiento'),
    path('tablas/', tablas, name='tablas')

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)