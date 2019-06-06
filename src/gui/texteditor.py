from tkinter import *
from tkinter.ttk import Frame, Scrollbar

import _cryptography as cryptography
import key_generator as kg
import config
import main
import math

# TODO:
# Display text

class TextEditor(Tk):
	def __init__(self, file, browser, newfile=False): # fake name
		super().__init__()
		self.title("Editing encrypted file: " + file)
		self.file = file
		self.browser = browser

		name = browser.getEncryptedFileName(self.file)
		with open(config.DATA_FOLDER + name, 'rb') as read:
			self.encryptedSalt = read.read(config.SALT_SIZE)
		del name

		frame = Frame(self,relief=RAISED, borderwidth=1)

		self.text = Text(self)

		self.text.bind('<KeyRelease>', self.onKeyPress)

		scrollX = Scrollbar(self, orient="horizontal", command=self.text.xview)
		scrollX.pack(side=BOTTOM, fill=X)

		scrollY = Scrollbar(self, orient="vertical", command=self.text.yview)
		scrollY.pack(side=RIGHT, fill=Y)

		self.text.pack(fill=BOTH, expand=True)

		self.text.configure(xscrollcommand=scrollX.set)
		self.text.configure(yscrollcommand=scrollY.set)

		if not newfile:
			#self.text.delete(0,END)
			self.text.insert(END, self.readDecryptedText())

		self.mainloop()

	def onKeyPress(self, event):
		self.writeEncryptedText()

	def readDecryptedText(self):
		realname = self.browser.getEncryptedFileName(self.file)
		read = open(config.DATA_FOLDER + realname, 'rb')
		data = read.read()[config.SALT_SIZE:]
		read.close()
		salt = self.browser.getSaltOfFile(realname)
		keys = self.browser.mkkey(min(len(data), kg.MAX), salt)
		del salt
		crypto = cryptography.DoubleCryptography(keys['pad'], keys['xor'])
		del keys
		decrypted = crypto.decrypt(data)
		del crypto

		return main.toString(decrypted)

		

	def writeEncryptedText(self):
		name = self.browser.getEncryptedFileName(self.file)
		text = self.text.get("1.0", "end-1c")
		salt = self.browser.getSaltOfFile(name)
		keys = self.browser.mkkey(len(text) % kg.MAX, salt)

		crypto = cryptography.DoubleCryptography(keys['pad'], keys['xor'])
		del keys
		encrypted = crypto.encrypt(text)

		with open(config.DATA_FOLDER + name, 'wb') as write:
			write.write(bytes(list(self.encryptedSalt) + encrypted))

		del crypto
		del encrypted
		del text


