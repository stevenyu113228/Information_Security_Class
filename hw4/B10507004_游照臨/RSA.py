from random import randint
from sys import argv


def phi(p, q):
    return (p-1)*(q-1)


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


def mod_inv(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    _, x, _ = egcd(a, m)
    return x % m


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


def gen_prime(b):
    a = randint(2**b, 2**(b+1))
    while miller_rabin_test(a) == False:
        a = randint(2**b, 2**(b+1))
    return a


def crt_dec(y, p, q, d):
    dp = d % (p-1)
    dq = d % (q-1)
    q_inv = mod_inv(q, p)

    m1 = enc_dec(y, dp, p)
    m2 = enc_dec(y, dq, q)
    h = q_inv*(m1-m2) % p
    m = m2 + h
    return m


if __name__ == '__main__':
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

    elif argv[1] == '-e':
        plaintext = argv[2]
        n = int(argv[3][2:], 16)
        e = int(argv[4][2:], 16)

        y = ''
        for i in plaintext:
            y += hex(enc_dec(ord(i), e, n))
        print(y)

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
