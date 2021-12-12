from       util import key_generation
import     cts
import     util

#===========================
tweaks     = [3,4] 
blocksize  = 256 
nr         = 76
nb_key     = 4
mode       = cts.MODE_CBC
r_x, r_y   = 1, 1
nw         = blocksize // 64 
#===========================

#set iv 
if ( nw == 4 ): 
    iv = cts.INITIAL_VECTEUR_4 
elif (nw == 8 ):
    iv = cts.INITIAL_VECTEUR_8 
elif (nw == 16 ): 
    iv = cts.INITIAL_VECTEUR_16 

#generation of initials list of keys, nb_keys in a round = nb of messages in a bloc = blocksize / messagesize  
keys= key_generation(nb_key)

class cipher_threefish:
    def __init__(self, blockSize, nr, key, tweak, mode, c_bloc):

        if blockSize not in [ 16,256, 512, 1024]:
            exit(0)

        if nr not in [ 72, 76, 80]:
            exit(0)
        
        if len(tweak) != 2:
            exit(0) 

        self.t = [None]*3
        self.t[0], self.t[1] = tweak[0], tweak[1]
        self.t[2] =  tweak[0] ^ tweak[1]
        self.blockSize = blockSize or cts.BLOCK_SIZE_BITS_512

        #nr is the total number of rounds 
        self.nr = nr or cts.ROUNDS_76

        #nw is the total number of words 
        self.nw  = int(blockSize/64)
        self.mode = mode

        #c_bloc is the bloc of bytes to cipher
        self.c_bloc = c_bloc[0:len(c_bloc)]       

        #generation of the first round's sub key calculated by the key and tweak 
        self.sub_key = key[0:len(key)]
        self.k = key

        # k is the copy ot the originate key used by key_update()
        for i in range(self.nw-3):
            self.sub_key[i] = key[i]
        self.sub_key[self.nw-3] = ( self.k[self.nw-3] + self.t[0] ) % 2**64
        self.sub_key[self.nw-2] = ( self.k[self.nw-2] + self.t[1] ) % 2**64
        self.sub_key[self.nw-1] = self.k[self.nw-1] 
        #calculate k (n+1)        
        
        k_add = self.k[0]
        for i in range(1,self.nw):
            k_add = k_add^self.k[i]
        self.k.append(k_add^cts.EXTENDED_KEY_SCHEDULE_CONST)
        
        if self.nw == 4:
            self.pi = cts.PI4_NW_4
            self.rpi = cts.RPI4_NW_4
            self.r = cts.R4_4_4
        elif self.nw == 8:
            self.pi = cts.PI8_NW_8
            self.rpi = cts.RPI8_NW_8
            self.r = cts.R8_8_8
        elif self.nw == 16:
            self.pi = cts.PI16_NW_16
            self.rpi = cts.RPI16_NW_16
            self.r = cts.R16_16_16
        
        self.depth = cts.DEPTH_OF_D_IN_R
        self.t[0], self.t[1] = tweak[0], tweak[1]
        self.t.append(tweak[0]^tweak[1])

        self.nk = nr/4 + 1

      
    def mix(self, r_x, r_y, np):
        np*=2
        self.c_bloc[np] = (self.c_bloc[np] + self.c_bloc[np+1])%(2**64)
        self.c_bloc[np+1] = self.c_bloc[np]^ (util.rotl(self.c_bloc[np+1], self.r[r_x % self.depth][r_y]))


    def demix(self, r_x, r_y, np):
        np*=2
        self.c_bloc[np+1] = (self.c_bloc[np+1]^self.c_bloc[np]  )%(2**64)
        self.c_bloc[np+1] = util.rotr(self.c_bloc[np+1], self.r[r_x % self.depth][r_y])
        self.c_bloc[np] = (self.c_bloc[np] - self.c_bloc[np+1])%(2**64)

    # update the subkey (executed after the end of one round's calculation) for the next round
    def key_update(self, c_round):
        for i in range(self.nw-3):
            self.sub_key[i] = self.k[(int(c_round/4)+i)%(self.nw+1)]
        self.sub_key[self.nw-3] = ( self.k[(int(c_round/4)+self.nw-3)%(self.nw+1)] + self.t[int(c_round/4)%3] ) % (2**64)
        self.sub_key[self.nw-2] = ( self.k[(int(c_round/4)+self.nw-2)%(self.nw+1)] + self.t[(int(c_round/4)+1)%3] ) % (2**64)
        self.sub_key[self.nw-3] = ( self.k[(int(c_round/4)+self.nw-3)%(self.nw+1)] + int(c_round/4) ) % (2**64)
    
    def diminution(self):
        for i in range(len(self.c_bloc)):
            self.c_bloc[i] = (self.c_bloc[i] - self.sub_key[i] )%(2**64)

    def addition(self):
        for i in range(len(self.c_bloc)):
            self.c_bloc[i] = (self.c_bloc[i] + self.sub_key[i] ) %(2**64)
        
    def permutation(self):
        tmp = self.c_bloc[0:len(self.c_bloc)]
        for i in range(self.nw):
            self.c_bloc[i] = tmp[self.pi[i]]

    def depermutation(self):
        tmp = self.c_bloc[0:len(self.c_bloc)]
        for i in range(self.nw):
            self.c_bloc[i] = tmp[self.rpi[i]]
    
    def get_blocs(self):
        print(self.c_bloc)

    def get_keys(self):
        print(self.sub_key)


def cipher_threefish_blocs(mode,c_blocs, keys, blocksize, nr, tweaks):
    cipher_blocs=[]
    cipher = []
    for k in range(len(c_blocs)):
        cipher.append(cipher_threefish (blocksize, nr, keys, tweaks, mode, c_blocs[k]))

        if (mode == cts.MODE_CBC):
            for w in range(nw):
                if(k == 0):
                    cipher[k].c_bloc[w]^=iv[w] 
                else:
                    cipher[k].c_bloc[w]^=cipher[k-1].c_bloc[w]

        #and for each bloc k to cipher 
        for i in range(nr+1):
            # for each round 
            if(i>0 and i<77):
                for b in range( int(cipher[k].nw/2)):
                    cipher[k].mix(r_x,r_y,b)
                cipher[k].permutation()
    
            if(i%4 == 0):
              cipher[k].key_update(i)
              cipher[k].addition()

        cipher_blocs.append(cipher[k].c_bloc)
    return  cipher_blocs

def decipher_threefish_blocs(mode,c_blocs, keys, blocksize, nr, tweaks):
    cipher=[]
    for i in range(len(c_blocs)):
        cipher.append(cipher_threefish (blocksize, nr, keys, tweaks, mode, c_blocs[i]))
    
    #start to decipher each bloc
    for k in range(len(c_blocs)-1,-1,-1):    
        for i in range(nr,-1,-1):


            if(i%4==0):
                cipher[k].key_update(i)
                cipher[k].diminution()
            if(i>0 and i<77):
                cipher[k].depermutation()
                for b in range(int(cipher[k].nw/2)):
                    cipher[k].demix(r_x,r_y,b)   

        # if on mode CBC, we xor with the precedent ciphered blocs
        if (mode == cts.MODE_CBC):
            for w in range(nw):
                if (k==0):
                    cipher[k].c_bloc[w]^=iv[w] 
                else:
                    cipher[k].c_bloc[w]^=cipher[k-1].c_bloc[w]

    for i in range(len(cipher)):
        c_blocs[i]=cipher[i].c_bloc
    return c_blocs

def decipher_threefish_file(filename,mode):
    fo = open(filename,"r")
    str1=fo.read()
    fo.closed

    blocs_list=str1.split('0b')
    c_blocs  = []
    tmp_list = []
    for i in range(1,len(blocs_list)):
        tmp_list.append(int(blocs_list[i],2))
        if (i%4 == 0 ):    
            c_blocs.append(tmp_list)
            tmp_list=[]    

    #set iv 
    if ( nw == 4 ) : iv = cts.INITIAL_VECTEUR_4 
    elif (nw == 8 ) : iv = cts.INITIAL_VECTEUR_8 
    elif (nw == 16 ) : iv = cts.INITIAL_VECTEUR_16 

    #generation of initials list of keys, nb_keys in a round = nb of messages in a bloc = blocksize / messagesize  
    keys= key_generation(nb_key)

    #c_blocs= util.readFile(filename, blocksize)
    c_blocs = decipher_threefish_blocs(mode,c_blocs, keys, blocksize, nr, tweaks)

    fo = open(filename,"w")
    fo.write(util.writeMsg(c_blocs))
    fo.close()

def cipher_threefish_file(filename,mode):
    #set iv 
    if ( nw == 4 ) : iv = cts.INITIAL_VECTEUR_4 
    elif (nw == 8 ) : iv = cts.INITIAL_VECTEUR_8 
    elif (nw == 16 ) : iv = cts.INITIAL_VECTEUR_16 

    #generation of initials list of keys, nb_keys in a round = nb of messages in a bloc = blocksize / messagesize  
    keys = key_generation(nb_key)

    c_blocs = util.readFile(filename, blocksize)
    c_blocs = cipher_threefish_blocs(mode,c_blocs, keys, blocksize, nr, tweaks)
    
    #util.writeFile(filename, c_blocs)
    str1=""
    for i in range(len(c_blocs)):
        for j in range(nw):
            str1+=str(bin(c_blocs[i][j]))
    
    fo = open(filename,"w+")
    fo.write(str1)
    fo.close()

def cipher_threefish_msg(msg,mode):
    #set iv 
    if ( nw == 4 ) : iv = cts.INITIAL_VECTEUR_4 
    elif (nw == 8 ) : iv = cts.INITIAL_VECTEUR_8 
    elif (nw == 16 ) : iv = cts.INITIAL_VECTEUR_16 

    #generation of initials list of keys, nb_keys in a round = nb of messages in a bloc = blocksize / messagesize  
    keys= key_generation(nb_key)

    #get blocs from files 
    c_blocs= util.readMsg(msg,blocksize)
    c_blocs = cipher_threefish_blocs(mode,c_blocs, keys, blocksize, nr, tweaks)
    
    str1=""
    for i in range(len(c_blocs)):
        for j in range(nw):
            str1+=str(bin(c_blocs[i][j]))
    return str1

def decipher_threefish_msg(msg,mode):
    blocs_list=msg.split('0b')
    c_blocs, tmp_list = [], []
    for i in range(1,len(blocs_list)):
        tmp_list.append(int(blocs_list[i],2))
        if (i%4 == 0 ):    
            c_blocs.append(tmp_list)
            tmp_list=[]    
    

    #set iv 
    if ( nw == 4 ) : iv = cts.INITIAL_VECTEUR_4 
    elif (nw == 8 ) : iv = cts.INITIAL_VECTEUR_8 
    elif (nw == 16 ) : iv = cts.INITIAL_VECTEUR_16 

    #generation of initials list of keys, nb_keys in a round = nb of messages in a bloc = blocksize / messagesize  
    keys= key_generation(nb_key)

    #c_blocs= util.readFile(filename, blocksize)
    c_blocs = decipher_threefish_blocs(mode,c_blocs, keys, blocksize, nr, tweaks)

    decipher_text=util.writeMsg(c_blocs)
    return decipher_text



