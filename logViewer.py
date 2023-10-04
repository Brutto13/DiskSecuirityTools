import json
import time
from tkinter.ttk import Progressbar
import SimpleProgressBarLib as progressBar

from SimpleProgressBarLib import ColorValue
from colorama import Fore, init
init(True)
print("Welcome to this simple log viewer tool")

filepath = input("enter filepath to your JSON file")

progress = progressBar.DeterminatedProgressBar(
    name="Reading JSON file",
    total=100,
    fill_char='_',
    start_char='<',
    ending_char='>',
    main_char='+'
)

for _ in range(100):
    progress.plot()
    time.sleep(0.01)
