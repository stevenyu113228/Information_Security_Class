# 資訊安全導論 HW5
> 四電機四甲 B10507004 游照臨

## 分工
All：四電機四甲 B10507004 游照臨

## 建置環境
- 作業系統：macOS Mojave 10.14.5
- 程式語言：Python 3.7.5  [Clang 11.0.0 (clang-1100.0.33.8)] on darwin
- 編輯環境：Visual Studio Code

## 操作方式
### 產生key
- 指令：`python3 DSA.py -keygen {bit數}`
    - eg：`python3 DSA.py -keygen 160`
- 回傳K_pub,K_pri
    - eg:
        ```
        ----------K_pub----------
        p = 0x1000000000000013a71ea30b8a41f251f39cce9df14616236bd777fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffbe8f471637baf472d61844110663be6c6f813a8178f
        q = 0x8b75f38fa711695553b5e8f2e4cc113636ddae79
        alpha = 0x481f6ae5b37d7792dad4d612f5675865a1256df23f5b9f900edc265636a53aa85413187afec9b82e96a736e113c8a36e1afb6114205db680e9441923f36449e4276dc9533f446b624a596902dfbb9dd2511ec08fe78cd7e7943f9abf09726e8ff256337
        2930ab4bcdfe3483be9bde05fa12a5d59c7b87f83d3db53bbbf22af23
        beta = 0xa57d77b7bbf27dd3c95d267eb7f71f2a53da8c644f3df9fe602a3f7081ff6fc29244b613d0ebd0e3fc6ffbfa2317e0556591fdd0013ffe02d64548849d96d850777e114f8cc292c7f6fdcf884c2f92590d21655d242c2bcbfcb26ef551f7c74cbc6ba42f
        c6ee54092e133c5da28e2119330f8df4adf626cd9a7ffb833bc2612e
        ----------K_pri----------
        d = 0x750e6691e1c320f73f25a48d9a80a3bd553e4a94
        ```
### 簽署
- 指令：`python3 DSA.py -sign {message} {p} {q} {alpha} {beta} {d}`
    - eg：
        ```
        python3 DSA.py -sign meow 0x1000000000000013a71ea30b8a41f251f39cce9df14616236bd777ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffbe8f471637baf472d61844110663be6c6f813a8178f 0x8b75f38fa711695553b5e8f2e4cc113636ddae79 0x481f6ae5b37d7792dad4d612f5675865a1256df23f5b9f900edc265636a53aa85413187afec9b82e96a736e113c8a36e1afb6114205db680e9441923f36449e4276dc9533f446b624a596902dfbb9dd2511ec08fe78cd7e7943f9abf09726e8ff2563372930ab4bcdfe3483be9bde05fa12a5d59c7b87f83d3db53bbbf22af23 0xa57d77b7bbf27dd3c95d267eb7f71f2a53da8c644f3df9fe602a3f7081ff6fc29244b613d0ebd0e3fc6ffbfa2317e0556591fdd0013ffe02d64548849d96d850777e114f8cc292c7f6fdcf884c2f92590d21655d242c2bcbfcb26ef551f7c74cbc6ba42fc6ee54092e133c5da28e21193308df4adf626cd9a7ffb833bc2612e 0x750e6691e1c320f73f25a48d9a80a3bd553e4a94
        ```

- 回傳 r,s
    - eg:
        ```
        r =  0x6a77e66da10ffd1bc9ca4deab65ac0362c410651
        s =  0x18130f4e5a7aa2c0e88d94a120e169895d2b88a9
        ```
### 驗證
- 指令 `python3 DSA.py -verify {message} {r} {s} {p} {q} {alpha} {beta}`
    - eg:
        ```
        python3 DSA.py -verify meow 0x6a77e66da10ffd1bc9ca4deab65ac0362c410651 0x18130f4e5a7aa2c0e88d94a120e169895d2b88a9 0x1000000000000013a71ea30b8a41f251f39cce9df14616236bd777ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffbe8f471637baf472d61844110663be6c6f813a8178f 0x8b75f38fa711695553b5e8f2e4cc113636ddae79 0x481f6ae5b37d7792dad4d612f5675865a1256df23f5b9f900edc265636a53aa85413187afec9b82e96a736e113c8a36e1afb6114205db680e9441923f36449e4276dc9533f446b624a596902dfbb9dd2511ec08fe78cd7e7943f9abf09726e8ff2563372930ab4bcdfe3483be9bde05fa12a5d59c7b87f83d3db53bbbf22af23 0xa57d77b7bbf27dd3c95d267eb7f71f2a53da8c644f3df9fe602a3f7081ff6fc29244b613d0ebd0e3fc6ffbfa2317e0556591fdd0013ffe02d64548849d96d850777e114f8cc292c7f6fdcf884c2f92590d21655d242c2bcbfcb26ef551f7c74cbc6ba42fc6ee54092e133c5da28e2119330f8df4adf626cd9a7ffb833bc2612e
        ```
- 回傳
    - Valid 或 Invalid

## 執行過程截圖
### 產生key
![](https://i.imgur.com/OebA4kh.png)

### 簽署
![](https://i.imgur.com/HNXZUTf.png)

### 驗證
- 成功
    - ![](https://i.imgur.com/oYm7LvK.png)
- 失敗
    - ![](https://i.imgur.com/ZKmcho0.png)

## 程式碼解說
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


### Square and Multiply
```python
def square_and_multiply(x, H, n):
    # use square and multiply
    # parm: (x,e,n) or (y,d,n)
    # return x^H mod n
    H = str(bin(H))[2:]
    y = 1
    for hi in H:  
        y = (y*y) % n
        if hi == '1':
            y = (y*x) % n
    return y
```
- 輸入x,H,n
- 使用Square and Multiply演算法計算出x^H^ mod n

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

### Generate key
```python
def gen_key(k=160):
    def gen_p(q):
        t = int((2**1024) / q)
        while miller_rabin_test(t * q + 1) == False:
            t -= 1
        return t * q + 1

    def gen_alpha(p,q):
        h = randint(2,p-1)
        while square_and_multiply(h,(p-1)//q,p) == 1:
            h = randint(2,p-1)
        return square_and_multiply(h,(p-1)//q,p)

    q = gen_prime(k)
    p = gen_p(q)
    alpha = gen_alpha(p,q)
    d = randint(1,q)
    beta = square_and_multiply(alpha,d,p)

    print("----------K_pub----------")
    print("p =",hex(p))
    print("q =",hex(q))
    print("alpha =",hex(alpha))
    print("beta =",hex(beta))

    print("----------K_pri----------")
    print("d =",hex(d))

```
- 首先先產生一個160 bit的q
- 接下來產生1024bit的p，其中因為p-1要是q的倍數，且p為質數，因此透過迴圈的方式計算出t，以達成p=t\*q+1
- 產生alpha的方式為先產生一個亂數h，使h^((p-1)//q) mod p不為1的值即為alpha
- 產生beta的方式為alpha^d mod p
- 
### Sign
```python
def sign(x,p,q,alpha,beta,d):
    k_E = randint(1,q)

    r = square_and_multiply(alpha,k_E,p) % q

    m = hashlib.sha1()
    data = x.encode("ascii")
    m.update(data)
    sha_x = m.hexdigest()
    sha_x = int(sha_x,16)

    k_E_inv = mod_inv(k_E,q)
    s = (sha_x + d * r ) * k_E_inv % q

    print('r = ', hex(r))
    print('s = ', hex(s))
```
- 簽署的過程首先需要先產生一個亂數k_E
- 透過alpha^k_E mod q 產生 r
- 將輸入的x經過sha1編碼，並產生與q的反元素
- 計算s = (sha_x + d * r ) * k_E_inv % q

### Verify
```python
def verify(x,r,s,p,q,alpha,beta):
    w = mod_inv(s,q)

    m = hashlib.sha1()
    data = x.encode("ascii")
    m.update(data)
    sha_x = m.hexdigest()
    sha_x = int(sha_x,16)

    u1 = w * sha_x % q
    u2 = w * r % q

    alpha_u1 = square_and_multiply(alpha,u1,p)
    beta_u2 = square_and_multiply(beta,u2,p)

    v = (alpha_u1*beta_u2 % p) % q

    if r == v:
        print("Valid")
    else:
        print("Invalid")
```
- 計算w為s對於q的反元素
- 重新將x做一次sha1的hash
- 並且計算u1,u2 以求得v
- 其中運用了a\*b mod c  = (a mod c) \* (b mod c)) mod c以達到減少計算量的效果
- 最後驗證r是否等於v以判斷是否驗證成功

### 主程式
```python
if __name__ == '__main__':
    if argv[1] == '-keygen':
        key_len = int(argv[2])
        gen_key(key_len)

    elif argv[1] == '-sign':
        x = argv[2]
        p = int(argv[3][2:],16)
        q = int(argv[4][2:],16)
        alpha = int(argv[5][2:],16)
        beta = int(argv[6][2:],16)
        d = int(argv[7][2:],16)
        sign(x,p,q,alpha,beta,d)
    
    elif argv[1] == '-verify':
        x = argv[2]
        r = int(argv[3][2:],16)
        s = int(argv[4][2:],16)
        p = int(argv[5][2:],16)
        q = int(argv[6][2:],16)
        alpha = int(argv[7][2:],16)
        beta = int(argv[8][2:],16)
        verify(x,r,s,p,q,alpha,beta)
```
- 當參數為keygen時，將bit數傳入gen_key函數
- 當參數為sign時，依序將x,p,q,alpha,beta,d等參數送入sign函數
- 當參數為verify時，依序將x,r,s,p,q,alpha,beta等參數送入sign函數

## 遇到困難與心得
在這次的Project中，我大致的了解了DSA的加密流程與實作的方法，在非常多的地方我使用到了前一次Project中，RSA所使用到的函數。例如計算反元素、Square and Multiply、Miller Rabin Test等。

在實作這次的過程中，我遇到最大的困難是在產生key時，無論是網路上的過程或老師的slide上都是先產生p再產生q，因為p-1要是q的倍數。但是如果先產生了p之後，需要對p-1做因數分解才有辦法取得到q，而且bit數也不一定可以順利地符合160bit。因此後來我想到的解法是反過來，先產生一個固定的q，並且乘以一個長度足夠的亂數算出p，並且透過Miller Rabin Test判斷是否為質數。

這是最後一次作業了！謝謝教授與助教這個學期在課堂與作業上的協助！這一堂課讓我學習到了很多。我是電機系的學生，因此在選課的時候無法選下學期教授開的網路安全課程。希望下學期還有機會可以繼續加簽到教授的課！