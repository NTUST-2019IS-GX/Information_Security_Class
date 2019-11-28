from Crypto.Cipher import AES
from myTool import byte_xor, byte_add, key_preprocess

CBC_iv = b'1234567890123456'
CTR_iv = b'\xe5\xad\xa6\xe4\xb9\xa0\xe5\xbe\x00\x00\x00\x00\x00\x00\x00\x00'


def EncryptAES(block_array, key, mode):

    key = key_preprocess(key)

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

    else:  # otherwise
        print("Error: Encrypt mode only support ECB/CBC/CTR")
        exit()


def DecryptAES(block_array, key, mode):
    # Do key preprocess
    key = key_preprocess(key)

    # new array to save decrypt blocks and new AES cipher
    decrypt_array = []
    cipher = AES.new(key, AES.MODE_ECB)

    # Determine Mode
    if mode == 'ECB':
        # Every block do once AES
        for block in block_array:
            decrypt_array.append(cipher.decrypt(block))
        return decrypt_array

    elif mode == 'CBC':
        iv = CBC_iv  # C0 = Initial Vector
        # Pi = Dk(Ci) xor Ci-1
        for block in block_array:
            decrypt_array.append(byte_xor(iv, cipher.decrypt(block)))
            iv = block
        return decrypt_array

    elif mode == 'CTR':
        counter = CTR_iv  # Initial Counter
        # Pi = Ek(CTR + i) xor Ci
        for block in block_array:
            decrypt_array.append(byte_xor(cipher.encrypt(counter), block))
            counter = byte_add(counter, 1)
        return decrypt_array

    else:  # otherwise
        print("Error: Decrypt mode only support ECB/CBC/CTR")
        exit()
