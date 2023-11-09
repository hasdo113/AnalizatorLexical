delimitatori = "();[]{}"
keywords = ['break', 'case', 'char', 'const', 'countinue', 'deafult', 'do', 'int', 'else', 'float',
            'for', 'if', 'long', 'return', 'short', 'signed', 'static', 'switch',
            'unsigned', 'void', 'while', 'main']  # main inclus
operatori = {'--', '++', '+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '&', '|', '^', '~',
             '>>', '<<', '=', '+=', '-=', '*='}

# Citesc continutul fisierului intr-o variabila
fisier = open("lexical.txt", "r")
continut = fisier.read()
continut = continut + " "  # Are nevoie de spatiu de final altfel nu ia ultimul lucru, pycharm sterge spatiul
numar_inceput_comentarii = continut.count("/*")
numar_sfarsit_comentarii = continut.count("*/")


def lex():
    buffer = ""
    linii = 0  # Incepem cu 0 si adaugam cate + 1 la printuri
    comentariu = 0  # Facem 0 si 1
    # Citim litera cu litera fisierul
    for caracter in continut:
        # Numar liniiei
        if caracter == '\n':
            linii = linii + 1  # De adaugat +1 la printur
        alnum = caracter.isalnum() or caracter in operatori  # Daca este alfanumeric sau operator (va fi negat)
        buffalnum = buffer[:-1].isalnum()  # Ultimul caracter alfanumeric -> daca este litera si urmeaza operator
        buffandop = buffalnum and caracter in operatori  # Aici le separa (ex beta++)
        numandbuff = buffer[:-1].isnumeric() and caracter.isalpha()
        conditie1 = not alnum or buffandop or numandbuff or caracter == ""  # Separa cuvintele intre ele, in special cand ajunge la spatiu/operator
        conditie2 = not caracter == "." or (
                caracter == "." and "." in buffer)  # Separa 2 delimitatoare una de alta, de exemplu 2 puncte (13.78.74)
        if conditie1 and conditie2:
            if buffer == "*/":
                comentariu = 0
                buffer = ""
            elif comentariu == 1 and buffer:
                print(buffer, ': comentariu ; lungime', len(buffer), '; linia', linii + 1)
                buffer = ""
            elif buffer in keywords:
                print(buffer, ': keyword ; lungime', len(buffer), '; linia', linii + 1)
                buffer = ""
            elif buffer in operatori:
                print(buffer, ': operator ; lungime', len(buffer), '; linia', linii + 1)
                buffer = ""
            elif "." in buffer:
                print(buffer, ': float ; lungime', len(buffer), '; linia', linii + 1)
                buffer = ""
            elif buffer == "/*":
                comentariu = 1
                buffer = ""
            elif buffer.isnumeric():
                print(buffer, ': int ; lungime', len(buffer), '; linia', linii + 1)
                buffer = ""
            elif buffer:
                conditie3 = buffer[0].isnumeric() or buffer[0] in operatori
                # ^ Daca incepe cu numar sau operator atunci eroare
                if conditie3:
                    print(buffer, ': EROARE ; lungime', len(buffer), '; linia', linii + 1)
                    buffer = ""
                else:
                    print(buffer, ': identifier ; lungime', len(buffer), '; linia', linii + 1)
                    buffer = ""
        conditie4 = caracter.isalnum() or caracter in operatori or caracter == "."  # Conditia de adaugat in buffer
        if caracter in delimitatori:
            print(caracter, ': delimitator ; lungime 1', '; linia', linii + 1)
            continue
        elif conditie4:  # Litera sau operator o adauga in cuvant
            buffer = buffer + caracter


if not numar_inceput_comentarii == numar_sfarsit_comentarii:
    print("EROARE : Nu ai inchis comentarii")
else:
    lex()
