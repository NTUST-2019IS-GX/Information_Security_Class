import sys
from random import randrange
from math import gcd

# Example input
# Rsa.py -init 1024
# Rsa.py -e {n} {e} {plaintext}
# Rsa.py -d {n} {d} {ciphertext}
# Rsa.py -crt {d} {p} {q} {ciphertext}


# Extend GCD Algorithm
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


# Find modular inverse
def modinv(a, m):
    # ax + my = gcd(a,m) = 1
    # ax - 1 = (-y)m
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# Miller Rabin Test
def miller_rabin(n):
    if n == 2 or n == 3:
        return True
    if not n & 1:
        return False

    k = 0
    m = n - 1

    while m % 2 == 0:
        m //= 2
        k += 1

    a = randrange(2, n - 1)
    b = pow(a, m, n)
    if b == 1:
        return True
    for i in range(k - 1):
        if b == n - 1:
            return True
        b = pow(b, 2, n)
    return b == n - 1


def init(bit_len, base=10):
    # Variables
    p = 0
    q = 0
    e = 0

    # Find p, q
    pq_check = [False, False]
    while not pq_check[0]:
        p = randrange(pow(2, bit_len - 1), pow(2, bit_len))
        pq_check[0] = miller_rabin(p)
    while not pq_check[1]:
        q = randrange(pow(2, bit_len - 1), pow(2, bit_len))
        while p == q:
            q = randrange(pow(2, bit_len - 1), pow(2, bit_len))
        pq_check[1] = miller_rabin(q)

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

    # dec/hex
    if base == 10:
        return p, q, n, e, d
    else:
        return hex(p), hex(q), hex(n), hex(e), hex(d)


def encrypt(n, e, plaintext, base=10):
    n = int(str(n), base)
    e = int(str(e), base)

    e = format(e, 'b')
    ciphertext = []

    # Square and Multiply
    for byte in plaintext:
        x = byte = ord(byte)
        for h in range(1, len(e)):
            x = pow(x, 2, n)
            if e[h] == '1':
                x = x * byte % n

        if base == 10:
            ciphertext.append(str(x))
        else:
            ciphertext.append(hex(x))
    return ciphertext


def decrypt(n, d, ciphertext, base=10):
    n = int(str(n), base)
    d = int(str(d), base)

    d = format(d, 'b')
    plaintext = ''

    # Square and Multiply
    for byte in ciphertext:
        x = byte = int(str(byte), base)
        for h in range(1, len(d)):
            x = pow(x, 2, n)
            if d[h] == '1':
                x = x * byte % n
        plaintext += chr(x)
    return plaintext


# Chinese Remainder Theorem
def decrypt_CRT(d, p, q, ciphertext, base=10):
    d = int(str(d), base)
    p = int(str(p), base)
    q = int(str(q), base)

    dP = d % (p - 1)
    dQ = d % (q - 1)
    # qInv = q^-1 mod p
    qInv = modinv(q, p)

    dP = format(dP, 'b')
    dQ = format(dQ, 'b')

    plaintext = ''
    for byte in ciphertext:
        x1 = x2 = byte = int(str(byte), base)

        # x1 = C^dP mod p
        for h in range(1, len(dP)):
            x1 = pow(x1, 2, p)
            if dP[h] == '1':
                x1 = x1 * byte % p

        # x2 = C^dQ mod q
        for h in range(1, len(dQ)):
            x2 = pow(x2, 2, q)
            if dQ[h] == '1':
                x2 = x2 * byte % q

        # h = qInv(x1 - x2) mod p
        h = qInv * (x1 - x2) % p

        # M = x2 + h * q
        plaintext += chr(x2 + h * q)
    return plaintext


def main():
    base = 10
    i = 1
    if sys.argv[i] == '-hex':
        base = 16
        i = 2

    if sys.argv[i] == '-init':
        bit_len = int(sys.argv[i+1])
        p, q, n, e, d = init(bit_len, base)

        print('Init', bit_len, 'bit key result:')
        print('p = ', p)
        print('q = ', q)
        print('n = ', n)
        print('e = ', e)
        print('d = ', d)

    elif sys.argv[i] == '-e':
        # Variables
        n = int(sys.argv[i+1], base)
        e = int(sys.argv[i+2], base)
        plaintext = sys.argv[i+3]

        print('Encrypt Result:')
        cipher_array = encrypt(n, e, plaintext, base)
        print(' '.join(cipher_array))

    elif sys.argv[i] == '-d':
        # Variables
        n = int(sys.argv[i+1], base)
        d = int(sys.argv[i+2], base)
        ciphertext = sys.argv[i+3:]

        print('Decrypt Result:')
        print(decrypt(n, d, ciphertext, base))

    elif sys.argv[i] == '-crt':
        # Variables
        d = int(sys.argv[i+1], base)
        p = int(sys.argv[i+2], base)
        q = int(sys.argv[i+3], base)
        ciphertext = sys.argv[i+4:]

        print('CRT Decrypt Result:')
        print(decrypt_CRT(d, p, q, ciphertext, base))

    else:
        raise Exception('No matching parameters, Please try again.')

    exit()


if __name__ == "__main__":
    main()
