import os
import platform
import subprocess
import os.path

from tkinter import messagebox as mb


WINDOWS = ['windows']
UNIX = ['darwin', 'linux', 'solaris']

# cross-platform
def openFileWithAnotherProgram(path):
	system = platform.system().lower()
	if system in WINDOWS:
		# Windows only!!!
		os.startfile(path)
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