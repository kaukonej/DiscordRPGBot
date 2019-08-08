class Move:
    def __init__(self, name, damage, element, crit):
        self.name = name
        self.damage = damage
        self.element = element
        self.critChange = crit

    def getName(self):
        return self.name

    def getDamage(self):
        return self.damage

    def getElement(self):
        return self.element