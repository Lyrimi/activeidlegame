import keyboard
import time
import random
import pyglet
from pyglet.window import key

window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)
fps_display = pyglet.window.FPSDisplay(window=window)
target = 0
global points
global currentupgrades
global keyToPress
global shopitemscost
points = 0

keyToPress = key.W

shopindex = 0
shopitems = ["multipliere", "moreClicks", "rush"]
shopitemscost = [1, 2, 3]
priceFactor = [1.1, 1.2, 1.3]
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
    
def newPrice():
    global shopindex
    global shopitemscost
    currentPriceFactor = priceFactor[shopindex]
    shopitemscost[shopindex] = int(shopitemscost[shopindex]*currentPriceFactor)
    
def givepoints():
    global points
    global currentupgrades
    #                       multiplier              moreClicks
    points += 1*(pow(1.1, currentupgrades[0]))*(currentupgrades[1]+1)
    
def update(dt):
    global points
    global keyToPress
    global shopindex
    # Point add
    if keys[key.W]:
        if keyToPress == key.W:
            givepoints()
            keyToPress = key.S
    
    if keys[key.S]:
        if keyToPress == key.S:
            givepoints()
            keyToPress = key.W
            
    if keys[key.LEFT]:
        if(shopindex > 0):
            shopindex -= 1
    
    if keys[key.RIGHT]:
        if(shopindex < (len(shopitems) -1)):
            shopindex += 1
            
    if keys[key.SPACE]:
        if(points >= shopitemscost[shopindex]):
            points -= shopitemscost[shopindex]
            currentupgrades[shopindex] += 1
            shopitemscost[shopindex] += 1
            newPrice()
    
pyglet.clock.schedule_interval(update, 0.1)
@window.event
def on_draw():
    global points
    global keyToPress
    global shopindex
    window.clear()
    pointsBox = pyglet.text.Label( str(points),
        font_name='Times New Roman',
        font_size=36,
        x=window.width//2, y=window.height//2 + 50,
        anchor_x='center', anchor_y='center')
    pointsBox.draw()
    
    shopBox = pyglet.text.Label( f"Current Shop item: {shopitems[shopindex]}, \nPrice: {shopitemscost[shopindex]}", 
        font_name='Times New Roman',
        font_size=36,
        x=window.width//2, y=window.height//2,
        anchor_x='center', anchor_y='center')
    shopBox.draw()
    
    upgradeCountBox = pyglet.text.Label( f"Current upgrades: {currentupgrades[shopindex]}", 
        font_name='Times New Roman',
        font_size=36,
        x=window.width//2, y=window.height//2 - 50,
        anchor_x='center', anchor_y='center')
    upgradeCountBox.draw()
    
    fps_display.draw()

pyglet.app.run()


window.set_visible()