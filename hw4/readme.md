# 資訊安全導論 HW4
> 四電機四甲 B10507004 游照臨
## 建置環境
- 作業系統：macOS Mojave 10.14.5
- 程式語言：Python 3.7.5  [Clang 11.0.0 (clang-1100.0.33.8)] on darwin
- 編輯環境：Visual Studio Code

## 操作方式
### 初始化
`python3 RSA.py init {長度}`
- 輸入
    - p跟q的長度bit數 e.g. 1024
- 輸出
    - p 使用16bit表示 0x...
    - q 使用16bit表示 0x...
    - n 使用16bit表示 0x...
    - e 固定為0x10010 = 65537
    - e 使用16bit表示 0x...

### 加密
`python3 RSA.py -e {plaintext} {n} {e}`
- 輸入
    - plaintext (Printable ASCII)
    - n 使用16bit表示 0x...
    - e 使用16bit表示 0x...

- 輸出
    - 加密結果 使用16bit表示 0x...

### 解密(普通方式)
`python3 RSA.py -d {ciphertext} {n} {d}`
- 輸入
    - ciphertext 使用16bit表示 0x...
    - n 使用16bit表示 0x...
    - d 使用16bit表示 0x...
- 輸出
    - 回傳解密結果為Printable ASCII

### 解密(CRT加速)
`python3 RSA.py -d {ciphertext} {p} {q} {d}`
- 輸入
    - ciphertext 使用16bit表示 0x...
    - p 使用16bit表示 0x...
    - q 使用16bit表示 0x...
    - d 使用16bit表示 0x...
- 輸出
    - 回傳解密結果為Printable ASCII
    
## 執行結果圖
### 初始化
![](https://i.imgur.com/cPwh6WC.jpg)

### 加密
![](https://i.imgur.com/q0v6q9R.jpg)

### 解密(普通方式)
![](https://i.imgur.com/77VZVOw.jpg)

### 解密(CRT加速)
![](https://i.imgur.com/qyre5H8.jpg)

## 程式碼解說
### phi函數
```python
def phi(p, q):
    return (p-1)*(q-1)
```
- 輸入p,q
- 回傳(p-1)(q-1)

### Square and Multiply
```python
def enc_dec(x, H, n):
    # use square and multiply
    # parm: (x,e,n) or (y,d,n)
    # return x^H mod n
    H = str(bin(H))[2:]
    y = 1
    for hi in H:  # Slide寫錯，要從h_t開始
        y = (y*y) % n
        if hi == '1':
            y = (y*x) % n
    return y
```
- 輸入x,H,n
- 使用Square and Multiply演算法計算出x^H^ mod n

### Mod Inv
```python
def mod_inv(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    _, x, _ = egcd(a, m)
    return x % m
```
- 輸入a,m
- 透過歐幾里得法取得乘法反元素

### Miller Rabin Test
```python
def miller_rabin_test(N, r=10):
    if N == 2:
        return True
    elif N % 2 == 0:
        return False

    m = N-1
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1

    m = int(m)

    for i in range(r):
        a = randint(2, N-1)
        b = enc_dec(a, m, N)
        if b != 1 and b != N-1:
            i = 1
            while i < k and b != (N-1):
                b = enc_dec(b, 2, N)
                if b == 1:
                    return False
                i = i + 1
            if b != N-1:
                return False
        return True
```
- 輸入數字N，回傳是否"有機會是質數"
- 預設會進行10次的test，以確保是否為質數

### Generate Prime
```python
def gen_prime(b):
    a = randint(2**b, 2**(b+1))
    while miller_rabin_test(a) == False:
        a = randint(2**b, 2**(b+1))
    return a
```
- 輸入bit數，透過Miller Rabin Test搭配Python內建的random函式庫取得大質數

### CRT Decrypt
```python
def crt_dec(y, p, q, d):
    dp = d % (p-1)
    dq = d % (q-1)
    q_inv = mod_inv(q, p)

    m1 = enc_dec(y, dp, p)
    m2 = enc_dec(y, dq, q)
    h = q_inv*(m1-m2) % p
    m = m2 + h
    return m
```
- 使用中國剩餘定理的方法，加速解密的速度
- 前提是需要多輸入p跟q

### 主程式
```python
if argv[1] == 'init':
    key_len = int(argv[2])
    e = 65537
    p = gen_prime(key_len)
    q = gen_prime(key_len)
    n = p*q
    ph = phi(p, q)
    d = mod_inv(e, ph)

    print('p = ', hex(p))
    print('q = ', hex(q))
    print('n = ', hex(n))
    print('e = ', hex(e))
    print('d = ', hex(d))
```
- 當參數為init時，讀取第2個參數為bit數
- 計算n,phi以及d
- 並print出結果

``` python
elif argv[1] == '-e':
    plaintext = argv[2]
    n = int(argv[3][2:], 16)
    e = int(argv[4][2:], 16)

    y = ''
    for i in plaintext:
        y += hex(enc_dec(ord(i), e, n))
    print(y)
```
- 當參數為e時，代表需要執行加密動作
- 先把n及e轉為int，並且依序把每個字元個別加密後輸出


```python
elif argv[1] == '-d':
    ciphertext = argv[2].split('0x')[1:]
    n = int(argv[3][2:], 16)
    d = int(argv[4][2:], 16)
    for i in ciphertext:
        i = int(i, 16)
        print(chr(enc_dec(i, d, n)), end='')
        
elif argv[1] == '-crt':
    ciphertext = argv[2].split('0x')[1:]
    p = int(argv[3][2:], 16)
    q = int(argv[4][2:], 16)
    d = int(argv[5][2:], 16)
    for i in ciphertext:
        i = int(i, 16)
        print(chr(crt_dec(i, p, q, d)), end='')
            
```
- 當參數為d時，代表需要進行解密動作
- 將不同字元先用0x分隔，轉為陣列
- 並且依序使用普通方式，或CRT加速方式解密



## 遇到困難與心得
在這次的Project中，我真的對於RSA有了進一步的了解。使用Square and Multiply的技巧可以快速的計算次方mod的結果，後來也查詢到其實python的pow功能，如果輸入第三個參數也可以達到同樣的效果，不過自己實作一次的感覺真的很棒。還有Miller Rabin Test搭配Random產生大質數。其中我遇到最大的問題是對於產生mod反元素的方式，原先我是單純透過while迴圈進行窮舉，發現效率非常低，後來才想到可以用最大公因數的解法！