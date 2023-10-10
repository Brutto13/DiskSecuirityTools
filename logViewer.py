import json
from colorama import Fore, init
init(True)

schema = {
    'operation':str,
    'files':{
        'keyFile':str,
        'filenames':list[str],
    }
}

filepath = input("Enter path to your JSON-formatted log file (*.json): ")

with open(filepath, "r") as file:
    data = json.loads(file.read())

print(f"{Fore.CYAN}Operation: {Fore.YELLOW}{data['operation']}")
print(f"{Fore.CYAN}Filepaths:{Fore.YELLOW}{''.join(data['files']['filenames'])}")
print(f"{Fore.CYAN}Used key: {Fore.YELLOW}{data['files']['keyfile']}")

input("That\'s all. <PRESS_ENTER_TO_CLOSE>")