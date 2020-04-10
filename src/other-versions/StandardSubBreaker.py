import sys
from random import randint, sample
from math import log
from time import time

def main():
    # get program start time
    startTime = time()

    cipherFile = sys.argv[1]
    print(cipherFile)
    cipherText = open(cipherFile).read().lower()
    # find the key for decrypting the cipher text using the log of trigrams and the cipher text
    key = decrypt(cipherText, getGrams())

    writeFile(translate(cipherText, key), cipherFile[: -4] + "-decrypted" + cipherFile[-4:])

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    mapping = ""
    # create a string repesentation of the key mapped to the alphabet and write it to the new key file name
    for i in range(len(alphabet)):
        mapping += alphabet[i] + " = " + key[i] + "\n"
    writeFile(mapping, cipherFile[: -4] + "-key" + cipherFile[-4:])

    # get program finish time and subtract start time to get total run time. Rounded to 3 decimal places
    print(round(time() - startTime, 3))

def writeFile(s, fileName):
    with open(fileName, "w") as f:
        f.write(s)

def decrypt(cipherText, gram):
    key = "abcdefghijklmnopqrstuvwxyz"
    bestScore = 0
    bestKey = ""
    # each outer loop generate a new random key, inner loop switch two letters of the random key
    # keep top score and best key for both the inner and outer loops
    for i in range(8):
        # generate a random arrangement of the alphabet
        key = ''.join(sample(key,len(key)))
        score = 0
        for j in range(10000):
            # switch two letters in the key
            testKey = genKey(key)
            # generate a score with the new key based on how close the translated
            # cipher text is to the english language
            testScore = calScore(gram, translate(cipherText, testKey))
            # record the new score and new key if it is better then the current best
            if testScore > score:
                key = testKey
                score = testScore
        # record the new score and new key if it is better then the current best
        if score > bestScore:
            bestScore = score
            bestKey = key
    return bestKey

# translate the cipher text with the new key
def translate(text, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    # map each letter of the alphabet to the  associated letter of the key
    keyMap = {alphabet[i]:key[i] for i in range(len(key))}
    # using the above mapping translate the cipher text and return it
    return "".join([keyMap[letter] if letter in keyMap else letter for letter in text])

# generate two random numbers between 0 and 25
# switch the letters at those positions of the random key
def genKey(key):
    keyList = list(key)
    first, second = randint(0,25), randint(0,25)
    keyList[first], keyList[second] = keyList[second], keyList[first]
    return "".join(keyList)

# loop through the predefined trigrams and their occurrences and create a mapping
def getGrams():
    mapping = {}
    for line in open("../helper-programs/trigrams.txt").read().strip().split("\n"):
        line = line.split(" = ")
        mapping[line[0].lower()] = float((line[1]))
    return mapping

# loop through the encrypted text file in blocks of 3 letters one letter forward each loop
# if block of letters in trigrams append to list then sum all values of the list
def calScore(grams, text):
    return sum([grams[text[i:i + 3]] for i in range(len(text) - 2) if text[i:i + 3] in grams])

if __name__ == '__main__':
    main()
