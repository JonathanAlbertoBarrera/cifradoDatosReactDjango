import os
import base64

clave = base64.urlsafe_b64encode(os.urandom(32)).decode()
print("Tu clave AES es:")
print(clave)