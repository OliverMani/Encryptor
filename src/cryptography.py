class DoubleCryptography:
	def __init__(self, key, xor):
		self.key = key
		self.xor = xor

	def crypt(self, data, encrypt):
		result = []
		for x in range(len(data)):
			char = data[x]
			if type(char) is str:
				char = ord(data[x])
			if encrypt:
				result.append(char + self.key[x % len(self.key)])
				result[x] ^= self.xor[x % len(self.xor)]
				result[x] %= 0x100
			else:
				result.append(char ^ self.xor[x % len(self.xor)])
				result[x] -= self.key[x % len(self.key)]
				result[x] %= 0x100
		return result

	def encrypt(self, data):
		return self.crypt(data, True)

	def decrypt(self, data):
		return self.crypt(data, False)

class Cryptography:
	def __init__(self, key):
		self.key = key

	def crypt(self, data, encrypt):
		result = []
		for x in range(len(data)):

			char = data[x]
			if type(char) is str:
				char = ord(data[x])

			if encrypt:
				result.append((char + self.key[x % len(self.key)]) % 256)
			else:
				result.append((char - self.key[x % len(self.key)]) % 256)
		return result

	def encrypt(self, data):
		return self.crypt(data, True)

	def decrypt(self, data):
		return self.crypt(data, False)