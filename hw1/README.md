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
# code here
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
# code here
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
# code here
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
# code here
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
# code here
```
