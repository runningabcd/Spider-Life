#### 暴雪hash
'''
暴雪公司有个经典的字符串的hash公式
先提一个简单的问题，假如有一个庞大的字符串数组，然后给你一个单独的字符串，让你从这个数组中查找是否有这个字符串并找到它，你会怎么做？
有一个方法最简单，老老实实从头查到尾，一个一个比较，直到找到为止，我想只要学过程序设计的人都能把这样一个程序作出来，但要是有程序员把这样的程序交给用户，我只能用无语来评价，或许它真的能工作，但也只能如此了。
最合适的算法自然是使用HashTable（哈希表），先介绍介绍其中的基本知识，所谓Hash，一般是一个整数，通过某种算法，可以把一个字符串"压缩" 成一个整数，这个数称为Hash，当然，无论如何，一个32位整数是无法对应回一个字符串的，但在程序中，两个字符串计算出的Hash值相等的可能非常小，下面看看在MPQ中的Hash算法
'''

'''
unsigned long HashString(char *lpszFileName, unsigned long dwHashType) 
{ 
unsigned char *key = (unsigned char *)lpszFileName 
unsigned long seed1 = 0x7FED7FED, seed2 = 0xEEEEEEEE 
int ch 
while(*key != 0) 
{ 
ch = toupper(*key++ ) 
seed1 = cryptTable[(dwHashType << 8) + ch] ^ (seed1 + seed2) 
seed2 = ch + seed1 + seed2 + (seed2 << 5) + 3 
} 
return seed1 
}
'''

'''
Blizzard的这个算法是非常高效的，被称为"One-Way Hash"，举个例子，字符串"unitneutralacritter.grp"通过这个算法得到的结果是0xA26067F3。 
是不是把第一个算法改进一下，改成逐个比较字符串的Hash值就可以了呢，答案是，远远不够，要想得到最快的算法，就不能进行逐个的比较，通常是构造一个哈希表(Hash Table)来解决问题，哈希表是一个大数组，这个数组的容量根据程序的要求来定义，例如1024，每一个Hash值通过取模运算 (mod)对应到数组中的一个位置，这样，只要比较这个字符串的哈希值对应的位置又没有被占用，就可以得到最后的结果了，想想这是什么速度？是的，是最快的O(1)，现在仔细看看这个算法吧
'''

'''
int GetHashTablePos(char *lpszString, SOMESTRUCTURE *lpTable, int nTableSize) 
{ 
int nHash = HashString(lpszString), nHashPos = nHash % nTableSize 
if (lpTable[nHashPos].bExists && !strcmp(lpTable[nHashPos].pString, lpszString)) 
return nHashPos 
else 
return -1 //Error value 
}
'''

'''
看到此，我想大家都在想一个很严重的问题："假如两个字符串在哈希表中对应的位置相同怎么办？",究竟一个数组容量是有限的，这种可能性很大。解决该问题的方法很多，我首先想到的就是用"链表",感谢大学里学的数据结构教会了这个百试百灵的法宝，我碰到的很多算法都可以转化成链表来解决，只要在哈希表的每个入口挂一个链表，保存所有对应的字符串就OK了。 
事情到此似乎有了完美的结局，假如是把问题独自交给我解决，此时我可能就要开始定义数据结构然后写代码了。然而Blizzard的程序员使用的方法则是更精妙的方法。基本原理就是：他们在哈希表中不是用一个哈希值而是用三个哈希值来校验字符串。 
中国有句古话"再一再二不能再三再四"，看来Blizzard也深得此话的精髓，假如说两个不同的字符串经过一个哈希算法得到的入口点一致有可能，但用三个不同的哈希算法算出的入口点都一致，那几乎可以肯定是不可能的事了，这个几率是1:18889465931478580854784，大概是10的 22.3次方分之一，对一个游戏程序来说足够安全了。 
现在再回到数据结构上，Blizzard使用的哈希表没有使用链表，而采用"顺延"的方式来解决问题，看看这个算法：
'''

'''
int GetHashTablePos(char *lpszString, MPQHASHTABLE *lpTable, int nTableSize) 
{ 
const int HASH_OFFSET = 0, HASH_A = 1, HASH_B = 2 
int nHash = HashString(lpszString, HASH_OFFSET) 
int nHashA = HashString(lpszString, HASH_A) 
int nHashB = HashString(lpszString, HASH_B) 
int nHashStart = nHash % nTableSize, nHashPos = nHashStart 
while (lpTable[nHashPos].bExists) 
{ 
if (lpTable[nHashPos].nHashA == nHashA && lpTable[nHashPos].nHashB == nHashB) 
return nHashPos 
else 
nHashPos = (nHashPos + 1) % nTableSize 
if (nHashPos == nHashStart) 
break 
} 
return -1 //Error value 
'''

'''
1. 计算出字符串的三个哈希值（一个用来确定位置，另外两个用来校验) 
2. 察看哈希表中的这个位置 
3. 哈希表中这个位置为空吗？假如为空，则肯定该字符串不存在，返回 
4. 假如存在，则检查其他两个哈希值是否也匹配，假如匹配，则表示找到了该字符串，返回 
5. 移到下一个位置，假如已经越界，则表示没有找到，返回 
6. 看看是不是又回到了原来的位置，假如是，则返回没找到 
7. 回到3 
怎么样，很简单的算法吧，但确实是天才的idea, 其实最优秀的算法往往是简单有效的算法。
'''

'''
/*********************************StringHash.h*********************************/

#pragma once

#define MAXTABLELEN 1024 // 默认哈希索引表大小 
////////////////////////////////////////////////////////////////////////// 
// 哈希索引表定义 
typedef struct _HASHTABLE
{ 
　　long nHashA 
　　long nHashB 
　　bool bExists 
}HASHTABLE, *PHASHTABLE 

class StringHash
{
public:
　　StringHash(const long nTableLength = MAXTABLELEN)
　　~StringHash(void)
private: 
　　unsigned long cryptTable[0x500] 
　　unsigned long m_tablelength // 哈希索引表长度 
　 HASHTABLE *m_HashIndexTable 
private:
　　void InitCryptTable() // 对哈希索引表预处理 
　　unsigned long HashString(const string& lpszString, unsigned long dwHashType) // 求取哈希值 
public:
　　bool Hash(string url)
　　unsigned long Hashed(string url) // 检测url是否被hash过
}

 

/*********************************StringHash.cpp*********************************/

#include "StdAfx.h"
#include "StringHash.h"

StringHash::StringHash(const long nTableLength /*= MAXTABLELEN*/)
{
　　InitCryptTable() 
　　m_tablelength = nTableLength 
　　//初始化hash表
　　m_HashIndexTable = new HASHTABLE[nTableLength] 
　　for ( int i = 0 i < nTableLength i++ ) 
　　{ 
　　　　m_HashIndexTable[i].nHashA = -1 
　　　　m_HashIndexTable[i].nHashB = -1 
　　　　m_HashIndexTable[i].bExists = false 
　　} 
}

StringHash::~StringHash(void)
{
　　//清理内存
　　if ( NULL != m_HashIndexTable ) 
　　{ 
　　　　delete []m_HashIndexTable 
　　　　m_HashIndexTable = NULL 
　　　　m_tablelength = 0 
　　} 
}

/************************************************************************/
/*函数名：InitCryptTable
/*功 能：对哈希索引表预处理 
/*返回值：无
/************************************************************************/
void StringHash::InitCryptTable() 
{ 
　 unsigned long seed = 0x00100001, index1 = 0, index2 = 0, i

　　for( index1 = 0 index1 < 0x100 index1++ ) 
　　{ 
　　　　for( index2 = index1, i = 0 i < 5 i++, index2 += 0x100 ) 
　　　　{ 
　　　　　　unsigned long temp1, temp2 
　　　　　　seed = (seed * 125 + 3) % 0x2AAAAB 
　　　　　　temp1 = (seed & 0xFFFF) << 0x10 
　　　　　　seed = (seed * 125 + 3) % 0x2AAAAB 
　　　　　　temp2 = (seed & 0xFFFF) 
　　　　　　cryptTable[index2] = ( temp1 | temp2 ) 
　　　　} 
　　} 
}

/************************************************************************/
/*函数名：HashString
/*功 能：求取哈希值 
/*返回值：返回hash值
/************************************************************************/
unsigned long StringHash::HashString(const string& lpszString, unsigned long dwHashType) 
{ 
　　unsigned char *key = (unsigned char *)(const_cast<char*>(lpszString.c_str())) 
　　unsigned long seed1 = 0x7FED7FED, seed2 = 0xEEEEEEEE 
　　int ch

　　while(*key != 0) 
　　{ 
　　　　ch = toupper(*key++)

　　　　seed1 = cryptTable[(dwHashType << 8) + ch] ^ (seed1 + seed2) 
　　　　seed2 = ch + seed1 + seed2 + (seed2 << 5) + 3 
　　} 
　　return seed1 
}

/************************************************************************/
/*函数名：Hashed
/*功 能：检测一个字符串是否被hash过
/*返回值：如果存在，返回位置；否则，返回-1
/************************************************************************/
unsigned long StringHash::Hashed(string lpszString)

{ 
　　const unsigned long HASH_OFFSET = 0, HASH_A = 1, HASH_B = 2 
　 //不同的字符串三次hash还会碰撞的几率无限接近于不可能
　　unsigned long nHash = HashString(lpszString, HASH_OFFSET) 
　 unsigned long nHashA = HashString(lpszString, HASH_A) 
　　unsigned long nHashB = HashString(lpszString, HASH_B) 
　 unsigned long nHashStart = nHash % m_tablelength, 
　　nHashPos = nHashStart

　　while ( m_HashIndexTable[nHashPos].bExists) 
　　{ 
　　if (m_HashIndexTable[nHashPos].nHashA == nHashA && m_HashIndexTable[nHashPos].nHashB == nHashB)
　　　　return nHashPos 
　　else 
　　nHashPos = (nHashPos + 1) % m_tablelength

　　if (nHashPos == nHashStart) 
　　break 
　　}

　　return -1 //没有找到 
}

/************************************************************************/
/*函数名：Hash
/*功 能：hash一个字符串 
/*返回值：成功，返回true；失败，返回false
/************************************************************************/
bool StringHash::Hash(string lpszString)
{ 
　　const unsigned long HASH_OFFSET = 0, HASH_A = 1, HASH_B = 2 
　　unsigned long nHash = HashString(lpszString, HASH_OFFSET) 
　　unsigned long nHashA = HashString(lpszString, HASH_A) 
　　unsigned long nHashB = HashString(lpszString, HASH_B) 
　　unsigned long nHashStart = nHash % m_tablelength, 
　　nHashPos = nHashStart

　　while ( m_HashIndexTable[nHashPos].bExists) 
　　{ 
　　　　nHashPos = (nHashPos + 1) % m_tablelength 
　　　　if (nHashPos == nHashStart) //一个轮回 
　　　　{ 
　　　　　　//hash表中没有空余的位置了,无法完成hash
　　　　　　return false 
　　　　} 
　　} 
　　m_HashIndexTable[nHashPos].bExists = true 
　　m_HashIndexTable[nHashPos].nHashA = nHashA 
　　m_HashIndexTable[nHashPos].nHashB = nHashB

　　return true 
}
'''

#### python版本的暴雪hash算法

# -*- coding:utf8 -*-
import time, random
import ctypes as C


class HashTable(C.Structure):
    _fields_ = [
        ('hashA', C.c_int64),
        ('hashB', C.c_int64),
        ('exists', C.c_bool),
        ('opt', C.c_int64),
        ('info', C.c_char * 64)
    ]

    def __init__(self, hashA, hashB, exists):
        self.hashA = hashA
        self.hashB = hashB
        self.exists = exists
        self.opt = 0


class HashString:

    def __init__(self):
        self.tableLength = 0
        self.cryptTable = (C.c_int * 0x500)()
        self.hashIndexTable = []

    def Init(self, tableLen=4194304):  # 4M = 4 * 1024 * 1024 = 4194304
        now = time.time()
        self.InitCryptTable()
        self.tableLength = tableLen
        self.hashIndexTable = C.cast(C.create_string_buffer(C.sizeof(HashTable) * self.tableLength),
                                     C.POINTER(HashTable))

    def InitCryptTable(self):
        seed = 0x00100001
        for index1 in range(0, 0x100):
            for i in range(0, 5):
                index2 = index1 + i * 0x100
                seed = (seed * 125 + 3) % 0x2aaaab
                temp1 = (seed * 0xffff) << 0x10
                seed = (seed * 125 + 3) % 0x2aaaab
                temp2 = (seed & 0xffff)
                self.cryptTable[index2] = (temp1 | temp2)

    def HashString(self, info, hashType):
        seed1 = 0x7fed7fed
        seed2 = 0xeeeeeeee
        for c in info:
            # ch = c.upper()
            ch = c
            seed1 = self.cryptTable[(hashType << 8) + ord(ch)] ^ (seed1 + seed2)
            seed2 = ord(ch) + seed1 + seed2 + (seed2 << 5) + 3
        return seed1

    def IsHashed(self, info):
        hashOffset = 0
        HashA = 1
        HashB = 2
        hash = self.HashString(info, hashOffset)
        hashA = self.HashString(info, HashA)
        hashB = self.HashString(info, HashB)
        hashStart = hash % self.tableLength
        hashPos = hashStart

        while self.hashIndexTable[hashPos].exists:
            if self.hashIndexTable[hashPos].hashA == hashA and self.hashIndexTable[hashPos].hashB == hashB and \
                    self.hashIndexTable[hashPos].info == info:
                return hashPos
            else:
                hashPos = (hashPos + 1) % self.tableLength
            if hashPos == hashStart:
                break

        return -1

    def Hash(self, info, opt=1):
        hashOffset = 0
        HashA = 1
        HashB = 2
        hash = self.HashString(info, hashOffset)
        hashA = self.HashString(info, HashA)
        hashB = self.HashString(info, HashB)
        hashStart = hash % self.tableLength
        hashPos = hashStart

        while self.hashIndexTable[hashPos].exists:
            hashPos = (hashPos + 1) % self.tableLength
            if hashPos == hashStart:
                return -1

        self.hashIndexTable[hashPos].exists = True
        self.hashIndexTable[hashPos].hashA = hashA
        self.hashIndexTable[hashPos].hashB = hashB
        self.hashIndexTable[hashPos].info = info
        self.hashIndexTable[hashPos].opt += opt

        return hashPos

    def UpdateHashOpt(self, hashPos, opt=0):
        if hashPos < 0 or hashPos > self.tableLength:
            return False

        self.hashIndexTable[hashPos].opt += opt

        return True

    def LoadHashOpt(self, hashPos):
        if hashPos < 0 or hashPos > self.tableLength:
            return False
        return self.hashIndexTable[hashPos].opt


def RandStr(seed, tmpLen):
    ran = ''
    seedLen = len(seed)
    for i in range(tmpLen):
        tmp = random.randint(0, seedLen - 1)  # inner is seedLen + 1
        ran += seed[tmp]
    return ran
