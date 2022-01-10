#!/usr/bin/python3  
# -*- coding: UTF-8 -*-

from   util     import *
from   md5      import *
from   fish     import cipher_threefish_msg
from   fish     import cipher_threefish_file
from   fish     import decipher_threefish_msg
from   fish     import decipher_threefish_file
from   platform import system
import keyboard
import os
import sys

# definition of constants
dictMenu = {
    "Encrypt" : [
        { 
            "ECB" : ["Enter your message:"]
        },
        {
            "CBC" : ["Enter your message:"]
        }
     ],
    "Decrypt" : [
        { 
            "ECB" : ["Enter your message:"]
        },
        {
            "CBC" : ["Enter your message:"]
        }
    ],
}

S = magenta("""\x1b[2JThree Fish\n\n""")

E = magenta("""
Press 'up' and 'down' to choose\nPress 'left' to back and 'right' to next 
Press ESC to exit
""")

message_file_path = 'assets/message.txt'
cipher_file_path = 'assets/cipher_text.txt'
plain_text_file_path = 'assets/plain_text.txt'


M = list(dictMenu)     # F menu
m = []                 # store menus except the F menu, 
n = []                 # store idx which has been chosen by user
idx = 0                # store idx for now, which sign that '=> ' should be at which line
menu = [dictMenu]      # store complete menu
rs = []                # rs answers of user

L = lambda arr: (arr[len(arr) - 1])
F = lambda arr: (arr[0])

def cls(arr):
    while len(arr) > 0:
        arr.pop()

def ask(arr):
    n = len(arr)
    while len(arr) > 0:
        if len(arr) == n:
            rs.append(input('\n-> ' + arr.pop() + '  '))
        else:
            rs.append(input('-> '   + arr.pop() + '  '))
    
# print menu which is m[len(m) - 1] or M
def show():
    s = S
    if len(m) == 0:
        for i in M:
            if M.index(i) == idx:
                s += green('=> ') + cyan(i) + '\n'
            else:
                s += green('   ') + cyan(i) + '\n'
    else:
        for i in m[len(m) - 1]:
            if m[len(m) - 1].index(i) == idx:
                s += green('=> ') + cyan(i) + '\n'
            else:
                s += green('   ') + cyan(i) + '\n'
    s += E
    print(s)

    print("\n\tn:" + str(n))
    print("\n\tm:" + str(m))
    print("\n\tindex:" + str(idx))
    print("\n\trs:" + str(rs))

def init():
    global menu
    
    if len(n) == 1 and len(m) == 0:
        menu.append(L(menu)[M[n[0]]])
        m.append(dechunk([list(i) for i in L(menu)]))
    elif len(n) > len(m):
        t = L(m)[L(n)]
        for i in L(menu):
            if F(list(i)) == t:
                menu.append(i[t])
                m.append(dechunk([list(j) for j in L(menu)]))
        
        if len(n) == 2:
            rs.append(n[1])
            ask([L(L(menu))])
            
            if F(n) == 0:
                ECB_CBC, s = rs
                if ECB_CBC == 0:
                    cipher_str = cipher_threefish_msg(s, cts.MODE_ECB)
                    print(green(cipher_str))
                elif ECB_CBC == 1:
                    print(green(cipher_threefish_msg(s, cts.MODE_CBC)))
            elif F(n) == 1:
                ECB_CBC, s = rs
                if ECB_CBC == 0:
                    print(green(decipher_threefish_msg(s, cts.MODE_ECB)))
                elif ECB_CBC == 1:
                    print(green(decipher_threefish_msg(s, cts.MODE_CBC)))
            #os._exit(0)
            sys.exit()

# listen left
def onLeft():
    global idx
    try:
        m.pop()
        n.pop()
        menu.pop()
        cls(rs)
        idx = 0
        init()
        show()
    except IndexError:
        show()

# listen right
def onRight():
    global idx
    n.append(idx)
    idx = 0
    init()
    show()

# listen up
def onUp():
    global idx
    if idx - 1 < 0:
        idx = (len(M) - 1) if len(n) == 0 else (len(m[len(m) - 1]) - 1)
    else:
        idx = idx - 1
    show()

# listen down
def onDown():
    global idx
    idx =  ((idx + 1) % len(M)) if len(n) == 0 else ((idx + 1) % len(m[len(m) - 1]))
    show()

# print start menu
show()


if system() == 'Windows':
    keyboard.add_hotkey(72, onUp)     # up clicked
    keyboard.add_hotkey(80, onDown)   # down clicked
    keyboard.add_hotkey(75, onLeft)   # left clicked
    keyboard.add_hotkey(77, onRight)  # right clicked
else:
    keyboard.add_hotkey(103, onUp)    # up clicked
    keyboard.add_hotkey(108, onDown)  # down clicked
    keyboard.add_hotkey(105, onLeft)  # left clicked
    keyboard.add_hotkey(106, onRight) # right clicked

# if 'esc' clicked, exit programme
keyboard.wait('esc') 
