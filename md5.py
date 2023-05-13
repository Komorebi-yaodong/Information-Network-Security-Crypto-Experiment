# MD5源码

import math

def show_bytes(x):
    print(hex(int.from_bytes(x,"big")))

S = [
    7, 12, 17, 22,
    5,  9, 14, 20,
    4, 11, 16, 23,
    6, 10, 15, 21
]


T = [int(pow(2, 32) * abs(math.sin(i + 1))) & 0xffffffff for i in range(64)]


def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff


def F(b,c,d):
    return (b & c) | (~b & d)


def G(b,c,d):
    return (d & b) | (~d & c)


def H(b,c,d):
    return b ^ c ^ d


def I(b,c,d):
    return c ^ (b | ~d)


g = [F,G,H,I]

def packing(msg):
    msg = bytearray(msg)
    length = len(msg)
    pad_len = 64 - ((length + 8) % 64)
    packing = 1 * b'\x80' + (pad_len - 1) * b'\x00'
    length_byte = ((length * 8)%(1<<64)).to_bytes(8, 'little')
    # len_packing = length_byte[4:8] + length_byte[:4]
    res = msg + packing + length_byte
    # show_bytes(res)
    return res


def Hmd5(words,A,B,C,D):
    def get_i(round,step):
        if round == 0:
            return step
        elif round == 1:
            return (1+5*step)%16
        elif round == 2:
            return (5+3*step)%16
        else:
            return (7*step)%16

    for round in range(4):
        for step in range(16):
            i = get_i(round,step)
            A = (A + g[round](B,C,D) + words[i] + T[16*round+step]) & 0xffffffff
            A = ((left_rotate(A,S[step%4+round*4]) + B)%(1<<32)) & 0xffffffff
            A,B,C,D = D,A,B,C
        #     print(hex(A),hex(B),hex(C),hex(D))
        # print("-".center(50,'-'))
    return A,B,C,D

def md5(msg:bytes):

    # 填充
    msg_packing = packing(msg)
    total_length = len(msg_packing)
    # show_bytes(msg_packing)
    # 初始化MD缓冲区
    A=0x67452301
    B=0xefcdab89
    C=0x98badcfe
    D=0x10325476
    a,b,c,d=A,B,C,D
    for i in range(0,total_length,64):
        y = msg_packing[i:i+64]
        words = [int.from_bytes(y[j:j+4], 'little') for j in range(0, 64, 4)]
        a,b,c,d = Hmd5(words,a,b,c,d)
        tmp1=(a + A) & 0xffffffff
        tmp2=(b + B) & 0xffffffff
        tmp3=(c + C) & 0xffffffff
        tmp4=(d + D) & 0xffffffff
        A,B,C,D=tmp1,tmp2,tmp3,tmp4
        a,b,c,d = tmp1,tmp2,tmp3,tmp4
        # print('='.center(75,'='))

    res = ""
    tmp = [a,b,c,d]
    for i in tmp:
        i_b = i.to_bytes(4,"little")
        a = int.from_bytes(i_b,"big")
        res = res + format(a,'08x')
    return res



# if __name__ == "__main__":
#     m = input()
#     ans = md5(m.encode('utf-8'))
#     print(ans)