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
global lastkeypressed
global shopitemscost
global rushActive
global rushCooldown
global rushTime
points = 0
rushActive = False
rushTime = 0
rushCooldown = 300

lastkeypressed = 0

shopindex = 0
shopitems = ["multipliere", "moreClicks", "rush"]
shopitemscost = [1, 2, 3]
priceFactor = [1.1, 1.2, 1.3]
currentupgrades = [0, 0, 0]
keyamountmultiplier = [1, 1 ,1, 1 ,1 ,1, 7]

def getkeynum():
    if(keys[key.W]):
        return 0
    if(keys[key.A]):
         return 1
    if(keys[key.S]):
         return 2
    if(keys[key.D]):
         return 3
    if(keys[key.E]):
        return 4
    if(keys[key.F]):
        return 5
    if(keys[key.G]):
        return 6
    
def newPrice():
    global shopindex
    global shopitemscost
    currentPriceFactor = priceFactor[shopindex]
    shopitemscost[shopindex] = int(shopitemscost[shopindex]*currentPriceFactor)
    
def givepoints(keyindex):
    global points
    global currentupgrades
    global keyamountmultiplier
    if (rushActive):
        points += (1*(pow(1.1, currentupgrades[0]))*(currentupgrades[1]+1))*keyamountmultiplier[keyindex]*(currentupgrades[2]*10)
    #                       multiplier              moreClicks              #difrent per key                    #rush
    else:
        points += (1*(pow(1.1, currentupgrades[0]))*(currentupgrades[1]+1))*keyamountmultiplier[keyindex]

def setrush():
    global rushTime
    global rushActive
    rushTime = 150
    rushActive = True
    
def update(dt):
    global rushActive
    global rushTime
    global rushCooldown
    global points
    global lastkeypressed
    global shopindex
    # Point add
    if (getkeynum() != None and getkeynum() !=lastkeypressed):
        givepoints(getkeynum())
        lastkeypressed = getkeynum()
            
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
            if (shopindex == 2 and currentupgrades[2] == 1):
                setrush()
            
            newPrice()

    if (rushTime > 0):
        rushTime -= 1
    elif (currentupgrades[2] >= 1):
        rushActive = False
        if(rushCooldown <= 0):
            setrush()
            rushCooldown = random.randint(300, 600)
        else:
            rushCooldown -= 1
            print(rushCooldown)
    
pyglet.clock.schedule_interval(update, 0.1)
@window.event
def on_draw():
    global points
    global keyToPress
    global shopindex
    global rushActive
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
    if (rushActive):
        rushBox = pyglet.text.Label( f"Rush Active", 
        font_name='Times New Roman',
        font_size=36,
        x=window.width//2, y=window.height//2 - 100,
        anchor_x='center', anchor_y='center')
        rushBox.color = (255, 0, 0, 255)
        rushBox.draw()
    
    fps_display.draw()

pyglet.app.run()

window.set_visible()