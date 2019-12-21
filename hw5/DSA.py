from sys import argv
from random import randint
import hashlib

def mod_inv(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    _, x, _ = egcd(a, m)
    return x % m

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
        b = square_and_multiply(a, m, N)
        if b != 1 and b != N-1:
            i = 1
            while i < k and b != (N-1):
                b = square_and_multiply(b, 2, N)
                if b == 1:
                    return False
                i = i + 1
            if b != N-1:
                return False
        return True


def gen_prime(b):
    a = randint(2**(b-1), 2**b)
    while miller_rabin_test(a) == False:
        a = randint(2**(b-1), 2**b)
    return a


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