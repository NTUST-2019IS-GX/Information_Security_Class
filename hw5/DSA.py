import hashlib
import os
import sys
from random import randrange
from myTools import *

# Example input
# DSA.py -keygen 160 dsa_privatekey.pem dsa_publickey.pem
# DSA.py -sign dsa_privatekey.pem dsa_publickey.pem doc.txt doc.sig
# DSA.py -verify dsa_publickey.pem doc.txt doc.sig


help_message = '''
Usage:	RSA.py COMMAND

Command:
    -keygen <bit-length> [<privatekey_name>] [<publickey_path>]
    -sign <privatekey_path> <publickey_path> <message_path> [<signature_name>]
    -verify <publickey_path> <message_path> <signature_name>
    -help
    
    * bit-length only support 160 bits.
'''
bit_len = 160
p_len = 1024


def keygen():
    # Generate p, q
    while True:
        q = randrange(2 ** (bit_len-1), 2 ** bit_len)
        if miller_rabin(q):
            break
    while True:
        padding = randrange(2 ** (p_len - bit_len - 1) - 1, 2 ** (p_len - bit_len))
        p = q * padding + 1
        if miller_rabin(p):
            break

    # Generate a
    h = 2
    exponent = (p - 1) // q
    while True:
        a = square_and_multiply(h, exponent, p)
        if p > 1:
            break
        h = h + 1

    # Generate d, b
    d = randrange(1, q)
    b = square_and_multiply(a, d, p)

    return p, q, a, b, d


def read_publickey(file_name):
    file = open(file_name, 'r')
    p = q = a = b = 0
    while True:
        key = file.readline().replace('\n', '')
        if key == '-----BEGIN PUBLIC KEY-----':
            p = int(file.readline().replace('\n', ''), 16)
            q = int(file.readline().replace('\n', ''), 16)
            a = int(file.readline().replace('\n', ''), 16)
            b = int(file.readline().replace('\n', ''), 16)
        elif key == '-----END PUBLIC KEY-----':
            file.close()
            break
    return p, q, a, b


def read_privatekey(file_name):
    file = open(file_name, 'r')
    d = 0
    while True:
        key = file.readline().replace('\n', '')
        if key == '-----BEGIN DSA PRIVATE KEY-----':
            d = int(file.readline().replace('\n', ''), 16)
        elif key == '-----END DSA PRIVATE KEY-----':
            file.close()
            break
    return d


def read_signature(file_name):
    file = open(file_name, 'r')
    r = s = 0
    while True:
        key = file.readline().replace('\n', '')
        if key == '-----BEGIN SIGNATURE-----':
            r = int(file.readline().replace('\n', ''), 16)
            s = int(file.readline().replace('\n', ''), 16)
        elif key == '-----END SIGNATURE-----':
            file.close()
            break
    return r, s


def write_publickey(file_name, p, q, a, b):
    publickey_file = open(file_name, 'w+')
    publickey_file.write('-----BEGIN PUBLIC KEY-----' + '\n')
    publickey_file.write(hex(p)[2:] + '\n')
    publickey_file.write(hex(q)[2:] + '\n')
    publickey_file.write(hex(a)[2:] + '\n')
    publickey_file.write(hex(b)[2:] + '\n')
    publickey_file.write('-----END PUBLIC KEY-----' + '\n')
    publickey_file.close()


def write_privatekey(file_name, d):
    privatekey_file = open(file_name, 'w+')
    privatekey_file.write('-----BEGIN DSA PRIVATE KEY-----' + '\n')
    privatekey_file.write(hex(d)[2:] + '\n')
    privatekey_file.write('-----END DSA PRIVATE KEY-----' + '\n')
    privatekey_file.close()


def write_signature(file_name, r, s):
    signature_file = open(file_name, 'w+')
    signature_file.write('-----BEGIN SIGNATURE-----' + '\n')
    signature_file.write(hex(r)[2:] + '\n')
    signature_file.write(hex(s)[2:] + '\n')
    signature_file.write('-----END SIGNATURE-----' + '\n')
    signature_file.close()


def main():
    # Argv error handling
    if len(sys.argv) <= 1:
        raise Exception(help_message)

    if sys.argv[1] == '-keygen':
        # Error Handling
        if len(sys.argv) < 3:
            raise Exception(help_message)
        if int(sys.argv[2]) != bit_len:
            raise Exception('bit-length only support 160 bits.')

        privatekey_name = 'dsa_privatekey.pem'
        publickey_name = 'dsa_publickey.pem'

        try:
            privatekey_name = sys.argv[3]
            publickey_name = sys.argv[4]
        except IndexError:
            pass

        # Key Generate
        p, q, a, b, d = keygen()

        # Write into files
        write_publickey(publickey_name, p, q, a, b)
        write_privatekey(privatekey_name, d)

    elif sys.argv[1] == '-sign':
        # Error Handling
        if len(sys.argv) < 5:
            raise Exception(help_message)
        d = read_privatekey(sys.argv[2])
        p, q, a, b = read_publickey(sys.argv[3])
        message_file = open(sys.argv[4], 'r')
        signature_name = os.path.splitext(message_file.name)[0] + '.sig'
        try:
            signature_name = sys.argv[5]
        except IndexError:
            pass

        # Compute hashed message
        sha = hashlib.sha1()
        message = message_file.read().encode('utf-8')
        sha.update(message)
        hash_message = sha.hexdigest()

        # Generate ke, r, s
        ke = randrange(1, q)
        r = square_and_multiply(a, ke, p) % q
        s1 = (int(hash_message, 16) + d * r) % q
        s2 = modinv(ke, q) % q
        s = (s1 * s2) % q

        # Write into files
        write_signature(signature_name, r, s)

    elif sys.argv[1] == '-verify':
        # Error Handling
        if len(sys.argv) < 5:
            raise Exception(help_message)
        p, q, a, b = read_publickey(sys.argv[2])
        message_file = open(sys.argv[3], 'r')
        r, s = read_signature(sys.argv[4])

        # Compute hashed message
        sha = hashlib.sha1()
        message = message_file.read().encode('utf-8')
        sha.update(message)
        hash_message = sha.hexdigest()

        # Generate w, v
        w = modinv(s, q)
        v1 = square_and_multiply(a, (w * int(hash_message, 16)) % q, p)
        v2 = square_and_multiply(b, (w * r) % q, p)
        v = ((v1 * v2) % p) % q

        if r == v:
            print('Verified OK')
        else:
            print('Verification Failure')

    elif sys.argv[1] == '-help':
        print(help_message)
    else:
        raise Exception(help_message)

    exit()


if __name__ == "__main__":
    main()
