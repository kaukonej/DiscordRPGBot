import random
from Move import Move

class Monster:
    def __init__(self):
        self.adjective = ''
        self.monName = ''
        # Stats
        # Vitality = Health. Increases by 10's. Max 120.
        self.currentHp = 10
        self.vitality = 10
        # Strength = Attack. Increases by 1's. Max 10.
        self.strength = 1
        # Resolve = Defense. Increases by 1's. Max 10.
        self.resolve = 1
        # Fortune = Luck. Increases by 1's. Max 10.
        self.fortune = 1

        # Keeps track of elements a monster is weak/strong to, as well as what element they are/attack with.
        self.element = ''
        self.weaknesses = []
        self.strengths = []

        self.possibleNames = ['Orc', 'Dark Elf', 'Wizard', 'Goblin', 'Warlord', 'Lich', 'Skeleton', 'Demon', 'Troll', 'Giant', 'Thief', 'Vampire', 'Mercenary', 'Specter', 'Slime']
        self.possibleAdjectives = ['Strong', 'Jittery', 'Prideful', 'Hideous', 'Evil', 'Strange', 'Fierce', 'Grotesque', 'Bloodthirsty', 'Vile', 'Mysterious', 'Ancient', 'Noble', 'Deformed']

    def getNames(self):
        return self.possibleNames

    def getAdjectives(self):
        return self.possibleAdjectives

    def setName(self, name):
        self.monName = name

    def setAdj(self, adj):
        self.adjective = adj

    '''
    # Used to calculate what level a monster is.
    '''
    def getLevel(self):
        return int(((self.vitality/10) + self.strength + self.resolve + self.fortune) - 6)

    '''
    # Randomly assigns a monster a name (determines defensive affinities) and adjective (determines offensive element)
    '''
    def giveName(self):
        self.monName = self.possibleNames[random.randint(0, len(self.possibleNames) - 1)]
        self.adjective = self.possibleAdjectives[random.randint(0, len(self.possibleAdjectives) - 1)]

    '''
    # Gives a monster an element, randomly, based on their adjective.
    '''
    def giveElement(self):
        self.element == None
        #print('Give element')
        #print('------' + self.monName + '------')
        random.seed(self.getElementSeed())
        ranNum = random.randint(1, 7)
        if (ranNum == 1):
            self.element = ('Fire')
        elif (ranNum == 2):
            self.element =('Water')
        elif (ranNum == 3):
            self.element =('Ice')
        elif (ranNum == 4):
            self.element =('Earth')
        elif (ranNum == 5):
            self.element =('Electric')
        elif (ranNum == 6):
            self.element =('Dark')
        elif (ranNum == 7):
            self.element =('Air')

    def getElement(self):
        return self.element

    '''
    # Gives monster 3 weaknesses, based on their name/race.
    '''
    def giveWeaknesses(self):
        self.weaknesses = []
        randomModifier = 0
        while len(self.weaknesses) < 3:
            random.seed(self.getNameSeed() + randomModifier)
            ranNum = random.randint(1, 7)
            weakness = ''
            if (ranNum == 1):
                weakness = ('Fire')
            elif (ranNum == 2):
                weakness = ('Water')
            elif (ranNum == 3):
                weakness = ('Ice')
            elif (ranNum == 4):
                weakness = ('Earth')
            elif (ranNum == 5):
                weakness = ('Electric')
            elif (ranNum == 6):
                weakness = ('Dark')
            elif (ranNum == 7):
                weakness = ('Air')

            alreadyHaveWeakness = False
            # Don't add the same weakness twice!
            for wk in self.weaknesses:
                if weakness == wk:
                    alreadyHaveWeakness = True
            if not (alreadyHaveWeakness):
                self.weaknesses.append(weakness)
            randomModifier = randomModifier + 1

    def getWeaknesses(self):
        return self.weaknesses

    '''
    # Gives a monster 2 strengths, based on their name/race, which are not already weaknesses.
    '''
    def giveStrengths(self):
        self.strengths = []
        randomModifier = 0
        while len(self.strengths) < 2:
            stren = ''
            random.seed(self.getNameSeed() + randomModifier)
            ranNum = random.randint(1, 7)
            if (ranNum == 1):
                stren = ('Fire')
            elif (ranNum == 2):
                stren =('Water')
            elif (ranNum == 3):
                stren =('Ice')
            elif (ranNum == 4):
                stren =('Earth')
            elif (ranNum == 5):
                stren =('Electric')
            elif (ranNum == 6):
                stren =('Dark')
            elif (ranNum == 7):
                stren =('Air')
            
            alreadyHaveStr = False
            # Make sure it isn't already a strength or weakness before adding it!
            for wk in self.weaknesses:
                if stren == wk:
                    alreadyHaveStr = True
            for st in self.strengths:
                if stren == st:
                    alreadyHaveStr = True
            if not (alreadyHaveStr):
                self.strengths.append(stren)
            randomModifier = randomModifier + 1

    def getStrengths(self):
        return self.strengths

    '''
    # Randomly assigns stats to a monster based on a total number of points passed in.
    '''
    def generateMonster(self, totalPoints):
        # levels the monster a set number of points up
        while totalPoints > 0:
            ranNum = random.randint(1,4)
            if ranNum == 1:
                self.vitality = self.vitality + 10
                self.currentHp = self.vitality
            elif ranNum == 2:
                self.strength = self.strength + 1
            elif (ranNum == 3):
                self.resolve = self.resolve + 1
            else:
                self.fortune = self.fortune + 1
            totalPoints = totalPoints - 1
        self.giveName()
        self.giveElement()
        #3 weaknesses, 2 strengths
        self.giveWeaknesses()
        self.giveStrengths()

    '''
    # Take damage based on both the passed in damage number, as well as the monster's defense.
    '''
    def takeDamage(self, damageDone):
        DEFENSE_MODIFIER = 5
        totalDamage = (damageDone - (self.resolve * DEFENSE_MODIFIER))
        if (totalDamage < 2):
            self.currentHp = self.currentHp - 1
        else:
            self.currentHp = self.currentHp - totalDamage
        if self.currentHp < 0:
            self.currentHp = 0
        return damageDone

    '''
    # Returns the element and power that this monster attacks with.
    '''
    def returnMove(self):
        return Move('', self.strength * random.randint(2,5), self.element, 0)
        
    def getCurrentHp(self):
        return self.currentHp

    def getMaxHp(self):
        return self.vitality

    def getName(self):
        return self.adjective + ' ' + self.monName

    '''
    # Get a seed based on this monster's name, used for elemental weaknesses/strengths.
    '''
    def getNameSeed(self):
        seed = 0
        for letter in self.monName:
            seed = seed + ord(letter)
        return seed

    '''
    # Get a seed based on this monster's adjective, used for it's offensive element.
    '''
    def getElementSeed(self):
        seed = 0
        for letter in self.adjective:
            seed = seed + ord(letter)
        return seed