from tkinter import *
from tkinter.ttk import Frame, Style, Label, Button

from gui.request_key import WordsKeyDialog
import config
import randomness as random


class WordsKeyGenerateWindow(Tk):

	def get_random_words(self):
		data = [random.generateRandomByte() for x in range(config.WORDS_LIST_LENGTH)]
		words = []
		print(data)
		for x in data:
			if config.WORDS[x][0] in words:
				words.append(config.WORDS[x][1])
			else:
				words.append(config.WORDS[x][0])
		return words

	def __init__(self, pattern=None):
		super().__init__()
		self.pattern = pattern
		self.title("Login")
		self.style = Style()
		self.style.theme_use(config.THEME)

		
		frame = Frame(self, relief=RAISED, borderwidth=1)
		frame.pack(expand=True, fill=BOTH)

		##btn_frame = Frame(frame, relief=RAISED, borderwidth=1)
		##btn_frame.pack(fill=X, expand=True, side=BOTTOM)

		exit = Button(self, text="Exit program", command=self.destroy)
		exit.pack(side=LEFT, fill=BOTH, expand=True)

		check = Button(self, text="I'm done typing, let's go!", command=self.lets_go)
		check.pack(side=LEFT, fill=BOTH, expand=True)

		instructions = Label(frame, text='Type the following list on paper the in same order below:')
		instructions.pack()

		listbox = Listbox(frame)
		listbox.pack(fill=BOTH, expand=True)

		self.key = pattern if pattern != None else self.get_random_words()

		for x in self.key:
			listbox.insert(END, x)

		width = 400
		height = 650
		x = (self.winfo_screenwidth() // 2) - (width // 2)
		y = (self.winfo_screenheight() // 2) - (height // 2)

		self.geometry("{}x{}+{}+{}".format(width, height, x, y))
		#self.resizable(False, False)

		self.mainloop()

	def lets_go(self):
		self.destroy()
		WordsKeyDialog(self.key)
