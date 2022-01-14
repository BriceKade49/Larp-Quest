import os
import shutil

# fetch all files
for file_name in os.listdir(r"Rooms\\"):
    # construct full file path
    source = r"Rooms\\" + file_name
    destination = r"NewRooms\\" + file_name
    # copy only files
    if os.path.isfile(source):
        shutil.copy(source, destination)
        print('copied', file_name)

