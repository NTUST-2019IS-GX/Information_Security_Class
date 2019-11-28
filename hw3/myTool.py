block_size = 16  # 128 bits


def pad(block, size):  # PKCS
    blank = size - len(block)
    for i in range(blank):
        block += bytes([blank])
    return block


def openppm(ppm_name):
    with open(ppm_name, mode='rb') as file:
        magic_number = file.readline()
        size = file.readline()
        maximum_value = file.readline()

        # Blocks process to en/decrypt
        blocks = []
        content = file.read(16)
        while content:
            blocks.append(content)
            content = file.read(16)

        # Do padding
        blocks[-1] = pad(blocks[-1], block_size)
    return magic_number, size, maximum_value, blocks


def writeppm(result_ppm, magic_number, size, maximum_value, blocks):
    with open(result_ppm, 'wb') as result:
        result.write(magic_number)
        result.write(size)
        result.write(maximum_value)
        for block in blocks:
            result.write(block)


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def byte_add(byte_val, int_val):
    int_val = int_val + int.from_bytes(byte_val, byteorder='big')
    return int_val.to_bytes(block_size, byteorder='big')


def key_preprocess(key):
    # string to bytes
    key = key.encode(encoding="utf-8")
    key_bytes = len(key)
    # 1 byte = 8 bits
    if key_bytes == 16 or key_bytes == 24 or key_bytes == 32:  # equal 128 or 192 or 256 bits
        return key
    else:
        if key_bytes < 16:  # key_bits < 128
            return pad(key, 16)
        elif key_bytes < 24:  # 128 < key_bits < 192
            return pad(key, 24)
        elif key_bytes < 32:  # 192 < key_bits < 256
            return pad(key, 32)
        else:  # otherwise
            print("Error: key length must be lower than 256 bit.")
            exit()
