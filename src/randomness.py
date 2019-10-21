# randomness.py - no seed required

import time

def generateRandomByte():
	begin = time.time()
	i = 0
	while i < 0xFF:
		while time.time() < begin + .05:
			i += 1
	return i & 0xFF

if __name__ == '__main__':
	print([generateRandomByte() for x in range(100)])
