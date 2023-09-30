SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUWZXYZ1234567890-=+!@#$%^&*()_[]{};\:"|,./<>?'

def transformMessage(mode: str, message: str, key: int, SymbolKey: str=SYMBOLS):
    '''
    d - deszyfrowanie\n
    s - szyfrowanie\n

    komunikat - `str`\n
    klucz - `int`\n
    '''
    if mode[0] == 'd':
        key = -key
    poPrzekształceniu = ''

    for symbol in message:
        indeksSymbolu = SymbolKey.find(symbol)
        if indeksSymbolu == -1: # Symbol nie znajduje się w SYMBOLE.
            # Dodaj ten symbol bez żadnych zmian.
            poPrzekształceniu += symbol
        else:
            # Szyfrowanie lub deszyfrowanie
            indeksSymbolu += key

            if indeksSymbolu >= len(SymbolKey):
                indeksSymbolu -= len(SymbolKey)
            elif indeksSymbolu < 0:
                indeksSymbolu += len(SymbolKey)

            poPrzekształceniu += SymbolKey[indeksSymbolu]
    return poPrzekształceniu

# def GenerateKeyFile(filename: str, password: str):
    