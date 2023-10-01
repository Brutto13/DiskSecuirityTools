import json
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from secuirityEncodings import *
from cryptography.fernet import Fernet

window = Tk()
window.title("Disc Secuirity Tools - Key Generation")
window.resizable(False, False)
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure(0, minsize=0, weight=1)

lab_filename = Label(text='Filename')
lab_password = Label(text='password')

ent_filename = Entry(width=45)
ent_password = Entry(width=45, show='*')

def browseFile():
    filepath = askdirectory()
    ent_filename.delete(0, END)
    ent_filename.insert(0, filepath)

def createKeys():
    privateName = ent_filename.get() + '\private.prv'
    publicName = ent_filename.get() + '\public.json'
    key = Fernet.generate_key()
    password = ent_password.get()

    with open(privateName, "w") as file:
        file.write(key.decode() + '\n')
        file.write(transformMessage("s", password, 25))
    
    with open(publicName, "w") as file:
        data = {
            'key':key.decode()
        }
        Data = json.dumps(data)
        file.write(Data)
    
    showinfo("Key Creation Tool", f"Key creation done!\nGenerated files:\n* private key: {privateName}\npublic key: {publicName}")

btn_browseFile = Button(text='Browse...', command=browseFile)
btn_GenerateKeys = Button(text='Generate Key', command=createKeys)

lab_filename.grid(row=0, column=0, padx=5, pady=5)
lab_password.grid(row=1, column=0, padx=5, pady=5)

ent_filename.grid(row=0, column=1, padx=5, pady=5)
ent_password.grid(row=1, column=1, padx=5, pady=5)

btn_browseFile.grid(row=0, column=2, padx=5, pady=5)
btn_GenerateKeys.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

window.mainloop()