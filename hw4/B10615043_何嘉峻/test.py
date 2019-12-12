from Rsa import init, encrypt, decrypt, decrypt_CRT


def main():
    base = input('Which base mode (dec/hex): ')
    if base == 'hex':
        base = 16
    else:
        base = 10

    bit_len = 1024
    p, q, n, e, d = init(bit_len, base)

    print('Init', bit_len, 'bit key result:')
    print('p = ', p)
    print('q = ', q)
    print('n = ', n)
    print('e = ', e)
    print('d = ', d)

    plaintext = input('Plaintext = ')

    cipher_array = encrypt(n, e, plaintext, base)
    print('Ciphertext =', ' '.join(cipher_array))

    result = decrypt(n, d, cipher_array, base)
    print('Origin Decrypt Result =', result)
    if result == plaintext:
        print('--- Origin Decrypt CORRECT ---')
    else:
        raise Exception('Origin Decrypt WRONG')

    crt_result = decrypt_CRT(d, p, q, cipher_array, base)
    print('CRT Decrypt Result =', crt_result)
    if crt_result == plaintext:
        print('--- CRT Decrypt CORRECT ---')
    else:
        raise Exception('CRT Decrypt WRONG')

    exit()


if __name__ == "__main__":
    main()
