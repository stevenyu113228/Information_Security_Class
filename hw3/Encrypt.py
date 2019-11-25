from sys import argv
from Crypto.Cipher import AES
import random


def ecb_encrypt(key,in_file_name,out_file_name):
    f_i = open(in_file_name,'rb').read()

    counter = 0
    counter1 = 0
    for i in f_i:
        counter1 += 1
        if i == 0x0a:
            counter += 1
        if counter == 3:
            break

    data = f_i[counter1:]
    padd_len = 16 - (len(data)%16)
    for i in range(padd_len):
        data += bytes([0])

    data_list = [data[i:i+16] for i in range(0, len(data), 16)]

    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext_list = [] 

    for i in data_list:
        ciphertext_list.append(cipher.encrypt(i))

    ciphertext = b''
    for i in ciphertext_list:
        ciphertext += i

    out = f_i[:counter1]+ciphertext
    with open(out_file_name,'wb') as f_o:
        f_o.write(out)

def cbc_encrypt(key,in_file_name,out_file_name):
    iv = input("Please input IV (0x...):")
    iv = int(iv[2:],16).to_bytes(16, byteorder="little")
    f_i = open(in_file_name,'rb').read()
    counter = 0
    counter1 = 0
    for i in f_i:
        counter1 += 1
        if i == 0x0a:
            counter += 1
        if counter == 3:
            break

    # header = f_i[:counter1].decode(encoding = 'ascii').split('\n')
    # l = int(header[1].split(' ')[0])
    # w = int(header[1].split(' ')[1])

    data = f_i[counter1:]
    padd_len = 16 - (len(data)%16)
    for i in range(padd_len):
        data += bytes([0])

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

    out = f_i[:counter1]+ciphertext
    with open(out_file_name,'wb') as f_o:
        f_o.write(out)



def cool_encrypt(key,in_file_name,out_file_name):
    iv_s = input("Please input IV (0x...):")
    iv = int(iv_s[2:],16).to_bytes(16, byteorder="little")
    f_i = open(in_file_name,'rb').read()
    counter = 0
    counter1 = 0
    for i in f_i:
        counter1 += 1
        if i == 0x0a:
            counter += 1
        if counter == 3:
            break

    data = f_i[counter1:]
    padd_len = 16 - (len(data)%16)
    for i in range(padd_len):
        data += bytes([0])

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

    out = f_i[:counter1]+ciphertext
    with open(out_file_name,'wb') as f_o:
        f_o.write(out)


if __name__ == '__main__':
    key = int(argv[2][2:],16).to_bytes(16, byteorder="little")
    in_file_name = argv[3]
    out_file_name = argv[4]

    if argv[1] == 'ECB':
        ecb_encrypt(key,in_file_name,out_file_name)
    elif argv[1] == 'CBC':
        cbc_encrypt(key,in_file_name,out_file_name)
    elif argv[1] == 'COOL':
        cool_encrypt(key,in_file_name,out_file_name)