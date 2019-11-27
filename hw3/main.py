from PIL import Image
from myTool import *
from EncryptAES import EncryptAES
from DecryptAES import DecryptAES
import sys

# main.py Tux.jpg ECB


def main():
    if len(sys.argv) != 3:
        print("Error: Wrong argv.")
        exit()

    img_name = sys.argv[1]
    ppm_name = img_name + '.ppm'

    encrypt_img = 'encrypt' + img_name
    encrypt_ppm = encrypt_img + '.ppm'

    im = Image.open(img_name)
    im.save(ppm_name, 'ppm')

    magic_number, size, maximum_value, blocks = openppm(ppm_name)

    arr_aes = EncryptAES(blocks, "put key", sys.argv[2])

    writeppm(encrypt_ppm, magic_number, size, maximum_value, arr_aes)

    im = Image.open(encrypt_ppm)
    im.save(encrypt_img, 'jpeg')

    # Decrypt

    decrypt_img = 'decrypt' + img_name
    decrypt_ppm = decrypt_img + '.ppm'

    magic_number, size, maximum_value, blocks = openppm(encrypt_ppm)

    arr_aes = DecryptAES(blocks, "put key", sys.argv[2])

    writeppm(decrypt_ppm, magic_number, size, maximum_value, arr_aes)

    im = Image.open(decrypt_ppm)
    im.save(decrypt_img, 'jpeg')

    exit()


if __name__ == "__main__":
    main()
