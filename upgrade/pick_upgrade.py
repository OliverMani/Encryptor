from tkinter import *
from tkinter import messagebox as mbox
#from tkinter.ttk import Frame, Button, Entry, Label#, Radiobutton
from tkinter.filedialog import askdirectory

import os
import platform
import shutil
import math
import key_generator as kg
import _cryptography as cryptography
import config

def _open(file, mode='rb'): 
	if platform.system().lower() == 'windows':
		file = file.replace('/', '\\')
	return open(file, mode)

def isHexOnly(check):
	n = '0123456789abcdef'
	h = check.lower()
	for x in h:
		if x not in n:
			return False
	return True

class AWindow(Tk):
	def __init__(self):
		super().__init__()

		self.title("Pick a upgrade")

		width = 280
		height = 180
		x = (self.winfo_screenwidth() // 2) - (width // 2)
		y = (self.winfo_screenheight() // 2) - (height // 2)

		self.geometry("{}x{}+{}+{}".format(width, height, x, y))
		self.resizable(False, False)

		self.select = IntVar()

		self.dir = 'data'

		frame = Frame(self, relief=RAISED, borderwidth=1)

		frame.pack(fill=BOTH, expand=True)

		Label(frame, text="Select an upgrade:").place(x=6, y=6)

		option = Radiobutton(frame, text='From v1.0 to v1.1', value=1, variable=self.select)
		option.select()
		option.place(x=6, y=36)

		Label(frame, text="Type in your encryptor password:").place(x=6, y=66)
		self.password = Entry(frame, show="\u2022")
		self.password.place(x=12, y=96)

		self.backup = IntVar()

		makeBackup = Checkbutton(frame, text='Make a backup for the encrypted files.', variable=self.backup, onvalue=1, offvalue=0)
		makeBackup.select()
		makeBackup.place(x=6, y=122)



		letsgo = Button(frame, text='Let\'s go!', width=30, command=self.letsgooo)
		letsgo.place(x=6, y=144)

		if not os.path.isdir('data'):
			wannafind = mbox.askyesno("Couldn't find 'data'", "We couldn't find the data directory, do you want to select the data folder?", icon="warning")
			if wannafind:
				directory = askdirectory()
				if directory != '':
					name = os.path.dirname(os.path.realpath(directory))
					if name == 'data':
						self.dir = directory
						self.mainloop()
					else:
						mbox.showerror('You didn\'t select "data"!\nThe program is closing')

		else:
			self.mainloop()

	def mkkey(self, length, salt=''):
		return kg.generateKeysOutOfPassword(self.password.get(), length, salt=salt)

	# Cryptography converter (from 1.0 to 1.1)
	def letsgooo(self):
		if self.backup.get():
			name = 'data_backup'
			i = 1
			while os.path.isdir(name):
				i += 1
				name = 'data_backup ' + str(i)
			os.mkdir(name, 493)
			for x in [f for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir, f))]:
				if isHexOnly(x):
					shutil.copyfile(self.dir + '/' + x, name + '/' + x)

		for x in os.listdir(self.dir):
			if isHexOnly(x):
				keys = self.mkkey(config.SALT_SIZE)
				crypto = cryptography.Cryptography(keys['pad'])
				f = open(self.dir + '/' + x, 'rb')
				encryptedSalt = f.read(config.SALT_SIZE)

				salt = ''.join([chr(x) for x in crypto.decrypt(encryptedSalt)])

				del crypto
				
				del keys

				data = f.read()

				f.close()

				keys = self.mkkey(len(data) % config.OLD_MAX_KEY_SIZE, salt=salt)
				
				crypto = cryptography.DoubleCryptography(keys['pad'], keys['xor'])
				del keys
				decrypted = crypto.decrypt(data)

				del data
				del crypto
				del f

				# DECRYPTING FINISHED
				# ENCRYPTING BEGINS (convert)
				

				keys = self.mkkey(min(len(decrypted), config.MAX_KEY_SIZE), salt=salt)
				crypto = cryptography.DoubleCryptography(keys['pad'], keys['xor'])
				encrypted = bytes(list(encryptedSalt) + crypto.encrypt(decrypted))
				del decrypted
				del encryptedSalt
				del crypto

				f = _open(self.dir + '/' + x, 'wb')
				f.write(encrypted)
				f.close()
				
				
		self.destroy()
				

if __name__ == '__main__':
	window = AWindow()






