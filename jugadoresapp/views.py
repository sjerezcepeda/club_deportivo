from django.shortcuts import render, redirect, get_object_or_404
from .models import Jugador
from .forms import JugadorForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def inicio(request):
    return render(request, 'jugadoresapp/inicio.html')

@login_required
def lista_jugadores(request):
    jugadores = Jugador.objects.all()
    return render(
        request,
        'jugadoresapp/lista.html',
        {'jugadores': jugadores}
    )

@login_required
def crear_jugador(request):
    if request.method == 'POST':
        formulario = JugadorForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_jugadores')
    else:
        formulario = JugadorForm()

    return render(
        request,
        'jugadoresapp/crear.html',
        {'formulario': formulario}
    )

@login_required
def editar_jugador(request, id):
    jugador = get_object_or_404(Jugador, id=id)

    if request.method == 'POST':
        formulario = JugadorForm(
            request.POST,
            instance=jugador
        )

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_jugadores')
    else:
        formulario = JugadorForm(instance=jugador)

    return render(
        request,
        'jugadoresapp/editar.html',
        {
            'formulario': formulario,
            'jugador': jugador
        }
    )

@login_required
def eliminar_jugador(request, id):
    jugador = get_object_or_404(Jugador, id=id)

    if request.method == 'POST':
        jugador.delete()
        return redirect('lista_jugadores')

    return render(
        request,
        'jugadoresapp/eliminar.html',
        {'jugador': jugador}
    )
class LoginApiView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        usuario = authenticate(
            username=username,
            password=password
        )

        if usuario is not None:
            token, creado = Token.objects.get_or_create(
                user=usuario
            )

            return Response({
                'mensaje': 'Autenticacion correcta',
                'usuario': usuario.username,
                'token': token.key
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Usuario o contraseña incorrectos'
        }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutApiView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        return Response({
            'mensaje': 'Sesión cerrada correctamente.'
        }, status=status.HTTP_200_OK)