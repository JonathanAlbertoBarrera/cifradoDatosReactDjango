import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# =====================================================
# AES (CIFRADO SIMÉTRICO EN REPOSO)
# =====================================================

# Cargamos la clave AES desde variable de entorno
AES_KEY = base64.urlsafe_b64decode(os.environ.get("AES_SECRET_KEY"))

def encrypt_email(email: str) -> str:
    """
    Cifra el email usando AES-GCM.
    Se utiliza para guardar el email cifrado en la base de datos.
    """
    aesgcm = AESGCM(AES_KEY)
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce, email.encode(), None)
    return base64.b64encode(nonce + encrypted).decode()


def decrypt_email(ciphertext: str) -> str:
    """
    Descifra el email almacenado en base de datos.
    """
    raw = base64.b64decode(ciphertext)
    nonce = raw[:12]
    encrypted = raw[12:]
    aesgcm = AESGCM(AES_KEY)
    return aesgcm.decrypt(nonce, encrypted, None).decode()


# =====================================================
#  RSA (CIFRADO ASIMÉTRICO FRONTEND → BACKEND)
# =====================================================

# Cargar clave privada desde archivo
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Cargar clave pública desde archivo
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(
        f.read()
    )

def get_public_key():
    """
    Devuelve la clave pública en formato PEM
    para que el frontend pueda cifrar datos.
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()


def decrypt_rsa(encrypted_data: bytes) -> bytes:
    """
    Descifra los datos enviados desde el frontend.
    """
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )