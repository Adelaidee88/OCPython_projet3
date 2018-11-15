import sys
import random # pour le random.sample sinon,
# from random import sample # dans ce cas remplacer random.sample() par sample()


class Square:
    # self.x = -1
    # self.y = -1

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def salutation(self):
        print("Bonjour !")

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.name)


#square = Square(1, 2, "m")
#print(square.x)
#print(square.y)
#square.salutation()
# 5 caractères differents sur la map pour le debug x pour un mur, espace pour une case libre, m pour McGyver,
# v pour vilain, o pour le loot

valid_carac = "x mvo"
map = [["o", "x", " ", " ", "x", "o", "x", " ", " ", "x", "o", "x", " ", " ", "x"], ["o", "x", " ", " ", "x", "o", "x", " ", " ", "x", "o", "x", " ", " ", "x"], ["o", "x", " ", " ", "x", "o", "x", " ", " ", "x", "o", "x", " ", " ", "x"]]
# liste de test pour voir si # parse() renvoie bien une liste quand une liste en paramètre
list_valid = []


def parse(s):
    #print(len(s))
    ret = []
    for caracter in s:
        if caracter == "x" or caracter == " " or caracter == "m" or caracter == "v" or caracter == "o":
            ret.append(caracter) # transformer la suite de caracteres en liste
        else:
            print("erreur1")
            sys.exit(-1)
    if len(ret) != 15:
        print("erreur2") # si la longueur de la chaine de caractères valides est différente de 15
        sys.exit(-1)           # quitte le programme
    return ret

# automatisation pour passer une liste, une liste de liste, ou un fichier

# liste de liste pour coordonnées ? avec liste_lignes de liste_valid qui correpond à une ligne, et donc 15 entrées dans
# liste_lignes
# juste une liste de coordonnées ? sur la base de coordonnee = [(square.x, square.y)] avec x et y de 1 à 15
# stockage coordonnées des cases vides liste free_square. On ajoute coordonnées à la liste quand caracter == " "
# random.sample(free_square, 3) et y placer o


for line in map:
    list_valid.append(parse(line))

print(list_valid[0][0])

for l in list_valid:
    print(l)

i = 0
while i < len(list_valid):
    j = 0
    while j < len(list_valid[i]):
        test = Square(i, j, list_valid[i][j])
        print(test)
        j = j + 1
    i = i + 1



# parse("nope")

# parse retourne une liste de caractères valides, vérifier que la ligne fait 15x15 ni plus ni moins sinon quit,
# automatiser pour pouvoir passer liste, liste de liste, ou un fichier qui contient du texte (une des deux)
# cours https://docs.python.org/2/library/random.html pour mettre aléatoirement des o sur des cases
# retranscrire implémentation pour le projet

# preparer un fichier texte sous la forme d'une map valide de 15x15 avec "x mv" (pas les objets) que je dois lire,
# le parser, ajouter le tout dans une map, l'afficher pour voir si ça marche. (code à modifier)

