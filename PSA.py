#============================================================
# AUTHORS
#============================================================

# Developed by: Damien Santiago and Christian Grey
# Contributers: Dr. Micah Fogel, Karrick McGinty, Black Barth, Matias Habib, 
# Developed on: October 21, 2020
# Version: 2.0
#
# >>> CHANGE LOG <<<
# total haul on quality of life for installation and code
# Technical Update:
#   - implementation of blum blum shub for cryptographically secure rng
# 
# Fun Updates:
#   - hex encoded keyfiles and keyfile import for reusing keys

#============================================================
# IMPORTS
#============================================================

import random
import math
from string import *
import os
import sys
import subprocess
import pynput
import socket
import rsa
import time
import pynput
import base64
import collections
from setuptools import setup
import hashlib

#============================================================
# CODE
#============================================================

'''
    Seed and Modulus values set default are for the Blum Blum Shub CSPNRG please do not use them in your independant implementation
    just for example purposes. If unticked, PSA will randomly generate independant values for you!
'''

# seed = 98058445173086425756314187824313391486180662632889614754131257593545951737971062379741943235654043964079243314126236092913014213810923267556235475713935022945422040099754359751989355864972588364689418164397488413271523516014666767717107749717928041678001339600059284372771209934489312144341115780543113599761
# modulus = 15131416176989085005365668501879732381707739602907189245350150478220468373854166874564322659519626133766412529183909428266816269856013081895945137451660065988850394079959890009540335771649899467755972642385135871987676558912450138244026325397032062687033850411711805106582969428796308677911138034360356944293256292903151132612978861526109474790893203579295827073738964858495822829930652023996860916310034441092270061707676561946156727426853869993261457162567864919641527333324773563442024791393128611452276275769596486881335192428748339780162866169720171239119564628527486381606946139640924193802833510784625061031997

seed = 0
modulus = 0

acceptedCharacters = ascii_letters + digits + punctuation + " "

class util:

    """The code for prime generation was taking from 
    https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb 
    and slightly modified for coherence and the process of making comments. Much respect to 
    the author of the article. """

    def prime(number, k=128): # determines primality with k number of passes through rabin miller. 128 by default.

        if number == 2 or number == 3: # inital checks for prime numbers 2 and three 
            return True
        if number <= 1 or number % 2 == 0:
            return False
        # find exponent s and base d for 2^s*d-1 = 1mod(n)
        exponent = 0
        base = number - 1 
        while base & 1 == 0:
            exponent += 1 # this satisfies the subsequent exponent for 2^s*d-1 = 1mod(n) such that d is the 
            base //= 2 # finds the mid point of the main number minus 1, which finds the base or d value for rabin miller
        # do k tests
        for _ in range(k): # iterate through the rabin miller test 128 times to determine primality
            fermatWitness = random.randrange(2, number - 1) # select a fermat witness
            testResult = pow(fermatWitness, base, number) # pow(x,y,z) such that it returns x^ymod(z). This tests for modular congruence to +-1 which will tell if a number is prime or not base on fermat witness 
            if testResult != 1 and testResult != number - 1:
                j = 1
                while j < exponent and testResult != number - 1:
                    testResult = pow(testResult, 2, number)
                    if testResult == 1:
                        return False
                    j += 1
                if testResult != number - 1:
                    return False    
                    
        return True

    def generatePrimeCandidate(length): # generate a possible prime number

        p = random.getrandbits(length) # generate random bits
        p |= (1 << length - 1) | 1  # apply a mask to set MSB and LSB to 1
        return p

    def generatePrimeNumber(length=1024): # generate prime with length of requested bits
        p = 4
        # keep generating while the primality test fail
        while not util.prime(p, 128):
            p = util.generatePrimeCandidate(length)
        return p

    def randomNumber(length = 128): # cool random function

        mouse = pynput.mouse.Controller()

        if length > 128: # the function can produce longer strings, but in general 128 is fine

            print("Please enter a number length 128 digits or lower")
            exit()
        
        else:

            mouseX = mouse.position[0] # grabbing of x position for mouse
            mouseY = mouse.position[1] # grabbing of y position for mouse

            SystemTime = int(str(time.time())[11:15]) # slice from milliseconds in system time float
            SystemTime2= int(str(time.time())[12:16]) # slice from milliseconds but transpose by one number

            # system slice 1 = s1
            # system slice 2 = s2
            # mouseX = X
            # mouseY = Y
            # ((X+s1)xor(s2))^((Y+s1)xor(s2))

            RandomNumber = str(pow((mouseX+SystemTime)^SystemTime2,(mouseY+SystemTime)^SystemTime2))[:length] # perform function as stated above and slice to the first 128 numebers
            
        return int(RandomNumber)

    def coPrime(a, b): # determine if two numbers a and b are coprime
        if math.gcd(a,b) == 1: # if the greatest common denominator is 1, then the numbers are coprime
            return True
        else:
            return False

    def randomListSelection(List): # generate secure random selection from a list with Blum Blum Shub and modulus of the list length

        if type(List) == list:

            return List[BBS.BlumBlumShub()%len(List)]
        
        else:

            return TypeError 

class BBS:

    def generateSeed(p,q): # this function generates a proper seed that is coprime to large (1024bit) primes p and q

        while True:

            s = util.randomNumber(128) # generate random number with mouse and xor

            if util.coPrime(s,p) and util.coPrime(s,q): # determine if generated number is coprime to p and q

                return s

            else:  # if the seed isn't coprime, then regenerate it and test it's coprimality 

                BBS.generateSeed(p,q)

    def generateValues(): # generate modulus and seed

        while True:

            p = util.generatePrimeNumber(1024) # generate p and q values that are 1024 bits
            q = util.generatePrimeNumber(1024)

            if p!=q: # check if they are equal 

                if p % 4 == 3 and q % 4 == 3: # if both p and q are congruent to 3mod(4)
                    
                    # seed = BBS.generateSeed(p,q) # generate seed
                    seed = util.generatePrimeNumber(1024)
                    modulus = p * q # multiply p and q for modulus
                    break 

                else: # regenerate p and q

                    pass
            
            else: # regenerate p and q
                
                pass

        file = open("values.txt","a")
        file.write(str(modulus))
        file.write("\n")
        file.write(str(seed))
        return modulus, seed # return modulus and seed

    def BlumBlumShub(): # generate a single number using blum blum shub

        global modulus
        global seed

        if modulus == 0 or seed == 0:
            modulus, seed = BBS.generateValues() # generate modulus and seed for blum blum shub rng generation
            return BBS.BlumBlumShub()
        else:
            data = [] # list to store least common bit of generated integers

            for i in range(10): # generate 10 bits and store them into data list

                seed = pow(seed,2)%modulus # a recursive for BBS generation
                binary = bin(seed).replace("0b","") # filtering of integer to binary 
                binaryCollection = collections.Counter(binary) # creates a dictionary for the number of letters and their frequency
                leastCommonBit = int(min(binaryCollection,key=binaryCollection.get))
                data.append(leastCommonBit) # returns the least common value of the dictionary values and their respective key

            result = int("".join(str(x) for x in data), 2) #joining of all data to an integer

            return result

class keyGeneration:

    '''haha this isn't finished, not even close'''

    def decodeKeyFile(keyFile): # a function for decoding the hex encoded files line by line

        decoded = [] # a list for storing decoded lines 

        for line in open(keyFile,"r").readlines(): # iterate through each line

            temp = [] # a temporary reference for storing the idividual cecoded characters of each line

            for character in line.replace("\n","").split(" "): # condense and trim newline for indiviual characters and iterate through them

                temp.append(''.join(chr(int(character,16)))) # append the decoded characters to temporary reference

            decoded.append("".join(temp)) # join the temporary reference for the decoded line to the final list after joining all elements from temporary reference

        return decoded

    def validateKeyfile(keyFile): # a function to check for repeated lines in keyfiles, if no repeated lines then the file is validated

        try: 
        
            validated = False # a boolean to set if a file is validated 
            stringsSet = set() # set for faster iteration
            for line in open(keyFile, "r"):
                if line in stringsSet: # if there is a copycat line, flag false and return it
                    validated = False
                    return validated
                else:   
                    validated = True
                stringsSet.add(line) # add line to seen lines

            return validated

        except FileNotFoundError: # if the files not found the file can't be validated

            print("Requested File for Validation not found")
            return validated 

    def generateStringKey(stringLength,blockHeight,numberOfVariableVariants): # a function to generate the string key

        variables = keyGeneration.generateVariables(numberOfVariableVariants) # a list of generated variables with requested variants
        RSNSCharacters = list(ascii_letters + digits + punctuation) # a list of all possible characters to select from for string generations

        StringKey = open("STRKEY.txt","a") 
        numberOfGeneratedStrings = 0 # instance for referencing number of generated strings
        totalNumberOfStrings = int(len(variables))*blockHeight # instance for the total number of required strings

        for i in range(int(len(variables)*blockHeight)): # for the required number of strings

            generatedString = str(' '.join(hex(ord(util.randomListSelection(RSNSCharacters))).replace("0x","") for i in range(stringLength)))+"\n" # generate a randomly generated hex encoded string
            percentageOfKeyCompletion = str(int(float(numberOfGeneratedStrings/totalNumberOfStrings)*100)) # a percentage for the number of strings generated to those required
            print("Generating Key: {}% Done".format(percentageOfKeyCompletion), end='\r') # print completion of key
            numberOfGeneratedStrings += 1 # increment the number of strings generated by 1
            StringKey.write(generatedString) # write generated encoded string to file
    
        # Key file validation for string repeats
        if keyGeneration.validateKeyfile("STRKEY.txt"): # fully validate key and complete function
    
            print("String Key Generated and Validated")
            StringKey.close()

        else:

            keyGeneration.generateStringKey(stringLength,blockHeight,numberOfVariableVariants)

    def generateVariables(numberOfVariableVariants): # a function to generate the sample size for random variable selection later on, i.e. generates the idividual variables themselves

        variables = [] # a storage for generated variables, also global

        # using ONLY ascii letters to iterate and define variables like A1 - z5 which should create 52x number of variables since there are 52 characters in ascii.letters
        for letter in ascii_letters:

            # indexing through the letters to effectively multiply out the iteration operation x number of times for x number of variants
            for index in range(1,numberOfVariableVariants+1):

                # a tuple used to join the letter iteration and index of iteration through a join method
                variableSeqence = (letter,str(index))
                
                # appending of joined variable to variable library which will be used later for generating equations
                variables.append("".join(variableSeqence))
        
        return variables

    def generateEquationsKey(numberOfVariableVariants,equationLength): # a function to generate the equations key

            numberOfGeneratedEquations = 0 # an instance for counting generated equations
            totalNumberOfEquations = len(list(acceptedCharacters)) # a constant for the total number of required equations

            variables = keyGeneration.generateVariables(numberOfVariableVariants) # a reference for variables to select from 
        
            equationKey = open("EQKEY.txt", "a") 
                
            print("Generating Equation file")

            equations = [] # list for plain generated equations

            # generate an equation for each accepted character for PSA
            for character in acceptedCharacters: 

                equations.append("+".join(util.randomListSelection(list(variables))for i in range(equationLength))+"\n") # append a random equation generated with Blum Blum Shub

            # generate an encoded string for the key file
            for equation in equations:

                temp = [] # temporary reference for encoded bytes
                percentageOfKeyCompletion = str(int(float(numberOfGeneratedEquations/totalNumberOfEquations)*100)) # percentage of generated equations to required ones

                # iterate through each equation and encode the individual bytes
                for character in equation: 
                    
                    temp.append(hex(ord(character)).replace("0x",""))
                
                temp.pop() # this is used to delete the "a" in the ends of the temporary instance for each equation
                numberOfGeneratedEquations += 1 # iterate for each equation encoded
                print("Generating Key: {}% Done".format(percentageOfKeyCompletion), end='\r') # print out progress
                equationKey.write(str(" ".join(temp))+"\n") # write encoded data to key file
    
    def signKeys(keyA,keyB): # a function to validate and sign a key pair in a way so they are linked together 
        
        Key1 = keyGeneration.decodeKeyFile(keyA) 
        Key2 = keyGeneration.decodeKeyFile(keyB)

        signature = str(time.time())[11:16]

        for i in range(5):

            signature += str(Key1[i]).replace("+","").join(Key2[i])

        signature = signature.encode()

        signature = str(hashlib.sha256(signature).hexdigest())

        keyFile1 = open(keyA,"a")
        keyFile2 = open(keyB,"a")

        keyFile1.write(signature)
        keyFile2.write(signature)
        
    def generateKeys(blockWidth,blockHeight,numberOfVariableVariants,equationLength): # a general function to generate the a key pair for PSA

        keyGeneration.generateEquationsKey(numberOfVariableVariants,equationLength)
        keyGeneration.generateStringKey(blockWidth,blockHeight,numberOfVariableVariants)

    def checkKeySigatures(A,B): # a function to check if key pair is a proper pair by checking the file signature 

        keyfileA = open(A,"r")
        keyfileB = open(B,"r")
        
        fileASignature = keyfileA.readlines()[-1]
        fileBSignature = keyfileB.readlines()[-1]

        if fileASignature == fileBSignature:

            return True

        else:

            return False

class PSA:

    def loadKeys(EQKEY,STRKEY): # function to load and return dictionaries for the key files

        variableBlock = {} # a dictionary to reference characters and their assigned equations
        setBlock = {} # a dictioanry to reference variables use in equations and lists which hold the possible values for them

        equationKey = keyGeneration.decodeKeyFile(EQKEY) 
        stringKey = keyGeneration.decodeKeyFile(STRKEY)

        numberOfVariableVariants = int(len(str(equationKey[0]).replace("+",""))/2) # this gets the number of variables based on the keyfiles

        variables = keyGeneration.generateVariables(numberOfVariableVariants) # generates a list of variables base on the calculated value from key

        blockHeight = int(len(stringKey)/len(variables)) # calculates the number of variants per variable based on the key file

        blocks = [stringKey[n:n+blockHeight] for n in range(0, len(stringKey), blockHeight)] # groups the file into the indepent blocks

        # if not keyGeneration.checkKeySigatures(EQKEY,stringKey):

        #     print("Keys return as invalid because either key signatures don't match for the pair or they aren't signed...")
        #     return None

        # else:

        # this assigns a dictionary with a key reference to the variables and the idepent blocks sliced earlier
        for i in range(len(variables)): 

            variableBlock[variables[i]]=blocks[i]
        
        # this creates a dictionary with a key reference to the characters like A, b, 4, 1, and the equations for their assignment
        for i in range(len(acceptedCharacters)):

            setBlock[list(acceptedCharacters)[i]] = equationKey[i]

        return variableBlock, setBlock

    def encrypt(input): # a function to encode to base64 and encrypt

        strings, equations = PSA.loadKeys("EQKEY.txt","STRKEY.txt") # load the keys

        encodedBytes = base64.b64encode(str(input).encode("utf-8")) # encoding the input to base64
        encodedStr = str(encodedBytes, "utf-8")

        encryptedBytes = [] # list for encrypted bytes

        # iterate through encoded data
        for character in encodedStr:
            # grab the encrypted byte for encoded data
            for variable in str(equations.get(character)).split("+"):
                # append data to list
                encryptedBytes.append(util.randomListSelection(strings.get(variable)))
        # join data and return
        encrypted = "".join(encryptedBytes)

        return encrypted

    def decrypt(input):

        strings, equations = PSA.loadKeys("EQKEY.txt","STRKEY.txt") # load keys
        stringSize = len(strings.get("a1")[0]) # calulate string size
        equationSize = len(str(equations.get("a")).split("+")) # calculate thw size of the equations

        start = 0 # starting index for slicing the encrypted strings
        end = equationSize*stringSize # end index of slice

        decryptedBytes = [] # list for decrypted bytes

        for i in range(int(len(input)/(equationSize*stringSize))): # iterate through for encrypted slice

            slice = str(input)[start:end] # create a slice to decrypt

            encryptedCharacter = [slice[n:n+stringSize] for n in range(0, len(slice), stringSize)] # split the slice into its substrings
            equationBytes = [] # a list for the individual equation variables

            # iterates through split list and tests if the value exists in the variables possible values
            for string in encryptedCharacter: 

                for key, value in strings.items():

                    if string in value: # if the split value is in possible values, append the key to equationBytes associated with the possible output

                        equationBytes.append(key)

            equation = "+".join(equationBytes) # join all the variables into a proper equations

            start+=equationSize*stringSize # add to slice for next byte to decrypt
            end+=equationSize*stringSize

            # test if equation is exists as a character assignment and if so append it's character 
            for key, value in equations.items(): 

                if equation == value:

                    decryptedBytes.append(key)

        decoded = str(base64.b64decode(str("".join(decryptedBytes))),'utf-8') # the decrypted bytes will be encoded in base64 we need to decode originally encrypted test
        
        return decoded

def interface():

    if os.path.exists("EQKEY.txt") and os.path.exists("STRKEY.txt"):

        userinput = input("What would you like to do (Encrpyt/Decrypt): ")

        if userinput.lower() == "e":

            data = input("Plaintext: ")
            print(PSA.encrypt(data)+"\n")
            interface()


        elif userinput.lower() == "d":

            data = input("Ciphertext: ")
            print(PSA.decrypt(data)+"\n")
            interface()

        elif userinput.lower() == "exit":

            exit()

        else:

            print("You didn't query right! Try again!")
            interface()

    else:

        print("Haha, your keys are having and existential crisis (i.e. they don't exist)")
        exit()

interface()
