from random import randint

class DoubleCryptography:
	def __init__(self, key, xor):
		self.key = key
		self.xor = xor

	def crypt(self, data, encrypt):
		result = []
		for x in range(len(data)):
			if encrypt:
				result.append(ord(data[x]) + self.key[x % len(self.key)])
				result[x] ^= self.xor[x%len(self.xor)]
			else:
				result.append(data[x] ^ self.xor[x%len(self.xor)])
				result[x] -= self.key[x % len(self.key)]
		return result

	def encrypt(self, data):
		return self.crypt(data, True)

	def decrypt(self, data):
		return self.crypt(data, False)

