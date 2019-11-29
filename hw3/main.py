from PIL import Image
from myTool import openppm, writeppm
from myAES import EncryptAES, DecryptAES
import sys
import os

# Example input
# main.py test_pic_1/Tux.png ECB linuxpenguinistux


def main():
    # Argv error handling
    if len(sys.argv) != 4:
        print("Error: Wrong argv. Format: main.py {picture name} {mode} {key (str)}")
        exit()

    # Save argv
    img_name = sys.argv[1]
    mode = sys.argv[2].upper()
    key = sys.argv[3].upper()

    # Open image File and get filename
    im = Image.open(img_name)
    filename = os.path.splitext(im.filename)[0]

    # Convert to RGB if mode == P
    if im.mode == "P":
        im = im.convert('RGB')

    # Save image to ppm
    ppm_name = filename + '.ppm'
    im.save(ppm_name, 'ppm')

    # Save ppm file attribute and do encrypt
    magic_number, size, maximum_value, blocks = openppm(ppm_name)
    arr_aes = EncryptAES(blocks, key, mode)

    # Write encrypt blocks into encrypt_ppm file
    encrypt_img = filename + '_encrypt.jpg'
    encrypt_ppm = filename + '_encrypt.ppm'
    writeppm(encrypt_ppm, magic_number, size, maximum_value, arr_aes)

    # Convert encrypt_ppm file to JPEG
    im = Image.open(encrypt_ppm)
    im.save(encrypt_img, 'jpeg')

    # Open encrypt_ppm file and do decrypt
    magic_number, size, maximum_value, blocks = openppm(encrypt_ppm)
    arr_aes = DecryptAES(blocks, key, mode)

    # Write decrypt blocks into decrypt_ppm file
    decrypt_img = filename + '_decrypt.jpg'
    decrypt_ppm = filename + '_decrypt.ppm'
    writeppm(decrypt_ppm, magic_number, size, maximum_value, arr_aes)

    # Convert decrypt_ppm file to JPEG
    im = Image.open(decrypt_ppm)
    im.save(decrypt_img, 'jpeg')

    exit()


if __name__ == "__main__":
    main()
