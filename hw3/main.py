from PIL import Image
from myTool import openppm, writeppm
from myAES import EncryptAES, DecryptAES
import sys
import os

# Example input
# main.py Tux.jpg ECB linuxpenguinistux


def main():
    if len(sys.argv) != 4:
        print("Error: Wrong argv. Format: main.py {picture name} {mode} {key (str)}")
        exit()

    img_name = sys.argv[1]
    mode = sys.argv[2].upper()
    key = sys.argv[3].upper()

    im = Image.open(img_name)
    filename = os.path.splitext(im.filename)[0]

    if im.mode == "P":
        im = im.convert('RGB')

    ppm_name = filename + '.ppm'
    im.save(ppm_name, 'ppm')

    magic_number, size, maximum_value, blocks = openppm(ppm_name)

    arr_aes = EncryptAES(blocks, key, mode)

    encrypt_img = filename + '_encrypt.jpg'
    encrypt_ppm = filename + '_encrypt.ppm'

    writeppm(encrypt_ppm, magic_number, size, maximum_value, arr_aes)

    im = Image.open(encrypt_ppm)
    im.save(encrypt_img, 'jpeg')

    # Decrypt

    magic_number, size, maximum_value, blocks = openppm(encrypt_ppm)

    arr_aes = DecryptAES(blocks, key, mode)

    decrypt_img = filename + '_decrypt.jpg'
    decrypt_ppm = filename + '_decrypt.ppm'

    writeppm(decrypt_ppm, magic_number, size, maximum_value, arr_aes)

    im = Image.open(decrypt_ppm)
    im.save(decrypt_img, 'jpeg')

    exit()


if __name__ == "__main__":
    main()
