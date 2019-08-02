# Work with Python 3.6
import discord
import random
import os, subprocess
import math
from Player import Player
from Encounter import Encounter
from datetime import datetime, timedelta
from threading import Timer

client = discord.Client()

playerList = []
encounterList = []
BOT_CHANNEL = 'bot-testing'

'''
# Method to open text a return it in the form of a String
'''
def get_token(filename):
    try:
        tokenFile = open('Tokens/' + filename, 'r')
        token = tokenFile.read().rstrip()
        tokenFile.close()
    except IOError:
        print('Failed to retrieve token from ' + filename)
        exit(1)
    return token

def readSavesFromFile():
    print('Reading saves from file')
    path = "Saves/"

    # Read in every save
    for fileA in os.listdir(path):
        try:
            saveFile = open(path + fileA, 'r')
            saveInfo = saveFile.read()
            saveFile.close()
        except IOError:
            print("Failed to read file: " + fileA)
        #print('Found file: ' + fileA + ', Save info: ' + saveInfo)
        # Split the string into it's individual parts to pass to a new player object
        stringList = saveInfo.split()
        try:
            id = stringList[0]
            exp = stringList[1]
            gold = stringList[2]
            pClass = stringList[3]
            vita = stringList[4]
            stre = stringList[5]
            defe = stringList[6]
            luck = stringList[7]
            levelUps = stringList[8]
            # Create the new player object, and add it to the player list
            newPlayer = Player()
            newPlayer.loadPlayer(id, int(exp), int(gold), pClass, int(vita), int(stre), int(defe), int(luck), int(levelUps))
            playerList.append(newPlayer)
        except:
            print("Could not load a save, skipping this save: " + fileA)
    print('All files read. Loaded ID\'s:')
    for player in playerList:
        #TODO Get username instead of ID?
        print(player.getID())

def getUserInfo(id):
    #print('playerlist len: ' + str(len(playerList)))
    for player in playerList:
        #print ('search id: ' + str(id) + ' | this id: ' + player.getID())
        if (str(player.getID()) == str(id)):
            return player
    #print ('Failed to find player, or there are no players')
    return Player()

def getEncounter(id):
    for enc in encounterList:
        if (enc.getOwner() == id):
            return enc
    return Encounter('')

# Adds a user to the player list, and creates a save for them
def addUser(id, channel, pClass):
    foundUser = False
    global playerList
    print('Players: ')
    if len(playerList) >= 1:
        for player in playerList:
            print(player.getID())
            if (player.getID() == id):
                print('USER ALREADY EXISTS')
                foundUser = True
    if (not foundUser):
        newPlayer = Player()
        newPlayer.generatePlayer(str(id), pClass)
        newPlayer.revive()
        playerList.append(newPlayer)
        print('Added ' + str(newPlayer.getID()))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    onStart()

def onStart():
    readSavesFromFile()
    #loadProgress()

    # On startup, send a message to let users know about the current task progress.
    #channels = getChannels()
    #for channel in channels:
        #await channel.send('**' + getCurrentProgressMessage() + '**' + '\n*[Use !progress to check progress]*')

@client.event
async def on_message(message):
    # get channel command was posted in
    channel = message.channel
    author = message.author
    id = author.id
    userInfo = getUserInfo(id)
    userMention = author.mention

    # we do not want the bot to reply to itself
    if author == client.user:
        return

    # Creates a save for the user if not already created
    elif message.content.startswith('!create'):
        if (getNumOfWords(message.content) == 2):
            userInfo = getUserInfo(id)
            # Check if their ID is in the system
            if userInfo.getID() == '':
                words = message.content.split()
                pClass = words[1].lower()
                if (pClass == 'warrior' or pClass == 'mage' or pClass == 'berserker' or pClass == 'hunter'):
                    # Lets user know they'll be added, and adds them
                    msg = 'Okay, {}, I\'ll create your character!'.format(userMention)
                    await channel.send(msg)
                    addUser(id, channel, words[1])
                    #TODO Remove this print
                    #print (playerList)
                else:
                    msg = 'Sorry, {}, it looks like you didn\'t enter a valid class. Please only use Warrior, Mage, Berserker, or Hunter.'.format(userMention)
                    await channel.send(msg)
            # Otherwise, if their ID is already in the system
            else:
                msg = '{}, looks like you\'ve already created a character!'.format(userMention)
                await channel.send(msg)
        else:
            msg = 'The correct format for this command is "!create [warrior/mage/berserker/hunter]", please try again.'
            await channel.send(msg)

    elif message.content.startswith('!fight'):
        userInfo = getUserInfo(id)
        usersEncounter = getEncounter(id)
        # Make sure character is made, and not in encounter
        if not (userInfo.getID() == '') and (usersEncounter.getOwner() == ''):
            # TODO Do I want to give full hp at start of every fight?
            userInfo.revive()
            newEncounter = Encounter(id)
            level = userInfo.getLevel()
            newEncounter.generateEncounterByLevel(level)
            encounterList.append(newEncounter)
            msg = 'Encounter created. Type !battleinfo to view information on your fight. Best of luck!'
            await channel.send(msg)
        else:
            msg = 'Either a character has not been created, or user is already in an encounter. Try !info and !battleinfo and see if either work.'
            await channel.send(msg)

    elif message.content.startswith('!battleinfo'):
        battleInfo = 'No battle info could be found.'
        for encounter in encounterList:
            if (encounter.getOwner() == id):
                battleInfo = encounter.toString()
        await channel.send(battleInfo)

    elif message.content.startswith('!attack'):
        # Make sure !attack [target]
        if (getNumOfWords(message.content) == 2):
            userInfo = getUserInfo(id)
            if not (userInfo.getID() == ''):
                myEncounter = getEncounter(id)
                # PLAYER EXISTS AND HAS A VALID ENCOUNTER, SO ATTACK
                if not (myEncounter.getOwner() == ''):
                    words = message.content.split()
                    target = int(words[1]) - 1
                    #print ("target: " + words[1])
                    if (myEncounter.getTargetHp(target) > 0):
                        preMonHp = myEncounter.getTargetHp(target)
                        myEncounter.damageMonster(target, userInfo.getStr())
                        afterMonHp = myEncounter.getTargetHp(target)
                        actualDamage = preMonHp - afterMonHp
                        msg = '{} did '.format(userMention) + str(actualDamage) + ' damage to ' + myEncounter.getMonName(target) + ', leaving it with ' + str(afterMonHp) + ' health.'
                        await channel.send(msg)
                        # PLAYER WINS ENCOUNTER
                        if (myEncounter.isEncounterOver()):
                            exp = myEncounter.calcExp()
                            gold = myEncounter.calcGold()
                            currLevel = userInfo.getLevel()
                            userInfo.addExp(exp)
                            userInfo.addGold(gold)
                            msg = 'You won, {}! I will now add '.format(userMention) + str(exp) + ' experience and ' + str(gold) + ' gold to your account.'
                            if (currLevel < userInfo.getLevel()):
                                msg = msg + '\nUser {} leveled up to level '.format(userMention) + str(userInfo.getLevel()) + '!'
                                userInfo.incCanLevel()
                            await channel.send(msg)
                            encounterList.remove(myEncounter)
                        # STILL IN ENCOUNTER
                        else:
                            damageToPlayer = myEncounter.calcTurnDamage() - (myEncounter.monsLeft() * userInfo.getDef())
                            if (damageToPlayer < 1):
                                damageToPlayer = 1
                            userInfo.takeDamage(damageToPlayer)
                            msg = '{} took '.format(userMention) + str(damageToPlayer) + ' damage from monsters, and now has ' + str(userInfo.getCurrentHp()) + ' health.'
                            await channel.send(msg)
                            # PLAYER LOSES ENCOUNTER
                            if (userInfo.isDead()):
                                msg = 'Looks like you died, {}. I\'ll revive you, but you won\'t receive any rewards.'.format(userMention)
                                await channel.send(msg)
                                userInfo.revive()
                                encounterList.remove(myEncounter)
                    else:
                        msg = 'Looks like you\'re trying to hit a dead monster, {}. I mean, maybe that was intentional, but isn\'t that a bit cruel and irresponsible? You should attack one of the monsters that are still alive.'.format(userMention)
                        await channel.send(msg)
                # NO ENCOUNTER FOUND
                else:
                    msg = 'Could not find encounter for {}.'.format(userMention)
                    await channel.send(msg)
            else:
                msg = 'User {}\'s info could not be found'.format(userMention)
                await channel.send(msg)
        else:
            msg = 'The correct format for this command is "!attack [target#]", please try again.'
            await channel.send(msg)

    elif message.content.startswith('!levelup'):
        if (getNumOfWords(message.content) == 2):
            userInfo = getUserInfo(id)
            if not (userInfo.getID() == ''):
                if (userInfo.canLevel()):
                    words = message.content.split()
                    skill = words[1].lower()
                    msg = 'User {} leveled up their '.format(userMention)
                    if (skill == 'vitality'):
                        userInfo.levelUp(1)
                        msg = msg + 'vitality to level ' + str(userInfo.getMaxHp() / 3) + '!'
                    elif (skill == 'strength'):
                        userInfo.levelUp(2)
                        msg = msg + 'strength to level ' + str(userInfo.getStr()) + '!'
                    elif (skill == 'resolve'):
                        userInfo.levelUp(3)
                        msg = msg + 'resolve to level ' + str(userInfo.getDef()) + '!'
                    elif (skill == 'fortune'):
                        userInfo.levelUp(4)
                        msg = msg + 'fortune to level ' + str(userInfo.getLuck()) + '!'
                    else:
                        msg = 'Please enter a valid skill to level up (Vitality (HP), Strength (ATK), Resolve (DEF), or Fortune (LCK)).'
                    await channel.send(msg)
                else:
                    msg = '{}, you cannot currently level up. Please earn more EXP to earn another opportunity to level!'.format(userMention)
                    await channel.send(msg)
            else:
                msg = 'User {}\'s info could not be found'.format(userMention)
                await channel.send(msg)
        else:
            msg = 'The correct format for this command is "!levelup [vitality/strength/resolve/fortune]", please try again.'
            await channel.send(msg)

    # Allows the user to get info on themselves or another user by mentioning them.
    elif message.content.startswith('!info'):
        userToCheck = None
        myMention = None
        words = message.content.split()
        # Ensures the command is being used correctly (1 or 0 mentions, where 0 gets info on yourself).
        if (len(words) > 2):
            await message.channel.send('To get info on someone, you need to mention a single user after typing !info. e.x. \'!info {}\'.'.format(userMention))
            return
        elif (len(message.mentions) == 1):
            userToCheck = message.mentions[0].id
            myMention = message.mentions[0]
        elif (len(words) == 2 and len(message.mentions) == 0):
            await message.channel.send('To get info on someone, you need to mention them after typing !info. e.x. \'!info {}\'.'.format(userMention))
            return
        else:
            userToCheck = id
            myMention = userMention

        userInfo = getUserInfo(userToCheck)
        # If valid user info was found, gets the appropriate info and informs the user.
        if not userInfo.getID() == '':
            msg = ('User {} is a level '.format(myMention) + str(userInfo.getLevel()) + ' ' + 
            userInfo.getClass() + ' with ' + str(userInfo.getCurrentHp()) + ' current health, ' + 
            str(userInfo.getExp()) + ' total experience, and ' + str(userInfo.getGold()) + ' gold.')
            await message.channel.send(msg)
        else:
            await message.channel.send("User info could not be found.")

    # TODO Use this to increase a player's level
    elif message.content.startswith('!+') and str(message.author) == 'Nanoodles#2942':
        words = message.content.split()
        amountToInc = words[2]

        if (len(words) != 3 or not len(message.mentions) == 1 or not isInt(amountToInc)):
            await message.channel.send('The proper syntax to increase daily contributions is \'!+ [@mention] [amount to increase]\'.')
        else:
            userToInc = message.mentions[0].id
            userInfo = getUserInfo(userToInc)
            if not (userInfo.getID() == ''):
                userInfo.incCanLevelXTimes(int(amountToInc))
                await channel.send("{}'s opportunities to level increased by ".format(message.mentions[0]) + str(amountToInc))

    # Prints a list of all the commands that users can use, minus the ones only I can use.
    elif message.content.startswith('!help'):
        msg = ("!join: Join the event if you haven't already!\n" +
            "!contribute: Use your daily contributions to further the progress on the current project.\n"
            "!progress: View information and progress made on the current project.\n" +
            "!info [optional:@user]: Check how many total contributions you've made, how many you can make a day, and whether or not you've already contributed today. If you mention a user, you can view their info.\n")
        await message.channel.send(msg)

# Gets all the channels named #general in all servers the bot is in.
def getChannels():
    channelList = []
    for server in client.guilds:
        for channel in server.channels:
            if channel.name == BOT_CHANNEL:
                channelList.append(channel)
    return channelList

# Checks if a passed in argument is an integer
def isInt(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def getNumOfWords(str):
    if str == '':
        return 0
    else:
        words = str.split()
        return len(words)

# Create a timer to reset people's ability to contribute at midnight.
# currentTime = datetime.today()
# timeToReset = currentTime.replace(day=currentTime.day, hour = 0, minute = 0, second = 0, microsecond = 0) + timedelta(days=1)
# #timeToReset = currentTime.replace(day=currentTime.day, hour = 0, minute = 0, second = 0, microsecond = 0)
# timeDiff = timeToReset - currentTime

# secondsUntilReset = timeDiff.total_seconds()

# resetTimer = Timer(secondsUntilReset, dailyReset)
# resetTimer.start()
# print("Reset timer started, seconds until reset (12am EST): " + str(secondsUntilReset))

# Get the token from the super secret token folder and start the bot
client.run(get_token('discord.txt'))