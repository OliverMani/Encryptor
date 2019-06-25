from tkinter import *
from tkinter import messagebox as mbox
from tkinter.ttk import Frame, Button, Style, Label, Entry, Treeview, Scrollbar, Checkbutton
from tkinter.filedialog import askopenfilename

import action_class as ac
import randomness as random
import main
import os
import gui.dialogs.input_dialog as inp
import _io_.fileutils as fileutils
import gui.texteditor as texteditor
import config


IMAGES_EXTENSION = ['png','jpg','jpeg','gif']

TYPE_NAMES = config.TYPE_NAMES

class BrowserWindow(Frame):

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
		

		create = Button(bline1, text="Create file", command=lambda: inp.getStringInput(title='Filename', message='Type in file name:', onenter=lambda i: [lambda:x() for x in [self.createFile(i, refresh=True), texteditor.TextEditor(i, self, True)]]))
		create.pack(side=LEFT, fill=BOTH, expand=True)
		upload = Button(bline1, text="Upload file", command=lambda: self.uploadFile(askopenfilename()))
		upload.pack(side=LEFT, fill=BOTH, expand=True)
		openf = Button(bline1, text="Open file", command=lambda: self.loadEncryptedFile(self.getEncryptedFileName(self.selected)))
		openf.pack(side=LEFT, fill=BOTH, expand=True)
		edit = Button(bline2, text="Edit file", command=lambda: texteditor.TextEditor(self.selected, self))
		edit.pack(side=LEFT, fill=BOTH, expand=True)
		explorer = Button(bline2, text="System explorer", command=lambda: fileutils.openFolder(config.DATA_FOLDER))
		explorer.pack(side=LEFT, fill=BOTH, expand=True)
		refresh = Button(bline2, text="Refresh", command=self.refresh)
		refresh.pack(side=LEFT, fill=BOTH, expand=True)
		delete = Button(bline3, text="Delete file", command=lambda: self.deleteFile(self.selected))
		delete.pack(side=LEFT, fill=BOTH, expand=True)
		rename = Button(bline3, text="Rename file", command=lambda: inp.getStringInput(title='Filename', message='Type in a new file name:', onenter=lambda i: self.renameFile(self.selected, i))) # no command yet
		rename.pack(side=LEFT, fill=BOTH, expand=True)
		cache = Button(bline3, text="Delete cache", command=lambda: mbox.showinfo("Cache", "Deleted " + str(main.deleteCache()) + " cache files!"))
		cache.pack(side=LEFT, fill=BOTH, expand=True)
		self.alwaysOnTop = Checkbutton(bline4, text="Always on top", variable=self.onTop, command=self.setAlwaysOnTop)
		self.alwaysOnTop.pack(side=LEFT, fill=BOTH)
		search = Button(bline4, text="Search files", command=lambda: inp.getStringInput(title='Search files', message="Input:", onenter=self.searchAndSelect))
		search.pack(side=LEFT, fill=BOTH, expand=True)
		fileTransfering = Button(bline4, text="File Transfering", state=DISABLED) # no command yet
		fileTransfering.pack(side=RIGHT, fill=BOTH, expand=True)
		quit = Button(bline5, text="Quit", command=self.onClose)
		quit.pack(side=BOTTOM, fill=BOTH, expand=True)

		self.fileAction = [openf, edit, delete, rename]
		#self.directoryAction = [] # for future purposes


		

		scrollY = Scrollbar(frame, orient="vertical", command=self.tree.yview)
		scrollY.pack(side=RIGHT, fill=Y)

		self.tree.pack(fill=BOTH, expand=True)

		self.tree.configure(yscrollcommand=scrollY.set)

		self.refresh()


	def __init__(self, password):
		super().__init__()
		self.password = password
		self.style = Style()
		self.style.theme_use(config.THEME)
		self.master.title(config.NAME)

		self.actions = ac.ActionClass(self.password)

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
		self.actions.createFile(realname)

		if refresh:
			self.refresh()

	def getSaltOfFile(self, file):
		return self.actions.getSaltOfFile(file)

	def getDecryptedFileName(self, realname):
		return self.actions.getDecryptedFileName(realname)

	def getEncryptedFileName(self, decrypted):
		return self.actions.getEncryptedFileName(decrypted)

	def uploadFile(self, path):
		self.actions.uploadFile(path)
		self.refresh()


	def loadEncryptedFile(self, realname, _open=True):
		if realname == None:
			return
		if not mbox.askyesno("Privacy warning", "This file has to be opened with another program, and the other program can do whatever it likes to do with the file, this file has also be written on the hard drive, which means that other programs on your computer can read the file DECRYPTED, do you want to continue?"):
			return
		self.actions.loadEncryptedFile(realname, _open)




	def refresh(self):
		self.tree.delete(*self.tree.get_children())

		i = 0
		self.files.clear()
		for x in os.listdir(config.DATA_FOLDER):
			name = self.getDecryptedFileName(x)
			if name != None:
				size = os.path.getsize(config.DATA_FOLDER + x) - 10
				t = "File"
				if '.' in name:
					t = TYPE_NAMES.get(name[name.rfind('.')+1:]) or "File"
				self.tree.insert("", i, text=name, values=(t, fileutils.getSizeString(size)))
				i += 1
		self.selected = None

		for x in self.fileAction:
			x.configure(state=DISABLED)

	def onTreeSelect(self, event):
		self.selected = self.tree.item(self.tree.focus())['text']

		for x in self.fileAction:
			x.configure(state=NORMAL)

	def onClose(self, event=None):
		self.master.destroy()
		main.shutdownHook(None, None)

	def deleteFile(self, fakename):
		self.actions.deleteFile(fakename)
		self.refresh()

	def renameFile(self, oldfakename, newfakename, refresh=True):
		self.actions.renameFile(oldfakename, newfakename)
		if refresh:
			self.refresh()

	def setAlwaysOnTop(self):
		self.master.attributes('-topmost', str(self.onTop.get()).lower())

	def searchAndSelect(self, search):
		for x in self.tree.get_children():
			name = self.tree.item(x)['text'].lower()
			if search.lower() in name.lower():
				self.tree.selection_set(x)
				return
		mbox.showinfo("Search", "No files found with '" + search + "' in the name!")
