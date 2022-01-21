# package for output font colored in cmd
from   colorama import init
from   colorama import Fore
init(autoreset=True)

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

def bytesToUtf8(str):
    return str.decode("utf-8", "strict")

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

def rFile(filename, mode = 'r'):
    fo = open(filename, mode)
    str = fo.read()
    fo.close()
    return str

def wFile(filename, str, pos = 0, mode = 'w'):
    fo = open(filename, mode)
    fo.write(str[pos:])
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

    return bytesToUtf8(bytes(clearZero([int('0b' + el, 2) for el in newArr])))

def magenta(str):
    return Fore.MAGENTA + str

def green(str):
    return Fore.GREEN + str

def cyan(str):
    return Fore.CYAN + str

def red(str):
    return Fore.RED + str

def cls(arr):
    while len(arr) > 0:
        arr.pop()

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
    # [12434255084567487610, 12582277207756613454, 12440124641901924412, 12469516777473785570]
    return k
