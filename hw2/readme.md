# 資訊安全導論 HW2
> 四電機四甲 游照臨：Encrypt <br>
> 組員：四電資四 黃文怡：Decrypt

## 開發環境
- Mac OSX 10.14.5
- Python 3.7.3
- Visual Studio Code

## 運行結果
![](https://i.imgur.com/DpxUK6J.png)

## 程式簡介
### 主程式
```python
def main(Key, Plaintext):
    key = "{:0>64d}".format(int(str(bin(int(Key[2:], 16)))[2:]))
    key_list = [int(i) for i in key]

    plaintext = "{:0>64d}".format(int(str(bin(int(Plaintext[2:], 16)))[2:]))
    plaintext_list = [int(i) for i in plaintext]

    keys = key_process(key_list)
    text = init_permutation(plaintext_list)

    L_text = text[:32]
    R_text = text[32:]

    for i in range(16):
        new_R_text = []
        t = f_function(R_text,keys[i])
        for j in range(32):
            new_R_text.append(L_text[j]^t[j])

        L_text = R_text
        R_text = new_R_text
        
    text = R_text + L_text
    text = final_permutation(text)
    text = [str(i) for i in text]
    text = ''.join(text)
    text = hex(int(text,2)).upper().replace('X','x')
    
    print(text)
```
1. 透過python字串填補的方式將輸入補充至64bit
2. 產出16把key
3. 把text分成左右兩半 進入函數中
4. 執行16次運算
    - 右半部與key執行f函數
    - 使f函數與左半部xor
    - 將原本的右半部放置到左半部
    - 並將f函數與左半部運算結果放到右半

### 代換
```python
def key_permutation(inp):
    ret = [0 for i in range(56)]    
    for i in range(len(ret)):
        ret[i] = inp[PC1[i]-1]
    return ret

def key2_permutation(inp):
    ret = [0 for i in range(48)]    
    for i in range(len(ret)):
        ret[i] = inp[PC2[i]-1]
    return ret

def E_expansion(inp):
    ret = [0 for i in range(48)]
    for i in range(len(ret)):
        ret[i] = inp[E[i]-1]
    return ret    

def P_permutation(inp):
    ret = [0 for i in range(32)]
    for i in range(len(ret)):
        ret[i] = inp[P[i]-1]
    return ret    

def final_permutation(inp):
    ret = [0 for i in range(64)]
    for i in range(len(ret)):
        ret[i] = inp[IP_INV[i]-1]
    return ret    
```
各項的代換與擴增方式皆相同
1. 準備1個與輸出空間箱等大小的空list
2. 透過查表的方式將值依序寫入
    - 由於表格從1開始，python陣列從0開始，故-1
3. 回傳資料

### Key產生
```python
key_schedule = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def key_process(key_list):
    k = key_permutation(key_list)
    keys = []
    for i in range(16):
        l,r = key_rotate(k,key_schedule[i])
        k = l+r
        keys.append(key2_permutation(k))
    return keys 
```
1. 將key進行permutation
2. 依照key_schedule的定義執行左移2格或1格
3. 輸出

### F函數
```python
def f_function(R,key):
    R1 = E_expansion(R)
    R2 = []
    for i in range(len(R1)):
        R2.append(R1[i]^key[i])
    i = 1
    R3 = []
    for k in range(0,48,6):
        sbox = SBOXES[i]
        i+=1
        r = R2[k]*2 + R2[k+5]
        l = R2[k+1]*8 + R2[k+2]*4 + R2[k+3]*2 + R2[k+4] 
        # 補滿4位數
        R3_ = "{:0>4d}".format(int(str(bin(sbox[r][l]))[2:]))

        R3_ = [int(i) for i in R3_]
        R3 += R3_
        
    ret = P_permutation(R3)
    return ret
```
1. 將數值進行Expansion
2. 將數值與key進行xor
3. 每6個1組，依照指定的bit透過Sbox查表
4. 進行Permutation
5. 回傳

<br><br>

## 遇到困難與心得
### 遇到困難
程式寫起來非常的順利，我覺得途中沒有遇到任何重大的困難，這樣的話遇到的困難這一項要怎麼寫啊？我覺得這個Project遇到最大的困難，就是不知道這一格可以寫什麼東西......嗚嗚嗚嗚QQ。

### 心得
在這一次的作業中，讓我學會了DES的加密與解密方式。自己實作過一次之後才發現，原本看著流程圖的理解與真實的架構還是有些許的差距。透過程式實作後使我對於DES的加解密有了更清晰的認識，謝謝老師與助教在上課與作業上的協助！！