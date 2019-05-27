from tkinter import *
from tkinter.ttk import Frame, Button, Style, Label, Entry

from gui.browser import BrowserWindow

motto = "Stay back, I bite!"
theme = "default"

class LoginWindow(Frame):

	def __init__(self,size,tk):
		super().__init__()
		self.tk = tk
		self.master.title("Login")
		self.style = Style()
		self.style.theme_use(theme)

		frame = Frame(self, relief=RAISED, borderwidth=1)

		frame.pack(fill=BOTH, expand=True)

		self.pack(fill=BOTH, expand=True)
		login = Button(self, text="Login", command=self.login)
		login.pack(side=RIGHT, padx=5, pady=5)
		cancel = Button(self, text="Exit program",command=tk.destroy)
		cancel.pack(side=RIGHT)

		title = Label(frame, text="Encryptor", font=("Lucida Grande", 30))
		title.place(x=size[0]//2, y=29, anchor=CENTER)

		subtitle = Label(frame, text=motto, font=("Lucida Grande", 13))
		subtitle.place(x=size[0]//2, y=70, anchor=CENTER)

		pwdLabel = Label(frame, text="Password:", font=("Lucida Grande", 12))
		pwdLabel.place(x=6, y=170)

		self.pwd = Entry(frame, show="\u2022")
		self.pwd.bind('<Return>', self.login)
		self.pwd.place(x=80, y=167, width=300, height=25)
	
	def login(self,event=None):
		password = self.pwd.get()
		del self.pwd

		self.tk.destroy()

		browser = BrowserWindow(password)
