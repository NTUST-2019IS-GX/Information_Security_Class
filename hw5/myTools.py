from random import randrange


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


# Square and Multiply
def square_and_multiply(base, exponent, mod):
    exponent = format(exponent, 'b')
    result = base

    for h in range(1, len(exponent)):
        result = pow(result, 2, mod)
        if exponent[h] == '1':
            result = result * base % mod

    return result
