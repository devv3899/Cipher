#!/usr/bin/python3

import sys


def fileExists(fileName):
	try:
		open(fileName, 'rb')
		return True
	except:
		return False

def getNextRandomNum(prevNum):
	return (prevNum * 1103515245 + 12345) % 256

def passwordToSeed(password):
	hash = 0
	for p in password:
		hash = ord(p) + (hash << 6) + (hash << 16) - hash;
	return hash

def main():

	numArgs = len(sys.argv)
	if numArgs != 4:
		print('Invalid number of arguments')
		print('Usage: scrypt password <ciphertext> <plaintext>')
		sys.exit(0)

	password = sys.argv[1]
	inputFileName = sys.argv[2]
	outputFileName = sys.argv[3]

	if not fileExists(inputFileName):
		print('Invalid input file')
		sys.exit(0)

	lastRandom = passwordToSeed(password)
	print('Using seed=' + str(lastRandom))
	writer = open(outputFileName, 'wb')

	with open(inputFileName, "rb") as f:
		b = f.read(1)
		while b:
			c = ord(b)
			lastRandom = getNextRandomNum(lastRandom)
			writer.write(bytes([c ^ lastRandom]))
			b = f.read(1)

		writer.close()


if __name__ == '__main__':
	main()