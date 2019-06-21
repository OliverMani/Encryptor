from gui import login
from tkinter import messagebox as mb
from sys import argv

import signal
import tkinter as tk
import os
import platform
import config
import console.textbased as console

VALID_SYSTEMS = ['windows', 'darwin', 'linux']

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
	for x in os.listdir(config.TMP_FOLDER):
		os.remove(config.TMP_FOLDER + x)
		i += 1
	print("Deleted", i, "cache files!")
	return i

def shutdownHook(signal=None, event=None):
	print("Shutting down...")
	deleteCache()
	exit(0)

def main(args=[]):
	gui = True
	if len(args) > 1:
		if args[1] == 'nogui':
			gui = False
	config.OS = platform.system().lower()
	config.DATA_FOLDER += '\\' if config.OS == 'windows' else '/'
	config.TMP_FOLDER += '\\' if config.OS == 'windows' else '/'

	if config.OS not in VALID_SYSTEMS:
		if gui:
			mb.showerror("Error", "You can't run Encryptor on this operating system!")
		else:
			print("You can't run Encryptor on this operating system!")
		return

	signal.signal(signal.SIGINT, shutdownHook)

	# non windowed process

	if not os.path.isdir(config.DATA_FOLDER):
		os.mkdir(config.DATA_FOLDER, 493)

	if not os.path.isdir(config.TMP_FOLDER):
		os.mkdir(config.TMP_FOLDER, 493)

	# end non windowed process
	if gui:
		root = tk.Tk()
		width = 400
		height = 260
		x = (root.winfo_screenwidth() // 2) - (width // 2)
		y = (root.winfo_screenheight() // 2) - (height // 2)

		root.geometry("{}x{}+{}+{}".format(width, height, x, y))
		root.resizable(False, False)

		app = login.LoginWindow([width,height],root)

		root.mainloop()
	else:
		console.init(args[1:])

# Initialize the entire program
if __name__ == "__main__":
	main(argv)
	shutdownHook(None, None)