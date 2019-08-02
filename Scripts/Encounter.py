import random
from Monster import Monster
import math

class Encounter:
    def __init__(self, owner):
        # Unsure how we want to do combat exactly, but was thinking we would generate encounters that players then interact with
        # each player can have 1 running encounter essentially, and we'll keep track of all encounters in RPGBot
        # This also allows for multiple people to use the bot at the same time (which is important)
        self.encounterOwner = owner

        # List of monsters in the encounter
        self.monList = []

        # 0 = no change, 1 = +1 to player's stats for this encoutner (for buffs/debuffs, etc)
        self.encounterAtkMod = 0
        self.encounterDefMod = 0
        self.encounterLuckMod = 0

    def generateEncounterByLevel(self, inputLevel):
        # Generate monster based on level typed in by user (can generate encounter of any level, essentially)
        # Make trash mobs worth 2 pt, normal mobs worth 4, and boss/elite mobs worth 6 or 12?
        # max points to gen monsters then is level 20 + 4 = 24, very easily divisible by multiple numbers (1, 2, 3, 4, 6, 8, 12)
        # basically, you get both MORE monsters as you level, as well as HARDER monsters as you level
        totalPoints = inputLevel + 4
        while totalPoints > 1:
            monsterType = random.randint(1,3)

            # Generate monsters based on points allocated based on either the level inputted, or the total number of points
            # allocated to the user which was provided. (ex. Level 1 player has 11 points allocated, Level 20 has 30)
            invalidMonType = False
            mon = Monster()
            #print('montype: ' + str(monsterType))
            #print ('total points: ' + str(totalPoints))
            if monsterType == 1:
                # 4 points weaker than user
                mon.generateMonster(inputLevel + 2)
                totalPoints = totalPoints - 2
            elif monsterType == 2 and totalPoints >= 5:
                # equal to user
                mon.generateMonster(inputLevel + 4)
                totalPoints = totalPoints - 5
            elif monsterType == 3 and totalPoints >= 10:
                # 2 points stronger than user
                mon.generateMonster(inputLevel + 6)
                totalPoints = totalPoints - 10
            else:
                invalidMonType = True
            #print ('total points: ' + str(totalPoints))
            if (not invalidMonType):
                #print('Encounter complete')
                self.monList.append(mon)

    def setOwner(self, userID):
        # set user this encounter is bound to
        self.encounterOwner == userID

    def getOwner(self):
        return self.encounterOwner

    def damageMonster(self, targetNumber, damageNumber):
        # damage a set monster a set amount
        # print ('Before loop')
        # for mon in self.monList:
        #     print(mon.getName())
        # print('After loop')
        self.monList[targetNumber].takeDamage(damageNumber)

    def getMonName(self, target):
        return self.monList[target].getName()

    def isEncounterOver(self):
        isOver = True
        for mon in self.monList:
            if (mon.getCurrentHp() > 0):
                isOver = False
        return isOver

    def getTargetHp(self, target):
        return self.monList[target].getCurrentHp()

    def calcExp(self):
        totalExp = 0
        for mon in self.monList:
            level = mon.getLevel()
            modifier = -1
            if (random.randint(1,3) == 1):
                modifier = 1
            totalExp = (level * 3) + (random.randint(1,level) * modifier)
        return totalExp

    def calcGold(self):
        totalGold = 0
        for mon in self.monList:
            totalGold = totalGold + mon.getLevel()
            modifier = random.randint(1,6)
        totalGold = totalGold * modifier
        return totalGold

    def monsLeft(self):
        monsLeft = 0
        for mon in self.monList:
            if mon.getCurrentHp() > 0:
                monsLeft = monsLeft + 1
        return monsLeft

    def calcTurnDamage(self):
        totalDamage = 0
        for mon in self.monList:
            if (mon.getCurrentHp() > 0):
                totalDamage = totalDamage + mon.calcDamage()
        return totalDamage

    def calcMonsterAttack(self, monsterIndex):
        # Calculate a monster's attack and return that value
        return self.monList[monsterIndex].calcDamage()

    def toString(self):
        # e.x. Below will return "1. MONSTER NAME: [|||||||     ] (7/12)"
        monIndex = 1
        msg = ''
        for monster in self.monList:
            name = monster.getName().upper()
            currentHp = monster.getCurrentHp()
            maxHp = monster.getMaxHp()

            currentHpBar = "\|" * math.floor((currentHp/maxHp) * 30) 
            remainingHpBar = " " * math.floor((1 - (currentHp/maxHp)) * 30)
            hpBar = '[**' + currentHpBar + '**' + remainingHpBar + ']   (' + str(currentHp) + '/' + str(maxHp) + ')  '
            if (currentHp == 0):
                hpBar = '[' + (' ' * 40) + ']   (' + str(currentHp) + '/' + str(maxHp) + ')  '

            msg = msg + (str(monIndex) + ': ' + hpBar + ' Lv. ' + str(monster.getLevel()) + ' ' + name + "\n")
            monIndex = monIndex + 1
        return msg