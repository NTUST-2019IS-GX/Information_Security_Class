#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys


def caesar(key, plaintext):
    ciphertext = ""
    for c in plaintext:
        ciphertext += chr((ord(c) - 97 + int(key)) % 26 + 97)
    return ciphertext


def playfair(key, plaintext):
    ciphertext = ""
    keylist = list(key)
    # TODO: playfair
    return ciphertext


def vernam(key, plaintext):
    ciphertext = ""
    key = str(key).lower()
    for i in range(len(plaintext)):
        ciphertext += chr((ord(plaintext[i]) + ord(key[i % len(key)]) - 194) % 26 + 97)
    return ciphertext


def row(key, plaintext):
    ciphertext = ""
    # TODO: row
    return ciphertext


def rail_fence(key, plaintext):
    ciphertext = ""
    key = int(key)-1
    index = -1
    add = 1
    railtable = [[] for i in range(key)]
    for i in range(len(plaintext)):
        index += add
        railtable[index].append(plaintext[i])
        if index == key:
            add = -1
        elif index == 0:
            add = 1
    for j in range(key):
        ciphertext += "".join(railtable[j])
    return ciphertext


def main():
    if len(sys.argv) != 4:
        print("Error: Wrong argv.")
        exit()
    cipher = str(sys.argv[1]).lower()
    key = sys.argv[2]
    plaintext = str(sys.argv[3]).lower()
    if cipher == "caesar":
        print(caesar(key, plaintext).upper())
    elif cipher == "playfair":
        print(playfair(key, plaintext).upper())
    elif cipher == "vernam":
        print(vernam(key, plaintext).upper())
    elif cipher == "row":
        print(row(key, plaintext).upper())
    elif cipher == "rail_fence":
        print(rail_fence(key, plaintext).upper())
    else:
        print("Error: Wrong cipher.")
        exit()


if __name__ == "__main__":
    main()
