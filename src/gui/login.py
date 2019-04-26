from tkinter import RAISED
from tkinter.ttk import Frame, Button, Style

class LoginWindow(Frame):
	def __init__(self,tk):
		super().__init__()
		width = 400
		height = 260
		x = (tk.winfo_screenwidth() // 2) - (width // 2)
		y = (tk.winfo_screenheight() // 2) - (height // 2)
		tk.geometry("{}x{}+{}+{}".format(width, height, x, y))
		tk.resizable(False, False)
		frame = Frame(self, relief=RAISED, borderwidth=1)
		frame.pack_propagate(0)
		self.master.title("Login")

		Style().configure("TFrame", background='#fff')