import random
from sys import argv
from Crypto.Cipher import AES

def ecb_decrypt(key,in_file_name,out_file_name):
    f_i = open(in_file_name,'rb').read()
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


def cbc_decrypt(key,in_file_name,out_file_name):
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
    header = f_i[:counter1].decode(encoding = 'ascii').split('\n')
    l = int(header[1].split(' ')[0])
    w = int(header[1].split(' ')[1])
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
    header = f_i[:counter1].decode(encoding = 'ascii').split('\n')
    l = int(header[1].split(' ')[0])
    w = int(header[1].split(' ')[1])
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

        

if __name__ == '__main__':
    key = int(argv[2][2:],16).to_bytes(16, byteorder="little")
    in_file_name = argv[3]
    out_file_name = argv[4]

    if argv[1] == 'ECB':
        ecb_decrypt(key,in_file_name,out_file_name)
    if argv[1] == 'CBC':
        cbc_decrypt(key,in_file_name,out_file_name)
    if argv[1] == 'COOL':
        cool_encrypt(key,in_file_name,out_file_name)