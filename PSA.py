#============================================================
# AUTHORS
#============================================================

# Developed by: Damien Santiago and Christain Grey
# Developed on: October 21, 2020
# Version: 1.2

# >>> CHANGE LOG <<<
# Added comments
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
BLOCKS = []

LIB_IDS = {} # dictionary to reference the strings
LIB_EQ = {} # dictionary to reference the equations
LIB_BLOCKS = {} # dictionary to reference the blocks

Accepted_Characters = string.ascii_letters + string.digits + " " # Accepts all ascii letters and space


def MakeIDS(NumOfVar): # This function adds to list IDS which is a reference to the variables used in substitution
    
    Letters = string.ascii_letters # covers all 52 standard english letters used in IDs

    for i in range(len(Letters)): # loop for every every letter

        Index = 1 # Create an index instance for the number after the letter

        for j in range(NumOfVar):
            
            IDS.append(str(Letters[i])+str(Index)) # add the created instances to the IDS list to be picked from later
            Index +=1 # Index by one and start over

def MakeStrings(StringLen, NumOfVar): # This function produces the string key by taking the number of blocks and creating the number of variants for the blocks

    RSNS_characters = string.ascii_letters + string.digits#creating possible outcomes for ascii, we include letters numbers and symbols

    for i in range(len(IDS)*NumOfVar): # for i in range of the varibles multiplied by the number of variants

        STRINGS.append(''.join(random.choice(RSNS_characters) for i in range(StringLen))) # Writing of strings to string list for reference

def MakeBlocks(NumOfVar):

    a = 0 # Indice for beginning
    b = NumOfVar # top of first range

    for i in range(len(IDS)): # for number of variables
      
        temp = [] # temp list for individual instance of X variants per block

        for i in STRINGS[a:b]: # for i in range of variants per block

            temp.append(i) # add the X number of variants to the temporary instance

        BLOCKS.append(temp) # add individual instance of block to array of blocks

        a += NumOfVar # increment by one block
        b += NumOfVar

def AssignDefinitions(): # Function to assign variables to their blocks
    
    try:
    
        n=0 # Indice for beginning indices in block assignment

        for i in IDS: # for number of variables

            LIB_BLOCKS[IDS[n]] = BLOCKS[n] # setting of variables to block and setting them to dictionary LIB_BLOCKS

            n+=1 # Increment the indice by one block and variable unanimously

    except IndexError:

        print("Index Error: Can't assign deginitions")

def AssignEquations(EqSize):

    try:

        for i in Accepted_Characters: # for each character that is supported 

            LIB_EQ[i] = '+'.join(random.choice(IDS) for i in range(EqSize)) # Select a random varible X amount of times and join them with a +, then set them to their respective equations in a dictionary.

    except KeyError:
        
        print("KeyError: Can't assign Equations")

def Encrypt(Userin):

    if isinstance(Userin,str): # if the input is a string

        encrypted = '' # set instance for reference

        for i in Userin: # for characater in the text input

            for n in LIB_EQ[i].split('+'): # and for variable in character equation 

                if n in LIB_BLOCKS: # if variable has an associated block

                    encrypted += random.choice(LIB_BLOCKS[n]) # select string randomly from the block

                else: # otherwise
                    
                    encrypted += "" # we got nothing
                    print('UNSUPPORTED DEFINITION ERROR: String was not encrypted properly due to use of an unssuported character or defnition, please try again') # Raise an error
    
        return encrypted

    else:

        print("UNSUPPORTED INPUT TYPE: PSA on excepts type string")


def Decrypt(Userin): #isn't currently valid

    if isinstance(Userin,str): # if input is a string

        decrypted = '' # Set instace for reference
        sliced = [] # List reference for sliced encrypted string
        eq1 = [] 
        eq2 = []

        x = 0 
        y = len(STRINGS[0]) # Reference to the length of variants
        a = len(STRINGS[0])

        cnt = 0

        for i in range(0,int(len(Userin)/y)): # for the number of letters in the sliced string

            sliced.append(Userin[x:y]) # append characters in range of slice to sliced list for future reference

            x += a # increment to next slice by referencing the length of sliced strings
            y += a
        # print(len(sliced)/a)
        for substring in sliced: # for slice in list reference

            for key, value in LIB_BLOCKS.items(): # for each block and the values of it's reference in dictionary

                for n in value: # for each value 

                    if substring == n: # if sliced reference is equal to the value
                        
                        eq1.append(key) # append the assigned variable to temporary equation reference
        
        for key in eq1: # for variable in temporary reference
            
            cnt +=1 # increment to count number of variables

        a = 0
        b = 5

        for key in eq1:

            eq2.append('+'.join(eq1[a:b]))

            a += 5
            b += 5
        # print(eq2)
        eq2 = list(filter(None, eq2))
        
        for equation in eq2:

            for key, value in LIB_EQ.items():

                if equation == value: 
                    
                    decrypted += key

        return decrypted

    else:

        print("UNSUPPORTED INPUT TYPE: PSA only excepts type string")

def init(NumberOfIDS, NumberOfEQ, BlockWidth, BlockHeight):

    MakeIDS(NumberOfIDS)
    MakeStrings(BlockWidth,BlockHeight)
    MakeBlocks(BlockHeight)
    AssignDefinitions()
    AssignEquations(NumberOfEQ)

init(5,5,30,32) #5 variants of variables, 5 variables per letter, 30 character long strings, 32 variants per block

Encrypted = Encrypt("test") # encrypting "Test"

print(Encrypted)
print(Decrypt(Encrypted)) # Decrpytion of encrypted string
