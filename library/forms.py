"""
Formularios para la aplicación
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import User, Game, Review, UserLibrary, Developer


class CustomUserCreationForm(UserCreationForm):
    """Formulario personalizado de registro"""
    email = forms.EmailField(required=True, label='Correo electrónico')
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Biografía')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            'bio',
            Submit('submit', 'Registrarse', css_class='btn btn-primary')
        )


class GameForm(forms.ModelForm):
    """Formulario para crear/editar juegos"""
    class Meta:
        model = Game
        fields = ['title', 'description', 'release_date', 'price', 'cover_image',
                 'steam_url', 'developer', 'categories']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            Row(
                Column('release_date', css_class='form-group col-md-6 mb-0'),
                Column('price', css_class='form-group col-md-6 mb-0'),
            ),
            'developer',
            'categories',
            'cover_image',
            'steam_url',
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )


class ReviewForm(forms.ModelForm):
    """Formulario para crear/editar reseñas"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5}),
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rating',
            'comment',
            Submit('submit', 'Publicar Reseña', css_class='btn btn-primary')
        )


class UserLibraryForm(forms.ModelForm):
    """Formulario para agregar juegos a la biblioteca"""
    class Meta:
        model = UserLibrary
        fields = ['hours_played', 'is_favorite', 'last_played']
        widgets = {
            'last_played': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'hours_played',
            'is_favorite',
            'last_played',
            Submit('submit', 'Actualizar', css_class='btn btn-primary')
        )


class DeveloperForm(forms.ModelForm):
    """Formulario para crear/editar desarrolladores"""
    class Meta:
        model = Developer
        fields = ['name', 'country', 'website', 'description', 'logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            Row(
                Column('country', css_class='form-group col-md-6 mb-0'),
                Column('website', css_class='form-group col-md-6 mb-0'),
            ),
            'description',
            'logo',
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )


class SearchForm(forms.Form):
    """Formulario de búsqueda"""
    query = forms.CharField(
        max_length=200,
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar juegos, desarrolladores...'})
    )
    category = forms.IntegerField(required=False, widget=forms.HiddenInput())
    min_rating = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=5,
        label='Calificación mínima',
        widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'max': '5'})
    )

