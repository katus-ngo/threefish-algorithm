# package for output font colored in cmd
from   time     import time
from   colorama import init
from   colorama import Fore, Back, Style
init(autoreset=True) 
import random
import math
import base64
import os
import cts

#===========================================
lfsr_mode = [ [1,4], 
            [1,3],
            [3,4,5,7],
            [1,4,7],
            [2,3,4,5]]
        
lfsr_init_str = ['0','1','0','1','0','1','1']
#===========================================

def rotl(x,n):
    a = x >> n 
    r = (x - a * 2**n)*(2**(64-n))
    return int(a + r)

def rotr(x, n):
    b = padRight(bin(x).replace("0b", ""), "0", 64)
    return int("".join(b[n:] + b[0:n]), 2) 

def per(list, pi):
    t = list[0:len(list)]
    for i in range(len(list)):
        list[i] = t[pi[i]]

def utf8ToBytes(str):
    return str.encode("utf-8")

def bytesToUtf8(str):
    return str.decode("utf-8", "strict")

def base64Encode(str):
    b = base64.b64encode(bytes(str, encoding="utf8"))
    return "".join([chr(i) for i in b])

def base64Decode(str):
    b = base64.b64decode(bytes(str, encoding="utf8"))
    return "".join([chr(i) for i in b])
    
def padLeft(s, char, n):
    return ('{:' + char + '<' + str(n) + '}').format(s)

def padCenter(s, char, n):
    return ('{:' + char + '^' + str(n) + '}').format(s)

def padRight(s, char, n):
    return ('{:' + char + '>' + str(n) + '}').format(s)
     
def chunk(arr, n):
    newArr = []
    idx = 0
    length = len(arr)
    while idx < length:
        newArr.append(arr[idx:idx+n])
        idx += n
    return newArr

def dechunk(arr):
    return [i for sublist in arr for i in sublist]

def clearZero(arr):
    l = len(arr) - 1
    while arr[l] == 0:
        arr.pop()
        l -= 1
    return arr

def readFile(filename, blockSize):
    # read file and encode with utf-8
    fo = open(filename, 'r')
    str = fo.read()
    fo.close()
    str_utf8 = str.encode("utf-8")

    # initialisation 
    numBlockByte = int(blockSize / 8)

    # transfer bytes to arr of byte
    arr = []
    for i in range(len(str_utf8)):
        arr.append(str_utf8[i])
    
    # completion according to blockSize
    length = len(arr)
    if length % numBlockByte != 0:
        if length < numBlockByte:
            decalage = numBlockByte - length
            for k in range(decalage):
                arr.append(0)
        if length > numBlockByte:
            decalage = int(numBlockByte - (length % numBlockByte))
            for j in range(decalage):
                arr.append(0)

    # divise arr in subArr of 8 items
    newArr = chunk(arr, 8)

    # join subArr
    for j in range(len(newArr)):
        newArr[j] = ''.join([padRight(bin(c).replace('0b', ''), '0', 8) for c in newArr[j]])
    
    # return arr of decimal
    numBlock = int(blockSize / 64)
    return chunk([int('0b' + el, 2) for el in newArr], numBlock)

def writeFile(filename, arr):
    fo = open(filename, 'w')
    newArr = dechunk([chunk(padRight(bin(el).replace('0b', ''), '0', 64), 8) for el in dechunk(arr)])

    # padRight char '0' to get 8 bits
    for i in range(len(newArr)):
        newArr[i] = padRight(newArr[i], '0', 8)

    # print(type(bytesToUtf8(bytes([int('0b' + el, 2) for el in newArr]))))

    fo.write(bytesToUtf8(bytes(clearZero([int('0b' + el, 2) for el in newArr]))))
    return fo.close()

def readMsg(str, blockSize):
    str_utf8 = str.encode("utf-8")

    # initialisation 
    numBlockByte = int(blockSize / 8)

    # transfer bytes to arr of byte
    arr = []
    for i in range(len(str_utf8)):
        arr.append(str_utf8[i])
    
    # completion according to blockSize
    length = len(arr)
    if length % numBlockByte != 0:
        if length < numBlockByte:
            decalage = numBlockByte - length
            for k in range(decalage):
                arr.append(0)
        if length > numBlockByte:
            decalage = int(numBlockByte - (length % numBlockByte))
            for j in range(decalage):
                arr.append(0)

    # divise arr in subArr of 8 items
    newArr = chunk(arr, 8)

    # join subArr
    for j in range(len(newArr)):
        newArr[j] = ''.join([padRight(bin(c).replace('0b', ''), '0', 8) for c in newArr[j]])
    
    # return arr of decimal
    numBlock = int(blockSize / 64)
    return chunk([int('0b' + el, 2) for el in newArr], numBlock)

def writeMsg(arr):
    newArr = dechunk([chunk(padRight(bin(el).replace('0b', ''), '0', 64), 8) for el in dechunk(arr)])

    # padRight char '0' to get 8 bits
    for i in range(len(newArr)):
        newArr[i] = padRight(newArr[i], '0', 8)

    # print(type(bytesToUtf8(bytes([int('0b' + el, 2) for el in newArr]))))
    return bytesToUtf8(bytes(clearZero([int('0b' + el, 2) for el in newArr])))

def magenta(str):
    return Fore.MAGENTA + str

def green(str):
    return Fore.GREEN + str

def cyan(str):
    return Fore.CYAN + str

def red(str):
    return Fore.RED + str

def IsExistDir(path):
    return os.path.isdir(path)

def IsExistFile(path):
    return os.path.exists(path)


def encode(s): 
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

def lfsr(lfsr_init_str):
    key = lfsr_init_str
    while len(key) < 65 :
        key.append( key[(len(key)-1)]^key[(len(key)-3)])
        #print(key)
    return key 


def lfsr_64bits(lfsr_init_str, l_mode):
    key = lfsr_init_str[0:len(lfsr_init_str)]
    new_bit = lfsr_init_str[l_mode[0]]

    #print(len(lfsr_init_str),len(key))
    while len(key) < 64 :
        for i in range(1,len(l_mode)): 
            new_bit = str(int(new_bit)^int(key[(len(key)-l_mode[i])]))
        key.append(new_bit)

    #transfer str to binary 
    str_key=''.join(key)
    
    sum, base = 0, 1
    for i in range(len(str_key)):
        sum += int(str_key[-i])*base
        base *= 2
    return sum 

def key_generation(nb_key):
    k = [None]*nb_key
    for j in range(nb_key):
        k[j] = lfsr_64bits(lfsr_init_str,lfsr_mode[j])
    return k
