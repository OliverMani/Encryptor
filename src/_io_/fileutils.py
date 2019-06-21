import os
import platform
import subprocess
import os.path
import config

from tkinter import messagebox as mb


WINDOWS = ['windows']
UNIX = ['darwin', 'linux']

# cross-platform
def openFileWithAnotherProgram(path):
	system = platform.system().lower()
	if system in WINDOWS:
		# Windows only!!!
		os.startfile(path.replace('/', '\\'))
	elif system in UNIX:
		#only unix and unix-like systems
		if system == 'linux':
			subprocess.call(['xdg-open', path])
		else:
			subprocess.call(['open', path])

def openFolder(path):
	if os.path.isdir(path):
		system = platform.system().lower()

		if system == 'windows':
			os.startfile(path.replace('/', '\\'))
		elif system == 'darwin':
			subprocess.Popen(['open', path])
		else:
			subprocess.Popen(['xdg-open', path])

def getSizeString(size, f='.2f'):
	if size < 1024:
		return str(size) + "B"
	elif size < 1024**2:
		return str(format(size / 1024, f)) + "KB"
	elif size < 1024**3:
		return str(format(size / (1024**2),f )) + "MB"
	else:
		return str(format(size / (1024**3), f)) + "GB"

def readInChunks(path, chunk=config.FILE_CHUNK, salted=False):
	with open(path, 'rb') as file:
		if salted:
			file.read(config.SALT_SIZE)
		while True:
			data = file.read(chunk)
			if not data:
				break
			yield data
