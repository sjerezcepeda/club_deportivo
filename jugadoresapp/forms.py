from datetime import date

from django import forms
from django.utils import timezone

from .models import Jugador


class JugadorForm(forms.ModelForm):

    class Meta:
        model = Jugador
        fields = [
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'posicion',
            'numero_camiseta',
            'fecha_ingreso',
            'activo'
        ]

        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'fecha_ingreso': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'numero_camiseta': forms.NumberInput(
                attrs={'min': 1, 'max': 99}
            )
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()

        if len(nombre) < 2:
            raise forms.ValidationError(
                'El nombre debe tener al menos 2 letras.'
            )

        if not nombre.isalpha():
            raise forms.ValidationError(
                'El nombre solo puede contener letras.'
            )

        return nombre.title()

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido'].strip()

        if len(apellido) < 2:
            raise forms.ValidationError(
                'El apellido debe tener al menos 2 letras.'
            )

        if not apellido.isalpha():
            raise forms.ValidationError(
                'El apellido solo puede contener letras.'
            )

        return apellido.title()

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        hoy = date.today()

        if fecha_nacimiento > hoy:
            raise forms.ValidationError(
                'La fecha de nacimiento no puede estar en el futuro.'
            )

        edad = hoy.year - fecha_nacimiento.year

        if (hoy.month, hoy.day) < (
            fecha_nacimiento.month,
            fecha_nacimiento.day
        ):
            edad = edad - 1

        if edad < 18 or edad > 40:
            raise forms.ValidationError(
                'El jugador debe tener entre 18 y 40 años.'
            )

        return fecha_nacimiento

    def clean_numero_camiseta(self):
        numero = self.cleaned_data['numero_camiseta']

        jugador_existente = Jugador.objects.filter(
            numero_camiseta=numero
        )

        if self.instance and self.instance.pk:
            jugador_existente = jugador_existente.exclude(
                pk=self.instance.pk
            )

        if jugador_existente.exists():
            raise forms.ValidationError(
                'El número de camiseta ' + str(numero) +
                ' ya está asignado a otro jugador.'
            )

        return numero

    def clean_fecha_ingreso(self):
        fecha_ingreso = self.cleaned_data['fecha_ingreso']

        if fecha_ingreso > timezone.now().date():
            raise forms.ValidationError(
                'La fecha de ingreso no puede ser en el futuro.'
            )

        return fecha_ingreso

    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')

        if nombre and apellido:
            jugador_existente = Jugador.objects.filter(
                nombre__iexact=nombre,
                apellido__iexact=apellido
            )

            if self.instance and self.instance.pk:
                jugador_existente = jugador_existente.exclude(
                    pk=self.instance.pk
                )

            if jugador_existente.exists():
                raise forms.ValidationError(
                    'Ya existe un jugador registrado con este nombre y apellido.'
                )

        return cleaned_data