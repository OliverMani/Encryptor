from tkinter import *
from tkinter import messagebox as mbox
from tkinter.ttk import Frame, Style, Label, Button, Entry

from gui.browser import BrowserWindow
from gui import make_key

import config

class WordsKeyDialog(Tk):
	
	def words_list_to_int_list(self, l):
		errors = []
		valid = [0 for x in range(len(l))]
		for x in range(len(l)):
			found = False
			for y in range(len(config.WORDS)):
				if l[x].lower() == config.WORDS[y][0].lower() or l[x].lower() == config.WORDS[y][1].lower():
					valid[x] = y;
					found = True
			if not found:
				errors.append(x)
		return {'valid':valid,'errors':errors}

	def __init__(self, correct_pattern=None):

		self.correct_pattern = correct_pattern

		self.key = [0 for x in range(config.WORDS_LIST_LENGTH)]

		self.inputs = []

		super().__init__()


		self.title("Login")
		self.style = Style()
		self.style.theme_use(config.THEME)

		
		frame = Frame(self, relief=RAISED, borderwidth=1)
		frame.pack(expand=True, fill=BOTH)

		##btn_frame = Frame(frame, relief=RAISED, borderwidth=1)
		##btn_frame.pack(fill=X, expand=True, side=BOTTOM)

		exit = Button(self, text="Exit program", command=self.destroy)
		exit.pack(side=LEFT, fill=BOTH, expand=True)

		login = Button(self, text="I'm done typing, let's go!", command=lambda: self.letsgo([self.inputs[x].get() for x in range(len(self.inputs))]))
		login.pack(side=LEFT, fill=BOTH, expand=True)

		instructions = Label(frame, text='Select your words list in CORRECT order:')
		instructions.grid(row=0, column=0, sticky=W+E)

		
		for x in range(config.WORDS_LIST_LENGTH):
			place = Frame(frame, relief=RAISED, borderwidth=1)
			Label(place, text=str(x+1) + ": ").pack(side=LEFT)
			keyword = Entry(place)
			keyword.pack(side=LEFT, fill=BOTH, expand=True)
			self.inputs.append(keyword)
			place.grid(row=x+1, column=0, padx=1, sticky=W+E)

		width = 400
		height = 650
		x = (self.winfo_screenwidth() // 2) - (width // 2)
		y = (self.winfo_screenheight() // 2) - (height // 2)

		self.geometry("{}x{}+{}+{}".format(width, height, x, y))
		#self.resizable(False, False)


		


		self.mainloop()

	def letsgo(self, inputs):
		
		info = self.words_list_to_int_list(inputs)
		self.key = info['valid']
		errors = info['errors']
		

		if len(errors) == 0:
			
			if self.correct_pattern != None:
				correct_pattern = self.words_list_to_int_list(self.correct_pattern)['valid']
				if correct_pattern == self.key:
					self.destroy()
					browser = BrowserWindow(''.join([chr(x) for x in self.key]))
					
				else:
					print("Currect:", correct_pattern, "vs yours:", self.key)
					mbox.showerror("Wrong words or order!", "Your list is wrong, could be wrong order, wrong words or typos!")
					
					make_key.WordsKeyGenerateWindow(self.correct_pattern)
					self.destroy()
			else:
				self.destroy()
				browser = BrowserWindow(''.join([chr(x) for x in self.key]))
		else:
			check = str([x+1 for x in errors])[1:-1]

			mbox.showwarning("Could not log in!", "Some words aren't currect, check line(s) " + check + "!")
			









