import random

class Monster:
    def __init__(self):
        self.adjective = ''
        self.monName = ''
        # Stats
        # Vitality = Health. Increases by 3's. Max 30.
        self.currentHp = 3
        self.vitality = 3
        # Strength = Attack. Increases by 1's. Max 10.
        self.strength = 1
        # Resolve = Defense. Increases by 1's. Max 10.
        self.resolve = 1
        # Fortune = Luck. Increases by 1's. Max 10.
        self.fortune = 1

        #TODO Add elemental weaknesses/strengths?

    def getLevel(self):
        return int(((self.vitality/3) + self.strength + self.resolve + self.fortune) - 6)

    def giveName(self):
        possibleNames = ['Orc', 'Dark Elf', 'Wizard', 'Goblin', 'Warlord', 'Lich', 'Skeleton', 'Demon', 'Troll', 'Giant', 'Thief', 'Vampire', 'Mercenary', 'Specter', 'Slime']
        possibleAdjectives = ['Strong', 'Jittery', 'Prideful', 'Hideous', 'Evil', 'Strange', 'Fierce', 'Grotesque', 'Bloodthirsty', 'Vile', 'Mysterious', 'Ancient', 'Noble', 'Deformed']
        self.monName = possibleNames[random.randint(0, len(possibleNames) - 1)]
        self.adjective = possibleAdjectives[random.randint(0, len(possibleAdjectives) - 1)]

    def generateMonster(self, totalPoints):
        # levels the monster a set number of points up
        while totalPoints > 0:
            ranNum = random.randint(1,4)
            if ranNum == 1:
                self.vitality = self.vitality + 3
                self.currentHp = self.vitality
            elif ranNum == 2:
                self.strength = self.strength + 1
            elif (ranNum == 3):
                self.resolve = self.resolve + 1
            else:
                self.fortune = self.fortune + 1
            totalPoints = totalPoints - 1
        self.giveName()

    def takeDamage(self, damageDone):
        totalDamage = (damageDone - self.resolve)
        if (totalDamage < 2):
            self.currentHp = self.currentHp - 1
        else:
            self.currentHp = self.currentHp - totalDamage
        if self.currentHp < 0:
            self.currentHp = 0

    def calcDamage(self):
        # For now, will just return strength. We can make multiple moves if we want to be fancy and use a random num gen
        return self.strength
        
    def getCurrentHp(self):
        return self.currentHp

    def getMaxHp(self):
        return self.vitality

    def getName(self):
        return self.adjective + ' ' + self.monName