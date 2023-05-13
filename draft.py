import time


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


def square_multiply(a, n, m):  # 平方乘算法
    t = a % m
    result = 1
    judge = 1
    while n > 0:
        if judge & n:
            result = (result * t) % m
            # result = montgomery_mul(result,t,m)
        n = n >> 1
        t = (t * t) % m
        # t = montgomery_mul(t,t,m)
    return result

def square_multiply_montgomery(a, n, m):  # 平方乘算法

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
    
    k = len(bin(m)) - 2
    r = 1 << k
    r_,m_,gcd = expand_gcd(r,m)

    def montgomery_mul_(a: int, b: int, n: int,k: int,r: int,n_: int)-> int:
        def redc(T,r,k,n_,n):
            m = ((T&(r-1))*n_)&(r-1)
            t = (T+m*n)>>k
            if t >= n:
                return t-n
            else:
                return t

        T = a*b*r
        return redc(T,r,k,n_,n)

    t = a % m
    result = 1
    judge = 1
    while n > 0:
        if judge & n:
            # result = (result * t) % m
            result = montgomery_mul_(result,t,m,k,r,m_)
        n = n >> 1
        # t = (t * t) % m
        t = montgomery_mul_(t,t,m,k,r,m_)
    return result
    


p = 112777397707584803419118575052195054017583300259494191154998439893529537631622184266788513941540592429138151585110778903119111521915362687400249271224753796696260754459112690162643580471713065080959101664820170525562931707819379555324156416391650267080233623964623635731140882167396925149718343223841089073923
q = 160383048560948598853344587358803784778832723250798923471247162098254563382511329741858721411668137743466179087821411944465002859978412173822401491420648859726023103665213630120569982088763939041006178153231440107800316492029342655132964860546912936549333154961603592588148020589112981662157020697494469493451
n = p*q

a = (p//2) & 510
b = (q//2) & 510
# b = 12
print("sq测试".center(75,'='))
start_time = time.time()
print(square_multiply(a,b,n))
print(time.time()-start_time)

print("sq+m测试".center(75,'='))
start_time = time.time()
print(square_multiply_montgomery(a,b,n))
print(time.time()-start_time)


print("pow测试".center(75,'='))
start_time = time.time()
print(pow(a,b,n))
print(time.time()-start_time)

# print((a*b)%n)
# print(montgomery_mul(a,b,n))