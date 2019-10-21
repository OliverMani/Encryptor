from tkinter import *
from tkinter.ttk import Frame, Button, Style, Label, Entry

from gui.browser import BrowserWindow
from gui.make_key import WordsKeyGenerateWindow
from gui.dialogs.custom_message_dialog import PasswordWarning
from gui.request_key import WordsKeyDialog

import passwordchecker

import config

class LoginWindow(Frame):

	def __init__(self,size,tk):
		super().__init__()
		self.tk = tk
		self.master.title("Login")
		self.style = Style()
		self.style.theme_use(config.THEME)

		frame = Frame(self, relief=RAISED, borderwidth=1)

		frame.pack(fill=BOTH, expand=True)

		self.pack(fill=BOTH, expand=True)
		self._login = Button(self, text="Login", command=self.login)
		self._login.pack(side=RIGHT, padx=5, pady=5)
		cancel = Button(self, text="Exit program",command=tk.destroy)
		cancel.pack(side=RIGHT, padx=5, pady=5)
		no_pwd = Button(self, text="Login without a password", command=self.no_pwd)
		no_pwd.pack(side=RIGHT)

		title = Label(frame, text=config.NAME + ' ' + config.VERSION, font=("Lucida Grande", 30))
		title.place(x=size[0]//2, y=29, anchor=CENTER)

		subtitle = Label(frame, text=config.MOTTO, font=("Lucida Grande", 13))
		subtitle.place(x=size[0]//2, y=70, anchor=CENTER)

		pwdLabel = Label(frame, text="Password:", font=("Lucida Grande", 12))
		pwdLabel.place(x=6, y=170)

		self.pwd = Entry(frame, show="\u2022")
		self.pwd.bind('<Return>', self.login)
		self.pwd.place(x=80, y=167, width=300, height=25)
	
	def no_pwd(self, event=None):
		
		hasPattern = PasswordWarning(self.tk, title="Dialog", message="Are you going to generate a new list or type in one?", buttons=['I don\'t have a words list, generate one!', 'I have my words list!'])
		self.tk.wait_window(hasPattern.top)
		self.tk.destroy()
		if hasPattern.accepted:
			WordsKeyDialog()
		else:
			WordsKeyGenerateWindow()


	def login(self,event=None):
		password = self.pwd.get()
		
		isSafe = passwordchecker.checkIfPasswordIsSafe(password)

		goAhead = isSafe['safe']

		if not goAhead:
			self._login.configure(state=DISABLED)
			warning = PasswordWarning(self.tk, title="Bad password", message=isSafe['message'], buttons=['Try another password', 'I don\'t care, go ahead!'])

			self.tk.wait_window(warning.top)

			goAhead = warning.accepted

			self._login.configure(state=NORMAL)

		if goAhead:
			del self.pwd
			self.tk.destroy()
			browser = BrowserWindow(password)
		