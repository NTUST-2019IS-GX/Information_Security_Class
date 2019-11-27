from PIL import Image
from myTool import openppm, writeppm
from myAES import EncryptAES, DecryptAES
import sys

# main.py Tux.jpg ECB


def main():
    if len(sys.argv) != 3:
        print("Error: Wrong argv.")
        exit()

    img_name = sys.argv[1]
    ppm_name = img_name + '.ppm'

    encrypt_img = 'encrypt_' + img_name
    encrypt_ppm = encrypt_img + '.ppm'

    im = Image.open(img_name)
    im.save(ppm_name, 'ppm')

    magic_number, size, maximum_value, blocks = openppm(ppm_name)

    # TODO: argv put key
    arr_aes = EncryptAES(blocks, "put key", sys.argv[2])

    writeppm(encrypt_ppm, magic_number, size, maximum_value, arr_aes)

    im = Image.open(encrypt_ppm)
    im.save(encrypt_img, 'jpeg')

    # Decrypt

    decrypt_img = 'decrypt_' + img_name
    decrypt_ppm = decrypt_img + '.ppm'

    magic_number, size, maximum_value, blocks = openppm(encrypt_ppm)

    # TODO: argv put key
    arr_aes = DecryptAES(blocks, "put key", sys.argv[2])

    writeppm(decrypt_ppm, magic_number, size, maximum_value, arr_aes)

    im = Image.open(decrypt_ppm)
    im.save(decrypt_img, 'jpeg')

    exit()


if __name__ == "__main__":
    main()
