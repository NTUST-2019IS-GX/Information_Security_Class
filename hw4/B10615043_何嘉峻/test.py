from Rsa import init, encrypt, decrypt


def main():
    bit_len = 1024
    p, q, n, e, d = init(bit_len)

    print('Init', bit_len, 'bit key result:')
    print('p = ', p)
    print('q = ', q)
    print('n = ', n)
    print('e = ', e)
    print('d = ', d)

    plaintext = input('Plaintext = ')

    cipher_array = encrypt(n, e, plaintext)
    print('Ciphertext =', ' '.join(cipher_array))

    if decrypt(n, d, cipher_array) == plaintext:
        print('Correct Result')
    else:
        print('Wrong Result')

    exit()


if __name__ == "__main__":
    main()
