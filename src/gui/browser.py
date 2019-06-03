from tkinter import *
from tkinter import messagebox as mbox
from tkinter.ttk import Frame, Button, Style, Label, Entry, Treeview, Scrollbar, Checkbutton
from tkinter.filedialog import askopenfilename
from cryptography import Cryptography, DoubleCryptography

import key_generator as kg
import randomness as random
import main
import os
import ntpath
import gui.dialogs.input_dialog as inp
import _io_.fileutils as fileutils
import gui.texteditor as texteditor
import math
import config


randomSalt = lambda: main.toString([random.generateRandomByte() for x in range(config.SALT_SIZE)])
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

		self.tree["columns"] = ("type", "size")
		self.tree.heading("#0", text="Filename")
		self.tree.column("#0", minwidth=250)
		self.tree.heading("type", text="Type of file")
		self.tree.column("type", width=90)
		self.tree.heading("size", text="File size")
		self.tree.column("size", width=120)


		
		self.onTop = BooleanVar()

		x = Scrollbar(self, orient='horizontal', command=self.tree.xview)
		y = Scrollbar(self, orient='vertical', command=self.tree.yview)

		self.tree.configure(yscroll=y.set, xscroll=x.set)

		

		bline5 = Frame(self, relief=RAISED)
		bline5.pack(side=BOTTOM, fill=BOTH)
		bline4 = Frame(self, relief=RAISED)
		bline4.pack(side=BOTTOM, fill=BOTH)
		bline3 = Frame(self, relief=RAISED)
		bline3.pack(side=BOTTOM, fill=BOTH)
		bline2 = Frame(self, relief=RAISED)
		bline2.pack(side=BOTTOM, fill=BOTH)
		bline1 = Frame(self, relief=RAISED)
		bline1.pack(side=BOTTOM, fill=BOTH)
		


		# TODO
		# Program texteditor window and open it when you create a file
		create = Button(bline1, text="Create file", command=lambda: inp.getStringInput(title='Filename', message='Type in file name:', onenter=lambda i: [lambda:x() for x in [self.createFile(i, refresh=True), texteditor.TextEditor(i, self)]]))
		create.pack(side=LEFT, fill=BOTH, expand=True)
		upload = Button(bline1, text="Upload file", command=lambda: self.uploadFile(askopenfilename()))
		upload.pack(side=LEFT, fill=BOTH, expand=True)
		openf = Button(bline1, text="Open file", command=lambda: self.loadEncryptedFile(self.getEncryptedFileName(self.selected)))
		openf.pack(side=LEFT, fill=BOTH, expand=True)
		edit = Button(bline2, text="Edit file", command=lambda: texteditor.TextEditor(self.selected, self))
		edit.pack(side=LEFT, fill=BOTH, expand=True)
		explorer = Button(bline2, text="System explorer", command=lambda: fileutils.openFolder('data/'))
		explorer.pack(side=LEFT, fill=BOTH, expand=True)
		refresh = Button(bline2, text="Refresh", command=self.refresh)
		refresh.pack(side=LEFT, fill=BOTH, expand=True)
		delete = Button(bline3, text="Delete file", command=lambda: self.deleteFile(self.selected))
		delete.pack(side=LEFT, fill=BOTH, expand=True)
		rename = Button(bline3, text="Rename file") # no command yet
		rename.pack(side=LEFT, fill=BOTH, expand=True)
		cache = Button(bline3, text="Delete cache", command=lambda: mbox.showinfo("Cache", "Deleted " + str(main.deleteCache()) + " cache files!"))
		cache.pack(side=LEFT, fill=BOTH, expand=True)
		self.alwaysOnTop = Checkbutton(bline4, text="Always on top", variable=self.onTop, command=self.setAlwaysOnTop)
		self.alwaysOnTop.pack(side=LEFT, fill=BOTH)
		search = Button(bline4, text="Search files") # no command yet
		search.pack(side=LEFT, fill=BOTH, expand=True)
		fileTransfering = Button(bline4, text="File Transfering", state=DISABLED) # no command yet
		fileTransfering.pack(side=RIGHT, fill=BOTH, expand=True)
		quit = Button(bline5, text="Quit", command=main.shutdownHook)
		quit.pack(side=BOTTOM, fill=BOTH, expand=True)

		self.fileAction = [openf, edit, delete, rename]
		#self.directoryAction = [] # for future purposes


		self.tree.pack(fill=BOTH, expand=True)

		self.refresh()


	def __init__(self, password):
		super().__init__()
		self.password = password
		self.style = Style()
		self.style.theme_use(config.THEME)
		self.master.title(config.NAME)

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

		self.master.protocol("WM_DELETE_WINDOW", self.onClose)
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

		keys = self.mkkey(config.SALT_SIZE)
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
		keys = self.mkkey(config.SALT_SIZE)
		crypto = Cryptography(keys['pad'])

		f = open('data/' + file, 'rb')
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
		crypto = DoubleCryptography(keys['pad'], keys['xor'])
		
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


	def loadEncryptedFile(self, realname, _open=True):
		if realname == None:
			return
		salt = self.getSaltOfFile(realname)
		file = open('data/' + realname, 'rb')
		data = file.read()[config.SALT_SIZE:]
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

		if _open:
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
		self.selected = None

		for x in self.fileAction:
			x.configure(state=DISABLED)

	def onTreeSelect(self, event):
		self.selected = self.tree.item(self.tree.focus())['text']

		for x in self.fileAction:
			x.configure(state=NORMAL)

	def onClose(self, event=None):
		main.shutdownHook(None, None)

	def deleteFile(self, fakename):
		realname = self.getEncryptedFileName(fakename)
		os.remove('data/' + realname)
		self.refresh()

	def renameFile(self, oldfakename, newfakename):
		oldrealname = self.getEncryptedFileName(oldfakename)
		salt = self.getSaltOfFile(oldrealname)

		keys = self.mkkey(len(newfakename), salt)
		crypto = DoubleCryptography(keys['pad'], keys['xor'])
		newrealname = toHex(crypto.encrypt(getFileName(realname)))

		del keys
		del crypto

		os.rename(oldrealname, newrealname)




	def setAlwaysOnTop(self):
		self.master.attributes('-topmost', str(self.onTop.get()).lower())











