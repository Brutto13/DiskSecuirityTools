import json

from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import *

window = Tk()
window.title("LogViever for DiscSecuirityTools")
window.resizable(False, False)
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure(0, minsize=0, weight=1)

schema = {
    'operation':str,
    'files':{
        'keyFile':str,
        'filenames':list[str],
    }
}

