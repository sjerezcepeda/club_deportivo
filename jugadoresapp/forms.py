import re
from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
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
            'nombre': forms.TextInput(
                attrs={'maxlength': 20}
            ),
            'apellido': forms.TextInput(
                attrs={'maxlength': 20}
            ),
            'posicion': forms.Select(
            attrs={
            'class': 'form-select'
            }
            ),
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

    def validar_texto(self, valor, nombre_campo):
        valor = valor.strip()

        if len(valor) < 2:
            raise forms.ValidationError(
                nombre_campo + ' debe tener al menos 2 letras.'
            )

        if len(valor) > 20:
            raise forms.ValidationError(
                nombre_campo + ' no puede superar los 20 caracteres.'
            )

        if not valor.isalpha():
            raise forms.ValidationError(
                nombre_campo + ' solo puede contener letras.'
            )

        if re.search(r'(.)\1\1', valor, re.IGNORECASE):
            raise forms.ValidationError(
                nombre_campo +
                ' no puede tener una letra repetida más de dos veces seguidas.'
            )

        return valor.title()

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']

        return self.validar_texto(
            nombre,
            'El nombre'
        )

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']

        return self.validar_texto(
            apellido,
            'El apellido'
        )

    def clean_posicion(self):
        posicion = self.cleaned_data['posicion']

        return self.validar_texto(
            posicion,
            'La posición'
        )

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

        if numero < 1 or numero > 99:
            raise forms.ValidationError(
                'El número de camiseta debe estar entre 1 y 99.'
            )

        jugadores = Jugador.objects.filter(
            numero_camiseta=numero
        )

        if self.instance and self.instance.pk:
            jugadores = jugadores.exclude(
                pk=self.instance.pk
            )

        if jugadores.exists():
            raise forms.ValidationError(
                'El número de camiseta ya está asignado.'
            )

        return numero

    def clean_fecha_ingreso(self):
        fecha_ingreso = self.cleaned_data['fecha_ingreso']

        if fecha_ingreso > timezone.now().date():
            raise forms.ValidationError(
                'La fecha de ingreso no puede ser futura.'
            )

        return fecha_ingreso

    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')

        if nombre and apellido:
            jugadores = Jugador.objects.filter(
                nombre__iexact=nombre,
                apellido__iexact=apellido
            )

            if self.instance and self.instance.pk:
                jugadores = jugadores.exclude(
                    pk=self.instance.pk
                )

            if jugadores.exists():
                raise forms.ValidationError(
                    'Ya existe un jugador registrado con este nombre y apellido.'
                )

        return cleaned_data
class RegistroUsuarioForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ejemplo: sergio_jerez',
            'maxlength': 20
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresa una contraseña',
            'maxlength': 20
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repite la contraseña',
            'maxlength': 20
        })

    def clean_username(self):
        username = self.cleaned_data['username'].strip()

        if len(username) > 20:
            raise forms.ValidationError(
                'El nombre de usuario no puede superar los 20 caracteres.'
            )

        if re.search(r'(.)\1\1', username, re.IGNORECASE):
            raise forms.ValidationError(
                'El nombre de usuario no puede tener un carácter repetido más de dos veces seguidas.'
            )

        return username

    def clean_password1(self):
        password = self.cleaned_data['password1']

        if len(password) > 20:
            raise forms.ValidationError(
                'La contraseña no puede superar los 20 caracteres.'
            )

        return password