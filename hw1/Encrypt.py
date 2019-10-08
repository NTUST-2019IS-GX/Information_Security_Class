#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys


def findchar(c, keytable):
    if c == "j":
        c = "i"
    for i in range(5):
        for j in range(5):
            if (c == keytable[i][j]):
                return [i, j]


def caesar(key, plaintext):
    ciphertext = ""
    for c in plaintext:
        ciphertext += chr((ord(c) - 97 + int(key)) % 26 + 97)
    return ciphertext


def playfair(key, plaintext):
    ciphertext = ""

    # --keytable(without "j")--
    key = str(key).replace('j', 'i')
    keylist = {}
    keytable = [[] for i in range(5)]
    for c in key:
        keylist[c] = 0  # only use key
    for i in range(26):
        if i != 9:  # without "j"
            keylist[chr(i + 97)] = 0  # only use key
    keylist = list(keylist.keys())
    for i in range(5):
        for j in range(5):
            keytable[i].append(keylist[j + i * 5])
        # print(keytable[i])

    # --makepair--
    textlist = []
    plaintext_temp = plaintext
    while len(plaintext_temp) > 0:
        temppair = ""
        temppair += plaintext_temp[0]
        plaintext_temp = plaintext_temp[1:]  # remove first char
        if len(plaintext_temp) == 0:
            temppair += "x"
        elif plaintext_temp[0] == temppair[0]:
            temppair += "x"
        else:
            temppair += plaintext_temp[0]
            plaintext_temp = plaintext_temp[1:]
        textlist.append(temppair)
    # print(textlist)

    # --encrypt--
    while len(textlist) > 0:
        a = findchar(textlist[0][0], keytable)
        b = findchar(textlist[0][1], keytable)
        if a[0] == b[0]:  # same row
            ciphertext += keytable[a[0]][(a[1] + 1) % 5] \
                          + keytable[b[0]][(b[1] + 1) % 5]
        elif a[1] == b[1]:  # same col
            ciphertext += keytable[(a[0] + 1) % 5][a[1]] \
                          + keytable[(b[0] + 1) % 5][b[1]]
        else:
            ciphertext += keytable[a[0]][b[1]] \
                          + keytable[b[0]][a[1]]
        textlist = textlist[1:]
    return ciphertext


def vernam(key, plaintext):  # proposed the autokey system
    ciphertext = ""
    key = str(key).lower() + plaintext
    for i in range(len(plaintext)):
        ciphertext += chr(((ord(plaintext[i]) - 97) ^ (ord(key[i]) - 97)) + 65)
    return ciphertext


def row(key, plaintext):
    ciphertext = ""
    key = int(key)
    keylist = []
    while key > 0:
        keylist.insert(0, key % 10)
        key //= 10
    keylen = len(keylist)
    textlen = len(plaintext)
    rowtable = {}
    for i in keylist:
        rowtable[i] = []
    for i in range(textlen):
        rowtable[int(list(rowtable.keys())[i % keylen])].append(plaintext[i])
    # print(rowtable)
    for i in range(keylen):
        # print(rowtable[i + 1])
        ciphertext += "".join(rowtable[i + 1])
    return ciphertext


def rail_fence(key, plaintext):
    ciphertext = ""
    key = int(key)
    index = -1
    add = 1
    railtable = [[] for i in range(key)]
    for i in range(len(plaintext)):
        index += add
        railtable[index].append(plaintext[i])
        if key == 1:
            add = 0
        elif index == key - 1:
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
        print(playfair(str(key).lower(), plaintext).upper())
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
