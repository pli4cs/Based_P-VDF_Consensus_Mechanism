# VDF-based anti-parallel computing and publicly verifiable consensus mechanism
## Introduction
Generally, existing consensus mechanisms cannot resist on parallel computing and have a tendency to be centralized, such as proof of work (PoW), proof of stake (PoS). This has led to malicious mining for the purpose of obtaining block rewards, causing a lot of waste of resources, especially power resources, and also affecting the security of the blockchain system. The verifiable delay function is introduced into this field, and a blockchain consensus mechanism is proposed that resists parallel computing and publicly verifies block rights. The secure hash function, the sequentiality of the verifiable delay function, and the random number are utilized in this mechanism to randomize the acquisition of block rights, making it independent of computing power. In this scenario, the probability of obtaining block rights cannot be increased by increasing computing power and equipment, therefore, malicious mining behavior becomes ineffective, and disappears with it.

## Description
His is the prototype code for the following paper implementation. Among them, `OursConsensusMechanism.py` is the prototype experimental code of the P-VDF-based blockchain consensus mechanism in Paper 1, `P-VDF.py` is the prototype code of the practical verifiable delay function P-VDF derived from Paper 3 adopted in Paper 1, `PoW.py` is the prototype code of the consensus mechanism based on proof of work, and `TestSha256.py` is the prototype code for testing the secure hash function sha256. Please cite the following paper if it is helpful to you.

`Paper 1`: 李鹏, 张明武, 杨波. 一种抗并行计算的公开可验证出块权的区块链共识机制. 密码学报. 2024, 11(6): 1370-1385. https://doi.org/10.13868/j.cnki.jcr.000742

LI P, ZHANG M W, YANG B. Blockchain Consensus Mechanism with Publicly Verifiable Block Rights Against Parallel Computing. Journal of Cryptologic Research. 2024, 11(6): 1370-1385. https://doi.org/10.13868/j.cnki.jcr.000742

`Paper 2`: 李鹏, 张明武, 杨波. 可验证延迟函数与延迟加密研究综述. 密码学报. 2024, 11(2): 282-307. https://doi.org/10.13868/j.cnki.jcr.000680

LI P, ZHANG M W, YANG B. A Survey on Verifiable Delay Functions and Delay Encryptions. Journal of Cryptologic Research. 2024, 11(2): 282-307. https://doi.org/10.13868/j.cnki.jcr.000680

`Paper 3`: A practical verifiable delay function and delay encryption scheme[J/OL]. IACR Cryptology ePrint Archive, 2021: 2021/1293. https://eprint.iacr.org/archive/2021/1293/1632747823.pdf


## Dependencies

The following dependencies can be installed using pip3 install [package]:

* hashlib
* math
* numpy (>= 1.21.2)
* pycryptodome (>= 3.10.4)
* random
