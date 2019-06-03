from tkinter import *
from tkinter.ttk import Frame
from cryptography import DoubleCryptography

import key_generator as kg
import config

# TODO:
# Display text

class TextEditor(Tk):
	def __init__(self, file, browser): # fake name
		super().__init__()
		self.title("Editing encrypted file: " + file)
		self.file = file
		self.browser = browser

		name = browser.getEncryptedFileName(self.file)
		with open('data/' + name, 'rb') as read:
			self.encryptedSalt = read.read(config.SALT_SIZE)
		del name

		frame = Frame(self,relief=RAISED, borderwidth=1)

		self.text = Text(self)

		self.text.bind('<KeyRelease>', self.onKeyPress)

		self.text.pack(fill=BOTH, expand=True)

		self.mainloop()

	def onKeyPress(self, event):
		self.writeEncryptedText()

	def readDecryptedText(self):
		realname = self.browser.getEncryptedFileName(self.file)
		read = open('data/' + realname, 'rb')
		data = read()[config.SALT_SIZE:]
		read.close()
		salt = self.browser.getSaltOfFile(name)
		keys = self.browser.mkkey(len(text) % kg.MAX, salt)
		del salt
		crypto = DoubleCryptography(keys['pad'], keys['xor'])
		del keys
		decrypted = crypto.decrypt(data)
		del crypto

		

	def writeEncryptedText(self):
		name = self.browser.getEncryptedFileName(self.file)
		text = self.text.get("1.0", "end-1c")
		salt = self.browser.getSaltOfFile(name)
		keys = self.browser.mkkey(len(text) % kg.MAX, salt)

		crypto = DoubleCryptography(keys['pad'], keys['xor'])
		del keys
		encrypted = crypto.encrypt(text)

		with open('data/' + name, 'wb') as write:
			write.write(bytes(list(self.encryptedSalt) + encrypted))

		del crypto
		del encrypted
		del text


