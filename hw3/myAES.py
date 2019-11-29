from Crypto.Cipher import AES
from myTool import byte_xor, byte_add, byte_shift, PRNGs, key_preprocess

iv = b'1234567890123456'  # Initial Vector


def EncryptAES(block_array, key, mode):

    key = key_preprocess(key)

    encrypt_array = []
    cipher = AES.new(key, AES.MODE_ECB)

    if mode == 'ECB':
        for block in block_array:
            encrypt_array.append(cipher.encrypt(block))
        return encrypt_array

    elif mode == 'CBC':
        cipher_block = iv  # Initial Vector
        for block in block_array:
            cipher_block = cipher.encrypt(byte_xor(cipher_block, block))
            encrypt_array.append(cipher_block)
        return encrypt_array

    elif mode == 'COOL':
        initial_vector = iv  # Initial Vector
        i = 0
        for block in block_array:
            encrypt_array.append(byte_xor(cipher.encrypt(initial_vector), block))
            # initial_vector = byte_add(initial_vector, 1) -> origin CTR
            initial_vector = byte_shift(initial_vector, PRNGs(i))  # shift RND byte
            i += 1
        return encrypt_array

    else:  # otherwise
        print("Error: Encrypt mode only support ECB/CBC/COOL")
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
        initial_vector = iv  # C0 = Initial Vector
        # Pi = Dk(Ci) xor Ci-1
        for block in block_array:
            decrypt_array.append(byte_xor(initial_vector, cipher.decrypt(block)))
            initial_vector = block
        return decrypt_array

    elif mode == 'COOL':
        initial_vector = iv  # Initial Counter
        # Pi = Ek(CTR + i) xor Ci
        i = 0
        for block in block_array:
            decrypt_array.append(byte_xor(cipher.encrypt(initial_vector), block))
            # initial_vector = byte_add(initial_vector, 1) -> origin CTR
            initial_vector = byte_shift(initial_vector, PRNGs(i))  # shift RND byte
            i += 1
        return decrypt_array

    else:  # otherwise
        print("Error: Decrypt mode only support ECB/CBC/COOL")
        exit()
