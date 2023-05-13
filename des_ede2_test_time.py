from des_ede2 import treble_des
import platform
import psutil
import time


def time_test(s,k1,k2,op,epoch):
    start_time = time.time()
    for i in range(epoch):
        s = int(treble_des(s, k1, k2, op),16)
    end_time = time.time()
    return end_time-start_time


print("系统信息：".center(75,'='))
print("操作系统名称：",platform.system())  # 获取操作系统名称
print("操作系统版本号：",platform.release())  # 获取操作系统版本号
print("CPU名称：",platform.processor())  # 获取CPU名称
memory = psutil.virtual_memory()
print("总内存大小：",memory.total/pow(2,30),"GB")  # 获取总内存大小
print("可用内存大小：",memory.available/pow(2,30),"GB")  # 获取可用内存大小
epoch = 5000

print("加密时间测试".center(75,'='))
s = 0x78e2025d31d06fde
k1 = 0xa530af81d46635e4
k2 = 0xfc6aa9db1d2b1224
sum = time_test(s,k1,k2,1,epoch)
print("迭代次数：",epoch)
print("总共耗时(s)：",sum)
print("平均耗时(s)：",sum/epoch)


print("解密时间测试".center(75,'='))
s = 0x618f1b32353b4f35
k1 = 0xc50f4b2e21282135
k2 = 0x35becf7d711ee29a
sum = time_test(s,k1,k2,0,epoch)
print("迭代次数：",epoch)
print("总共耗时(s)：",sum)
print("平均耗时(s)：",sum/epoch)