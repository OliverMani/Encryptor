from tkinter import *
from tkinter.ttk import Frame, Button, Style, Label, Entry

import config

TEXT = None

def getStringInput(title='', message='', onenter=None):
	TEXT = None
	inp = InputDialog(title, message, onenter)

class InputDialog(Tk):
	def __init__(self, title='', message='', onenter=None):
		super().__init__()

		self.title(title)

		width = 200
		height = 70
		x = (self.winfo_screenwidth() // 2) - (width // 2)
		y = (self.winfo_screenheight() // 2) - (height // 2)

		self.geometry("{}x{}+{}+{}".format(width, height, x, y))
		self.resizable(False, False)

		frame = Frame(self, relief=RAISED, borderwidth=1)
		frame.style = Style()
		frame.style.theme_use(config.THEME)
		frame.pack(fill=BOTH, expand=True)

		message = Label(frame, text=message)
		message.pack()

		self.entry = Entry(frame)
		self.entry.pack()

		okButton = Button(frame, text="OK", command=lambda: self.onReturn(onenter))
		okButton.pack()

		#self.pack()

		self.mainloop()

	def onReturn(self, onenter):
		text = self.entry.get()
		self.destroy()
		if onenter != None:
			onenter(text)
		
