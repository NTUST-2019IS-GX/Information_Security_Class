block_size = 16


def pad(block):
    blank = block_size - len(block)
    for i in range(blank):
        block += bytes([blank])
    return block


def openppm(ppm_name):
    with open(ppm_name, mode='rb') as file:
        magic_number = file.readline()
        size = file.readline()
        maximum_value = file.readline()

        # Blocks process to encrypt
        blocks = []
        content = file.read(16)
        while content:
            blocks.append(content)
            content = file.read(16)

        # Padding Process
        blocks[-1] = pad(blocks[-1])
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
