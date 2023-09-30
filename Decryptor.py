import os
import sys

from tkinter import *
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

# setting up labels
lab_folderPath = Label(text='Folder path')
lab_keyFile = Label(text='Key file (*.key)')
lab_exclude = Label(text='Excluded files')

# setting up entrys
WIDTH = 20
ent_folderpath = Entry(width=WIDTH)
ent_keyFile = Entry(width=WIDTH)

# setting up Text's widgets
HEIGHT = 20
WIDTH = 30
txt_Excluded_files = Text(width=WIDTH, height=HEIGHT)