from Crypto.Cipher import AES
from myTool import byte_xor, byte_add, key_preprocess

CBC_iv = b'1234567890123456'
CTR_iv = b'\xe5\xad\xa6\xe4\xb9\xa0\xe5\xbe\x00\x00\x00\x00\x00\x00\x00\x00'


def EncryptAES(block_array, key, mode):

    # TODO: key process
    key = key_preprocess(key)
    key = b'1234567890123456'

    encrypt_array = []
    cipher = AES.new(key, AES.MODE_ECB)

    if mode == 'ECB':
        for block in block_array:
            encrypt_array.append(cipher.encrypt(block))
        return encrypt_array

    elif mode == 'CBC':
        cipher_block = CBC_iv  # Initial Vector
        for block in block_array:
            cipher_block = cipher.encrypt(byte_xor(cipher_block, block))
            encrypt_array.append(cipher_block)
        return encrypt_array

    elif mode == 'CTR':
        initial_vector = CTR_iv  # Initial Vector
        for block in block_array:
            encrypt_array.append(byte_xor(cipher.encrypt(initial_vector), block))
            initial_vector = byte_add(initial_vector, 1)
        return encrypt_array


def DecryptAES(block_array, key, mode):

    # TODO: key process
    key = key_preprocess(key)
    key = b'1234567890123456'

    decrypt_array = []
    cipher = AES.new(key, AES.MODE_ECB)

    if mode == 'ECB':
        for block in block_array:
            decrypt_array.append(cipher.decrypt(block))
        return decrypt_array

    elif mode == 'CBC':
        iv = CBC_iv
        for block in block_array:
            decrypt_array.append(byte_xor(iv, cipher.decrypt(block)))
            iv = block
        return decrypt_array

    elif mode == 'CTR':
        counter = CTR_iv
        for block in block_array:
            decrypt_array.append(byte_xor(cipher.encrypt(counter), block))
            counter = byte_add(counter, 1)
        return decrypt_array
