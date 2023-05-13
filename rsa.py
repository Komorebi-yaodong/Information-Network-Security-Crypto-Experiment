# RSA源码

import random


def montgomery_mul(a: int, b: int, n: int) -> int:
    def expand_gcd(a, b):
        x0, y0, x1, y1 = 1, 0, 0, 1
        
        a0,b0=a,b
        while b0 != 0:
            q, r = divmod(a0, b0)
            a0, b0 = b0, r
            x0, y0, x1, y1 = x1, y1, x0 - q * x1, y0 - q * y1
        
        if x0 < 0:
            x0 = x0%b
            y0 = (a0-x0*a)//b

        return x0, -y0 ,a0
    
    def redc(T,r,k,n_,n):
        m = ((T&(r-1))*n_)&(r-1)
        t = (T+m*n)>>k
        if t >= n:
            return t-n
        else:
            return t

    k = len(bin(n)) - 2
    r = 1 << k
    r_,n_,gcd = expand_gcd(r,n)
    T = a*b*r
    return redc(T,r,k,n_,n)


def is_prime(n):  # Miller-Rabin素性检验
    if n == 1:
        return False
    if n == 2:
        return True
    time = 5
    t = n - 1
    k = 0
    judge = 0
    while t & 1 == 0:
        k += 1
        t = t >> 1
    q = t

    for i in range(time):
        judge = 0
        a = random.randint(2, n-1)
        if pow(a, q, n) == 1:
            judge = 1
        for j in range(k):
            if pow(a, (2 ** j) * q, n) == n - 1:
                judge = 1
        # print(judge,a)
        if judge == 0:
            break

    if judge == 1:
        return True
    else:
        return False


# def expand_gcd(a, b):
#     def sub_gcd(a,b):
#         if b == 0:
#             return 1,0,a
#         else:
#             x_, y_ , gcd = sub_gcd(b, a % b)
#             x = y_
#             y = x_ - (a // b) * y_
#             return x,y,gcd
#     x,y,gcd = sub_gcd(a,b)
#     if x < 0:
#         x = x%b
#         y = (gcd-x*a)//b
#     return x,y,gcd
    

def expand_gcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    
    a0,b0=a,b
    while b0 != 0:
        q, r = divmod(a0, b0)
        a0, b0 = b0, r
        x0, y0, x1, y1 = x1, y1, x0 - q * x1, y0 - q * y1
    
    if x0 < 0:
        x0 = x0%b
        y0 = (a0-x0*a)//b

    return x0, y0 ,a0


def check(p,q):
    if is_prime(p) and is_prime(q):
        return True
    else:
        return False


def decry_rsa(c, d, p, q, n):  # 中国剩余定理加速RSA解码 ：密文，密钥dpq，公钥n
    d1 = d % (p - 1)
    d2 = d % (q - 1)
    c1 = c % p
    c2 = c % q
    m1 = pow(c1, d1, p)
    m2 = pow(c2, d2, q)
    a1 = expand_gcd(q, p)[0]
    a2 = expand_gcd(p, q)[0]
    # m = (m1 * a1 * q + m2 * a2 * p) % n
    m = (montgomery_mul(montgomery_mul(m1,a1,n),q,n)+montgomery_mul(montgomery_mul(m2,a2,n),p,n))%n
    return m


def encry_rsa(m, n, e):
    c = pow(m, e, n)
    return c


def rsa(x, p, q, e, op):
    if check(p,q):
        n = p * q
        elur = (p - 1) * (q - 1)
        if op == 1:
            res = encry_rsa(x, n, e)
        else:
            d = expand_gcd(e, elur)[0]
            res = decry_rsa(x, d, p, q, n)
        return res
    else:
        res = "Mole ! Terminate !"
        return res


if __name__ == "__main__":
    p = int(input().strip())
    q = int(input().strip())
    e = int(input().strip())
    x = int(input().strip())
    op = int(input().strip())

    ans = rsa(x, p, q, e, op)

    print(ans)