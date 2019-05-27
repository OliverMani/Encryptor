from tkinter import *
from tkinter.ttk import Frame, Button, Style, Label, Entry, Treeview, Scrollbar
from tkinter.filedialog import askopenfilename
from cryptography import Cryptography, DoubleCryptography

import key_generator as kg
import randomness as random
import main
import os
import ntpath
import gui.dialogs.input_dialog as inp
import _io_.fileutils as fileutils

randomSalt = lambda: main.toString([random.generateRandomByte() for x in range(10)])
getFileName = lambda _: ntpath.split(_)[1] or ntpath.basename(ntpath.split(_)[0])
toHex = lambda _: bytes(main.toString(_), 'utf-8').hex() if type(_) is str else bytes(_).hex()

IMAGES_EXTENTION = ['png','jpg','jpeg','gif']

class BrowserWindow(Frame):

	def mkkey(self, length, salt=''):
		return kg.generateKeysOutOfPassword(self.password, length, salt=salt)

	def initUI(self):
		#self.master.overrideredirect(True)
		frame = Frame(self, relief=RAISED, borderwidth=1)
		frame.pack(fill=BOTH,expand=True)
		self.tree = Treeview(frame)

		self.selected = None
		self.files = {}

		self.tree.bind("<<TreeviewSelect>>", self.onTreeSelect)

		self.tree["columns"] = ("type", "uploaded", "modified")
		self.tree.heading("#0", text="Filename")
		self.tree.column("#0", minwidth=250)
		self.tree.heading("type", text="Type of file")
		self.tree.column("type", width=90)
		self.tree.heading("uploaded", text="Uploaded")
		self.tree.column("uploaded", width=120)


		self.refresh()

		x = Scrollbar(self, orient='horizontal', command=self.tree.xview)
		y = Scrollbar(self, orient='vertical', command=self.tree.yview)

		self.tree.configure(yscroll=y.set, xscroll=x.set)


		# TODO
		# Program texteditor window and open it when you create a file
		create = Button(self, text="Create a text file", command=lambda: inp.getStringInput(title='Filename', message='Type in file name:', onenter=lambda i: self.createFile(i, refresh=True)))
		create.pack(side=LEFT, padx=6, pady=6)
		upload = Button(self, text="Upload file", command=lambda: self.uploadFile(askopenfilename()))
		upload.pack(side=LEFT, padx=6, pady=6)
		openf = Button(self, text="Open file", command=lambda: self.loadEncryptedFile(self.getEncryptedFileName(self.selected)))
		openf.pack(side=LEFT, padx=6, pady=6)

		self.tree.pack(fill=BOTH,expand=True)


	def __init__(self, password):
		super().__init__()
		self.password = password
		self.style = Style()
		self.style.theme_use("default")
		self.master.title("Encryptor")

		width = 500
		height = 670
		x = (self.master.winfo_screenwidth() // 2) - (width // 2)
		y = (self.master.winfo_screenheight() // 2) - (height // 2)

		self.master.geometry("{}x{}+{}+{}".format(width, height, x, y))
		#self.master.resizable(False, False)
		
		#filename = askopenfilename()
		#self.uploadFile(filename)

		self.initUI()

		self.pack(fill=BOTH, expand=True)

		
		self.master.mainloop()

	# creates a file inside the "data" folder
	def createFile(self, realname, refresh=False):
		if realname == None:
			return

		salt = randomSalt()

		keys = self.mkkey(len(realname), salt)
		crypto = DoubleCryptography(keys['pad'], keys['xor'])
		name = toHex(crypto.encrypt(getFileName(realname)))

		del keys
		del crypto

		# if the file name does already exist in the os file system then we want to pick another name by running this function again
		if os.path.isfile('data/' + name):
			return self.createFile(realname)

		keys = self.mkkey(10)
		crypto = Cryptography(keys['pad'])

		encryptedSalt = crypto.encrypt(salt)

		with open('data/' + name, 'wb') as file:
			file.write(bytes(encryptedSalt))

		del salt
		del encryptedSalt
		del crypto

		if refresh:
			self.refresh()

		return name

	def getSaltOfFile(self, file):
		if not main.isHexOnly(file):
			return
		keys = self.mkkey(10)
		crypto = Cryptography(keys['pad'])

		f = open('data/' + file, 'rb')
		encryptedSalt = f.read(10)
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

		keys = self.mkkey((len(realname)//2)+1, salt)
		crypto = DoubleCryptography(keys['pad'], keys['xor'])
		
		name = main.toString(crypto.decrypt(bytes.fromhex(realname)))

		del keys
		del crypto

		self.files[name] = realname

		return name

	# ???
	def getEncryptedFileName(self, decrypted):
		return self.files.get(decrypted)

	def uploadFile(self, path):
		if path == "" or path == None:
			return
		filename = self.createFile(getFileName(path))

		
		read = open(path, 'rb')
		data = read.read()
		read.close()

		salt = self.getSaltOfFile(filename)
		keys = self.mkkey(len(data) % kg.MAX, salt)
		crypto = DoubleCryptography(keys['pad'], keys['xor'])
		del keys
		encrypted = crypto.encrypt(data)

		# clean up memory
		del data
		del read
		del crypto

		with open('data/' + filename, 'ab') as write:
			write.write(bytes(encrypted))
		del encrypted

		self.refresh()


	def loadEncryptedFile(self, realname):
		if realname == None:
			return
		salt = self.getSaltOfFile(realname)
		file = open('data/' + realname, 'rb')
		data = file.read()[10:]
		file.close()
		keys = self.mkkey(len(data), salt)
		crypto = DoubleCryptography(keys['pad'], keys['xor'])
		del keys
		decrypted = crypto.decrypt(data)
		del data
		name = self.getDecryptedFileName(realname)
		with open('tmp/' + name, 'wb') as write:
			write.write(bytes(decrypted))
		del decrypted
		del crypto

		fileutils.openFileWithAnotherProgram('tmp/' + name)


	def refresh(self):
		self.tree.delete(*self.tree.get_children())

		i = 0
		self.files.clear()
		for x in os.listdir('data/'):
			name = self.getDecryptedFileName(x)
			if name != None:
				self.tree.insert("", i, text=name, values=("File"))
				i += 1

	def onTreeSelect(self, event):
		self.selected = self.tree.item(self.tree.focus())['text']


















