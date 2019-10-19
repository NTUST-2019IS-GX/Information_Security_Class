# HW2

Implement DES encryption and decryption (Please don’t call the existing DES library)

+ **Example**\
Plaintext= `0xabcdef0123456789`\
Key= `0xafafafafafafafaf`\
Ciphertext= `0x4C30FC30FB2B0BFF`


## 開發環境
+ **IDE:** PyCharm 2019.2
+ **Language:** Python 3.7

## I/O
+ Plaintext, Key, Ciphertext 皆為64bits的Hex，共16位英數字\
Ex: 0x0123456789abcdef, 0x0001650012fedcba
### Input
```
python ./EncryptDES.py {Key} {Plaintext}
python ./DecryptDES.py {Key} {Ciphertext}
```

### Output
```
{Plaintext} or {Ciphertext}
```

### Example
```
$ python ./EncryptDES.py 0xAFAFAFAFAFAFAFAF 0xabcdef0123456789
0x4C30FC30FB2B0BFF
$ python ./DecryptDES.py 0xAFAFAFAFAFAFAFAF 0x4C30FC30FB2B0BFF
0xabcdef0123456789

$ python ./EncryptDES.py 0x1259ACBD6544FCDA 0xabcdef0123456789
0xB82CB4CAE5C4371C
$ python ./DecryptDES.py 0x1259ACBD6544FCDA 0xB82CB4CAE5C4371C
0xabcdef0123456789
```

## 分工

* `Encrypt` B10615013 四資工三甲 李聿鎧 
* `Decrypt` B10615043 四資工三甲 何嘉峻 

## Code Explain

### Encrypt
``` python
# TODO
```

### Decrypt
``` python
# TODO
```
