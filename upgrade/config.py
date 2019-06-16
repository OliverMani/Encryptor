# Changing the values can mess up some files that are already encrypted with default configuration
SALT_SIZE=10 #salt length
MAX_KEY_SIZE=1024**2 # 1 MB (25mb takes too much memory)
OLD_MAX_KEY_SIZE = 25*1024**2
DATA_FOLDER = 'data'
FILE_CHUNK = 1024**2
