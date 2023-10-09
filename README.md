# Disc Secuirity Tools
## Encryptor
### Manual
#### Folder Path:
enter path to the folder
that you want to encrypt (The browse button will help you)

#### Key file:
enter path to your key file (*.prv, The button browse will help you)

#### Excluding the files
You can enter paths to files that you
don't want to encrypt (Add button will help you again)

### Warnings:
1) Do not encrypt/loose your private key
2) There are 2 keys Private key (*.prv) and JSON-formatted public key (*.json)

## Decryptor
### Manual
#### Folder path:
enter path to the folder
that you want to decrypt (The browse button will help you)

#### Key file:
enter path to your key file ([...].prv, The button browse will help you)

#### Excluding the files
You can enter paths to files that you
don't want to decrypt (Add button will help you again)

### Warnings:
1) Do not encrypt/loose your private key
2) There are 2 keys Private key ([...].prv) and JSON-formatted public key ([...].json)

## CLI-version
Both programs are avaible in CLI-version.
Arguments are:
### --folder
A path to your folder that you want to encrypt

### --key
A path to your key file (*.prv for private and *.json for public one)

### --backup-files (optional)
Boolean argument. If provided the program will create
backup of original files.
WARNING: Files will have name <filename>.<fileExtension>-origin
for example:
file.txt -> file.txt-origin
file.zip -> file.zip-origin
