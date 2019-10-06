# HW1

Please implement the methods below and follow the slide to make sure that your
(input, output) format is correct.

**Plaintext:** doyourbestandthenletgo

1. **Caesar cipher:**
Key=5
2. **Playfair cipher:**
Key=COMP
3. **Vernam proposed the autokey system:**
Key=TEC
4. **Row transposition:**
Key=45362178
5. **Rail fence cipher:**
Key=2

## 開發環境
+ **IDE:** PyCharm 2019.2
+ **Language:** Python 3.7

## I/O
### Input
```
python Encrypt.py {Cipher} {Key} {Plaintext}
python Decrypt.py {Cipher} {Key} {Ciphertext}
```

#### {Cipher}
```
caesar
playfair
vernam
row
rail_fence
```

### Output
```
{Plaintext} or {Ciphertext}
```

### Example
```
$ python Encrypt.py caesar 7 keepgoingnevergiveup
RLLWNVPUNULCLYNPCLBW
$ python Decrypt.py caesar 7 RLLWNVPUNULCLYNPCLBW
keepgoingnevergiveup
```

## 分工

* `Encrypt` B10615013 四資工三甲 李聿鎧 
* `Decrypt` B10615043 四資工三甲 何嘉峻 

## Code Explain

### Caesar cipher

#### Encrypt
``` python
def caesar(key, plaintext):
    ciphertext = ""
    for c in plaintext:
        ciphertext += chr((ord(c) - 97 + int(key)) % 26 + 97)  # 做Caesar位移，字元若超過Z則回到A
    return ciphertext
```

#### Decrypt
``` python
class DecryptMethod: #父類別（預處理字串等）
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
            # p = (c - k) mod 26
            self.plaintext += (chr((ord(i) - 65 - int(self.key)) % 26 + 65))
        self.plaintext = self.plaintext.lower()
        return self.plaintext
```

### Playfair cipher

#### Encrypt
``` python
# Tool Function: 傳入字元，回傳字元keytable的位置
def findchar(c, keytable):
    if c == "j":
        c = "i"
    for i in range(5):
        for j in range(5):
            if (c == keytable[i][j]):
                return [i, j]


def playfair(key, plaintext): 
    ciphertext = ""

    # --keytable(不使用 "j")--
    key = str(key).replace('j', 'i')  # 把所有的"j"取代成"i"
    keylist = {}  # 利用Dictionary的key特性，去除重複字元且保留順序
    keytable = [[] for i in range(5)]
    for c in key:
        keylist[c] = 0  # 將密鑰依序加入Dictionary的key
    for i in range(26):
        if i != 9:  # 不使用"j"
            keylist[chr(i + 97)] = 0  # 將a-z依序加入Dictionary的key(除了"j")
    keylist = list(keylist.keys())  # 將keylist的key轉為純list
    for i in range(5):
        for j in range(5):
            keytable[i].append(keylist[j + i * 5])  # 將list依序放進5*5的list中

    # --makepair--
    textlist = []
    plaintext_temp = plaintext
    while len(plaintext_temp) > 0:  # 把list中字元依照規則，字元兩兩一組加入textlist
        temppair = ""
        temppair += plaintext_temp[0]  # 把list第0個字元加到temp
        plaintext_temp = plaintext_temp[1:]  # 移除list第0個字元
        if len(plaintext_temp) == 0:  # 如果list沒字元了，就把"x"加入temp
            temppair += "x"
        elif plaintext_temp[0] == temppair[0]:  # 如果list第0個字元跟textlist第0字元重複，就把"x"加入temp
            temppair += "x"
        else:  
            temppair += plaintext_temp[0]  # 把list第0個字元加到temp
            plaintext_temp = plaintext_temp[1:]  # 移除list第0個字元
        textlist.append(temppair)  

    # --encrypt--
    while len(textlist) > 0:  
        a = findchar(textlist[0][0], keytable)  # 在keytable尋找該字元在哪個位置
        b = findchar(textlist[0][1], keytable)  # 在keytable尋找該字元在哪個位置
        if a[0] == b[0]:  # 若兩個字母在同一橫列，取這兩個字母右方的字母
            ciphertext += keytable[a[0]][(a[1] + 1) % 5] \
                          + keytable[b[0]][(b[1] + 1) % 5]
        elif a[1] == b[1]:  # 若兩個字母在同一直行，取這兩個字母下方的字母
            ciphertext += keytable[(a[0] + 1) % 5][a[1]] \
                          + keytable[(b[0] + 1) % 5][b[1]]
        else:  # 若兩個字母不在同一直行或同一橫列，在矩陣中找出另外兩個字母，使這四個字母成為一個長方形的四個角
            ciphertext += keytable[a[0]][b[1]] \
                          + keytable[b[0]][a[1]]
        textlist = textlist[1:]
    return ciphertext
```

#### Decrypt
``` python
class Playfair(DecryptMethod):
    def __init__(self, key, ciphertext): # 預處理 key, 建 key table, 將 ciphertext 分成兩個字一組
        super().__init__(key, ciphertext)
        self.key = self.key.upper()
        self.key_table = self.make_key_table()
        self.cipher_group = self.make_cipher_group()

    def decrypt(self):
        for group in self.cipher_group:
            # 先找到兩字的位置
            pos0 = self.get_pos(group[0])
            pos1 = self.get_pos(group[1])

            if pos0[0] == pos1[0]:  # 同一個 row 
                self.plaintext += self.get_letter(pos0[0], (pos0[1] - 1) % 5)
                self.plaintext += self.get_letter(pos1[0], (pos1[1] - 1) % 5)
            elif pos0[1] == pos1[1]:  # 同一個 col
                self.plaintext += self.get_letter((pos0[0] - 1) % 5, pos0[1])
                self.plaintext += self.get_letter((pos1[0] - 1) % 5, pos1[1])
            else: # 不同 col & row
                self.plaintext += self.get_letter(pos0[0], pos1[1])
                self.plaintext += self.get_letter(pos1[0], pos0[1])
        self.plaintext = self.plaintext.lower()
        return self.plaintext

    def make_key_table(self):
        letter = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        key = self.key.replace('J', 'I') # 如果 key 裡面有 'J' 先替換成 'I'

        row = 0 # 紀錄 table 建到第幾列
        col = 0 # 紀錄 table 建到第幾行
        key_table = [[]]
        
        # 先把 key 提入 key_table
        for i in key:
            if letter.find(i, 0) != -1:
                if col == 5: # 判斷換行
                    col = 0
                    row += 1
                    key_table.append([])
                # 填入 key_table 後，從 key 和 letter 中移除，避免重複
                key_table[row].append(i)
                col += 1
                key = key.replace(i, '')
                letter = letter.replace(i, '')
                
        # 剩下沒填過的字母依序填入 key_table
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
        ciphertext = self.ciphertext.replace('J', 'I') # 如果 ciphertext 裡面有 'J' 先替換成 'I'
        append = True # 判斷是否 append []
        table_index = -1
        cipher_group = []

        # 填入兩兩一組
        for i in range(len(ciphertext)):
            if append:
                cipher_group.append([])
                table_index += 1
                append = False
            else:
                append = True
            cipher_group[table_index].append(ciphertext[i])
        return cipher_group
        
    # Tool Function：傳入欲尋找字母，回傳字母在 key_table 的位置
    def get_pos(self, letter):
        for row in self.key_table:
            if letter in row:
                return [self.key_table.index(row), row.index(letter)]
                
    # Tool Function：傳入欲尋找位置，回傳在 key_table 的位置中的字母
    def get_letter(self, row, col):
        return self.key_table[row][col]
```

### Vernam proposed the autokey system

#### Encrypt
``` python
def vernam(key, plaintext):  # proposed the autokey system
    ciphertext = ""
    key = str(key).lower() + plaintext  # 把plaintext加在key後面(autokey system)
    for i in range(len(plaintext)):
        ciphertext += chr(((ord(plaintext[i]) - 97) ^ (ord(key[i]) - 97)) + 65)  # 依序把plaintext跟key做XOR
    return ciphertext
```

#### Decrypt
``` python
class Vernam(DecryptMethod):
    def __init__(self, key, ciphertext): # 預處理 key
        super().__init__(key, ciphertext)
        self.key = self.key.upper()

    def decrypt(self):
        key = self.key
        ciphertext = self.ciphertext
        # 以一開始的 key XOR 出後面的部分字串，再以解出來的部份字串為新的 key，繼續往後 XOR 直到ciphertext 全 XOR 完
        while len(ciphertext) != 0:
            key = self.vernam_xor(key, ciphertext[:len(key):])
            ciphertext = ciphertext[len(key)::]
            self.plaintext += key
        self.plaintext = self.plaintext.lower()
        return self.plaintext
        
    # Tool Function: 將兩字串做 XOR 後回傳結果
    def vernam_xor(self, part_key, part_ciphertext):
        plaintext = ''
        for i in range(len(part_ciphertext)):
            plaintext += chr(((ord(part_ciphertext[i]) - 65) ^ (ord(part_key[i]) - 65)) + 65)
        return plaintext

```

### Row transposition

#### Encrypt
``` python
def row(key, plaintext):
    ciphertext = ""
    key = int(key)
    keylist = []
    while key > 0:
        keylist.insert(0, key % 10)  # 把Row number依序加到keylist
        key //= 10
    keylen = len(keylist)
    textlen = len(plaintext)
    rowtable = {}
    for i in keylist:
        rowtable[i] = [] # 依照keylist的號碼建立key
    for i in range(textlen):
        rowtable[int(list(rowtable.keys())[i % keylen])].append(plaintext[i])  # 依序把每個字元依照rowtable之key產生先後順序(非key的大小順序)加入
    for i in range(keylen):
        ciphertext += "".join(rowtable[i + 1])  # 依照rowtable的key由小到大輸出value
    return ciphertext
```

#### Decrypt
``` python
class RowTransposition(DecryptMethod):
    def __init__(self, key, ciphertext): # 預先計算 table 會有幾個 row 以及判斷最後一個 row 是否全滿
        super().__init__(key, ciphertext)
        self.row = 0 # 紀錄有幾個 row
        self.table = self.make_table() # 建好空的表個
        self.extend = len(self.ciphertext) % len(self.key) # 紀錄最後一個 row 會有幾個字

    def decrypt(self):
        ciphertext = self.ciphertext
        # 填表
        for i in range(len(self.key)):
            index = self.key.find(str(i + 1)) # 找到 要對應表格 col 的位置
            
            # 如果最後一行不是全滿的情況，要用對應 col 的位置（index）判斷是否需要填入最後一行
            times = self.row # 要填入幾個 row 
            if self.extend != 0: 
                if index >= self.extend:
                    times -= 1
                    
            # 以 col 直向填入表格
            for j in range(times):
                self.table[j][index] = ciphertext[0]
                ciphertext = ciphertext[1::]
                
        # 以 row 橫向還原 plaintext
        for i in self.table:
            for j in i:
                self.plaintext += j
        self.plaintext = self.plaintext.lower()
        return self.plaintext

    def make_table(self):
        # 如果餘數為0表示不需要多加一行
        if len(self.ciphertext) % len(self.key) == 0:
            self.row = int(len(self.ciphertext) / len(self.key))
        else:
            self.row = int(len(self.ciphertext) / len(self.key)) + 1
        
        # 建空的表格 row * len(key)
        table = []
        for i in range(self.row):
            table.append([])
            for j in range(len(self.key)):
                table[i].append('')
        return table
```

### Rail fence cipher

#### Encrypt
``` python
def rail_fence(key, plaintext):
    ciphertext = ""
    key = int(key) - 1
    index = -1
    add = 1  # 方向由0至n
    railtable = [[] for i in range(key)]
    for i in range(len(plaintext)):  # 依序由0至n至0..，依此類推
        index += add
        railtable[index].append(plaintext[i])  # 把值加進指定的Row
        if index == key:
            add = -1  # 方向由n至0
        elif index == 0:
            add = 1  # 方向由0至n
    for j in range(key):
        ciphertext += "".join(railtable[j])  # 依序將每個row輸出
    return ciphertext
```

#### Decrypt
``` python
class RailFence(DecryptMethod):
    def __init__(self, key, ciphertext): #預處理 key，建空 Fence
        super().__init__(key, ciphertext)
        self.key = int(self.key)
        self.fence = self.make_fence()

    def decrypt(self):
        ciphertext = self.ciphertext
        # 先將 ciphertext 填回去之前 fence 中填入的字元
        for part_fence in self.fence:
            while '-' in part_fence:
                index = part_fence.index('-')
                part_fence[index] = ciphertext[0]
                ciphertext = ciphertext[1::]
                
        # 將填好的 Fence 還原 plaintext
        descending = 1 # 紀錄Fence方向 ↘ / ↗
        index = 0
        for i in range(len(self.ciphertext)):
            for j in range(self.key):
                if j == index:
                    self.plaintext += self.fence[index][i]
            # 按照方向更換 row index
            index += descending
            if index == (self.key - 1):
                descending = -1
            elif index == 0:
                descending = 1
        self.plaintext = self.plaintext.lower()
        return self.plaintext

    # 先按照 ciphertext 長度做出相同長度的 Fence，先固定填入某個字元
    def make_fence(self):
        fence = []
        for i in range(self.key):
            fence.append([])
        descending = 1 # 紀錄Fence方向 ↘ / ↗
        index = 0
        for i in range(len(self.ciphertext)):
            for j in range(self.key):
                if j == index:
                    fence[j].append('-')
                else:
                    fence[j].append('')
            index += descending
            if index == (self.key - 1):
                descending = -1
            elif index == 0:
                descending = 1
        return fence
```
