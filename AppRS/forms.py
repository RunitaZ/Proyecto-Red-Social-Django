from django import forms
from .models import Post, PerfilUsuario, Comentario
from django.forms import ModelForm
from django.contrib.auth.models import User

class UserProfileForm(ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['nombre', 'biografia', 'fecha_nacimiento', 'foto_perfil', 'edad']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "descripcion", "importante", 'imagen']
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control"}),
            "importante": forms.CheckboxInput(attrs={"class": "form-check-input"}),
             "imagen": forms.ClearableFileInput(attrs={"class": "form-control-file"})
        }


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['foto_perfil', 'biografia']
        widgets = {
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
         }
         
class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']



class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'placeholder': 'Escribe tu comentario aquí...',
                'rows': 1,  # Define el número de filas (altura)
                'cols': 45,  # Define el número de columnas (ancho)
                'style': 'resize: none;'
            }),
        }
