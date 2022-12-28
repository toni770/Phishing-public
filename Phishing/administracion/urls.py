from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/<str:empresa>/<str:plantilla>', views.dashboard, name='dashboard-e-p'),
    path('dashboard/<str:empresa>', views.dashboard, name='dashboard-e'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('servicios/<str:op>', views.servicios_menu, name='servicios-menu'),
    path('cliente/<str:id>', views.clientes, name='clientes'),
    path('crearEmpresa', views.crear_empresa, name='crear-empresa'),
    path('crearCorreo/<str:id>', views.crear_correo, name='crear-correo'),
    path('borrarEmpresa/<str:id>', views.borrar_empresa, name='borrar-empresa'),
    path('borrarCorreo/<str:id>', views.borrar_correo, name='borrar-correo'),
    path('cambiarNombreEmpresa/<str:id>', views.cambiar_nombre_empresa, name='cambiar-nombre-empresa'),
    path('phishing/<str:id>', views.phishing, name='phishing'),
    path('logins/<str:intweb>/<str:servicio>', views.web_status, name='web-status'),
    path('status/<str:intmail>', views.mail_status, name='mail-status'),
    path('notFound', views.not_found, name='not-found'),
    path('plantilla', views.crear_plantilla, name='crear-plantilla'),
    path('borrarPlantilla/<str:id>', views.eliminar_plantilla, name='eliminar-plantilla'),
    path('editarPlantilla/<str:id>', views.editar_plantilla, name='editar-plantilla'),
    path('opciones/<str:op>', views.opciones_menu, name='opciones-menu'),
    path('logout', views.logout_view, name='logout'),
    path('test', views.testing, name='test'),
    path('<str:opcion>', views.index_menu, name='index-menu'),
]