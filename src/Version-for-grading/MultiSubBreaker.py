import sys
from random import randint, sample
from math import log
from multiprocessing import Process, Queue
from threading import Thread
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
    # a queue object to allow threads and processes to communicate and share data
    scores = Queue()
    processes = []
    # for loop for creating and starting processes. Append them to a list so they can be joined
    for i in range(8):
        # create a process with the genThreads to generate threads
        process = Process(target=genThreads, args=(gram, cipherText, scores))
        processes.append(process)
        process.start()
    # for each process created join them so the main process wont complete until all
    # the sub processes complete
    for process in processes:
        process.join()

    bestKey = ""
    bestScore = 0
    # loop through the queue and check which high score is the best then return the key associated with it
    for i in range(scores.qsize()):
        score = scores.get()
        if score[0] > bestScore:
            bestScore, bestKey = score[0], score[1]
    return bestKey

def genThreads(gram, cipherText, scores):
    threads = []
    # for loop for creating and starting threads. Append them to a list so they can be joined
    for j in range(2):
        # create a thread with the testKey as the target to find the best key from the random key
        # by switching two letters and generating a score
        thread = Thread(target=testKeys, args=(gram, cipherText, scores))
        threads.append(thread)
        thread.start()
    
    # for each process created join them so the main process wont complete until all
    # the sub processes complete
    for thread in threads:
        thread.join()

# each thread created will generate a random key, then loop changing two letters each time
# and calaulate a score. Keep the best score and key
def testKeys(gram, cipherText, scores):
    score = 0
    key = "abcdefghijklmnopqrstuvwxyz"
    # generate a random arrangement of the alphabet
    key = ''.join(sample(key,len(key)))
    for j in range(5000):
        # switch two letters of the new key
        testKey = genKey(key)
        # generate a score with the new key based on how close the translated
        # cipher text is to the english language
        testScore = calScore(gram, translate(cipherText, testKey))
        # record the new score and new key if it is better then the current best
        if testScore > score:
            key, score = testKey, testScore
    # put the best score and key in the queue
    scores.put([score, key])

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
