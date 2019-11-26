from PIL import Image
from Crypto.Cipher import AES
from myTool import *
import sys


def ECB(block_array, key):
    encrypt_array = []
    cipher = AES.new(key, AES.MODE_ECB)
    for block in block_array:
        encrypt_array.append(cipher.encrypt(block))
    return encrypt_array


def CBC(block_array, key):
    return 0


def CTR(block_array, key):
    return 0


def EncryptAES(block_array, key, mode):
    # 128/192/256
    key = b'1234567890123456'

    if mode == 'ECB':
        return ECB(block_array, key)
    elif mode == 'CBC':
        return CBC(block_array, key)
    elif mode == 'CTR':
        return CTR(block_array, key)


def main():
    # if len(sys.argv) != 4:
    #     print("Error: Wrong argv.")
    #     exit()

    ppm_name = 'myppm.ppm'
    img_name = 'Tux.jpg'

    result_ppm = 'result.ppm'
    result_img = 'result.jpg'

    im = Image.open(img_name)
    im.save(ppm_name, 'ppm')

    magic_number, size, maximum_value, blocks = openppm(ppm_name)

    arr_aes = EncryptAES(blocks, "put key", 'ECB')
    # arr_aes = blocks

    writeppm(result_ppm, magic_number, size, maximum_value, arr_aes)

    im = Image.open(result_ppm)
    im.save(result_img, 'jpeg')

    exit()


if __name__ == "__main__":
    main()
