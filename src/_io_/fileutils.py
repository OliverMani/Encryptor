import os
import platform
import subprocess
import os.path

from tkinter import messagebox as mb


WINDOWS = ['windows']
UNIX = ['darwin', 'linux', 'unix']

# cross-platform
def openFileWithAnotherProgram(path):
	system = platform.system().lower()
	if system in WINDOWS:
		# Windows only!!!
		os.startfile(path.replace('/', '\\'))
	elif system in UNIX:
		#only unix and unix-like systems
		subprocess.call(['open', path])

def openFolder(path):
	if os.path.isdir(path):
		system = platform.system().lower()

		if system == 'windows':
			os.startfile(path)
		elif system == 'darwin':
			subprocess.Popen(['open', path])
		else:
			subprocess.Popen(['xdg-open', path])