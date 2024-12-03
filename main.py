import keyboard
import time
import random
import pygame

target = 0
global points
global currentupgrades
points = 0

shopindex = 0
shopitems = ["multipliere", "moreClicks", "rush"]
shopitemscost = [1, 2, 3]
currentupgrades = [0, 0, 0]

def getkeynum():
    if(keyboard.is_pressed("w")):
        return 0
    if(keyboard.is_pressed("a")):
        return 1
    if(keyboard.is_pressed("s")):
        return 2
    if(keyboard.is_pressed("d")):
        return 3
    if(keyboard.is_pressed("e")):
        return 4
    if(keyboard.is_pressed("f")):
        return 5
    if(keyboard.is_pressed("g")):
        return 6

def showshop():
    print(f"Current Shop item: {shopitems[shopindex]}, \nPrice: {shopitemscost[shopindex]}")
    print(f"Current Owned: {currentupgrades[shopindex]}")
    time.sleep(0.75)

def givepoints():
    global points
    global currentupgrades
    points += 1*(pow(1.1, currentupgrades[0]))*(currentupgrades[1]+1)





while True:
    time.sleep(0.1)

    if (getkeynum() == target):
        target = random.randint(0,6)
        givepoints()
        print("Corret keypressed")
        print("New target is " + str(target))
        print(f"Current points: {points}")

    if (keyboard.is_pressed("left")):
        if(shopindex > 0):
            shopindex -= 1
            showshop()

    if (keyboard.is_pressed("right")):
        if(shopindex < (len(shopitems) -1)):
            shopindex += 1
            showshop()
    
    if(keyboard.is_pressed("space")):
        if(points >= shopitemscost[shopindex]):
            points -= shopitemscost[shopindex]
            currentupgrades[shopindex] += 1
            shopitemscost[shopindex] += 1
            showshop()
            print(f"Current points: {points}")
