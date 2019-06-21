# Changing the values can mess up some files that are already encrypted with default configuration
SALT_SIZE=10 #salt length
MAX_KEY_SIZE=1024**2 # 1 MB (25mb takes too much memory)
THEME = 'default'
DATA_FOLDER = 'data'
TMP_FOLDER = 'tmp'
FILE_CHUNK = 1024**2

#info
NAME='Encryptor'
VERSION='v1.1'
AUTHOR='Óliver Máni'
MOTTO='I can\'t stop!'

TYPE_NAMES = {
	'mp4':'Video',
	'mov':'Video',
	'webm':'Video',
	'avi':'Video',
	'png':'Photo',
	'jpeg':'Photo',
	'jpg':'Photo',
	'gif':'Animated\ photo',
	'exe':'Windows\ application',
	'msi':'Windows\ installer',
	'py':'Python\ script',
	'js':'Javascript',
	'html':'HTML\ web\ page',
	'css':'CSS\ file',
	'zip':'ZIP\ file',
	'txt':'Text\ file',
	'mp3':'Audio',
	'ogg':'Audio',
	'wav':'Audio'
}