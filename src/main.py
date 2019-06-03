from gui import login
from tkinter import messagebox as mb

import signal
import tkinter as tk
import os
import platform
import config

VALID_SYSTEMS = ['windows', 'darwin', 'linux', 'unix']

def isHexOnly(check):
	n = '0123456789abcdef'
	h = check.lower()
	for x in h:
		if x not in n:
			return False
	return True

def toString(data):
	return ''.join([chr(x) for x in data])

def deleteCache():
	print("Deleting cache...")
	i = 0
	for x in os.listdir('tmp/'):
		os.remove('tmp/' + x)
		i += 1
	print("Deleted", i, "cache files!")
	return i

def shutdownHook(signal=None, event=None):
	print("Shutting down...")
	deleteCache()
	exit(0)

def main():
	config.OS = platform.system().lower()
	config.DATA_FOLDER += '\\' if config.OS == 'windows' else '/'
	if config.OS not in VALID_SYSTEMS:
		mb.showerror("Error", "You can't run Encryptor on this operating system!")
		return

	signal.signal(signal.SIGINT, shutdownHook)

	# non windowed process

	if not os.path.isdir("data/"):
		os.mkdir("data/", 493)

	if not os.path.isdir("tmp/"):
		os.mkdir("tmp/", 493)

	# end non windowed process

	root = tk.Tk()
	width = 400
	height = 260
	x = (root.winfo_screenwidth() // 2) - (width // 2)
	y = (root.winfo_screenheight() // 2) - (height // 2)

	root.geometry("{}x{}+{}+{}".format(width, height, x, y))
	root.resizable(False, False)

	app = login.LoginWindow([width,height],root)

	root.mainloop()

# Initialize the entire program
if __name__ == "__main__":
	main()
	shutdownHook(None, None)