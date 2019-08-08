from Move import Move

class Player:

    def __init__(self):
        self.playerID = ''
        self.charClass = ''

        # EXP = level. Calculated based on how much experience your character has, gain more exp from failed rolls (6 or less)
        # Level 1 = 5exp, 2 = 5+10xp (15xp), 3=5+10+15xp (30xp), etc. lvl 20 = level 19 + 100xp (1050xp)
        self.experience = 0

        # TODO Currency to buy things? Idk what we'll do with these but leaving this here for later
        self.goldPieces = 0

        # Stats
        # Vitality = Health. Increases by 10's. Max 120.
        self.currentHp = 30
        self.vitality = 12
        # Strength = Attack. Increases by 1's. Max 10.
        self.strength = 2
        # Resolve = Defense. Increases by 1's. Max 10.
        self.resolve = 2
        # Fortune = Luck. Increases by 1's. Max 10.
        self.fortune = 2

        self.timesCanLevel = 0

        #Elements: Fire, water, ice, earth, air, electric, dark
        self.weaknesses = []
        self.strengths = []
        self.moveSet = []

    # Used to contain info about players. Can have the system save this object to a file which can be read by the bot.
    def generatePlayer(self, username, className):
        self.playerID = username
        self.charClass = className

        if self.charClass.lower() == 'warrior':
            self.resolve = 3
        elif self.charClass.lower() == 'mage':
            self.vitality = 20
            self.strength = 3
            self.fortune = 3
        elif self.charClass.lower() == 'berserker':
            self.vitality = 40
            self.strength = 3
            self.fortune = 1
        elif self.charClass.lower() == 'hunter':
            self.vitality = 20
            self.fortune = 4

        self.setMovesAndElements()

        self.currentHp = self.vitality

        self.timesCanLevel = 0

        # Write info to file using playerID. Probably name it playerID.txt in a folder called "Saves"
        if (not (self.playerID == '')):
            self.writeInfo()

    def setMovesAndElements(self):
        if self.charClass.lower() == 'warrior':
            self.weaknesses = ['Fire', 'Electric']
            self.strengths = ['Earth', 'Air']
            earthAttack = Move('Groundbreaking Strike', 15, 'Earth', 30)
            airAttack = Move('Skyward Slash', 20, 'Air', 10)
            self.moveSet = [earthAttack, airAttack]
        elif self.charClass.lower() == 'mage':
            self.weaknesses = ['Ice', 'Air']
            self.strengths = ['Dark', 'Fire']
            explosionAttack = Move('Bakuretsu', 25, 'Fire', 5)
            darkAttack = Move('Dragon of the Darkness Flame', 20, 'Dark', 15)
            self.moveSet = [explosionAttack, darkAttack]
        elif self.charClass.lower() == 'berserker':
            self.weaknesses = ['Water', 'Dark']
            self.strengths = ['Electric', 'Fire']
            thunderAttack = Move('Thunder Cross Split Attack', 15, 'Electric', 30)
            fireAttack = Move('Scarlet Overdrive', 20, 'Fire', 10)
            self.moveSet = [thunderAttack, fireAttack]
        elif self.charClass.lower() == 'hunter':
            self.weaknesses = ['Earth', 'Fire']
            self.strengths = ['Water', 'Dark']
            waterAttack = Move('Flowing Finisher', 30, 'Water', 0)
            darkAttack = Move('Silent Strike', 20, 'Dark', 50)
            self.moveSet = [waterAttack, darkAttack]

    def getMoveset(self):
        return self.moveSet

    def getWeaknesses(self):
        return self.weaknesses

    def getStrengths(self):
        return self.strengths

    def loadPlayer(self, username, experience, gold, className, vita, stre, defe, luck, levelUps):
        self.playerID = username
        self.charClass = className
        self.experience = experience
        self.goldPieces = gold
        self.charClass = className
        self.vitality = vita
        self.strength = stre
        self.resolve = defe
        self.fortune = luck
        self.timesCanLevel = levelUps

    def levelUp(self, skillChoice):
        if (skillChoice == 1):
            self.vitality = self.vitality + 10
        elif (skillChoice == 2):
            self.strength = self.strength + 1
        elif (skillChoice == 3):
            self.resolve = self.resolve + 1
        elif (skillChoice == 4):
            self.fortune = self.fortune + 1
        else:
            # throw an error?
            return
        self.writeInfo()
        self.timesCanLevel = self.timesCanLevel - 1

    def getID(self):
        return self.playerID

    def getCurrentHp(self):
        return self.currentHp

    def getMaxHp(self):
        return self.vitality

    def getStr(self):
        return self.strength

    def getDef(self):
        return self.resolve
    
    def getLuck(self):
        return self.fortune

    def getExp(self):
        return self.experience
    
    def getGold(self):
        return self.goldPieces

    def addExp(self, total):
        self.experience = self.experience + int(total)
        self.writeInfo()

    def addGold(self, total):
        self.goldPieces = self.goldPieces + int(total)
        self.writeInfo()

    def getMaxMoveIndex(self):
        num = 0
        for move in self.moveSet:
            num = num + 1
        #print ("max move index: " + str(num - 1))
        return num - 1

    def takeDamage(self, damage, element):
        damageToDo = damage
        for weakness in self.weaknesses:
            if (weakness == element):
                damageToDo = damageToDo * 2
                break
        for stren in self.strengths:
            if (stren == element):
                damageToDo = damageToDo / 2
                break
        DEFENSE_MODIFIER = 10
        actualDamage = int(damageToDo - (self.resolve * DEFENSE_MODIFIER))
        if (actualDamage < 1):
            actualDamage = 1
        self.currentHp = self.currentHp - actualDamage
        #print ('to player, last num returned: ' + str(damageToDo) + ' - ' + str(self.resolve * DEFENSE_MODIFIER) + ' = ' + str(actualDamage))
        return actualDamage

    def revive(self):
        self.currentHp = self.vitality

    def incCanLevel(self):
        self.timesCanLevel = self.timesCanLevel + 1
        self.writeInfo()

    def incCanLevelXTimes(self, total):
        self.timesCanLevel = self.timesCanLevel + total
        self.writeInfo()

    def canLevel(self):
        if (self.timesCanLevel > 0):
            return True
        else:
            return False

    def isDead(self):
        if (self.currentHp < 1):
            return True
        else:
            return False

    def getLevel(self):
        expPerLevel = 5
        currentLevel = 1
        exp = self.experience
        while(exp > expPerLevel):
            exp = exp - expPerLevel
            expPerLevel = expPerLevel + 5
            currentLevel = currentLevel + 1
        return currentLevel

    def getClass(self):
        return str(self.charClass)

    def writeInfo(self):
        file = open('Saves/' + str(self.playerID) + '.txt', 'w+')
        thingsToSave = [self.playerID, self.experience, self.goldPieces, self.charClass, self.vitality, self.strength, self.resolve, self.fortune, self.timesCanLevel]
        for thing in thingsToSave:
            file.write(str(thing) + ' ')
        file.close()