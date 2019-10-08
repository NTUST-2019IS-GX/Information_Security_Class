# HW1 Decrypt
# encoding=utf-8
# ~ python Decrypt.py {Cipher} {Key} {Ciphertext}

import sys


class DecryptMethod:
    def __init__(self, key, ciphertext):
        self.key = key
        self.ciphertext = ciphertext.replace(' ', '')
        self.ciphertext = self.ciphertext.upper()
        self.plaintext = ''

    def decrypt(self):
        return self.plaintext.lower()


class Caesar(DecryptMethod):
    def decrypt(self):
        for i in self.ciphertext:
            self.plaintext += (chr((ord(i) - 65 - int(self.key)) % 26 + 65))
        self.plaintext = self.plaintext.lower()
        return self.plaintext


class Playfair(DecryptMethod):
    def __init__(self, key, ciphertext):
        super().__init__(key, ciphertext)
        self.key = self.key.upper()
        self.key_table = self.make_key_table()
        self.cipher_group = self.make_cipher_group()

    def decrypt(self):
        for group in self.cipher_group:
            pos0 = self.get_pos(group[0])
            pos1 = self.get_pos(group[1])

            if pos0[0] == pos1[0]:  # same row
                self.plaintext += self.get_letter(pos0[0], (pos0[1] - 1) % 5)
                self.plaintext += self.get_letter(pos1[0], (pos1[1] - 1) % 5)
            elif pos0[1] == pos1[1]:  # same column
                self.plaintext += self.get_letter((pos0[0] - 1) % 5, pos0[1])
                self.plaintext += self.get_letter((pos1[0] - 1) % 5, pos1[1])
            else:
                self.plaintext += self.get_letter(pos0[0], pos1[1])
                self.plaintext += self.get_letter(pos1[0], pos0[1])
        self.plaintext = self.plaintext.lower()
        return self.plaintext

    def make_key_table(self):
        letter = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        key = self.key.replace('J', 'I')

        row = 0
        col = 0
        key_table = [[]]

        for i in key:
            if letter.find(i, 0) != -1:
                if col == 5:
                    col = 0
                    row += 1
                    key_table.append([])

                key_table[row].append(i)
                col += 1
                key = key.replace(i, '')
                letter = letter.replace(i, '')

        for i in letter:
            if letter.find(i, 0) != -1:
                if col == 5:
                    col = 0
                    row += 1
                    key_table.append([])

                key_table[row].append(i)
                col += 1
                letter = letter.replace(i, '')
        return key_table

    def make_cipher_group(self):
        ciphertext = self.ciphertext.replace('J', 'I')
        append = True
        table_index = -1
        cipher_group = []

        for i in range(len(ciphertext)):
            if append:
                cipher_group.append([])
                table_index += 1
                append = False
            else:
                append = True
            cipher_group[table_index].append(ciphertext[i])
        return cipher_group

    def get_pos(self, letter):
        for row in self.key_table:
            if letter in row:
                return [self.key_table.index(row), row.index(letter)]

    def get_letter(self, row, col):
        return self.key_table[row][col]


class Vernam(DecryptMethod):
    def __init__(self, key, ciphertext):
        super().__init__(key, ciphertext)
        self.key = self.key.upper()

    def decrypt(self):
        key = self.key
        ciphertext = self.ciphertext
        while len(ciphertext) != 0:
            key = self.vernam_xor(key, ciphertext[:len(key):])
            ciphertext = ciphertext[len(key)::]
            self.plaintext += key
        self.plaintext = self.plaintext.lower()
        return self.plaintext

    def vernam_xor(self, part_key, part_ciphertext):
        plaintext = ''
        for i in range(len(part_ciphertext)):
            plaintext += chr(((ord(part_ciphertext[i]) - 65) ^ (ord(part_key[i]) - 65)) + 65)
        return plaintext


class RowTransposition(DecryptMethod):
    def __init__(self, key, ciphertext):
        super().__init__(key, ciphertext)
        self.row = 0
        self.table = self.make_table()
        self.extend = len(self.ciphertext) % len(self.key)

    def decrypt(self):
        ciphertext = self.ciphertext
        for i in range(len(self.key)):
            index = self.key.find(str(i + 1))
            times = self.row
            if self.extend != 0:
                if index >= self.extend:
                    times -= 1
            for j in range(times):
                self.table[j][index] = ciphertext[0]
                ciphertext = ciphertext[1::]
        for i in self.table:
            for j in i:
                self.plaintext += j
        self.plaintext = self.plaintext.lower()
        return self.plaintext

    def make_table(self):
        if len(self.ciphertext) % len(self.key) == 0:
            self.row = int(len(self.ciphertext) / len(self.key))
        else:
            self.row = int(len(self.ciphertext) / len(self.key)) + 1
        table = []
        for i in range(self.row):
            table.append([])
            for j in range(len(self.key)):
                table[i].append('')
        return table


class RailFence(DecryptMethod):
    def __init__(self, key, ciphertext):
        super().__init__(key, ciphertext)
        self.key = int(self.key)
        self.fence = self.make_fence()

    def decrypt(self):
        ciphertext = self.ciphertext
        for part_fence in self.fence:
            while '-' in part_fence:
                index = part_fence.index('-')
                part_fence[index] = ciphertext[0]
                ciphertext = ciphertext[1::]
        descending = 1
        index = 0
        for i in range(len(self.ciphertext)):
            for j in range(self.key):
                if j == index:
                    self.plaintext += self.fence[index][i]
            if self.key > 1:
                index += descending
                if index == (self.key - 1):
                    descending = -1
                elif index == 0:
                    descending = 1
        self.plaintext = self.plaintext.lower()
        return self.plaintext

    def make_fence(self):
        fence = []
        for i in range(self.key):
            fence.append([])
        descending = 1
        index = 0
        for i in range(len(self.ciphertext)):
            for j in range(self.key):
                if j == index:
                    fence[j].append('-')
                else:
                    fence[j].append('')
            if self.key > 1:
                index += descending
                if index == (self.key - 1):
                    descending = -1
                elif index == 0:
                    descending = 1
        return fence


def main():
    if len(sys.argv) != 4:
        print("Error: Wrong argv.")
        exit()
    cipher = str(sys.argv[1]).lower()
    key = sys.argv[2]
    ciphertext = str(sys.argv[3]).lower()
    if cipher == "caesar":
        print(Caesar(key, ciphertext).decrypt())
    elif cipher == "playfair":
        print(Playfair(key, ciphertext).decrypt())
    elif cipher == "vernam":
        print(Vernam(key, ciphertext).decrypt())
    elif cipher == "row":
        print(RowTransposition(key, ciphertext).decrypt())
    elif cipher == "rail_fence":
        print(RailFence(key, ciphertext).decrypt())
    else:
        print("Error: Wrong cipher.")
        exit()


if __name__ == "__main__":
    main()
