import datetime
from hashlib import sha256
import time
import math
import random
from Crypto.Util import number

SEC_PARM_BIT=1024 #PracticalVDF的安全参数位数
TIMESTEP=400000    #PracticalVDF的时间参数
DIFFICULTY=5   #区块链的出块的目标难度，表示16进制表示的sha256哈希值有多少个0为前导
RAND_LEFT_MIN=1  #区块链出块产生随机数区间的左端点值
RAND_RIGHT_MAX=1024 #区块链出块产生随机数区间的右端点值
global doubleHashComputeStartTime
doubleHashComputeStartTime=0

class PracticalVDF:
    def __init__(self):
        return

    # 校验器设置-将模数设置为Blum整数,输入安全参数1^k,也就是x和bits，返回公共参数pp和素数p,q
    def Setup(x,bits):
        def genPrime(bits):
            potential_prime = 1
            while potential_prime % 4 == 1:
                potential_prime = number.getPrime(bits)
            return potential_prime

        x = 0
        while x <1:
            p = genPrime(bits)
            q = genPrime(bits)
            if p != q and q % 4 != 1:
                N = p * q
                pp = N
            x += 1
        return pp,p,q

    #验证程序生成器-即使一次性使用单独的设置程序和生成器来定义序列性
    #输入给公共参数pp,时间参数t,素数p和q,返回困难性问题实例C
    def Gen(pp, t, p, q):
        N = pp
        J_p, J_q = 1, 1
        while not (J_p == 1 and J_q != 1) and not (J_q == 1 and J_p != 1):
            x = random.randrange(2, N)
            J_p = pow(x, (p - 1) // 2, p)  # Always == 1 or == p-1, use Euler's Criterion
            J_q = pow(x, (q - 1) // 2, q)  # Always == 1 or == q-1, use Euler's Criterion
        x_0 = pow(x, 2, N)

        #现在生成x_minus_t
        omega_p = (p + 1) // 4  # Tonelli Shanks, need p = 3 mod 4, Extend Eulers Criterion for proof
        omega_q = (q + 1) // 4  # Tonelli Shanks, need q = 3 mod 4, Extend Eulers Criterion for proof

        alpha_p = pow(x_0, pow(omega_p, t, p - 1), p)  # reduce mod p-1 is Eulers Theorem
        alpha_q = pow(x_0, pow(omega_q, t, q - 1), q)  # reduce mod p-1 is Eulers Theorem

        x_minus_t = ((alpha_p * q * pow(q, -1, p)) + (
                    alpha_q * p * pow(p, -1, q))) % N  # Chinese Remainder Theorem to find Mod N.
        C = (x, x_0, x_minus_t)
        return C


    #证明程序 Eval
    def Eval(pp, C, t):
        #print(C)
        x = C[0]
        x_0 = C[1]
        x_minus_t = C[2]
        N = pp

        # evaluation of VDF here
        x_prime = pow(x_minus_t, pow(2, t - 1), N)  # hard work here

        # now use EEA to find the factors of N
        factor1 = math.gcd(x - x_prime, N)
        # factor2 = math.gcd(x+x_prime, N) #O(M(N)logN)
        factor2 = N // factor1  # O(M(N)), so logN better than finding gcd
        y = (factor1, factor2)
        return y

    # 验证程序Verify
    def Verify(pp, C, t, y):
        V = 'reject'
        factor1 = y[0]
        factor2 = y[1]
        x_0 = C[1]
        x_minus_t = C[2]
        N = pp

        if factor1 == 1 or factor2 == 1:
            return V
        if (factor1 * factor2 == pp) and (pow(x_minus_t, pow(2, t, (factor1 - 1) * (factor2 - 1)), N) == x_0):
            V = 'accept'
        return V


class Block:

    def __init__(self, index, timestamp, data, previousHash, CurrentVdfParm=[], NextVdfParm=[], y=""):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        # 当前区块出块的VDF参数CurrentVdfParm=[pp, C, t, k]
        self.CurrentVdfParm = CurrentVdfParm
        # 发布下个区块出块的VDF参数,NextVdfParm
        self.NextVdfParm = NextVdfParm
        # 用于产生下一个区块的VDF所有参数为(pp, C, t, k)

        self.nonce = 0 # 代表当前计算了多少次hash计算
        self.r = 0 #随机数累加的结果


        # y为上一个区块设置的产生当前区块的困难性问题实例C的解
        self.y=y
        self.difficulty = DIFFICULTY
        self.hash = self.calculateHash()


    def getCurrentVdfParm(self):
        return self.CurrentVdfParm

    def getNextVdfParm(self):
        return self.NextVdfParm

    def setCurrentVdfParm(self, CurrentVdfParm):
        self.CurrentVdfParm = CurrentVdfParm

    def setNextVdfParm(self, NextVdfParm):
        self.NextVdfParm = NextVdfParm


    def setVdfY(self, y):
        self.y = y

    def calculateHash(self):
        markleRoot = sha256(str(self.data).encode('utf-8')).hexdigest()
        plainData = str(self.previousHash)+str(markleRoot)+str(self.index) + str(self.timestamp) +str(self.difficulty)+str(self.nonce)+str(self.y)+str(self.CurrentVdfParm[0])+str(self.CurrentVdfParm[1])+str(self.CurrentVdfParm[2])+str(self.CurrentVdfParm[3])+str(self.r)
        douleHash=sha256(sha256(plainData.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
        #print("douleHash result: "+douleHash)
        #print('random number r: ',self.r)
        #print(self.t)
        #print(self.nonce)
        return douleHash

    # 竞争出块权 difficulty代表难度 表示前difficulty位都为0才算成功
    def minerBlock(self, newBlock, difficulty, CurrentVdfParm):
        start_time = time.time()
        pp=CurrentVdfParm[0]
        C=CurrentVdfParm[1]
        t=CurrentVdfParm[2]
        # 求解困难性问题实例C的解y
        y= PracticalVDF.Eval(pp, C, t)   # y = (1, pp) #lazy eval
        newBlock.setVdfY(y)

        print('y:', y)
        print('Eval time: '+str(round(time.time() - start_time, 2))+'s')
        global doubleHashComputeStartTime
        doubleHashComputeStartTime = time.time()
        self.r = 0 #初始化
        decint = 0 #初始化
        # 目标值设为满足难度difficulty的最大哈希值(用十进制整数表示)+1
        target = pow(2, 256 - self.difficulty * 4)
        targethex=HexstrAndDecint.DecintToHexstr(target)

        #双sha256哈希值(用十进制整数表示) < 目标值 * r 成立时结束循环
        while (decint >= target * self.r ):
            self.nonce = self.nonce + 1
            self.r=self.r+random.randint(RAND_LEFT_MIN,RAND_RIGHT_MAX)
            self.hash = self.calculateHash()
            # 将十六进制字符串形式表示的哈希值转成十进制整型数
            decint = HexstrAndDecint.HexstrToDecint(self.hash)

        print('CurrentBlockHash:',self.hash)
        #print('MaxTargetHash +1:',targethex)

        k = SEC_PARM_BIT
        pp, p, q = PracticalVDF.Setup(1, k)
        C = PracticalVDF.Gen(pp, t, p, q)
        #NextVdfParm=[]
        NextVdfParm=[pp, C, t, k]
        newBlock.setNextVdfParm(NextVdfParm)
        #print("count: "+str(count))

    def __str__(self):
        return str(self.__dict__)


class BlockChain:

    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.difficulty = DIFFICULTY
        self.t = TIMESTEP
        self.k = SEC_PARM_BIT



    def createGenesisBlock(self):
        #获取区块链相关初始参数
        t=TIMESTEP
        k=SEC_PARM_BIT

        start_time = time.time()
        #共识机制中VDF的初始设置，初始化相关参数,
        pp, p, q = PracticalVDF.Setup(1, k)
        print('pp:', pp)
        print('Set time: '+str(round(time.time() - start_time, 2))+'s')

        #产生下一个区块出块的困难性问题实例C
        start_time = time.time()
        C= PracticalVDF.Gen(pp, t, p, q)
        print('C, t:', C, t) #t是求解C需要花费序列步骤数
        print('Gen time: '+ str(round(time.time() - start_time, 2))+'s')
        #firstblock=self.getLatestBlock()
        #firstblock.setVdfParm(pp, C, t)

        #当前区块出块的VDF参数
        CurrentVdfParm = ['', '', '', '']
        #下个区块出块的VDF参数
        NextVdfParm = [pp, C, t, k]

        #返回创世块,其中(pp, C, t, k)为用于产生下一个区块的VDF所有参数
        #这是创世块,所以previousHash和y的值为空，即""
        return Block(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "genesis block data", "", CurrentVdfParm, NextVdfParm, "")

    def setBlockVdfParm(self):
        return




    def getLatestBlock(self):
        #返回区块链的最后最新的一个区块
        return self.chain[len(self.chain) - 1]

    # 添加区块前需要 做一道计算题?,做完后才能把区块加入到链上
    def addBlock(self, newBlock,CurrentVdfParm=[], y=""):
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.minerBlock(newBlock,self.difficulty,CurrentVdfParm)
        self.chain.append(newBlock)

    def __str__(self):
        return str(self.__dict__)

    def chainIsValid(self):
        for index in range(1, len(self.chain)):
            currentBlock = self.chain[index]
            previousBlock = self.chain[index - 1]

            CurrentVdfParm=currentBlock.getCurrentVdfParm()

            V=PracticalVDF.Verify(CurrentVdfParm[0],CurrentVdfParm[1],CurrentVdfParm[2],currentBlock.y)
            if V == 'reject':
                print(V)
                return False
            if (currentBlock.hash != currentBlock.calculateHash()):
                print(currentBlock.hash)
                print(currentBlock.calculateHash())
                return False
            if previousBlock.hash != currentBlock.previousHash:
                print(previousBlock.hash)
                print(currentBlock.previousHash)
                return False
        return True

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
        #print(binstr)

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


def main():
    myCoin = BlockChain()
    blockNume=50


    # 下面打印了每个区块挖掘需要的时间 比特币通过一定的机制控制在10分钟出一个块
    # 其实就是根据当前网络算力 调整我们上面difficulty值的大小,如果你在
    # 本地把上面代码difficulty的值调很大你可以看到很久都不会出计算结果
    print("\nMiner %s blocks " % blockNume)
    for i in range(1,blockNume+1):
        print("\n")
        lastblock = myCoin.getLatestBlock()
        NextVdfParm = lastblock.getNextVdfParm()

        print("start to miner block No. "+str(i)+" time : " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        startMineBlockNoITime = time.time()

        myCoin.addBlock(Block(i, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "BlockData is {amount:"+str(random.randint(0,1000))+"}", lastblock.hash, lastblock.getNextVdfParm()),lastblock.getNextVdfParm())
        endMineBlockNoITime=time.time()
        print("compute block No. "+str(i)+" doubleHash time completed" + ",used " + str(round(endMineBlockNoITime-doubleHashComputeStartTime,2)) + "s")
        print("miner block No. "+str(i)+" time completed" + ",used " + str(round(endMineBlockNoITime-startMineBlockNoITime,2)) + "s")

    # 打印区块信息
    print("print block info ####:\n")
    for block in myCoin.chain:
        print("\n")
        print(block)

    # 检查区块链是否有效
    print("\nbefore tamper block,blockchain is valid ###")
    print(myCoin.chainIsValid())

    # 篡改区块信息后，再次检查区块链
    myCoin.chain[blockNume-5].data = "{amount:1002}"
    print("after tamper block,blockchain is valid ###")
    print(myCoin.chainIsValid())
if __name__ == '__main__':
    main()