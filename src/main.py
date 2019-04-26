import tkinter as tk

from gui import login
from tkinter.ttk import Frame, Button, Style

from cryptography import DoubleCryptography

def to_string(data):
	res = ""
	for x in data:
		res += chr(x)
	return res

def main():
	text = "hello world"

	pad = [10,20,30]
	xor = [77,56,24]

	crypto = DoubleCryptography(pad,xor)

	print(to_string(crypto.decrypt(crypto.encrypt(text)))) # checks if the encryption system works


	root = tk.Tk()
	
	login.LoginWindow(root)
	root.mainloop()

# Initialize the whole program
if __name__ == "__main__":
	main()