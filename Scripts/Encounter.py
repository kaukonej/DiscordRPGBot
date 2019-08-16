import random
from Monster import Monster
import math

class Encounter:
    def __init__(self, owner):
        self.encounterOwner = owner

        # List of monsters in the encounter
        self.monList = []

    '''
    # Returns a list of all the monsters generated for this encounter.
    '''
    def getMonList(self):
        return self.monList

    '''
    # Generate monsters for encounter based on user's level.
    '''
    def generateEncounterByLevel(self, inputLevel):
        totalPoints = inputLevel + 4
        while totalPoints > 1:
            monsterType = random.randint(1,3)
            invalidMonType = False
            mon = Monster()
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
            # Once the monster is made, add it to the list.
            if (not invalidMonType):
                self.monList.append(mon)

    '''
    # Returns a list of monsters with more than 0 health.
    '''
    def getAliveMons(self):
        aliveList = []
        for mon in self.monList:
            if mon.getCurrentHp() > 0:
                aliveList.append(mon)
        return aliveList

    '''
    # Sets the owner of this encounter to the passed in ID.
    '''
    def setOwner(self, userID):
        # set user this encounter is bound to
        self.encounterOwner == userID

    def getOwner(self):
        return self.encounterOwner

    '''
    # Damages a monster a certain amount, based on the move type and the monster's elemental affinities.
    '''
    def damageMonster(self, targetNumber, damageNumber, move):
        monToHit = self.monList[targetNumber]
        modifier = 1.0
        for weakness in monToHit.getWeaknesses():
            if weakness == move.getElement():
                modifier = modifier * 2.0
        for strength in monToHit.getStrengths():
            if strength == move.getElement():
                modifier = modifier / 2.0
        dmgToDo = int(damageNumber * modifier)
        monToHit.takeDamage(dmgToDo)
        return [dmgToDo, modifier]

    '''
    # Returns the name of the monster at the specified index.
    '''
    def getMonName(self, target):
        return self.monList[target].getName()

    '''
    # Checks if all the monsters in an encounter are dead.
    '''
    def isEncounterOver(self):
        isOver = True
        for mon in self.monList:
            if (mon.getCurrentHp() > 0):
                isOver = False
        return isOver

    '''
    # Gets how much HP a specified monster still has.
    '''
    def getTargetHp(self, target):
        return self.monList[target].getCurrentHp()

    '''
    # Calculates how much EXP is rewarded if the encounter is beaten.
    '''
    def calcExp(self):
        totalExp = 0
        for mon in self.monList:
            level = mon.getLevel()
            modifier = -1
            if (random.randint(1,3) == 1):
                modifier = 1
            totalExp = (level * 3) + (random.randint(1,level) * modifier)
        return totalExp

    '''
    # Calculates how much gold is rewarded if the encounter is beaten.
    '''
    def calcGold(self):
        totalGold = 0
        for mon in self.monList:
            totalGold = totalGold + mon.getLevel()
            modifier = random.randint(1,6)
        totalGold = totalGold * modifier
        return totalGold

    '''
    # Returns how many monsters are still alive in an encounter.
    '''
    def monsLeft(self):
        monsLeft = 0
        for mon in self.monList:
            if mon.getCurrentHp() > 0:
                monsLeft = monsLeft + 1
        return monsLeft

    '''
    # Returns a list of attacks from any monsters who are still alive.
    '''
    def getEnemyMoves(self):
        enemyMoves = []
        for mon in self.monList:
            if (mon.getCurrentHp() > 0):
                enemyMoves.append(mon.returnMove())
        return enemyMoves

    '''
    # Calculate a monster's attack and return that value
    '''
    def calcMonsterAttack(self, monsterIndex):
        return self.monList[monsterIndex].calcDamage()

    '''
    # Returns a string regarding monsters and their health for the bot to use.
    '''
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