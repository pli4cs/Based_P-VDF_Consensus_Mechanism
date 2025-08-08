import datetime
from hashlib import sha256
import time
import math
import random

#十六进制字符串与十进制整型数的互相转换
class HexstrAndDecint:
    def __init__(self):
        return

    # 十六进制字符串转十进制整型数
    def HexstrToDecint(hexstr):
        dict = {"0": "0000", "1": "0001", "2": "0010", "3": "0011",
                "4": "0100", "5": "0101", "6": "0110", "7": "0111",
                "8": "1000", "9": "1001", "a": "1010", "b": "1011",
                "c": "1100", "d": "1101", "e": "1110", "f": "1111",
                }
        #十六进制字符串转二进制字符串
        binstr = ''
        for i in hexstr:
            #print(i)
            binstr += dict[i]
        print(binstr)

        # 二进制字符串转十进制整型数
        #binstr="00100101"
        decint = 0
        for i in binstr:
            if "1" == i:
                decint = decint * 2 + 1
            elif "0" == i:
                decint = decint * 2
        #print(decint)
        return decint

    # 十进制整型数转十六进制字符串
    def DecintToHexstr(decint):
        #decint=7
        binstr=""
        # 十进制整型数转二进制字符串
        if decint == 0:
            binstr = "0"
        else:
            while(decint != 0):
                if(decint%2 == 0):
                    binstr = "0" + binstr
                else:
                    binstr = "1" + binstr
                decint = decint//2
        #print(binstr)
        #将二进制字符串左填充0，补满256位
        count = 256 - len(binstr)
        while(count):
            binstr = "0" + binstr
            count = count - 1
        #print(binstr)

        # 二进制字符串转十六进制字符串
        dict = {"0000": "0", "0001": "1", "0010": "2", "0011": "3",
                "0100": "4", "0101": "5", "0110": "6", "0111": "7",
                "1000": "8", "1001": "9", "1010": "a", "1011": "b",
                "1100": "c", "1101": "d", "1110": "e", "1111": "f",
                }
        hexstr=""
        for i in range(0,len(binstr),4):
            hexstr=hexstr + dict[binstr[i+0:i+4]]
        #print(hexstr)
        return hexstr

"""""
a=int(input("输入十进制整数："))
b=int(input("输入十进制整数："))
bin_a=bin(a)
bin_b=bin(b)
"""""
plainData = '你好呀！'
Hash = sha256(plainData.encode('utf-8'))
#print("hash: %s" % Hash.digest())
#print(bin(Hash))
hash_hexdigest = Hash.hexdigest()
print("hash_hexdigest: %s" % hash_hexdigest)
decint=HexstrAndDecint.HexstrToDecint(hash_hexdigest)
#print(decint)
print("hash_hexdigest: %s" % HexstrAndDecint.DecintToHexstr(decint))
#print(int(Hash.digest()))
#print(type((Hash*156).digest()))
#print(Hash.bin())
#print(int(Hash.digest()))
#print(Hash)
    # print("douleHash result: "+douleHash)
    # print('random number r: ',self.r)
    # print(self.t)
    # print(self.nonce)
