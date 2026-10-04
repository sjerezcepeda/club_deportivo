from datetime import date

from rest_framework import serializers

from .models import Jugador


class JugadorSerializer(serializers.ModelSerializer):

    edad = serializers.ReadOnlyField(
        source='calcular_edad'
    )

    class Meta:
        model = Jugador
        fields = [
            'id',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'edad',
            'posicion',
            'numero_camiseta',
            'fecha_ingreso',
            'activo'
        ]

    def validate_nombre(self, valor):
        valor = valor.strip()

        if len(valor) < 2:
            raise serializers.ValidationError(
                'El nombre debe tener al menos 2 letras.'
            )

        if not valor.isalpha():
            raise serializers.ValidationError(
                'El nombre solo puede contener letras.'
            )

        return valor.title()

    def validate_apellido(self, valor):
        valor = valor.strip()

        if len(valor) < 2:
            raise serializers.ValidationError(
                'El apellido debe tener al menos 2 letras.'
            )

        if not valor.isalpha():
            raise serializers.ValidationError(
                'El apellido solo puede contener letras.'
            )

        return valor.title()

    def validate_fecha_nacimiento(self, fecha_nacimiento):
        hoy = date.today()

        if fecha_nacimiento > hoy:
            raise serializers.ValidationError(
                'La fecha de nacimiento no puede estar en el futuro.'
            )

        edad = hoy.year - fecha_nacimiento.year

        if (hoy.month, hoy.day) < (
            fecha_nacimiento.month,
            fecha_nacimiento.day
        ):
            edad = edad - 1

        if edad < 18 or edad > 40:
            raise serializers.ValidationError(
                'El jugador debe tener entre 18 y 40 años.'
            )

        return fecha_nacimiento

    def validate_numero_camiseta(self, numero):
        if numero < 1 or numero > 99:
            raise serializers.ValidationError(
                'El número de camiseta debe estar entre 1 y 99.'
            )

        jugadores = Jugador.objects.filter(
            numero_camiseta=numero
        )

        if self.instance:
            jugadores = jugadores.exclude(
                pk=self.instance.pk
            )

        if jugadores.exists():
            raise serializers.ValidationError(
                'El número de camiseta ya está asignado.'
            )

        return numero

    def validate_fecha_ingreso(self, fecha_ingreso):
        if fecha_ingreso > date.today():
            raise serializers.ValidationError(
                'La fecha de ingreso no puede ser futura.'
            )

        return fecha_ingreso

    def validate(self, datos):
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')

        if nombre and apellido:
            jugadores = Jugador.objects.filter(
                nombre__iexact=nombre,
                apellido__iexact=apellido
            )

            if self.instance:
                jugadores = jugadores.exclude(
                    pk=self.instance.pk
                )

            if jugadores.exists():
                raise serializers.ValidationError(
                    'Ya existe un jugador con ese nombre y apellido.'
                )

        return datos