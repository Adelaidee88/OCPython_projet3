from square import *

class Map:

    def __init__(self, lst):
        self.lst = []
        i = 0
        while i < len(lst):
            j = 0
            while j < len(lst[i]):
                test = Square.__init__(i, j, lst[i][j])
                print(test)
                j = j + 1
            i = i + 1
