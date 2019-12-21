# 資訊安全導論 HW3
## 簡介
### 工作分配
加密：四電機四甲 游照臨 B10507004<br>
解密：四電機四甲 游照臨 B10507004

因為我的組員二退了，所以我剩下一人一組

不過其實HW1跟HW2的加解密也都是我一個人寫的......

所以沒關係QAQ

### 執行環境
- 作業系統：macOS Mojave 10.14.5
- 程式語言：Python 3.7.5  [Clang 11.0.0 (clang-1100.0.33.8)] on darwin
- 編輯環境：Visual Studio Code

## img2ppm
```python
from PIL import Image
from sys import argv

if argv[1] == 'i2p':
    a = Image.open(argv[2])
    a.save(argv[2][:argv[2].find('.')]+'.ppm')
elif argv[1] == 'p2a':
    a = Image.open(argv[2])
    a.save(argv[2][:argv[2].find('.')]+'.jpg')  

```
![](https://i.imgur.com/5SxvDJ9.png)
首先我先透過python的PIL的轉檔功能，寫了一款可以直接透過指令方式將jpg、bmp等檔案轉換成ppm的格式。
<br>
<br>

## 功能展示
### Encrypt
指令：
`python3 Encrypt.py 加密方式 密碼 輸入檔名 輸出檔名`

(CBC、COOL等方式會需要在輸入完上述指令後按Enter再輸入IV)
![](https://i.imgur.com/NJqY5Xl.png)

#### ECB
```python
data_list = [data[i:i+16] for i in range(0, len(data), 16)]

cipher = AES.new(key, AES.MODE_ECB)
ciphertext_list = [] 

for i in data_list:
    ciphertext_list.append(cipher.encrypt(i))

ciphertext = b''
for i in ciphertext_list:
    ciphertext += i
```
將padding後的資料每16Bytes一組，並解依序送入加密

![](https://i.imgur.com/3jGycx6.png)

#### CBC
```python
data_list = [data[i:i+16] for i in range(0, len(data), 16)]

cipher = AES.new(key, AES.MODE_ECB)
ciphertext_list = [] 

for i in range(len(data_list)):
    if i == 0:
        xor = iv
    else:
        xor = ciphertext_list[i-1]

    enc_data_list = [bytes([a^b]) for a,b in zip(data_list[i],xor)]
    enc_data = b''
    for i in enc_data_list:
        enc_data += i

    ciphertext_list.append(cipher.encrypt(enc_data))

ciphertext = b''
for i in ciphertext_list:
    ciphertext += i
```
將padding後的資料每16Bytes一組，總共需要進行len(data_list)次的xor。
其中，第0次需要xor的對象為iv，而之後則為前一次加密後的結果

![](https://i.imgur.com/NhOt9hw.jpg)

#### COOL
```python
data_list = [data[i:i+16] for i in range(0, len(data), 16)]

cipher = AES.new(key, AES.MODE_ECB)
ciphertext_list = [] 

for i in range(len(data_list)):
    enc_data_list = [bytes([a^b]) for a,b in zip(data_list[i],iv)]
    enc_data = b''
    for i in enc_data_list:
        enc_data += i

    ciphertext_list.append(cipher.encrypt(enc_data))

random.seed(int(iv_s[2:],16))
s = random.sample(range(len(data_list)), len(data_list))

ciphertext_list1 = ciphertext_list
ciphertext_list = ['' for i in range(len(data_list))]
for i in range(len(s)):
    ciphertext_list[i] = ciphertext_list1[s[i]]

ciphertext = b''
for i in ciphertext_list:
    ciphertext += i
```
自行設計的加密方式，與ECB類似，但每個block加密前都會先進行一次xor iv的動作。
單純僅作上述方法會類似ECB，保留圖案的輪廓，因此我採用Permutation的方式。先將python的random seed設定為iv之值，產生一個不重複的亂數序列，並且透過序列數值的方式進行重新排列，以達到不保有輪廓的效果。

![](https://i.imgur.com/j07IzhT.png)


### Decrypt
`python3 Decrypt.py 加密方式 密碼 輸入檔名 輸出檔名`

(CBC、COOL等方式會需要在輸入完上述指令後按Enter再輸入IV)
![](https://i.imgur.com/2x1XHml.png)

#### ECB
```python
data = f_i[counter1:]

cipher = AES.new(key, AES.MODE_ECB)
data_list = [data[i:i+16] for i in range(0, len(data), 16)]
plaintext_list = [] 
for i in data_list:
    plaintext_list.append(cipher.decrypt(i))

plaintext = b''
for i in plaintext_list:
    plaintext += i

padd_len = 16 - ((l*w*3)%16)
plaintext = plaintext[:-padd_len]
dec_data = f_i[:counter1] + plaintext

with open(out_file_name,'wb') as f_o:
    f_o.write(dec_data)
```
尋找至圖片的資料區域後，拆分為16Bytes為一組的Block，進行解密。並將先前padding的內容刪除。

![](https://i.imgur.com/4ljTMg6.png)

#### CBC
```python
data = f_i[counter1:]

cipher = AES.new(key, AES.MODE_ECB)
data_list = [data[i:i+16] for i in range(0, len(data), 16)]
plaintext_list = [] 

for i in range(len(data_list)):
    if i == 0:
        xor = iv
    else:
        xor = data_list[i-1]
    dec = cipher.decrypt(data_list[i])

    dec_data_list = [bytes([a^b]) for a,b in zip(dec,xor)]
    dec_data = b''
    for i in dec_data_list:
        dec_data += i
    plaintext_list.append(dec_data)



plaintext = b''
for i in plaintext_list:
    plaintext += i

padd_len = 16 - ((l*w*3)%16)
plaintext = plaintext[:-padd_len]
dec_data = f_i[:counter1] + plaintext

with open(out_file_name,'wb') as f_o:
    f_o.write(dec_data)
```
將資料以16Bytes為一組，區分為Block後，進行解密。解密完成後，第0次需要xor的對象為iv，後面則為先前加密後的結果。

![](https://i.imgur.com/IrrF9pr.jpg)

#### COOL
```python
data = f_i[counter1:]

cipher = AES.new(key, AES.MODE_ECB)
data_list = [data[i:i+16] for i in range(0, len(data), 16)]
plaintext_list = [] 

for i in range(len(data_list)):
    dec = cipher.decrypt(data_list[i])
    dec_data_list = [bytes([a^b]) for a,b in zip(dec,iv)]
    dec_data = b''
    for i in dec_data_list:
        dec_data += i
    plaintext_list.append(dec_data)

random.seed(int(iv_s[2:],16))
s = random.sample(range(len(data_list)), len(data_list))

plaintext_list1 = plaintext_list
plaintext_list = ['' for i in range(len(data_list))]
for i in range(len(s)):
    plaintext_list[s[i]] = plaintext_list1[i]

plaintext = b''
for i in plaintext_list:
    plaintext += i

padd_len = 16 - ((l*w*3)%16)
plaintext = plaintext[:-padd_len]
dec_data = f_i[:counter1] + plaintext

with open(out_file_name,'wb') as f_o:
    f_o.write(dec_data)
```
將資料區分Block後進行解密，解密完後分別與iv進行xor(因為xor兩次視為不變)，並且將資料組合起來。由於提供了與加密相同的iv，因此設定為Random seed的話，產生出來的亂數會與先前相同，因此可以做反向的Permutation，將資料物歸原位。

![](https://i.imgur.com/Fyo8lG0.png)

## PPM
### Data type

在一開始查看了Wiki後，發現還是不太了解，而送入的圖片也因為過大而不方便觀察。
![](https://i.imgur.com/KSHJ98G.png)

因此我透過Photoshop自行設計了一個2x2的圖片檔案，並且轉換為ppm格式以方便觀察。
![](https://i.imgur.com/iOvvTFg.png)
![](https://i.imgur.com/3YCM9eG.png)
可以觀察出
- P6代表PPM格式
- 第一個0x0A後面代表的是長寬
- 第二個0x0A後面代表的是色彩深度
- 第三個0x0A後為資料，資料為RGB照順序的一個串列

因此寫入資料前，需要備份第三個0x0A的資料，以確保檔案標頭不會被影響。

### Padding
由於資料部份不一定會是AES支援的16Bytes，因此需要進行Padding以填充滿。我的執行方式是透過補0x00的方式將資料湊滿16Bytes
```python
data = f_i[counter1:]
padd_len = 16 - (len(data)%16)
for i in range(padd_len):
    data += bytes([0])
```
根據實驗表示，以MAC OS內建的圖片瀏覽器開啟Padding後的圖片，會自動忽略最後面Padding的資料，因此不會影響到。

解密時，可以透過讀取檔案標頭的方式，確認原始的長寬，並且計算出先前Padding出來的資料，再進行刪除。
```python
counter = 0
counter1 = 0
for i in f_i:
    counter1 += 1
    if i == 0x0a:
        counter += 1
    if counter == 3:
        break
header = f_i[:counter1].decode(encoding = 'ascii').split('\n')
l = int(header[1].split(' ')[0])
w = int(header[1].split(' ')[1])
data = f_i[counter1:]
#-----
padd_len = 16 - ((l*w*3)%16)
plaintext = plaintext[:-padd_len]
dec_data = f_i[:counter1] + plaintext
```

## 遇到困難與心得
這一次的作業相較於之前都簡單了許多，讓我對於區塊加密的方式也有了更深的認識。困難方面，剛開始觀察助教的投影片，發現到hex的101 editor是需要付費版的，因此我另外尋找，改用了0xED。

對於檔案格式而言，先前我對於ppm格式完全不了解，因此也透過如上所述，使用Photoshop自行產生了一張2x2px的圖片，分別是RGB與白色，方便觀察，就對於檔案格式有了一目了然的了解。

另外由於我的組員已經二退了，因此這一次的作業無論加密與解密都是我一個人完成的，相較於他人可能花費的時間會更多一點點。想請問助教，這堂課的Project有需要一定要兩個人嗎？因為我是電機系的學生，算是外系，與資工系同學也都不熟，請問接下來的作業我可以一個人獨立完成嗎？(我覺得我應該是可以Handle)

謝謝教授與助教！！