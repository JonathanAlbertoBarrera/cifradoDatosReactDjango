import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# =========================
#  AES (CIFRADO EN REPOSO) SIMETRICO
# =========================

AES_KEY = base64.urlsafe_b64decode(os.environ.get("AES_SECRET_KEY"))

def encrypt_email(email: str) -> str:
    """
    Cifra el email usando AES.
    Esto es para guardarlo en la base de datos.
    """
    aesgcm = AESGCM(AES_KEY)
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce, email.encode(), None)
    return base64.b64encode(nonce + encrypted).decode()

def decrypt_email(ciphertext: str) -> str:
    """
    Descifra el email cuando lo queremos mostrar.
    """
    raw = base64.b64decode(ciphertext)
    nonce = raw[:12]
    encrypted = raw[12:]
    aesgcm = AESGCM(AES_KEY)
    return aesgcm.decrypt(nonce, encrypted, None).decode()


# =========================
#  RSA (CIFRADO ASIMETRICO FRONTEND → BACKEND)
# =========================

# Generamos clave privada (solo vive en el backend)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Generamos clave pública (se enviará al frontend)
public_key = private_key.public_key()

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
    Descifra los datos que vienen del frontend.
    """
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )