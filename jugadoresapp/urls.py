from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path(
        'jugadores/',
        views.lista_jugadores,
        name='lista_jugadores'
    ),
    path(
        'jugadores/crear/',
        views.crear_jugador,
        name='crear_jugador'
    ),
    path(
        'jugadores/editar/<int:id>/',
        views.editar_jugador,
        name='editar_jugador'
    ),
    path(
        'jugadores/eliminar/<int:id>/',
        views.eliminar_jugador,
        name='eliminar_jugador'
    ),
]