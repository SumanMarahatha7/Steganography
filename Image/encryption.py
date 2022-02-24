import os
import math
import string
import random

from PIL import Image
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def get_key(key):
    main_key = SHA256.new(key.encode('utf-8')).digest()
    key1 = key[:math.floor(len(key) / 2)]
    key2 = key[math.floor(len(key) / 2):]
    key1 = SHA256.new(key1.encode('utf-8')).digest()
    key2 = SHA256.new(key2.encode('utf-8')).digest()
    return main_key, key1, key2


def encrypt(key, filename):
    with open(filename, 'rb') as file:
        infile = file.read()
        main_key, key1, key2 = get_key(key)

        iv = os.urandom(16)
        encrypting = AES.new(main_key, AES.MODE_CFB, iv)
        outfile = key1 + encrypting.encrypt(infile)

        encrypting_new = AES.new(key2, AES.MODE_CFB, iv)
        final = iv + encrypting_new.encrypt(outfile)

        with open(filename, 'wb') as encrypted:
            encrypted.write(final)


def decrypt(key, filename):
    ext = filename.split(".")[1]
    with open(filename, 'rb') as file:
        final = file.read()
        main_key, key1, key2 = get_key(key)

        iv = final[:16]
        decrypter_new = AES.new(key2, AES.MODE_CFB, iv)
        outfile = decrypter_new.decrypt(final[16:])

        if outfile[:32] == key1:
            decrypter = AES.new(main_key, AES.MODE_CFB, iv)
            infile = decrypter.decrypt(outfile[32:])
            r_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(5))
            with open(f"media/DecryptedImage/processing-{r_str}.{ext}", 'wb') as writing:
                writing.write(infile)
            image = Image.open(f"media/DecryptedImage/processing-{r_str}.{ext}")
            return {"image": image.filename}
        else:
            return {'error': 'Key doest matches'}
