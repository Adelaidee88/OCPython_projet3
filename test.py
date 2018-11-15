from parse import parse
from carre import Square

laby = open("maze.txt", "r")  # ouverture du fichier maze.txt
contenu = laby.read()  # renvoie le contenu du fichier


maze = []  # création de la liste finale du laby (= list_valid)
maze_list = []  # création de la liste de liste de ligne (= map)
maze_str = contenu.splitlines()  # séparation de chaque ligne du fichier en liste de chaines de caractères

#print(maze_str)  # visuel de la liste de chaines de caractère

for line in maze_str:
    maze_list.append(parse(line))  # on parse chaque ligne de caractère pour avoir une liste de listes

#print(maze_list)  # visuel de la liste de listes

for line in maze_list:
    maze.append(parse(line))  # on parse chaque liste de listes


#for l in maze:
    #print(l)

i = 0
while i < len(maze):
    j = 0
    while j < len(maze[i]):
        test = Square(i, j, maze[i][j])
        #print(test)
        j = j + 1
    i = i + 1

