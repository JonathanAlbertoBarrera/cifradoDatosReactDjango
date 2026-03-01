from django.contrib import admin
from django.urls import path
from users.views import RegistroUsuario, ListaUsuarios,ObtenerClavePublica

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/registro/', RegistroUsuario.as_view()),#endpoint post
    path('api/usuarios/', ListaUsuarios.as_view()),#endpoint get
    path('api/public-key/', ObtenerClavePublica.as_view()),#endpoint get
]