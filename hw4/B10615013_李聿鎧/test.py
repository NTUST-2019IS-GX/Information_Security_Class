#!/usr/bin/python
# encoding=utf-8
# HW4 RSA-test B10615013
from RSA import initial, encrypt, decrypt

plaintext = "Daniel Han Kuo-yu is a Taiwanese politician. He was a member of the Legislative Yuan from 1993 to 2002, " \
            "representing a portion of Taipei County for three terms. He later became general manager of Taipei " \
            "Agricultural Products Marketing Corporation. In 2017, Han contested the Kuomintang chairmanship, " \
            "losing to Wu Den-yih. Han was elected Mayor of Kaohsiung in November 2018, and became the first " \
            "Kuomintang politician since Wu in 1998 to hold the office. Han is the KMT's nominee running against " \
            "incumbent president Tsai Ing-wen in the 2020 Taiwan presidential election. "

ciphertext = ""

p, q, n, e, d = initial(1024)
print("==KEY==")
print("p=" + str(p))
print("q=" + str(q))
print("n=" + str(n))
print("e=" + str(e))
print("d=" + str(d) + "\n")

print("==PLAINTEXT==")
print(plaintext + "\n")

print("==CIPHERTEXT==")
ciphertext = encrypt(plaintext, n, e)
print(ciphertext + "\n")

print("==CIPHERTEXT DECRYPT==")
plaintext_decrypt = decrypt(ciphertext, n, d)
print(plaintext_decrypt + "\n")

if plaintext == plaintext_decrypt:
    print("SUCCESS")