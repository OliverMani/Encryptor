import randomness as random
import string

def makeRandomPassword(length=20):
	pwd = ""
	for x in range(length):
		pwd += chr((random.generateRandomByte() % 94)+32)
	return pwd

def removeChars(chars, word):
	return ''.join(list(filter(lambda x: x not in chars, word)))

# TODO:
# Check for more patterns
#
def check(_file, password):
	file = open(_file, 'r')
	passwords = file.read().split('\n')
	file.close()

	password = password.lower()

	for x in [x.lower() for x in passwords]:
		if x == password:
			return False
		
		if (removeChars('0123456789', password) == x or '') or (removeChars(' ', password) == x or '') or (removeChars('0123456789 ',password) == x or ''):
			return False
		if ' ' in password:
			for x in password.split(' '):
				if not check(_file, x):
					return False
	
	return True




def checkIfPasswordIsSafe(password):
	if password == '' or None:
		return {'safe':False, 'message':'You didn\'t type a password!'}
	if len(password) < 18:
		return {'safe':False, 'message':'Your password is short, you should make it at least 18 characters long!'}
	if removeChars(string.ascii_lowercase, password.lower()) == '':
		return {'safe':False, 'message':'The password contains only letters'}
	if removeChars('0123456789', password) == '':
		return {'safe':False, 'message':'The password contains only numbers'}
	if removeChars(string.ascii_lowercase + '0123456789', password.lower()) == '':
		return {'safe':False, 'message':'The password contains only letters and numbers'}
	#if not check('res/dictionary/english.txt', password):
	#	return {'safe':False, 'message':'This password contains a word!'}
	#if not check('res/dictionary/popular_passwords.txt', password):
	#	return {'safe':False, 'message':'This password can be cracked instantly!'}
	return {'safe':True, 'message':'Safe!'}

# testing
if __name__ == '__main__':
	print(checkIfPasswordIsSafe(input("Type in a password: ")))