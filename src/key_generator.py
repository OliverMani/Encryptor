import math
import hashlib
import config

# modifying this variable's value might mess up the entire decryption system
MAX = config.MAX_KEY_SIZE

# used for testing purposes
def match(a,b):
	c = 0
	for x in range(min(len(a), len(b))):
		if(a[x] == b[x]):
			print(a[x],end="")
			c+=1
		else:
			print(" ",end="")
	print("\nMatched chars:", c, "out of", max(len(a),len(b)), "characters! (", format(c / max(len(a),len(b))*100, '.2f'), "% )")

def generateKeysOutOfPassword(password, length, salt='', unlimited=False):
	if length > MAX and not unlimited: # 1 gb is the max
		raise ValueError("The key size is limited to " + str(MAX) + " bytes, set 'unlimited' to True to create larger keys.")

	hlen = math.ceil(length / 64)

	password = salt + password

	if hlen < 1:
		hlen = 1

	sha256 = hashlib.sha256()
	sha512 = hashlib.sha512()

	pad = []
	xor = []

	for y in range(hlen):
		sha512.update(str.encode(password))
		sha256.update(str.encode(password))
		for x in list(sha512.digest()):
			pad.append(x)

		for x in list(sha256.digest()):
			xor.append(x)

		sha256.update(str.encode(password))

		for x in list(sha256.digest()):
			xor.append(x)

	return {'pad': pad[:length], 'xor': xor[:length]}

# for testing purposes
if __name__ == '__main__':
	keys = generateKeysOutOfPassword("hAYPNTmCkSHOv1OEdfQjTsyvJ3oqUM0KJXLYcqNyYflmJ1uEBNWGouZDVQDnb9TK4ukGZRu9Ur1cWnoIoLbphTPWbl6EPSlErM62", 1024**2)
	match(bytesToString(keys['pad']), bytesToString(keys['key']))