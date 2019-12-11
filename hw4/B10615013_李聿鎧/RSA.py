#!/usr/bin/python
# encoding=utf-8
# python ./Rsa.py -i {bits}
# python ./Rsa.py -e {plaintext_filename} {PublicKey_filename}
# python ./Rsa.py -d {ciphertext_filename} {PrivateKey_filename}
import sys
from random import randint, getrandbits
from math import gcd


def MillerRabinTest(n):  # Miller–Rabin primality test
    m = n - 1
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1
    a = randint(2, n - 1)  # a in {2, ..., n-2}
    b = pow(a, m, n)
    if b != 1 and b != n - 1:
        i = 1
        while i < k and b != n - 1:
            b = pow(b, 2, n)
            if b == 1:
                return False
            i += 1
        if b != n - 1:
            return False
    return True


def isPrime(n):
    # Corner cases
    if n <= 1:
        return False
    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    # Miller–Rabin primality test
    for _ in range(3):
        if not MillerRabinTest(n):
            return False

    return True


def get_RndPrime(bits):
    rnd = int("1" + format(getrandbits(bits - 1), 'b').zfill(bits - 1), 2)
    while not isPrime(rnd):
        rnd = int("1" + format(getrandbits(bits - 1), 'b').zfill(bits - 1), 2)
    return rnd


def ext_euclid(a, b):
    old_s, s = 1, 0
    old_t, t = 0, 1
    old_r, r = a, b
    if b == 0:
        return 1, 0, a
    else:
        while r != 0:
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
            old_t, t = t, old_t - q * t
    return old_s, old_t, old_r


def mod_inverse(a, b):
    x, y, g = ext_euclid(a, b)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % b

def initial(bits):
    p = get_RndPrime(bits)
    q = get_RndPrime(bits)
    n = p * q
    e = 0
    d = 1

    phi = (p - 1) * (q - 1)
    for i in range(2, phi):
        if gcd(i, phi) == 1:
            e = i
            break

    # Extended Euclidean algorithm
    d = mod_inverse(e, phi)

    return p, q, n, e, d


def encrypt(plaintext, n, e):
    ciphertext = ""
    for c in plaintext:
        c = ord(c)
        ciphertext += str(pow(c, e, n)) + ","
    return ciphertext[:len(ciphertext) - 1]


def decrypt(ciphertext, n, d):
    plaintext = ""
    cipher_array = ciphertext.split(",")
    for c in cipher_array:
        c = int(c)
        plaintext += chr(pow(c, d, n))
    return plaintext


def readKey(filename):
    fp = open(filename)
    lines = fp.readlines()
    key_array = lines[0].split(",")
    return int(key_array[0]), int(key_array[1])  # n, e_or_d


def writeKey(filename, n, e_or_d):
    fp = open(filename, "w")
    fp.writelines(str(n) + "," + str(e_or_d))
    fp.close()


def readfile(filename):
    fp = open(filename)
    lines = fp.readlines()
    return lines

def writefile(filename, text):
    fp = open(filename, "w")
    fp.writelines(str(text))
    fp.close()


def main():
    option = sys.argv[1]
    if option == "-i":  # Create key
        bits = int(sys.argv[2])
        print("Creating key...")
        p, q, n, e, d = initial(bits)
        writeKey("kPublic", n, e)
        writeKey("kPrivate", n, d)
        print("Success!!")
        print(">> N=" + str(n))
        print(">> e=" + str(e))
        print(">> d=" + str(d))
        print("The public key file has been save as \"kPublic\"\nThe private key file has been save as \"kPrivate\"\n")

    elif option == "-e":  # Encrypt
        plainFileName = str(sys.argv[2])
        plaintext = readfile(plainFileName)[0].replace("\n", "")
        keyName = str(sys.argv[3])
        n, d = readKey(keyName)
        ciphertext = encrypt(plaintext, n, d)
        print(ciphertext + "\n")
        writefile("ciphertext.txt", ciphertext)


    elif option == "-d":  # Decrypt
        cipherFileName = str(sys.argv[2])
        ciphertext = readfile(cipherFileName)[0].replace("\n", "")
        keyName = str(sys.argv[3])
        n, e = readKey(keyName)
        plaintext = decrypt(ciphertext, n, e)
        print(plaintext + "\n")
        writefile("plaintext_decrypt.txt", plaintext)

    else:
        print("Wrong argv")


if __name__ == '__main__':
    main()
