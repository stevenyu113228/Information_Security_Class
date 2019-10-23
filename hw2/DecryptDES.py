import sys

# 題目要求的表格
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

SBOXES = {1:
              [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
               [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
               [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
               [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
               ],
          2:
              [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
               [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
               [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
               [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
               ],
          3:
              [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
               [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
               [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
               [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
               ],
          4:
              [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
               [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
               [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
               [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
               ],
          5:
              [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
               [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
               [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
               [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
               ],
          6:
              [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
               [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
               [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
               [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
               ],
          7:
              [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
               [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
               [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
               [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
               ],
          8:
              [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
               [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
               [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
               [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
               ]
          }

key_schedule = [0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def key_permutation(inp):
    ret = [0 for i in range(56)]  # 56個0空陣列
    for i in range(len(ret)):  # 跑56次
        ret[i] = inp[PC1[i] - 1]  # 因為python從第0格算，所以要減1
    return ret


def key2_permutation(inp):
    ret = [0 for i in range(48)]  # 48個0空陣列
    for i in range(len(ret)):  # 跑48次
        ret[i] = inp[PC2[i] - 1]  # 因為python從第0格算，所以要減1
    return ret


def E_expansion(inp):
    ret = [0 for i in range(48)]  # 48個0空陣列
    for i in range(len(ret)):  # 跑48次
        ret[i] = inp[E[i] - 1]  # 因為python從第0格算，所以要減1
    return ret


def P_permutation(inp):
    ret = [0 for i in range(32)]  # 32個0空陣列
    for i in range(len(ret)):  # 跑32次
        ret[i] = inp[P[i] - 1]  # 因為python從第0格算，所以要減1
    return ret


def final_permutation(inp):
    ret = [0 for i in range(64)]  # 64個0空陣列
    for i in range(len(ret)):  # 跑64次
        ret[i] = inp[IP_INV[i] - 1]  # 因為python從第0格算，所以要減1
    return ret


def key_rotate(key, bit):
    l_key = key[:28]  # 0~27(左半部的key)
    r_key = key[28:]  # 28~55(右半部的key)

    bit=-bit
    # rotate right
    l_key = l_key[bit:] + l_key[:bit]  # 看移幾格
    r_key = r_key[bit:] + r_key[:bit]
    return l_key, r_key  # 回傳左右key


def key_process(key_list):
    k = key_permutation(key_list)  # 先讓他從0開始放到陣列
    keys = []
    for i in range(16):
        l, r = key_rotate(k, key_schedule[i])  # 取得左右兩邊已經rotate的key
        k = l + r  # 組合回來
        keys.append(key2_permutation(k))  # 排列好從0開始後成為字串
    return keys


def f_function(R, key):
    R1 = E_expansion(R)
    R2 = []
    for i in range(len(R1)):
        R2.append(R1[i] ^ key[i])  # 把R1跟key XOR後的結果存到R2
    i = 1  # 待會從第一個SBOX開始
    R3 = []
    for k in range(0, 48, 6):  # 0,6,12,18,24,30,36,42(共8個SBOX)
        sbox = SBOXES[i]
        i += 1
        r = R2[k] * 2 + R2[k + 5]  # 取數字把二進位換成普通的10進位數字
        l = R2[k + 1] * 8 + R2[k + 2] * 4 + R2[k + 3] * 2 + R2[k + 4]  # 取數字把二進位換成普通的10進位數字
        # 補滿4位數
        R3_ = "{:0>4d}".format(int(str(bin(sbox[r][l]))[2:]))  # 把SBOX中r、l變成binary再變成string()

        R3_ = [int(i) for i in R3_]
        R3 += R3_

    ret = P_permutation(R3)  # 排列好從0開始去掉0b
    return ret


def init_permutation(inp):
    ret = [0 for i in range(64)]  # 建立64格空陣列
    for i in range(len(IP)):
        ret[i] = inp[IP[i] - 1]  # 因為python從第0格算，所以要減1
    return ret


def main(Key, Ciphertext):
    key = "{:0>64d}".format(int(str(bin(int(Key[2:], 16)))[2:]))
    key_list = [int(i) for i in key]  # 把key的每個值放成陣列

    Ciphertext = "{:0>64d}".format(int(str(bin(int(Ciphertext[2:], 16)))[2:]))
    Ciphertext_list = [int(i) for i in Ciphertext]  # 把Ciphertext的每個值放成陣列

    keys = key_process(key_list)  # 已經rotate的key
    Ciphertext = init_permutation(Ciphertext_list)  # 調整好位置的Ciphertext

    L_text = Ciphertext[:32]  # 左半部Ciphertext
    R_text = Ciphertext[32:]  # 右半部Ciphertext

    for i in range(16):  # 16rounds
        new_R_text = []
        t = f_function(R_text, keys[i])
        for j in range(32):
            new_R_text.append(L_text[j] ^ t[j])  # 新的R的每個bit=上個L^f(上個R,key)

        L_text = R_text  # 而L是上個R
        R_text = new_R_text

    Ciphertext = R_text + L_text  # 全部是右+左(因為最後一次還是換位置了)
    Ciphertext = final_permutation(Ciphertext)  # 調整位置陣列從0算起
    Ciphertext = [str(i) for i in Ciphertext]
    Ciphertext = ''.join(Ciphertext)
    Ciphertext = hex(int(Ciphertext, 2))  # 將銘文變成小寫

    print(Ciphertext)  # 輸出銘文


if __name__ == '__main__':
    inp = sys.argv
    Key = inp[1]
    Key= Key.lower()
    Ciphertext = inp[2]
    main(Key, Ciphertext)

