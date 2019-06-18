import tkinter as tk
from tkinter.ttk import Button, Style, Frame

import config

class PasswordWarning(object):
	def __init__(self, parent, message='Message', title='Message', buttons=['Cancel', 'OK']):
		self.top = tk.Toplevel(parent)
		self.top.style = Style()
		self.top.style.theme_use(config.THEME)
		self.top.title(title)

		frame = Frame(self.top, relief=tk.RAISED, borderwidth=1)

		width = 430
		height = 150

		x = (self.top.winfo_screenwidth() // 2) - (width // 2)
		y = (self.top.winfo_screenheight() // 2) - (height // 2)

		self.top.geometry("{}x{}+{}+{}".format(width, height, x, y))
		self.top.resizable(False, False)

		frame.pack(fill=tk.BOTH, expand=True)

		self.message = tk.Message(frame, text=message, relief=tk.RAISED, justify=tk.LEFT, anchor=tk.NW)
		self.message.pack(fill=tk.BOTH,expand=True, side=tk.LEFT, anchor=tk.NW)

		cancel = Button(self.top, text=buttons[0], command=lambda: self.setStatus(False))
		cancel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		
		goAhead = Button(self.top, text=buttons[1], command=lambda: self.setStatus(True))
		goAhead.pack(side=tk.RIGHT)

		self.accepted = None
		
	def setStatus(self, boo):
		self.accepted = boo
		self.top.destroy()
