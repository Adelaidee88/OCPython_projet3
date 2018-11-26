class Square:
    # self.x = -1
    # self.y = -1

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    # def salutation(self):
        # print("Bonjour !")

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.name)
