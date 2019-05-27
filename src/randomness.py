# randomness.py - no seed required

import time

def generateRandomByte():
	begin = time.time()
	i = 0
	while i < 0xFF:
		while time.time() < begin + .005:
			i += 1
	return i & 0xFF