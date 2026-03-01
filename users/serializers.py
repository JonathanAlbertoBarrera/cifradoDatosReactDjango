from rest_framework import serializers
from .models import Usuario
from security_utils import encrypt_email, decrypt_email

class UsuarioSerializer(serializers.ModelSerializer):

    # Este campo será el que reciba el email normal desde el frontend
    email = serializers.CharField(write_only=True)

    # Este campo será el que se muestre cuando listemos usuarios
    email_mostrado = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'email', 'email_mostrado']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Aquí interceptamos los datos antes de guardarlos.
        Ciframos el email y dejamos que el modelo
        se encargue de hashear el password.
        """

        email_plano = validated_data.pop('email')

        usuario = Usuario(
            username=validated_data['username'],
            password=validated_data['password'],
            email_encrypted=encrypt_email(email_plano)
        )

        usuario.save()
        return usuario

    def get_email_mostrado(self, obj):
        """
        Este método descifra el email
        cuando enviamos datos al frontend.
        """
        return decrypt_email(obj.email_encrypted)