import sys


def parse(s):
    """Put a string of 15 characters into a list if they are x, " ", m, v or o"""
    ret = []
    for caracter in s:
        if caracter == "x" or caracter == " " or caracter == "m" or caracter == "v" or caracter == "o":
            ret.append(caracter)  # change string in list of characters
        else:
            print("erreur1")
            sys.exit(-1)
    if len(ret) != 15:
        print("erreur2") # if the length of the list is different of 15
        sys.exit(-1)           # exit the program
    return ret

if __name__ == "__main__":
    pass