from md5 import md5 as mymd5
import platform
import psutil
import time
from hashlib import md5


def time_test(path):

    with open(path,'rb') as f:
        data = f.read()
        length = len(data)
        print("文件信息".center(75,'='))
        print("文件大小：",length/(pow(2,20)),"MB")

        print("自写MD5函数测试".center(75,'='))
        start_time = time.time()
        res1 = mymd5(data)
        end_time = time.time()
        print("返回结果：",res1)
        print("运行时间：",end_time-start_time,"s")

        print("库MD5函数测试".center(75,'='))
        start_time = time.time()
        res2 = md5(data)
        end_time = time.time()
        print("返回结果：",res2.hexdigest())
        print("运行时间：",end_time-start_time,"s")


print("系统信息：".center(75,'='))
print("操作系统名称：",platform.system())  # 获取操作系统名称
print("操作系统版本号：",platform.release())  # 获取操作系统版本号
print("CPU名称：",platform.processor())  # 获取CPU名称
memory = psutil.virtual_memory()
print("总内存大小：",memory.total/pow(2,30),"GB")  # 获取总内存大小
print("可用内存大小：",memory.available/pow(2,30),"GB")  # 获取可用内存大小

path = "./galaxy.bmp"
time_test(path)