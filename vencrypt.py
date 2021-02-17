#!/usr/bin/python3

import sys


def fileExists(fileName):
	try:
		open(fileName, 'rb')
		return True
	except:
		return False

def readFileBytes(fileName):
	f = open(fileName, 'rb')
	result = []
	b = f.read(1)
	while b:
		result.append(b)
		b = f.read(1)
	return result

def main():

	numArgs = len(sys.argv)
	if numArgs != 4:
		print('Invalid number of arguments')
		print('Usage: vencrypt <keyfile> <plaintext> <ciphertext>')
		sys.exit(0)

	keyFileName = sys.argv[1]
	inputFileName = sys.argv[2]
	outputFileName = sys.argv[3]

	if not fileExists(keyFileName):
		print('Invalid Key file')
		sys.exit(0)

	if not fileExists(inputFileName):
		print('Invalid input file')
		sys.exit(0)

	keyBytes = readFileBytes(keyFileName)
	writer = open(outputFileName, 'wb')

	byteIndex = 0
	keyLength = len(keyBytes)
	with open(inputFileName, "rb") as f:
		b = f.read(1)
		while b:
			rowIndex = ord(b)
			colIndex = ord(keyBytes[byteIndex])

			writer.write(bytes([((rowIndex + colIndex) % 256)]))

			# Increment byteIndex so that we can connect
			# to appropriate key byte
			byteIndex = (byteIndex + 1) % keyLength
			b = f.read(1)

		writer.close()


if __name__ == '__main__':
	main()