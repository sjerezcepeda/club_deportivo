from datetime import date

from django.db import models
from django.db.models import Q


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    fecha_nacimiento = models.DateField()

    posicion = models.CharField(max_length=50)

    numero_camiseta = models.IntegerField(unique=True)

    fecha_ingreso = models.DateField()

    activo = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(numero_camiseta__gte=1) &
                      Q(numero_camiseta__lte=99),
                name='numero_camiseta_entre_1_y_99'
            ),
            models.UniqueConstraint(
                fields=['nombre', 'apellido'],
                name='nombre_apellido_unico'
            )
        ]

    def calcular_edad(self):
        hoy = date.today()

        edad = hoy.year - self.fecha_nacimiento.year

        if (hoy.month, hoy.day) < (
            self.fecha_nacimiento.month,
            self.fecha_nacimiento.day
        ):
            edad = edad - 1

        return edad

    def __str__(self):
        return self.nombre + " " + self.apellido