# HW2 Decrypt DES
# encoding=utf-8
# ~ python Decrypt.py {Key} {Ciphertext}

import sys
from myDES import DESMethod


def main():
    if len(sys.argv) != 3:
        print("Error: Wrong argv.")
        exit()
    key = sys.argv[1]
    ciphertext = sys.argv[2]
    des = DESMethod(key, ciphertext)
    print(des.decrypt())


if __name__ == "__main__":
    main()
