# KNOWN BUG LIST:
# Health in battles is delayed
# Enemy health doesn't always correspond to what is shown in the text box
# gameText.txt is occassionally read wrong, unknown cause

# TODO
# dynamic xp and levelling system if time allows
# decisions
# loss of defending in path 7
# typewriter effect for the battles

## prerequisites
import random # used for random level generation, damage and flee chance
import os # used for the clear command
import time # used for endings
import sys # used for typewriter effect
from time import sleep # same as line above

# open required game text files
gameTextFile = open("gameText.txt", encoding="utf8") # adding encoding because VSC told me to
roomsFile = open("rooms.txt", encoding = "utf8")
enemiesFile = open("enemies.txt", encoding = "utf8")
gameText = gameTextFile.readlines() # readlines automatically puts linebreaks
rooms = roomsFile.read().splitlines() # read + splitlines does not put linebreaks
enemies = enemiesFile.read().splitlines()

# setting stats
level = 0
xp = 0
maxHealth = 100 + level * 15 # each level max health is increased by 15
health = maxHealth
attack = round(25 + level * 1.5) # each level attack is increased by 1.5x
defence = 5 + level * 5 # each level defense is increased by 5

# setting misc variables
betterShield = False
hasShield = True
fleeSuccess = False

# clear() does NOT work in grok for some dumb reason, but does work in windows/linux
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

# action centre designed to make sure that the file isn't cluttered with the same code
def action_centre():
    global action
    global target
    global fleeSuccess
    commandSuccess = False
    while commandSuccess == False:
        action = input("ACTION: ").upper()
        if action == "ATK":
            while commandSuccess == False:
                target = input("TARGET: ").upper()
                if target == "A":
                    commandSuccess = True
                    target = "A" 
                elif target == "B":
                    commandSuccess = True
                    target = "B"
                elif target == "C":
                    commandSuccess = True
                    target = "C"
                else:
                    print("Pick targets A, B, or C")
        elif action == "DEF":
            commandSuccess = True
        elif action == "FLE":
            commandSuccess = True
            fleeSuccess = bool(random.getrandbits(1))
        else:
            print("Pick action ATK, DEF or FLE")


# typewriter effect command prints 7 lines from the starting line (startLine) in gametext.txt
# it is used in parts of the game when there is no interactivity (area info, story, etc.)
def typewriter(startLine):
    startLine = startLine - 2 # stops from starting lines at 0 and instead the visual line
    currentLine = startLine
    line = gameText[0]
    clear()
    for char in line: # creates starting box shape
        sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()
    while currentLine != startLine + 7: # loops until it hits the 7th line
        currentLine = currentLine + 1
        line = gameText[currentLine]
        for char in line:
            sleep(0.005)
            sys.stdout.write(char)
            sys.stdout.flush()
    line = gameText[1]
    for char in line: # creates ending box shape
        sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()
    input("Press enter to continue:")

# made for code simplicity
def box_top():
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")

def box_action():
    print("┣━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print("  ATK DEF FLE")
    print("┗━━━━━━━━━━━━━┛")

# healing for certain parts of the game
def heal():
    global health
    health = maxHealth

# extremely structred command allows for easy and precise battles with only a few numbers
# all inputs must be ints, room and enemies correspond to the correct lines and health and damage
# are ints, not connected to anything external. select the full name line, not initials
# TODO - add something I forgot
def battle_sequence(battleRoom, battleEnemies, enemiesMaxHealth, enemyAttack, enemyDefence):
    # setting global variables for outside of the function
    global health # stops "Redefining name 'health' from outer scope" error
    global level
    global maxHealth
    global defence
    global attack
    global battleEnemyAHealth
    global battleEnemyBHealth
    global battleEnemyCHealth

    # checking level
    maxHealth = 100 + level * 15 # each level max health is increased by 15
    health = maxHealth
    attack = round(25 + level * 1.5) # each level attack is increased by 1.5x
    if hasShield is False:
        defence = 0
    elif betterShield is True:
        defence = 6 + level * 6 # increases defense by +1 if you did the quest
    else:
        defence = 5 + level * 5 # each level defense is increased by 5

    # setting variables
    battleEnemies = battleEnemies - 1
    turn = 1
    enemyAction = "DEF"
    battleStatus = "nothing"
    battleOver = False
    battleEnemyAHealth = enemiesMaxHealth
    battleEnemyBHealth = enemiesMaxHealth
    battleEnemyCHealth = enemiesMaxHealth
    enemyADead = False
    enemyBDead = False
    enemyCDead = False

    while battleOver == False:

        enemyAttackRand = enemyAttack + random.randrange(int(-enemyAttack/10), int(enemyAttack/10)) # implemented here to avoid "DeprecationWarning"
        playerAttackRand = attack + random.randrange(int(-attack/10), int(attack/10))

        # enemy logic (sort of)
        if health < 10:
            enemyAction = "ATK"
        else:
            enemyActionDecider = random.randrange(1, 3) # can be tweaked if needed
            if enemyActionDecider == 1: # currently 33% chance
                enemyAction = "DEF"
            else:
                enemyAction = "ATK"

        clear()
        print(rooms[battleRoom])
        print("  Pripos", str(health) + "/" + str(maxHealth), "HP")
        print("  A", enemies[battleEnemies + 1], str(battleEnemyAHealth) + "/" + str(enemiesMaxHealth),
            "B", enemies[battleEnemies + 1], str(battleEnemyBHealth) + "/" + str(enemiesMaxHealth),
            "C", enemies[battleEnemies + 1], str(battleEnemyCHealth) + "/" + str(enemiesMaxHealth),)
        box_top()

        if battleStatus == "won":
            battleOver = True
            print("  You defeated", enemies[battleEnemies] + "!")
            level = level + 1
            print("  You earned", random.randrange(10, 50), "xp and are level", level)
        elif battleStatus == "loss":
            battleOver = True
            print("  Game Over! You got captured, and were")
            print("  not able to save The Lost Kingdom...")
            box_action()
            time.sleep(10)
            sys.exit()

        if turn == 1: # only happens on turn 1
            print("  You encounter some", enemies[battleEnemies] + "!")
            print("  What do you do?")
        elif battleOver is False and action == "ATK": # player action top row, enemy action at bottom row
            if enemyADead is True and target == "A" or enemyBDead is True and target == "B" or enemyCDead is True and target == "C":
                print("  They're already dead!")
            else:
                if battleOver is False:
                    print("  You attack", target, enemies[battleEnemies + 1], "for", playerAttackRand)
        elif battleOver is False and action == "DEF":
            print("  You defend for", defence)
        elif battleOver is False and fleeSuccess != 1 and action == "FLE":
            print("  You fail to flee!")
        elif fleeSuccess == 1:
            if fleeSuccess == 1:
                print("  You flee, but the kingdom is")
                print("  still in ruins.")
                box_action()
                time.sleep(10)
                sys.exit()

        if turn > 1 and battleOver is False and enemyAction == "ATK":
            print(" ", enemies[battleEnemies] + " attack for", enemyAttackRand)
            if action != "DEF":
                health = health - enemyAttackRand
        elif turn > 1 and battleOver is False and enemyAction == "DEF":
            print(" ", enemies[battleEnemies] + " defend for", enemyDefence)
            # if turn != 1: # for some reason it breaks without this
            if action == "ATK":
                playerAttackRand = playerAttackRand - enemyDefence

        box_action()

        if battleOver is False: # most likely not necesary
            action_centre()
        else:
            input("Press enter to continue: ")

        if battleOver is False:
            if action == "ATK":
                if target == "A":
                    if battleEnemyAHealth == 0:
                        enemyADead = True
                    else:
                        battleEnemyAHealth = battleEnemyAHealth - playerAttackRand
                elif target == "B":
                    if battleEnemyBHealth == 0:
                        enemyBDead = True
                    else:
                        battleEnemyBHealth = battleEnemyBHealth - playerAttackRand
                else:
                    if battleEnemyCHealth == 0:
                        enemyCDead = True
                    else:
                        battleEnemyCHealth = battleEnemyCHealth - playerAttackRand
            elif action == "DEF":
                if enemyAttackRand > defence and enemyAction == "ATK": # prevents getting extra health when defending
                    health = health - (enemyAttackRand - defence)

            if battleEnemyAHealth < 1: # prevents health from going below 0
                battleEnemyAHealth = 0
            if battleEnemyBHealth < 1:
                battleEnemyBHealth = 0
            if battleEnemyCHealth < 1:
                battleEnemyCHealth = 0

            if battleEnemyAHealth == 0: # stacking so it works (doesn't with and for some reason)
                if battleEnemyBHealth == 0:
                    if battleEnemyCHealth == 0:
                        battleStatus = "won" # win condition
            if health < 0:
                battleStatus = "loss" # loss condition https://cad-comic.com/comic/loss/

        turn = turn + 1

def decision(startLine):
    global pathDecision
    correctAnswer = False
    pathDecision = "nothing"
    startLine = startLine - 2 # stops from starting lines at 0 and instead the visual line
    currentLine = startLine
    line = gameText[0]
    clear()
    for char in line: # creates starting box shape
        sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()
    while currentLine != startLine + 7: # loops until it hits the 7th line
        currentLine = currentLine + 1
        line = gameText[currentLine]
        for char in line:
            sleep(0.005)
            sys.stdout.write(char)
            sys.stdout.flush()
    line = gameText[1]
    for char in line: # creates ending box shape
        sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()
    while correctAnswer is False:
        pathDecision = input("What do you want to do? ").upper()
        if pathDecision == "A":
            correctAnswer = True
        elif pathDecision == "B":
            correctAnswer = True
        else:
            print("Pick option A or B")

def triple_decision(startLine):
    global pathDecision
    correctAnswer = False
    pathDecision = "nothing"
    startLine = startLine - 2 # stops from starting lines at 0 and instead the visual line
    currentLine = startLine
    line = gameText[0]
    clear()
    for char in line: # creates starting box shape
        sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()
    while currentLine != startLine + 7: # loops until it hits the 7th line
        currentLine = currentLine + 1
        line = gameText[currentLine]
        for char in line:
            sleep(0.005)
            sys.stdout.write(char)
            sys.stdout.flush()
    line = gameText[1]
    for char in line: # creates ending box shape
        sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()
    while correctAnswer is False:
        pathDecision = input("What do you want to do? ").upper()
        if pathDecision == "A":
            correctAnswer = True
        elif pathDecision == "B":
            correctAnswer = True
        elif pathDecision == "C":
            correctAnswer = True
        else:
            print("Pick option A, B or C")

def ending(startLine): # shows 7 lines of text in a box and then closes the game
    startLine = startLine - 2 # stops from starting lines at 0 and instead the visual line
    currentLine = startLine
    line = gameText[0]
    clear()
    for char in line: # creates starting box shape
        sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()
    while currentLine != startLine + 7: # loops until it hits the 7th line
        currentLine = currentLine + 1
        line = gameText[currentLine]
        for char in line:
            sleep(0.005)
            sys.stdout.write(char)
            sys.stdout.flush()
    line = gameText[1]
    for char in line: # creates ending box shape
        sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()
    time.sleep(10)
    sys.exit()

clear()

# Introduction
typewriter(3)
typewriter(11)
battle_sequence(1, 1, 50, 10, 10)
heal()

# # Starting mountain
typewriter(19)
typewriter(27)
battle_sequence(19, 9, 60, 10, 5)

# # Dragon cave
typewriter(35)
triple_decision(43)

# Path A from dragon (Q2)
if pathDecision == "A":
    typewriter(52)
    typewriter(60)
    typewriter(68)
    decision(76)
    if pathDecision == "A":
        attack = round(attack * 1.5)
        typewriter(84)
    typewriter(92)
    decision(100)
    if pathDecision == "A":
        ending(109) # ending 5
    # decision B
    heal()
    typewriter(118)
    typewriter(126)
    typewriter(134)
    battle_sequence(13, 5, 80, 15, 10)
    typewriter(142)
    battle_sequence(17, 3, 90, 30, 20)
    typewriter(150)
    typewriter(158)
    ending(166) # ending 4

# Path B from dragon (Q1)
elif pathDecision == "B":
    hasShield = False
    typewriter(175)
    typewriter(183)
    battle_sequence(2, 3, 70, 10, 15)
    typewriter(191)
    battle_sequence(10, 11, 75, 25, 10)
    typewriter(199)
    heal()
    decision(207)
    if pathDecision == "A":
        typewriter(215)
        battle_sequence(3, 7, 80, 20, 5)
        typewriter(223)
        battle_sequence(3, 7, 90, 30, 10)
        typewriter(231)
        heal()
        typewriter(239)
        betterShield = True

# Path C from dragon (Q3)
else:
    typewriter(248)
    decision(256)
    typewriter(264)

# Path B and C merging together
typewriter(273)
typewriter(281)
decision(289)
if pathDecision == "A":
    battle_sequence(0, 3, 250, 70, 50)
    ending(297)
typewriter(305)
typewriter(313)
typewriter(321)
typewriter(329)
battle_sequence(0, 5, 70, 15, 10)
typewriter(337)
typewriter(345)
