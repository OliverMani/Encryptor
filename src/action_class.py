import _cryptography as cryptography
import key_generator as kg
import randomness as random
import main
import os
import ntpath
import _io_.fileutils as fileutils
import math
import config


randomSalt = lambda: main.toString([random.generateRandomByte() for x in range(config.SALT_SIZE)])
getFileName = lambda _: ntpath.split(_)[1] or ntpath.basename(ntpath.split(_)[0])
toHex = lambda _: bytes(main.toString(_), 'utf-8').hex() if type(_) is str else bytes(_).hex()

IMAGES_EXTENSION = ['png','jpg','jpeg','gif']

TYPE_NAMES = {
	'mp4':'Video',
	'mov':'Video',
	'webm':'Video',
	'avi':'Video',
	'png':'Photo',
	'jpeg':'Photo',
	'jpg':'Photo',
	'gif':'Animated\ photo',
	'exe':'Windows\ application',
	'msi':'Windows\ installer',
	'py':'Python\ script',
	'js':'Javascript',
	'html':'HTML\ web\ page',
	'css':'CSS\ file',
	'zip':'ZIP\ file',
	'txt':'Text\ file',
	'mp3':'Audio',
	'ogg':'Audio',
	'wav':'Audio'
}

class ActionClass:

	def mkkey(self, length, salt=''):
		return kg.generateKeysOutOfPassword(self.password, length, salt=salt)

	def __init__(self, password):
		self.password = password
		self.files = {}

	# creates a file inside the "data" folder
	def createFile(self, realname):
		if realname == None:
			return

		salt = randomSalt()

		keys = self.mkkey(len(realname), salt)
		crypto = cryptography.DoubleCryptography(keys['pad'], keys['xor'])
		name = toHex(crypto.encrypt(getFileName(realname)))

		del keys
		del crypto

		# if the file name does already exist in the os file system then we want to pick another name by running this function again
		if os.path.isfile(config.DATA_FOLDER + name):
			return self.createFile(realname)

		keys = self.mkkey(config.SALT_SIZE)
		crypto = cryptography.Cryptography(keys['pad'])

		encryptedSalt = crypto.encrypt(salt)

		with open(config.DATA_FOLDER + name, 'wb') as file:
			file.write(bytes(encryptedSalt))

		del salt
		del encryptedSalt
		del crypto

		

		return name

	def getSaltOfFile(self, file):
		if not main.isHexOnly(file):
			return
		keys = self.mkkey(config.SALT_SIZE)
		crypto = cryptography.Cryptography(keys['pad'])

		f = open(config.DATA_FOLDER + file, 'rb')
		encryptedSalt = f.read(config.SALT_SIZE)
		f.close()

		salt = main.toString(crypto.decrypt(encryptedSalt))

		del crypto
		del keys

		return salt

	def getDecryptedFileName(self, realname):
		if not main.isHexOnly(realname):
			return
		# we need to unlock the salt before we start to decrypt the filename
		salt = self.getSaltOfFile(realname)

		keys = self.mkkey(math.ceil(len(realname)/2), salt)
		crypto = cryptography.DoubleCryptography(keys['pad'], keys['xor'])
		
		name = main.toString(crypto.decrypt(bytes.fromhex(realname)))

		del keys
		del crypto

		self.files[name] = realname

		return name

	def getEncryptedFileName(self, decrypted):
		return self.files.get(decrypted)

	def uploadFile(self, path):
		if path == "" or path == None:
			return



		filename = self.createFile(getFileName(path))
		size = os.path.getsize(path)

		salt = self.getSaltOfFile(filename)
		keys = self.mkkey(min(size-config.SALT_SIZE, config.MAX_KEY_SIZE), salt)
		crypto = cryptography.DoubleCryptography(keys['pad'], keys['xor'])

		del keys
		
		for data in fileutils.readInChunks(path):
			
			encrypted = crypto.encrypt(data)

			# clean up memory
			del data
			
			with open(config.DATA_FOLDER + filename, 'ab') as write:
				write.write(bytes(encrypted))
			del encrypted

		
		del crypto


	def loadEncryptedFile(self, realname, _open=True):
		if realname == None:
			return
		
		size = os.path.getsize(config.DATA_FOLDER + realname)

		name = self.getDecryptedFileName(realname)

		salt = self.getSaltOfFile(realname)

		keys = self.mkkey(min(size-config.SALT_SIZE, config.MAX_KEY_SIZE), salt)

		crypto = cryptography.DoubleCryptography(keys['pad'], keys['xor'])

		del keys
		
		built = 0


		with open(config.TMP_FOLDER + name, 'wb') as file:
			for chunk in fileutils.readInChunks(config.DATA_FOLDER + realname, salted=True):
				decrypted = crypto.decrypt(chunk)
				del chunk
				file.write(bytes(decrypted))
				del decrypted

				built += config.FILE_CHUNK


		del crypto

		if _open:
			fileutils.openFileWithAnotherProgram(config.TMP_FOLDER + name)


	def deleteFile(self, fakename):
		realname = self.getEncryptedFileName(fakename)
		os.remove(config.DATA_FOLDER + realname)

	def renameFile(self, oldfakename, newfakename):
		oldrealname = self.getEncryptedFileName(oldfakename)
		salt = self.getSaltOfFile(oldrealname)

		keys = self.mkkey(len(newfakename), salt)
		crypto = cryptography.DoubleCryptography(keys['pad'], keys['xor'])
		newrealname = toHex(crypto.encrypt(newfakename))

		del keys
		del crypto

		newrealname = config.DATA_FOLDER + newrealname
		oldrealname = config.DATA_FOLDER + oldrealname

		os.rename(oldrealname, newrealname)