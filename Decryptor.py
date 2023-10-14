import json
import os
import sys
import datetime

from tkinter import Tk, StringVar, END
import tkinter.ttk as ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *

from secuirityEncodings import *
from cryptography.fernet import Fernet

encryptionSettingsSCHEMA = {
    'operation':str,
    'files':{
        'keyFile':str,
        'filenames':list[str],
    }
}

# setting up window
window = Tk()
window.title("Disc Decryption Tool")
window.resizable(False, False)
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure(0, minsize=0, weight=1)


progress = ttk.Progressbar(window, mode='indeterminate', orient='horizontal')
# setting up labels
lab_folderPath = ttk.Label(text='Folder path')
lab_keyFile = ttk.Label(text='Key file')
# lab_exclude = Label(frm_excluded_management, text='Excluded files')

# setting up entrys
WIDTH = 76
ent_folderpath = ttk.Entry(width=WIDTH)
ent_keyFile = ttk.Entry(width=WIDTH)

disc_list = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
var_disc = StringVar(window)
opt_disc = ttk.OptionMenu(window, var_disc, *disc_list)

# def browseFolder():
#     filepath = askdirectory()
#     ent_folderpath.delete(0, END)
#     ent_folderpath.insert(0, filepath)

def browseKeyFile():
    filepath = askopenfilename(
        filetypes=[( 'JSON-formatted public key file', '*.json')]
    )

    ent_keyFile.delete(0, END)
    ent_keyFile.insert(0, filepath)

def encrypt():
    
    os.chdir(var_disc.get() + ':/')
    # TODO read the key file
    with open(ent_keyFile.get(), "r") as file:
        content = json.loads(file.read())
        key = content['key'].encode()
    
    fernet = Fernet(key)
    fileslist = []
    # Ask for password
    confirm = askokcancel("Decryptor - confirmation", "Warning: You are decrypting files, if you chosen wrong key, you will loose them without way back!\nAre you sure you want to continue?")
    if confirm:
        # create list of excluded files XXX
        # print(os.listdir(ent_folderpath.get()))
        dirToEncrypt = var_disc.get() + ':/'
        print(dirToEncrypt)
        for root, dirs, files in os.walk('.'):
            for filename in files:
                filepath = os.path.join(root, filename)
                print(filename)
                with open(filepath, "rb") as file:
                    original = file.read()
                
                with open(filepath, "wb") as file:
                    decrypted = fernet.decrypt(original)
                    file.write(decrypted)
                
                fileslist.append(filename)
                progress.step()
                
        
        showinfo("Decryptor - Done", "Succesfully Decrypted Files:\n%s" % ('\n'.join(fileslist)))
        if askyesno("Encryptor", "Do you want to save JSON-formatted log?\n(it can be viewed by logViewer Tool)"):
            with open(f'decryption-lastest-log.json', "x") as file:
                data = {
                    'operation':'DECRYPTION',
                    'files':{
                        'keyFile':ent_keyFile.get(),
                        'filenames':fileslist,
                    }
                }
                file.write(json.dumps(data))

    
    else:
        showerror("Decryptor - CANCELED", "Decrypting stpped by the user!")
    

btn_encrypt = ttk.Button(text='Decrypt files', command=encrypt)
btn_browseKey = ttk.Button(text='Browse...', command=browseKeyFile)
# btn_browseFolder = ttk.Button(text='Browse...', command=browseFolder)
# btn_addExcludedFile = ttk.Button( text='Add file', command=BTNAddExcludedFile)

# Grid
lab_folderPath.grid(row=0, column=0, padx=5, pady=5)
lab_keyFile.grid(row=1, column=0, padx=5, pady=5)


opt_disc.grid(row=0, column=1, padx=5, pady=5, sticky='w')
ent_keyFile.grid(row=1, column=1, padx=5, pady=5)
# txt_Excluded_files.grid(row=2, column=1, padx=5, pady=5)

# frm_excluded_management.grid(row=2, column=0, padx=5, pady=5, sticky='n')
# lab_exclude.grid(row=0, column=0, padx=5, pady=5)
# btn_addExcludedFile.grid(row=1, column=0, padx=5, pady=5, sticky='ew')


# btn_browseFolder.grid(row=0, column=2, padx=5, pady=5)
btn_browseKey.grid(row=1, column=2, padx=5, pady=5)
btn_encrypt.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
progress.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
window.mainloop()