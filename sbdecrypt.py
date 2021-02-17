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

	lastBlock = None
	with open(inputFileName, "rb") as f:

		cipherText = createInitializationVector()

		# We are sure that now data will be in chunks of 16 bytes.
		b = f.read(16)
		while b:
			
			keyStream = [getNextRandomNum() for _ in range(16)]

			temp_block = xor(bytearray(b), keyStream)

			for k in keyStream[::-1]:
				first = (k >> 4) & 0xF
				last = k & 0xF
				temp_block[first], temp_block[last] = temp_block[last], temp_block[first]

			# If there is block from prev iteration, print it to
			# file now.
			if lastBlock:
				for x in lastBlock:
					writer.write(bytes([x]))
			lastBlock = xor(cipherText, temp_block)

			cipherText = bytearray(b)
			b = f.read(16)

		# We retain the lastBlock, so that we can remove the padding
		lastByte = lastBlock[-1]
		for x in lastBlock[0:16-lastByte]:
			writer.write(bytes([x]))

		writer.close()


if __name__ == '__main__':
	main()