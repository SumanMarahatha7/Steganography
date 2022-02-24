# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from PIL import Image


# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def gen_data(data):
    # list of binary codes
    # of given data
    new_data = []

    for i in data:
        new_data.append(format(ord(i), '08b'))
    return new_data


# Pixels are modified according to the
# 8-bit binary data and finally returned
def mod_pix(pix, data):
    datalist = gen_data(data)
    len_data = len(datalist)
    im_data = iter(pix)

    for i in range(len_data):

        # Extracting 3 pixels at a time
        pix = [value for value in im_data.__next__()[:3] +
               im_data.__next__()[:3] +
               im_data.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                if pix[j] % 2 != 0:
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        # Eigh^th pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if i == len_data - 1:
            if pix[-1] % 2 == 0:
                pix[-1] -= 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(new_img, data):
    w = new_img.size[0]
    (x, y) = (0, 0)

    for pixel in mod_pix(new_img.getdata(), data):

        # Putting modified pixels in the new image
        new_img.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1


# Encode data into image
def encode(img, msg):
    image = Image.open(img)

    if len(msg) == 0:
        raise ValueError('Data is empty')

    new_img = image.copy()
    encode_enc(new_img, msg)

    new_img_name = img
    new_img.save(new_img_name)


# Decode the data in the image
def decode(img_path):
    image = Image.open(img_path, 'r')
    data = ''
    img_data = iter(image.getdata())
    while True:
        pixels = [value for value in img_data.__next__()[:3] +
                  img_data.__next__()[:3] +
                  img_data.__next__()[:3]]
        # string of binary data
        bin_str = ''

        for i in pixels[:8]:
            if i % 2 == 0:
                bin_str += '0'
            else:
                bin_str += '1'

        data += chr(int(bin_str, 2))
        if pixels[-1] % 2 != 0:
            return data
