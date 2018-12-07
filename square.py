class Square:
    """Define a case of the labyrinth
    with its coordinates and its name value"""

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return str(self.x) + " " + \
               str(self.y) + " " + str(self.name)
