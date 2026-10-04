from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Jugador
from .serializers import JugadorSerializer


class JugadorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    permission_classes = [IsAuthenticated]


class JugadorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    permission_classes = [IsAuthenticated]