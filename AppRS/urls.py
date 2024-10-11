from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('iniciosesion/', views.inicio_sesion, name='iniciosesion'),
    path('crearcuenta/', views.crear_cuenta, name='crearcuenta'),
    path('cerrarsesion/', views.cerrar_sesion, name='cerrarsesion'),
    path('home/', views.home, name='home'),
    path('privacidad/', views.privacidad, name='privacidad'),
    path('terminos/', views.terminos, name='terminos'),
    path('buscar/', views.buscar, name='buscar'),
    path('publicacion/crear/',views.addPublicacion, name='crearPublicacion'),
    path('perfil/', views.perfil, name='perfil'),  # Muestra el perfil del usuario autenticado
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/<str:username>/', views.perfil, name='ver_perfil'),  # Muestra el perfil de otro usuario por su nombre de usuario
    path('publicacion/editar/<int:post_id>/', views.editarPublicacion, name='editarPublicacion'),
    path('publicacion/eliminar/<int:post_id>/', views.EliminarPubli, name='eliminarPublicacion'),
    path('publicacion/guardar/', views.toggle_guardar_publicacion, name='toggle_guardar_publicacion')



   
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    