from math import log

def count():
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	trigrams = {}

	# generate all prossible trigrams and them the value 0 in a dictionary
	for l in alphabet:
		for le in alphabet:
			for let in alphabet:
				trigrams[l + le + let] = 0

	# loop through the text file and when a trigram encountered increment that trigram by one in the dictionary
	with open("./LargeText.txt", "r") as b:
		book = b.read().lower()
		for i in range(len(book) - 2):
			if book[i:i+3] in trigrams:
				trigrams[book[i:i+3]] += 1

	# find the log of the trigrams
	with open("./trigrams.txt", "w") as f:
		for k, v in reversed(sorted(trigrams.items(), key=lambda item: item[1])):
			if int(v) > 0:
				f.write(str(k) + " = "  + str(log(v)) + "\n")

count()