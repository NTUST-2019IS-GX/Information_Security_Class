# HW2 DES random test
# encoding=utf-8
# ~ python test.py {times}
import random
import sys
from myDES import DESMethod


def main():
    if len(sys.argv) != 2:
        print("Error: Wrong argv.")
        exit()
    s = 0
    f = 0
    for j in range(int(sys.argv[1])):
        key = "0x"
        for i in range(16):
            key += random.choice("0123456789ABCDEF")
        plaintext = "0x"
        for i in range(16):
            plaintext += random.choice("0123456789abcdef")

        des = DESMethod(key, plaintext)
        en = des.encrypt()
        des = DESMethod(key, en)
        de = des.decrypt()

        print("## test " + str(j) + " start ##")
        if plaintext == de:
            print("--Success--")
            print("plaintext = " + plaintext)
            print("      key = " + key)
            print("  encrypt = " + en)
            print("  decrypt = " + de)
            s += 1
        else:
            print("==Fail==")
            print("plaintext = " + plaintext)
            print("      key = " + key)
            print("  encrypt = " + en)
            print("  decrypt = " + de)
            f += 1
            input()  # pause to check fail data

    print("")
    print("##### REPORT #####")
    print("Success: " + str(s))
    print("   Fail: " + str(f))


if __name__ == "__main__":
    main()
