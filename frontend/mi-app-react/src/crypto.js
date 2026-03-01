// Esta función cifra datos usando la clave pública RSA
export async function cifrarDatos(datos, publicKeyPem) {

  // Convertimos la clave PEM en formato usable
  const binaryDer = window.atob(
    publicKeyPem
      .replace("-----BEGIN PUBLIC KEY-----", "")
      .replace("-----END PUBLIC KEY-----", "")
      .replace(/\n/g, "")
  );

  const binaryArray = Uint8Array.from(binaryDer, c => c.charCodeAt(0));

  const publicKey = await window.crypto.subtle.importKey(
    "spki",
    binaryArray,
    {
      name: "RSA-OAEP",
      hash: "SHA-256"
    },
    false,
    ["encrypt"]
  );

  const encoded = new TextEncoder().encode(JSON.stringify(datos));

  const encrypted = await window.crypto.subtle.encrypt(
    { name: "RSA-OAEP" },
    publicKey,
    encoded
  );

  return btoa(String.fromCharCode(...new Uint8Array(encrypted)));
}