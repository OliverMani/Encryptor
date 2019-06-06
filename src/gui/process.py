from tkinter import *

class ProcessWindow(Tk):
	def __init__(self, title='', message='', cancelable=False):
		super().__init__()
		self.title(title)
		self.resizable(False, False)

		width = 400
		height = 260
		x = (root.winfo_screenwidth() // 2) - (width // 2)
		y = (root.winfo_screenheight() // 2) - (height // 2)

		self.geometry("{}x{}+{}+{}".format(width, height, x, y))

		msg = Label(self, text=message)
		msg.pack(side=TOP, fill=X)

		process = Processbar(self, orient="horizontal", length=200, mode="determinate")
		process.pack()