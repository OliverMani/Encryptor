import math
import hashlib

def make_long_hash(sha, len):
	hlen = math.ceil(len / len(sha))
	for x in range(hlen):
		pass

def match(a,b):
	c = 0
	for x in range(min(len(a), len(b))):
		if(a[x] == b[x]):
			print(a[x],end="")
			c+=1
		else:
			print(" ",end="")
	print("\nMatched chars:", c, "out of", max(len(a),len(b)), "characters! (", format(c / max(len(a),len(b))*100, '.2f'), "% )")



sha512 = hashlib.sha512()
sha256 = hashlib.sha256()

pwd = b"WrwigvreWfrw124Gwe"

sha512.update(pwd)
sha256.update(pwd)

_sha256 = sha256.hexdigest()
sha256.update(pwd)

print(list(sha256.digest()))

#match(sha512.hexdigest(), _sha256 + sha256.hexdigest())