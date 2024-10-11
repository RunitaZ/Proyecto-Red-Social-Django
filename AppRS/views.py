"""Modulo para manejar las respuestas de las urls"""

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from .models import PerfilUsuario, Post, Comentario
from .forms import PostForm, EditarPerfilForm, EditarUsuarioForm, ComentarioForm
import traceback

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse
#Estas importaciones proporcionan las funciones y clases necesarias para manejar
# la autenticación, renderización de plantillas y redirecciones en Django.
from django.contrib.auth.models import User # Modelo de usuario predeterminado de Django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("home")  # Redirigir si el usuario ya está logueado
    return render(request, 'index.html')

def crear_cuenta(request):
    if request.user.is_authenticated:
        return redirect("home")  # Redirigir si el usuario ya está logueado

    form = UserCreationForm # Instancia del formulario
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save() # Guardar el usuario en la base de datos
                login(request, user) # Iniciar sesión automáticamente
                return redirect("home")
            except:
                return render(request, "crearCuenta.html", {"error": "El usuario ya existe"})
        else:
            return render(request, "crearCuenta.html", {"error": "Las contraseñas no coinciden"})
    return render(request, "crearCuenta.html",{"form": form})


#
def inicio_sesion(request):
    if request.user.is_authenticated:
        return redirect("home")  # Redirigir si el usuario ya está logueado
    
    if request.method == "GET":
        return render(request, "inicioSesion.html", {"form": AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "inicioSesion.html",
                {
                    "form": AuthenticationForm,
                    "error": "El nombre o la contraseña del usuario, es incorrecta",
                },
            )
        else:
            login(request, user)
    return redirect("home")

def cerrar_sesion(request):
    logout(request)
    return redirect("index")

def posts(request):
    if request.user.is_authenticated:
        return render(request, "publicacion.html", {"data": "aquí se verán las publicaciones creadas"})
    return redirect("index")

def buscar(request):
    query = request.GET.get('q')
    if query:
        usuarios = User.objects.filter(username__icontains=query)
        return render(request, 'buscar.html', {'usuarios': usuarios})
    return render(request, 'buscar.html')

def home(request):
    
    #MUESTRA PUBLICACIONES Y COMENTARIOS
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created')

        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)

            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.usuario = request.user
                comentario.post = post
                comentario.save()
                print(f"Comentario guardado: {comentario.contenido}")
                return redirect('home')  # Redirige a la misma vista para ver el nuevo comentario

        # Si no hay un POST, inicializa el formulario vacío
        comentario_form = ComentarioForm()

        return render(request, "home.html", {
            "posts": posts,
            "comentario_form": comentario_form,  # Pasar el formulario a la plantilla
        })
    
    return redirect("index")
    
    
    #OTRO QUE SOLO MOSTRABA LAS PUBLICACIONES
    # if request.user.is_authenticated:
    #     # Filtrar publicaciones del usuario autenticado
    #     #posts = Post.objects.filter(user=request.user).order_by('-created')
    #     posts =Post.objects.all().order_by('-created')
    #     return render(request, "home.html", {"posts": posts})
    # return redirect("index")


def perfil(request, username=None):
    if request.user.is_authenticated:
        if username:
            # Si se proporciona un nombre de usuario, obtenemos el perfil del usuario indicado
            user = get_object_or_404(User, username=username)
            
        else:
            # Si no se proporciona un nombre de usuario, mostramos el perfil del usuario autenticado
            user = request.user
            
        # Obtener el perfil del usuario
        perfil_usuario = get_object_or_404(PerfilUsuario, nombre=user)
        
        # Obtener las publicaciones del usuario
        posts = Post.objects.filter(user=user).order_by('-created')
        
        guardados = perfil_usuario.posts_guardados.all()  # Obtener publicaciones guardadas
        # print(f"Posts: {posts}, Guardados: {guardados}")
        # Pasar los datos del perfil y las publicaciones al contexto
        context = {
            'perfil': perfil_usuario,
            'posts': posts,
            'num_publicaciones': posts.count(),
            'num_seguidores': perfil_usuario.num_seguidores(),
            'num_seguidos': perfil_usuario.num_seguidos(),
            'guardados': guardados,  # Agregar los posts guardados al contexto
        }
        return render(request, "perfil.html", context)
    return redirect("index")  # Si no está autenticado, redirige a la página principal

def editar_perfil(request, username=None):
    if request.user.is_authenticated:
        if username:
            # Si se proporciona un nombre de usuario, obtenemos el perfil del usuario indicado
            user = get_object_or_404(User, username=username)
        else:
            # Si no se proporciona un nombre de usuario, mostramos el perfil del usuario autenticado
            user = request.user
        
        # Obtener el perfil del usuario autenticado o buscado
        perfil_usuario = get_object_or_404(PerfilUsuario, nombre=user)

        if request.method == "POST":
            user_form = EditarUsuarioForm(request.POST, instance=user)
            perfil_form = EditarPerfilForm(request.POST, request.FILES, instance=perfil_usuario)

            if user_form.is_valid() and perfil_form.is_valid():
                user_form.save()
                perfil_form.save()
                return redirect('perfil')  # Redirigimos al perfil después de guardar
        else:
            user_form = EditarUsuarioForm(instance=user)
            perfil_form = EditarPerfilForm(instance=perfil_usuario)

        # Pasar los formularios al contexto
        context = {
            'user_form': user_form,
            'perfil_form': perfil_form,
        }
        return render(request, "editar_perfil.html", context)

    return redirect("index")  # Si no está autenticado, redirige a la página principal
    

def addPublicacion(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "Publicacion.html", {"form": PostForm})
        else:
            try:
                print(request.POST)
                form = PostForm(
                    request.POST, request.FILES
                )  # Crear el formulario con los datos enviados
                
                if form.is_valid():
                    nuevo_post = form.save(
                        commit=False
                    )  # Obtener los datos de ese form
                    nuevo_post.user = request.user
                    nuevo_post.save()
                    return redirect("home")
            except:
                return render(
                    request,
                    "Publicacion.html",
                  {"form": form, "error": "No se pudo crear la publicación"},  # Aquí devuelve el mismo formulario con los datos ingresados
                )

    redirect("login")

#    return render(request, 'Publicacion.html')

def editarPublicacion(request, post_id):
    post=get_object_or_404(Post, id=post_id, user =request.user)
    if request.method=="POST":
        form = PostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PostForm(instance = post)
        return render(request, "editarPublicacion.html", {"form":form, 'post': post})
    
    
    
def EliminarPubli(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == "POST":
        post.delete()
        return redirect("home")
    
    return render(request, "elimiPubli.html", {"post": post})
    

@login_required
@require_POST
def toggle_guardar_publicacion(request):
    """Agrega o quita una publicación de las publicaciones guardadas del usuario."""
    try:
        data = json.loads(request.body)  # Cargamos los datos del cuerpo de la solicitud JSON
        post_id = data.get('post_id')  # Asegúrate de obtener el post_id correctamente
       # print(f"Post ID: {post_id}")
        post = get_object_or_404(Post, id=post_id)
        perfil = request.user.perfilusuario
        print(perfil)
        if post in perfil.posts_guardados.all():
            perfil.posts_guardados.remove(post)
            saved = False
        else:
            perfil.posts_guardados.add(post)
            saved = True

        return JsonResponse({'saved': saved})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'Algo salió mal.'}, status=400)



def privacidad(request):
    return render(request, 'privacidad.html')

def terminos(request):
    return render(request, 'terminos.html')



def comentarios(request, post_id):
    return redirect("home")
  
  
  # post = get_object_or_404(Post, id=post_id)
    # comentarios = post.comentarios.all()  # Obtener todos los comentarios para la publicación

    # if request.method == "POST" and request.user.is_authenticated:
    #     comentario_form = ComentarioForm(request.POST)
    #     if comentario_form.is_valid():
    #         nuevo_comentario = comentario_form.save(commit=False)
    #         nuevo_comentario.post = post
    #         nuevo_comentario.usuario = request.user
    #         nuevo_comentario.save()
    #         return redirect('home', post_id=post.id)
    # else:
    #     comentario_form = ComentarioForm()

    # context = {
    #     'post': post,
    #     'comentarios': comentarios,
    #     'comentario_form': comentario_form,
    # }
    # return render(request, 'home.html', context)