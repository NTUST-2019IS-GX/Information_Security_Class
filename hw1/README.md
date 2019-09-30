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