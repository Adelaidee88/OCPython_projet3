import sys

def parse(s):
    #print(len(s))
    ret = []
    for caracter in s:
        if caracter == "x" or caracter == " " or caracter == "m" or caracter == "v" or caracter == "o":
            ret.append(caracter)  # transformer la suite de caracteres en liste
        else:
            print("erreur1")
            sys.exit(-1)
    if len(ret) != 15:
        print("erreur2") # si la longueur de la chaine de caractères valides est différente de 15
        sys.exit(-1)           # quitte le programme
    return ret
