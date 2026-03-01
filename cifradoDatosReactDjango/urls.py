from django.contrib import admin
from django.urls import path
from users.views import RegistroUsuario, ListaUsuarios

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/registro/', RegistroUsuario.as_view()),#endpoint post
    path('api/usuarios/', ListaUsuarios.as_view()),#endpoint get
]