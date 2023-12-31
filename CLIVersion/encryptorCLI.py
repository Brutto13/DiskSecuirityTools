import os
import argparse
import json

from secuirityEncodings import *
from cryptography.fernet import Fernet
from colorama import Fore, Back, Style, init

init(autoreset=True)

# ExitCodes:
FileNotFoundErrorCode = 1
NameErrorCode = 2
TypeErrorCode = 3
ValueErrorCode = 4
UnhandlederrorCode = -1

# Colors
BOOT=Style.BRIGHT + '[BOOT]: '
INFO =  Fore.CYAN + '[INFO]: '
WARN =Fore.YELLOW + '[WARN]: '
ERROR = Fore.RED + '[ERROR]: '
FATAL = Back.RED + '[FATAL]: '

parser = argparse.ArgumentParser()
parser.add_argument('--folder', dest='folder', required=True)
parser.add_argument('--key', dest='keyfile', required=True)
# optional
parser.add_argument('--skip-errors', action='store_true', default=False, required=False, dest='skipErrors')
parser.add_argument('--backup-files', action='store_true', default=False, required=False, dest='makeBackup')
# parser.add_argument('--encrypt-subfolders', action='store_true', default=False, required=False, dest='encryptSubFolders')
# info datas
parser.add_argument('--version', action='store_true', default=False, required=False, dest='showVersionInfo')

args = parser.parse_args()

print(BOOT + 'Parsing')

if args.showVersionInfo:
    print('Version: β-0001')
    input()
    quit()

def crashProgram(ExitCode: str):
    quit(ExitCode)


def Encrypt(folder: str, key_path: str):
    os.chdir(folder)
    print(INFO + 'Enrypting folder: ' + Fore.YELLOW + folder)
    try:
        with open(key_path, "r") as file:
            content = file.readlines()
            key = content[0].encode()
            password = transformMessage("d", content[1], 25)
    except Exception as e:
        if args.skipErrors:
            print(ERROR + f"Failed to load key file ({key})")
            print(ERROR + f"{e}")
            print(FATAL + "Failed to skip this error!")
            quit(f"ExitCode: {UnhandlederrorCode}")

    
    fernet = Fernet(key)
    fileslist = []
    # Ask for password
    passwordEntered = input("Enter Password: ")
    if passwordEntered  == password:
        # create list of excluded files XXX

        
        # print(os.listdir(ent_folderpath.get()))
        # print(dirToEncrypt)
        print(INFO + "Generating Folder Structure...")
        for root, dirs, files in os.walk('.'):
            for filename in files:
                print(INFO + f'Processing file: {Fore.YELLOW}{filename}{Fore.CYAN}...{Fore.RESET}')
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as file:
                    original = file.read()
                
                with open(filepath, "wb") as file:
                    encrypted = fernet.encrypt(original)
                    file.write(encrypted)
                
                if args.makeBackup:
                    with open(filepath+'-origin', "bx") as file:
                        print(INFO + f'Copying original content of file \"{filepath}\" -> \"{filepath+"-origin"}\"')
                        file.write(original)

                fileslist.append(filename)
        
        print(INFO + f'Succesfully encrypted {Fore.YELLOW}{len(fileslist)}{Fore.CYAN}{Fore.RESET}')
        input()


        if input("Do you want to save JSON-formatted log file"):
            with open(f'encryption-lastest-log.json', "x") as file:
                data = {
                    'operation':'ENCRYPTION',
                    'files':{
                        'keyFile':key_path,
                        'filenames':fileslist,
                    }
                }
                file.write(json.dumps(data))

    
    else:
        print(ERROR + "Verification Failed! REASON: \"Wrong Password\"")
    # except FileNotFoundError:
    #     showerror("Encryptor - Error", "No such file or directory (ERR2)")
    # except Exception as e:
    #     showerror("Encryptor - fatal error", f"Fatal exception occured:\n{e}")

Encrypt(args.folder, args.keyfile)