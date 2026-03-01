import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

AES_KEY = base64.urlsafe_b64decode(os.environ.get("AES_SECRET_KEY"))

def encrypt_email(email: str) -> str:
    aesgcm = AESGCM(AES_KEY)
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce, email.encode(), None)
    return base64.b64encode(nonce + encrypted).decode()

def decrypt_email(ciphertext: str) -> str:
    raw = base64.b64decode(ciphertext)
    nonce = raw[:12]
    encrypted = raw[12:]
    aesgcm = AESGCM(AES_KEY)
    return aesgcm.decrypt(nonce, encrypted, None).decode()