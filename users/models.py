from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email_encrypted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Este método se ejecuta automáticamente cada vez que se guarda
        un objeto Usuario en la base de datos.

        Lo que hacemos aquí es verificar si la contraseña ya está
        hasheada. Si no lo está, la convertimos en un hash seguro
        usando el sistema de Django (PBKDF2).
        """

        # Si la contraseña NO empieza con 'pbkdf2_'
        # significa que aún no ha sido hasheada
        if not self.password.startswith('pbkdf2_'):

            # Convertimos la contraseña en texto plano
            # a un hash seguro irreversible
            self.password = make_password(self.password)

        # Llamamos al método save original de Django
        # para que realmente guarde el objeto
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Este método define cómo se muestra el objeto
        cuando lo imprimes o lo ves en el admin.

        En vez de mostrar:
        Usuario object (1)

        Mostrará el username.
        """
        return self.username