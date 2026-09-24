from django.shortcuts import render, redirect, get_object_or_404
from .models import Jugador
from .forms import JugadorForm


def inicio(request):
    return render(request, 'jugadoresapp/inicio.html')


def lista_jugadores(request):
    jugadores = Jugador.objects.all()
    return render(
        request,
        'jugadoresapp/lista.html',
        {'jugadores': jugadores}
    )


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