from Image.encryption import encrypt, decrypt
from Image.stenography import encode, decode


def steno_encrypt(key, msg, path):
    encode(path, msg)
    encrypt(key, path)


def steno_decrypt(key, path):
    response = decrypt(key, path)
    if "image" in response.keys():
        response = dict(response, **{"msg": decode(response["image"])})
    return response
