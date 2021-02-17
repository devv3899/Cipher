#!/usr/bin/python3

import sys

seed = None

def fileExists(fileName):
	try:
		open(fileName, 'rb')
		return True
	except:
		return False

def getNextRandomNum():
	global seed
	seed = (seed * 1103515245 + 12345) % 256
	return seed

def passwordToSeed(password):
	hash = 0
	for p in password:
		hash = ord(p) + (hash << 6) + (hash << 16) - hash;
	return hash

def createInitializationVector():
	return [getNextRandomNum() for _ in range(16)]

def xor(t1, t2):
	return [a ^ b for (a, b) in zip(t1, t2)]

def main():
	global seed
	numArgs = len(sys.argv)
	if numArgs != 4:
		print('Invalid number of arguments')
		print('Usage: scrypt password <cipherText> <plaintext>')
		sys.exit(0)

	password = sys.argv[1]
	inputFileName = sys.argv[2]
	outputFileName = sys.argv[3]

	if not fileExists(inputFileName):
		print('Invalid input file')
		sys.exit(0)

	seed = passwordToSeed(password)
	print('Using seed=' + str(seed))
	writer = open(outputFileName, 'wb')

	with open(inputFileName, "rb") as f:

		cipherText = createInitializationVector()

		lastBlockLength = 0
		b = f.read(16)
		while b or lastBlockLength == 16:

			plaintext = bytearray() if not b else bytearray(b)
			lastBlockLength = len(b)

			# We need to add padding here only
			pad = 16 - len(plaintext)
			while len(plaintext) != 16:
				plaintext.append(pad)

			temp_block = xor(plaintext, cipherText)

			keyStream = [getNextRandomNum() for _ in range(16)]
			for k in keyStream:
				first = (k >> 4) & 0xF
				last = k & 0xF
				temp_block[first], temp_block[last] = temp_block[last], temp_block[first]

			cipherText = xor(temp_block, keyStream)

			for b in cipherText:
				writer.write(bytes([b]))
			b = f.read(16)

		writer.close()


if __name__ == '__main__':
	main()