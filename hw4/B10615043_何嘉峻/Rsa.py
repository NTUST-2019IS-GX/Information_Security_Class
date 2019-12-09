import sys
from random import randrange
from math import gcd

# Example input
# Rsa.py init 1024
# Rsa.py -e {n} {e} {plaintext}
# Rsa.py -d {n} {d} {ciphertext}


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def check(a, s, d, n):
    x = pow(a, d, n)
    if x == 1:
        return True
    for i in range(s - 1):
        if x == n - 1:
            return True
        x = pow(x, 2, n)
    return x == n - 1


def miller_rabin(n, k=10):
    if n == 2 or n == 3:
        return True
    if not n & 1:
        return False

    s = 0
    d = n - 1

    while d % 2 == 0:
        d >>= 1
        s += 1

    for i in range(k):
        a = randrange(2, n - 1)
        if not check(a, s, d, n):
            return False
    return True


def init(bit_len):
    # Variables
    p = 0
    q = 0
    e = 0

    # Find p, q
    pq_check = [False, False]
    while not pq_check[0]:
        p = randrange(pow(2, bit_len - 1), pow(2, bit_len))
        pq_check[0] = miller_rabin(p, 1)
    while not pq_check[1]:
        q = randrange(pow(2, bit_len - 1), pow(2, bit_len))
        pq_check[1] = miller_rabin(q, 1)

    n = p * q

    # φ(p x q) = (p - 1) * (q - 1)
    phi = (p - 1) * (q - 1)

    # Find e
    for i in range(2, phi):
        if gcd(i, phi) == 1:
            e = i
            break

    # Find d
    d = modinv(e, phi)

    return p, q, n, e, d


def encrypt(n, e, plaintext):
    e = format(e, 'b')
    ciphertext = []

    for byte in plaintext:
        x = byte = ord(byte)
        for h in range(1, len(e)):
            x = pow(x, 2, n)
            if e[h] == '1':
                x = x * byte % n
        ciphertext.append(str(x))
    return ciphertext


def decrypt(n, d, ciphertext):
    d = format(d, 'b')
    plaintext = ''

    for byte in ciphertext:
        x = byte = int(byte)
        for h in range(1, len(d)):
            x = pow(x, 2, n)
            if d[h] == '1':
                x = x * byte % n
        plaintext += chr(x)
    return plaintext


def main():
    # Argv error handling
    # if len(sys.argv) > 5:
    #     print("Error: Wrong argv. Format: ")
    #     exit()

    if sys.argv[1] == 'init':
        bit_len = int(sys.argv[2])
        p, q, n, e, d = init(bit_len)

        print('Init', bit_len, 'bit key result:')
        print('p = ', p)
        print('q = ', q)
        print('n = ', n)
        print('e = ', e)
        print('d = ', d)

    elif sys.argv[1] == '-e':
        # Variables
        n = int(sys.argv[2])
        e = int(sys.argv[3])
        plaintext = sys.argv[4]

        print('Encrypt Result:')
        cipher_array = encrypt(n, e, plaintext)
        print(' '.join(cipher_array))

    elif sys.argv[1] == '-d':
        # Variables
        n = int(sys.argv[2])
        d = int(sys.argv[3])
        ciphertext = sys.argv[4:]

        print('Decrypt Result:')
        print(decrypt(n, d, ciphertext))

    exit()


if __name__ == "__main__":
    main()
