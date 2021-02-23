#============================================================
# AUTHORS
#============================================================

# Developed by: Damien Santiago and Christain Grey
# Developed on: October 21, 2020
# Version: 1.1

# >>> CHANGE LOG <<<
#
#

#============================================================
# IMPORTS
#============================================================

import random
import math
import string

#============================================================
# CODE
#============================================================

IDS = []
STRINGS = []
Block = []

LIB_IDS = {} # dictionary to reference the strings
LIB_EQ = {} # dictionary to reference the equations
LIB_BLOCKS = {} # dictionary to reference the blocks

Accepted_Characters = string.ascii_letters + string.digits + " " # Accepts all ascii letters and space


def MakeIDS(NumOfVar):
    
    Letters = string.ascii_letters # covers all standard english letters used in IDs

    for i in range(len(Letters)): # loop for every every letter

        Index = 1 # Create an index instance for the number after the letter

        for j in range(NumOfVar):
            
            IDS.append(str(Letters[i])+str(Index)) # add the created instances to the IDS list to be picked from later
            Index +=1 # Index by one and start over


def MakeStrings(StringLen, NumOfVar):

    RSNS_characters = string.ascii_letters + string.digits#creating possible outcomes for ascii, we include letters numbers and symbols

    for i in range(len(IDS)*NumOfVar):

        STRINGS.append(''.join(random.choice(RSNS_characters) for i in range(StringLen))) #writing of data to key


def MakeBlocks(NumOfVar):

    a = 0
    b = NumOfVar

    for i in range(len(IDS)):
      
        temp = []

        for i in STRINGS[a:b]:

            temp.append(i)

        Block.append(temp)

        a += NumOfVar
        b += NumOfVar


def AssignDefinitions():
    
    try:
    
        n=0

        for i in IDS:

            LIB_BLOCKS[IDS[n]] = Block[n]

            n+=1

    except IndexError:
        pass


def AssignEquations(EqSize):

    try:

        for i in Accepted_Characters:

            LIB_EQ[i] = '+'.join(random.choice(IDS) for i in range(EqSize)) 

    except KeyError:
        pass


def Encrypt(Userin):

    if isinstance(Userin,str):

        encrypted = ''

        for i in Userin:

            for n in LIB_EQ[i].split('+'):

                if n in LIB_BLOCKS:

                    encrypted += random.choice(LIB_BLOCKS[n])

                else:
                    
                    encrypted += ""
                    print('UNSUPPORTED DEFINITION ERROR: String was not encrypted properly due to use of an unssuported character or defnition, please try again')
    
        return encrypted

    else:

        print("UNSUPPORTED INPUT TYPE: PSA on excepts type string")


def Decrypt(Userin):

    if isinstance(Userin,str):

        decrypted = ''
        sliced = []
        eq1 = []
        eq2 = []

        x = 0
        y = len(STRINGS[0])
        a = len(STRINGS[0])

        cnt = 0

        for i in range(0,int(len(Userin)/y)):

            sliced.append(Userin[x:y])

            x += a
            y += a

        for substring in sliced: 

            for key, value in LIB_BLOCKS.items():

                for n in value:

                    if substring == n: 
                        
                        eq1.append(key)
        
        for key in eq1:
            
            cnt +=1

        a = 0
        b = 4

        for key in eq1:

            eq2.append('+'.join(eq1[a:b]))

            a += 4
            b += 4

        eq2 = list(filter(None, eq2))
        
        for equation in eq2:

            for key, value in LIB_EQ.items():

                if equation == value: 
                    
                    decrypted += key

        return decrypted

    else:

        print("UNSUPPORTED INPUT TYPE: PSA only excepts type string")

def init(NumberOfIDS = '5', NumberOfEQ = '4', BlockWidth = '30', BlockHeight = '32' ):

    MakeIDS(NumberOfIDS)
    MakeStrings(BlockWidth,BlockHeight)
    MakeBlocks(BlockHeight)
    AssignDefinitions()
    AssignEquations(NumberOfEQ)

init(4,4,30,32)

# print(IDS, "\n")
# print(STRINGS, "\n")
# print(LIB_BLOCKS, "\n")
# print(LIB_EQ, "\n")
#print(LIB_BLOCKS[LIB_EQ['a'].split('+')[1]][1])
# print(Encrypt("test"))
# print(Encrypt("test"))
# print(Encrypt("test"))
# print(Encrypt("test"))

print(Encrypt('Fuck it ALLL 123'),"\n")
print(Encrypt('Fuck it ALLL 123'),"\n")
print(Encrypt('Fuck it ALLL 123'),"\n")
print(Encrypt('Fuck it ALLL 123'),"\n")

print(Decrypt(Encrypt('Fuck it ALL 123')))