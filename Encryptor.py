import os
import sys

from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *
from secuirityEncodings import *
from cryptography.fernet import Fernet

# setting up window
window = Tk()
window.title("Disc Encryption Tool")
window.resizable(False, False)
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure(0, minsize=0, weight=1)

# setting up frames
frm_excluded_management = Frame()

# setting up labels
lab_folderPath = Label(text='Folder path')
lab_keyFile = Label(text='Key file')
lab_exclude = Label(text='Excluded files')

# setting up entrys
WIDTH = 50
ent_folderpath = Entry(width=WIDTH)
ent_keyFile = Entry(width=WIDTH)

# setting up Text's widgets
HEIGHT = 10
WIDTH = 38
txt_Excluded_files = Text(width=WIDTH, height=HEIGHT)

def browseFolder():
    filepath = askdirectory()
    ent_folderpath.delete(0, END)
    ent_folderpath.insert(0, filepath)

def browseKeyFile():
    filepath = askopenfilename(
        filetypes=[( 'Private key file', '*.prv')]
    )

    ent_keyFile.delete(0, END)
    ent_keyFile.insert(0, filepath)

def BTNAddExcludedFile():
    filepath = askopenfilename()
    txt_Excluded_files.insert(END, filepath + '\n')

def encrypt():
    try:
        # TODO read the key file
        with open(ent_keyFile.get(), "rb") as file:
            content = file.readlines()
            key = content[0].encode()
            password = transformMessage("d", content[1], 25)
        
        fernet = Fernet(key)
        fileslist = []
        # Ask for password
        if askstring("Encryptor - Verification", "Enter password") == password and askokcancel("Encryptor - confirmation", "WARNING: When you encrypt the folder\nthe only way to get them back is to use the key file\nDo not loose it\nARE YOU SURE YOU WISH TO PROCEED?  "):
            # create list of excluded files XXX
            ExcludedFiles = txt_Excluded_files.get(0, END).split(sep='\n')
            for filename in os.listdir(ent_folderpath.get()):
                if filename not in ExcludedFiles:
                    with open(filename, "rb") as file:
                        original = file.read()
                    with open(filename, "wb") as file:
                        encrypted = fernet.encrypt(original)
                        file.write(encrypted)
                    fileslist.append(filename)
                    
            
            showinfo("Encryptor - Done", "Succesfully Encrypted Files:%s" % ('\n'.join(fileslist)))
            
        
        else:
            showerror("Encryptor", "Operation canceled")
    except FileNotFoundError:
        showerror("Encryptor - Error", "No such file or directory (ERR2)")
    except Exception as e:
        showerror("Encryptor - fatal error", f"Fatal exception occured:\n{e}")

btn_encrypt = Button(text='Encrypt files', command=encrypt)
btn_browseKey = Button(text='Browse...', command=browseKeyFile)
btn_browseFolder = Button(text='Browse...', command=browseFolder)
btn_addExcludedFile = Button(text='Add file', command=BTNAddExcludedFile)

# Grid
lab_folderPath.grid(row=0, column=0, padx=5, pady=5)
lab_keyFile.grid(row=1, column=0, padx=5, pady=5)
lab_exclude.grid(row=2, column=0, padx=5, pady=5)

ent_folderpath.grid(row=0, column=1, padx=5, pady=5)
ent_keyFile.grid(row=1, column=1, padx=5, pady=5)
txt_Excluded_files.grid(row=2, column=1, padx=5, pady=5)

btn_browseFolder.grid(row=0, column=2, padx=5, pady=5)
btn_browseKey.grid(row=1, column=2, padx=5, pady=5)
btn_encrypt.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

window.mainloop()