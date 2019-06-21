# import encryptor classes
import config
import action_class as ac
import _io_.fileutils as fileutils
# import python standard below
import getpass
import os
import readline

wait = lambda: input("Press ENTER to continue...")


class Value:
	def __init__(self, value):
		self.value = value

	def set(self, value):
		self.value = value

	def get(self):
		return self.value

decoration = "-+-+-+-+-+-+-+-+-+-+-+-+-+-"

actions = Value(None)
running = Value(True)

actionList = {
	'L':lambda:listFiles(),
	'U':lambda:uploadFile(),
	'O':lambda:openFile(),
	'Q':lambda:running.set(False),
}

def uploadFile():
	path = input("Type in the path of the file (on your filesystem): ")
	print("Uploading file... this might take several minutes")
	try:
		actions.value.uploadFile(path)
		print("Done!")
	except FileNotFoundError:
		print("The file was not found")
		wait()

	

def openFile():
	listFiles(False)
	ask = lambda:input("Type in the number of the file you want to open (0 to cancel): ")
	file = ask()
	while not file.isdigit():
		print("This is not number! Try again:")
		file = ask()
	del ask

def listCommands():
	print("""List of commands (type a latter to run):
 [L] - List encrypted files
 [U] - Upload file
 [O] - Open encrypted file
 [F] - Refresh
 [D] - Delete encrypted file
 [R] - Rename encrypted file
 [A] - Delete cache
 [S] - Search for encrypted files
 [Q] - Quit
""")

def doSomething(l):
	if l == None or l == '':
		return False
	if actionList.get(l.upper()) == None:
		print("Unknown command")
		return True
	actionList.get(l.upper())()
	return True
	
def listFiles(_wait=True):
	i = 1
	print("NUMBER | NAME | TYPE OF FILE | FILESIZE")

	longestName = max([len(x) for x in actions.value.files.keys()])

	for key, value in actions.value.files.items():
		t = "File"
		if '.' in key:
			t = config.TYPE_NAMES.get(key[key.rfind('.')+1:]) or "File"
		size = os.path.getsize(config.DATA_FOLDER + value) - 10

		spaces = longestName - len(key) + 1

		print(i, "-", key + ' '*spaces, t + ",", fileutils.getSizeString(size))
		i += 1
	if _wait:
		wait()
def refresh():
	actions.value.files.clear()
	for x in os.listdir(config.DATA_FOLDER):
		actions.value.getDecryptedFileName(x)

def init(args=[]):
	print(config.NAME.upper(), config.VERSION)
	print(config.MOTTO)
	print(decoration)
	password = getpass.getpass('Enter your Encryptor password: ')
	actions.value = ac.ActionClass(password)

	refresh()

	l = True
	while running.value:
		if l:
			listCommands()
		l = True
		test = input("Input: ")
		l = doSomething(test)

