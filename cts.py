EXTENDED_KEY_SCHEDULE_CONST = 0x1bd11bdaa9fc1a22 
 
BLOCK_SIZE_BITS_256 = 256
BLOCK_SIZE_BITS_512 = 512
BLOCK_SIZE_BITS_1024 = 1024

ROUNDS_72 = 72
ROUNDS_76 = 76
ROUNDS_80 = 80

WORDS_4 = 4
WORDS_8 = 8
WORDS_16 = 16

MODE_CBC = 1
MODE_ECB = 0 

INITIAL_VECTEUR_4 = [ 0x1bd11bdaa9faaa22,0x1bd11bdaa9fc1a30,0x1b12345aa9fc1a22,0x1bd22bd449fc1a22]
INITIAL_VECTEUR_8 = [ 0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,
                      0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22]
INITIAL_VECTEUR_16 =[ 0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,
                      0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,
                      0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,
                      0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22,0x1bd11bdaa9fc1a22]


TWEAK_VALUES = 3
SUBKEY_INTERVAL = 4
	
NW_4 = 4
PI4_NW_4 = (0, 3, 2, 1)
	
NW_8 = 8
PI8_NW_8 = (2, 1, 4, 7, 6, 5, 0, 3)
	
NW_16 = 16
PI16_NW_16 = (0, 9, 2, 13, 6, 11, 4, 15, 10, 7, 12, 3, 14, 5, 8, 1)
 
RNW_4 = 4
RPI4_NW_4 = (0, 3, 2, 1)

RNW_8 = 8
RPI8_NW_8 = (6, 1, 0, 7, 2, 5, 4, 3)

RNW_16 = 16
RPI16_NW_16 = (0, 15, 2, 11, 6, 13, 4, 9, 14, 1, 8, 5, 10, 3, 12, 7)
 
DEPTH_OF_D_IN_R = 8

R4_4_4 = (
            (5, 56),
#           (36, 28),
            (36, 2),
            (13, 46),
            (58, 44),
            (26, 20),
            (53, 35),
            (11, 42),
            (59, 50)
    )
 
R8_8_8 = (
 			(38, 30, 50, 53),
 			(48, 20, 43, 31),
 			(34, 14, 15, 27),
 			(26, 12, 58, 7),
 			(33, 49, 8, 42),
 			(39, 27, 41, 14),
 			(29, 26, 11, 9),
 			(33, 51, 39, 35)
 	)

R16_16_16 = (
                (55, 43, 37, 40, 16, 22, 38, 12),
                (25, 25, 46, 13, 14, 13, 52, 57),
                (33, 8, 18, 57, 21, 12, 32, 54),
                (34, 43, 25, 60, 44, 9, 59, 34),
                (28, 7, 47, 48, 51, 9, 35, 41),
                (17, 6, 18, 25, 43, 42, 40, 15),
                (58, 7, 32, 45, 19, 18, 2, 56),
                (47, 49, 27, 58, 37, 48, 53, 56),
	)

TEXT_EXTENSION = ['txt', 'text']
