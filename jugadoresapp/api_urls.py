from django.urls import path

from .api_views import (
    JugadorDetailAPIView,
    JugadorListCreateAPIView
)
from .views import LoginApiView, LogoutApiView


urlpatterns = [
    path(
        'login/',
        LoginApiView.as_view(),
        name='api_login'
    ),

    path(
        'logout/',
        LogoutApiView.as_view(),
        name='api_logout'
    ),

    path(
        'jugadores/',
        JugadorListCreateAPIView.as_view(),
        name='api_jugadores'
    ),

    path(
        'jugadores/<int:pk>/',
        JugadorDetailAPIView.as_view(),
        name='api_jugador_detalle'
    ),
]