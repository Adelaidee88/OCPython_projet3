class Loot:
    """Loot characterized by coordinates,
    name and picked status"""

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.picked = False
