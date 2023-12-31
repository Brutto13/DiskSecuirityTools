import json
import os
import time

# tkinter imports
# from tkinter import *
from tkinter import Tk, StringVar, END
import tkinter.ttk as ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *

# other imports
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
window.title("Disc Encryption Tool")
window.resizable(False, False)
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure(0, minsize=0, weight=1)

# progress = ttk.Progressbar(window, mode='indeterminate', orient='horizontal')

# setting up labels
lab_folderPath = ttk.Label(text='Encrypted Disc')
lab_keyFile = ttk.Label(text='Key file')


# setting up entrys
WIDTH = 76
ent_folderpath = ttk.Entry(width=WIDTH)
ent_keyFile = ttk.Entry(width=WIDTH)
ent_backupFolder = ttk.Entry(width=WIDTH)

disc_list = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] # XXX ONLY FOR TESTING Removed discs C: and R: and E:
var_disc = StringVar(window)
opt_disc = ttk.OptionMenu(window, var_disc, *disc_list)



def browseKeyFile():
    filepath = askopenfilename(
        filetypes=[('Private key file', '*.prv')]
    )

    ent_keyFile.delete(0, END)
    ent_keyFile.insert(0, filepath)


def encrypt():
    try:
        os.chdir(var_disc.get() + ':/')
        backup = ent_backupFolder.get()
        if var_disc.get() == 'C':
            if not askokcancel("Encryptor - Critical Warning", "WARNING! You are encrypting disc \"C\"\nThat means that if you won\'t decrypt it before\nshutting down computer\nYou won\'t run OS again!!!\nAre you sure you want to continue???", icon='warning'):
                showerror("Encrypptor - Interrupted", "Operation Interrupted by the user!")
                return None

        with open(ent_keyFile.get(), "r") as file:
            content = file.readlines()
            key = content[0].encode()
            password = transformMessage("d", content[1], 25)
        
        fernet = Fernet(key)
        fileslist = []
        # Ask for password
        confirm = askokcancel("Encryptor - confirmation", "WARNING: When you encrypt the folder\nthe only way to get them back is to use the key file\nDo not loose/encrypt it\nARE YOU SURE YOU WISH TO PROCEED?  ")
        passwordEntered = askstring("Encryptor - Verification", "Enter password")
        if passwordEntered  == password and confirm:
            dirToEncrypt = var_disc.get() + ':/'
            print(dirToEncrypt)
            for root, dirs, files in os.walk('.'):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    print(filename)
                
                    with open(filepath, "rb") as file:
                        original = file.read()
                    
                    with open(filepath, "wb") as file:
                        encrypted = fernet.encrypt(original)
                        file.write(encrypted)
                    
                    with open(backup + filename, "wb") as file:
                        file.write(original)

                    fileslist.append(dirToEncrypt + filename)
                    # window.mainloop()
                    # progress.step()
            
            showinfo("Encryptor - Done", "Succesfully Encrypted Files:\n%s" % ('\n'.join(fileslist)))
            if askyesno("Encryptor", "Do you want to save JSON-formatted settings?"):
                with open(f'encryption-lastest-log.json', "x") as file:
                    data = {
                        'operation':'ENCRYPTION',
                        'files':{
                            'keyFile':ent_keyFile.get(),
                            'filenames':fileslist,
                        }
                    }
                    file.write(json.dumps(data))

        
        else:
            showerror("Encryptor", "Operation canceled")
    
    except FileNotFoundError: showerror("Encryptor", f"Disc \"{var_disc.get()}\" couldn\'t be resolved!"); return None
    except PermissionError: showerror("Encryptor", "Permission Error");                                    return None
    except Exception as e: showerror("Encryptor - Fatal Error", e);                                        return None

btn_encrypt = ttk.Button(text='Encrypt files', command=encrypt)
btn_browseKey = ttk.Button(text='Browse...', command=browseKeyFile)

# Grid
lab_folderPath.grid(row=0, column=0, padx=5, pady=5)
lab_keyFile.grid(row=1, column=0, padx=5, pady=5)

opt_disc.grid(row=0, column=1, padx=5, pady=5, sticky='w')
ent_keyFile.grid(row=1, column=1, padx=5, pady=5)

btn_browseKey.grid(row=1, column=2, padx=5, pady=5)
btn_encrypt.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
# progress.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

window.mainloop()
