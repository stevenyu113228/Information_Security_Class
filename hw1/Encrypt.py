import sys
from math import ceil


def caesar(inp):
    key = inp[0]
    plaintext = inp[1]

    # 把輸入的值轉ascii並加上偏移量
    inp_str_offset = [ord(i)+int(key) for i in plaintext]

    # 把加過頭ㄉ(122=z)扣26回去 mod26 的功能
    inp_str_offset_mod = [(i if i<123 else i-26) for i in inp_str_offset]

    # 把list轉string並改大寫
    return ''.join([chr(i) for i in inp_str_offset_mod]).upper()


def playfair(inp):
    key = inp[0]
    plaintext = inp[1]

    # 建立空表格
    table = list()

    # 準備一個A到Z的LIST
    a_z = [chr(65+i) for i in range(0,26)]

    # 刪掉J
    a_z.remove('J')

    # 把J變成I 並換成大寫
    plaintext = plaintext.replace('j','i').upper()
    
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
    plaintext_addx = list(plaintext)
    for i in range(0,len(plaintext)-1,2):
        if plaintext[i] == plaintext[i+1]:
            plaintext_addx.insert(i+1,'X')

    # 長度是奇數的話，補X
    if len(plaintext_addx)%2 == 1:
        plaintext_addx.append('X')
    
    for i in range(0,len(plaintext_addx)-1,2):
        # 如果在同一個row
        # +1是因為表格從1開始算比較直覺
        if (table.index(plaintext_addx[i])//5 + 1) == \
            (table.index(plaintext_addx[i+1])//5 + 1):

            # 如果左半邊那個字在表格最右邊
            if (table.index(plaintext_addx[i]))%5 == 4:
                plaintext_addx[i] = table[table.index(plaintext_addx[i])-4]
            else:
                plaintext_addx[i] = table[table.index(plaintext_addx[i])+1]

            # 如果右半邊那個字在表格最右邊
            if (table.index(plaintext_addx[i+1]))%5 == 4:
                plaintext_addx[i+1] = table[table.index(plaintext_addx[i+1])-4]
            else:
                plaintext_addx[i+1] = table[table.index(plaintext_addx[i+1])+1]


        # 如果在同一個column
        elif (table.index(plaintext_addx[i])+1)%5 == \
            (table.index(plaintext_addx[i+1])+1)%5:
            # 如果左半邊的字在表格最下面
            if table.index(plaintext_addx[i])+1 > 20:
                plaintext_addx[i] = table[table.index(plaintext_addx[i])-20]
            else:
                plaintext_addx[i] = table[table.index(plaintext_addx[i])+5]

            if table.index(plaintext_addx[i])+1 > 20:
                plaintext_addx[i+1] = table[table.index(plaintext_addx[i+1])-20]
            else:
                plaintext_addx[i+1] = table[table.index(plaintext_addx[i+1])+5]

        # 如果不在同一個row也不在同一個column
        # 使之成為長方形的四個角(替換成橫的)
        else:
            a = table.index(plaintext_addx[i])
            b = table.index(plaintext_addx[i+1])
            plaintext_addx[i] = table[a-a%5+b%5]
            plaintext_addx[i+1] = table[b-b%5+a%5]
            # pass

    return ''.join(plaintext_addx)
    


def vernam(inp):
    key = inp[0]
    plaintext = inp[1]
    
    # plaintext轉數字(0~25)
    plaintext_list_num = [ord(i)-ord('a') for i in plaintext]

    # key轉數字(0~25)
    key_list_num = [ord(i)-ord('A') for i in key]
   
    cipher_text = []
    for i in range(len(plaintext_list_num)):
        cipher_text.append((plaintext_list_num[i]^key_list_num[i%len(key_list_num)]))

    return ''.join([chr(i+ord('A')) for i in cipher_text]).upper()

def row(inp):
    key = inp[0]
    plaintext = inp[1]

    key = [int(i) for i in key]
    
    max_key = max(key)
    cipher_text = ''

    # 依照row順序填寫
    k = []
    for i in range(1,len(key)+1):
        k.append(key.index(i))

    for i in k:
        for j in range(ceil(len(plaintext)/max_key)):
            cipher_text += plaintext[j*max_key+i] \
            if len(plaintext) > j*max_key+i else ''
            
    return cipher_text.upper()

def rail_fence(inp):
    key = int(inp[0])
    plaintext = inp[1]
    
    rail = ['' for i in range(key)]

    r = 0
    back = False
    for i in plaintext:
        rail[r] += i

        # 往回走(右上)
        if back:
            r -= 1
            if r == -1:
                r += 2
                back = False

        # 順著走(右下)
        else:
            r += 1
            if r == key:
                r -= 2
                back = True

    return ''.join(rail).upper()


def main():
    inp = sys.argv
    cipher = ['caesar','playfair','vernam','row','rail_fence']
    if len(inp) != 4 or inp[1] not in cipher:
        print("Input arguments error!")
    else:
        if inp[1] == cipher[0]:
            ans = caesar(inp[2:])

        elif inp[1] == cipher[1]:
            ans = playfair(inp[2:])

        elif inp[1] == cipher[2]:
            ans = vernam(inp[2:])

        elif inp[1] == cipher[3]:
            ans = row(inp[2:])

        elif inp[1] == cipher[4]:
            ans = rail_fence(inp[2:])

        print(ans)



if __name__ == '__main__':
    main()