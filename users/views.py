from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer
import base64
import json
from security_utils import get_public_key, decrypt_rsa

class RegistroUsuario(APIView):

    def post(self, request):
        """
        Aquí esperamos recibir los datos cifrados
        en base64 desde el frontend.
        """

        try:
            #  Recibimos "data"
            encrypted_base64 = request.data.get("data")

            # Convertimos base64 → bytes
            encrypted_bytes = base64.b64decode(encrypted_base64)

            # Desciframos con clave privada RSA
            decrypted_bytes = decrypt_rsa(encrypted_bytes)

            # Convertimos JSON string → dict
            data = json.loads(decrypted_bytes.decode())

        except Exception as e:
            return Response({"error": "Error al descifrar datos"}, status=400)

        # Ahora usamos el serializer normal
        serializer = UsuarioSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario creado correctamente"}, status=201)

        return Response(serializer.errors, status=400)


class ListaUsuarios(APIView):

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    
class ObtenerClavePublica(APIView):
    """
    Devuelve la clave pública RSA.
    El frontend la usará para cifrar los datos.
    """

    def get(self, request):
        return Response({"public_key": get_public_key()})