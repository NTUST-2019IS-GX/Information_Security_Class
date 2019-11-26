from PIL import Image
from Crypto.Cipher import AES
from myTool import *
import sys


def ECB(block_array, key):
    decrypt_array = []
    cipher = AES.new(key, AES.MODE_ECB)
    for block in block_array:
        decrypt_array.append(cipher.decrypt(block))
    return decrypt_array


def CBC(block_array, key):
    return 0


def CTR(block_array, key):
    return 0


def DecryptAES(block_array, key, mode):
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

    ppm_name = 'result.ppm'
    img_name = 'result.jpg'

    result_ppm = 'recover.ppm'
    result_img = 'recover.jpg'

    # im = Image.open(img_name)
    # im.save(ppm_name)

    magic_number, size, maximum_value, blocks = openppm(ppm_name)

    arr_aes = DecryptAES(blocks, "put key", 'ECB')
    # arr_aes = blocks

    writeppm(result_ppm, magic_number, size, maximum_value, arr_aes)

    im = Image.open(result_ppm)
    im.save(result_img, 'jpeg')
    exit()


if __name__ == "__main__":
    main()
