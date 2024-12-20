# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from .layers.utilities import translator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

def index_page(request):
    return render(request, 'index.html')
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/user-enrollment.html', {
                'error_message': 'El nombre de usuario ya está en uso. Por favor, elija otro.'
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        send_mail(
            'Bienvenido a nuestra aplicación',
            f'Sus credenciales de acceso:\nUsuario: {username}\nContraseña: {password}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return home(request)
    return render(request, 'registration/user-enrollment.html')
# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request, page=1):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)
    image_paginator = Paginator(images, per_page=6)
    image_page = image_paginator.get_page(page)
    return render(request, 'home.html', { 'images': image_page, 'favourite_list': favourite_list })


def search(request, page=1):
    search_msg = request.POST.get('query', '')
    images = [];
    favourite_list = []
    if (search_msg != ''):
        images = services.getAllImages(search_msg);
        image_paginator = Paginator(images, per_page=6)
        image_page = image_paginator.get_page(page)
        favourite_list = services.getAllFavourites(request)
        
        return render(request, 'home.html', { 'images': image_page, 'favourite_list': favourite_list })
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    return home(request)

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return getAllFavouritesByUser(request)

@login_required
def exit(request):
    pass