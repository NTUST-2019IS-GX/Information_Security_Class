from Crypto.Cipher import AES
from myTool import *


def ECB(block_array, key):
    decrypt_array = []
    cipher = AES.new(key, AES.MODE_ECB)
    for block in block_array:
        decrypt_array.append(cipher.decrypt(block))
    return decrypt_array


def CBC(block_array, key):
    decrypt_array = []
    iv = b'1234567890123456'
    cipher = AES.new(key, AES.MODE_ECB)
    for block in block_array:
        decrypt_array.append(byte_xor(iv, cipher.decrypt(block)))
        iv = block
    return decrypt_array


def CTR(block_array, key):
    decrypt_array = []
    counter = b'\xe5\xad\xa6\xe4\xb9\xa0\xe5\xbe\x00\x00\x00\x00\x00\x00\x00\x01'
    cipher = AES.new(key, AES.MODE_ECB)
    for block in block_array:
        decrypt_array.append(byte_xor(cipher.decrypt(counter), block))
        counter = byte_add(counter, 1)
    return decrypt_array


def DecryptAES(block_array, key, mode):
    # 128/192/256
    key = b'1234567890123456'

    if mode == 'ECB':
        return ECB(block_array, key)
    elif mode == 'CBC':
        return CBC(block_array, key)
    elif mode == 'CTR':
        return CTR(block_array, key)
