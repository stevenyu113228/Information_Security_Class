import sys
import math
def caesar(key,ciphertext):
    key = int(key)
    b=[]
    plaintext=''
    for i in ciphertext:
        afterminus=ord(i)-key
        #加密是位移key,現在減回來
        if(afterminus<65):
            a=afterminus+26
            b.append(a)
            #把減超過的加回來
        else:
            b.append(afterminus)

    for i in b:
        plaintext += chr(i)
    print (plaintext.lower())
    #用小寫印出來


def playfair(key, ciphertext):
    # 建立空表格
    table = list()

    # 準備一個A到Z的LIST
    a_z = [chr(65 + i) for i in range(0, 26)]

    # 刪掉J
    a_z.remove('J')

    # 清除重複的key
    new_key = []
    for i in key:
        if i not in new_key:
            new_key.append(i)

    # 把密碼先放進去表格裡
    for i in new_key:
        table.append(i)
        # 把放進去的從A至Z的表格中刪除
        a_z.remove(i)

    # 把剩下的A到Z字母放進表格
    for i in a_z:
        table.append(i)
    # table建立完成

    # 兩兩一組，重複的補X
    cipher_text_addx = list(ciphertext)

    for i in range(0, len(cipher_text_addx) - 1, 2):
        # 如果在同一個row
        # +1是因為表格從1開始算比較直覺
        if (table.index(cipher_text_addx[i]) // 5 + 1) == \
                (table.index(cipher_text_addx[i + 1]) // 5 + 1):
            # 如果左半邊那個字在表格最左邊
            if (table.index(cipher_text_addx[i])) % 5 == 0:
                cipher_text_addx[i] = table[table.index(cipher_text_addx[i]) + 4]
            else:
                cipher_text_addx[i] = table[table.index(cipher_text_addx[i]) - 1]

            # 如果右半邊那個字在表格最左邊
            if (table.index(cipher_text_addx[i + 1])) % 5 == 0:
                print("AA")
                cipher_text_addx[i + 1] = table[table.index(cipher_text_addx[i + 1]) + 4]
            else:
                cipher_text_addx[i + 1] = table[table.index(cipher_text_addx[i + 1]) - 1]


        # 如果在同一個column
        elif (table.index(cipher_text_addx[i]) + 1) % 5 == \
                (table.index(cipher_text_addx[i + 1]) + 1) % 5:
            # 如果左半邊的字在表格最上面
            if table.index(cipher_text_addx[i]) + 1 < 5:
                cipher_text_addx[i] = table[table.index(cipher_text_addx[i]) + 20]
            else:
                cipher_text_addx[i] = table[table.index(cipher_text_addx[i]) - 5]

            if table.index(cipher_text_addx[i]) + 1 < 5:
                cipher_text_addx[i + 1] = table[table.index(cipher_text_addx[i + 1]) + 20]
            else:
                cipher_text_addx[i + 1] = table[table.index(cipher_text_addx[i + 1]) - 5]

        # 如果不在同一個row也不在同一個column
        # 使之成為長方形的四個角(替換成橫的)
        else:
            a = table.index(cipher_text_addx[i])
            b = table.index(cipher_text_addx[i + 1])
            cipher_text_addx[i] = table[a - a % 5 + b % 5]
            cipher_text_addx[i + 1] = table[b - b % 5 + a % 5]
            # pass

    print(''.join(cipher_text_addx).lower())
    # 把結果印出來

def vernam(key,ciphertext):
    b=[]
    k=[]
    plaintext=''
    for i in ciphertext:
        b.append(ord(i)-ord("A"))

    for i in key:
        k.append(ord(i)-ord("A"))
    #因為等等要XOR所以要換成0~25
    for i in range(len(b)):
        afterxor= b[i] ^ k[i % len(k)]
        #再XOR一次就回回到XOR前
        character=chr(afterxor+ord('a'))
        plaintext+= character

    print(plaintext)
    #把結果印出來


def row(key, ciphertext):
    length = math.ceil(len(ciphertext) / len(key))
    # 除完之後無條件進位就是欄數

    k = len(key) - len(ciphertext) % len(key)
    # print(k)
    ciphertext = list(ciphertext)

    for i in range(k):
        if i == 0:
            ciphertext.append("1")
        else:
            ciphertext.insert(len(ciphertext) - 3 * i, "1")
    # 用1補滿缺的字

    # print(ciphertext)
    group = []
    for i in range(0, len(ciphertext), length):
        group.append(ciphertext[i:i + length])

        # 取出同行的,每length個一組

    key_list = []
    plaintext = ''
    for i in key:
        key_list.append(int(i))
    # 把key值放到keylist並轉成數字
    for j in range(length):
        for i in key_list:
            plaintext += group[i - 1][j]

    plaintext = plaintext.replace("1", "")
    # 把填補用的1給刪除掉

    print(plaintext.lower())
    # 把結果用小寫印出來

def rail_fence(key,ciphertext):
    key=int(key)
    fence = [[] for i in range(key)]
    rail  = 0
    variable   = 1

    for i in ciphertext:
        fence[rail].append(i)
        rail += variable
        #一開始往右下增加

        if rail == key-1 or rail == 0:
            variable = -variable
        #如果撞到邊的話讓他往右上加(行數遞減)
    #fence抓住那些該在哪一行


    rFence = [[] for i in range(key)]

    i = 0
    length= len(ciphertext)
    ciphertext = list(ciphertext)
    for r in fence:
        for j in range(len(r)):
            rFence[i].append(ciphertext[0])
            #print(rFence)
            ciphertext.remove(ciphertext[0])
        i += 1
    #抓出哪些在哪一行

    rail = 0
    var  = 1
    plaintext = ''
    for i in range(length):
        plaintext += rFence[rail][0]
        rFence[rail].remove(rFence[rail][0])
        rail += var

        if rail == key-1 or rail == 0:
            var = -var
    print(plaintext.lower())
    #將全部排進r字串,變回原來銘文

def main():
    inp = sys.argv
    cipher = ['caesar','playfair','vernam','row','rail_fence']
    if len(inp) != 4 or inp[1] not in cipher:
        print("Input arguments error!")
    else:
        if inp[1] == cipher[0]:
            caesar(inp[2],inp[3])

        elif inp[1] == cipher[1]:
            playfair(inp[2],inp[3])

        elif inp[1] == cipher[2]:
            vernam(inp[2],inp[3])

        elif inp[1] == cipher[3]:
            row(inp[2],inp[3])

        elif inp[1] == cipher[4]:
            rail_fence(inp[2],inp[3])


if __name__ == '__main__':
    main()