import time
import random
import pyglet
from pyglet.window import key

window = pyglet.window.Window(fullscreen=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)
fps_display = pyglet.window.FPSDisplay(window=window)
target = 0

global lost
global losttimer

global points
global currentupgrades
global lastkeypressed
global shopitemscost
global rushActive
global rushCooldown
global rushTime
global renttimer
global rentamount
global rentgrow
global rentactive
global rentmaxtimer
shopitems = ["Multipliere", "MoreClicks", "Rush", "AutoClicker DON'T", "Increase Rent"]
shopItemColor = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (0, 255, 255, 255), (255, 0, 255, 0 )]
priceFactor = [1.15, 1.05, 1.25, 10, 1]

def reset():
    global lost
    global losttimer
    lost = False
    losttimer = 200
    
    global points
    global currentupgrades
    global lastkeypressed
    global shopitemscost
    global rushActive
    global rushCooldown
    global rushTime
    global renttimer
    global rentamount
    global rentgrow
    global rentactive
    global rentmaxtimer
    rentmaxtimer = 100
    rentactive = False
    rentgrow = 1.05
    rentamount = 5
    renttimer = 100
    points = 0
    rushActive = False
    rushTime = 0
    rushCooldown = 300
    
    lastkeypressed = key.W
    
    
    shopitemscost = [1, 5, 20, 1_000_000, 0]
    
    currentupgrades = [0, 0, 0, 0, 0]

reset()
    

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
    
def newPrice(index):
    global shopitemscost
    currentPriceFactor = priceFactor[index]
    shopitemscost[index] = int(shopitemscost[index]*currentPriceFactor)
    
def givepoints():
    global points
    global currentupgrades
    global keyamountmultiplier
    if (rushActive):
        points += (1*(pow(1.1, currentupgrades[0]))*(currentupgrades[1]+1))*(currentupgrades[2]*10)*(currentupgrades[4]+1)
    #                       multiplier              moreClicks                   #rush
    else:
        points += (1*(pow(1.1, currentupgrades[0]))*(currentupgrades[1]+1))

def setrush():
    global rushTime
    global rushActive
    rushTime = 150
    rushActive = True
    
def update(dt):
    global rentamount
    global renttimer
    global rushActive
    global rushTime
    global rushCooldown
    global points
    global lastkeypressed
    global shopindex
    global lost
    global rentactive
    global rentmaxtimer
    global rentgrow
    global losttimer
    # Point add
    if (getkeynum() != None):
        pressedkey = getkeynum()
        if(pressedkey < len(shopitems)):
            
            if(points >= shopitemscost[pressedkey]):
                points -= shopitemscost[pressedkey]
                currentupgrades[pressedkey] += 1
                shopitemscost[pressedkey] += 1
                if (pressedkey == 2 and currentupgrades[2] == 1):
                    setrush()
                newPrice(pressedkey)
        #givepoints(getkeynum())
        #lastkeypressed = getkeynum()
            
    if keys[key.LEFT] and lastkeypressed != key.LEFT:
        givepoints()
        lastkeypressed = key.LEFT
    
    if keys[key.RIGHT] and lastkeypressed != key.RIGHT:
        givepoints()
        lastkeypressed = key.RIGHT

    if (rushTime > 0):
        rushTime -= 1
    elif (currentupgrades[2] >= 1):
        rushActive = False
        if(rushCooldown <= 0):
            setrush()
            rushCooldown = random.randint(300, 600)
        else:
            rushCooldown -= 1
    
    if (renttimer > 0 and rentactive):
        renttimer -=1
    elif (rentactive):
        points -= rentamount 
        rentamount = rentamount*rentgrow
        renttimer = rentmaxtimer

        if(points < 0):
            lost = True
    elif (points > 10):
        rentactive = True

    if(keys[key.H]):
        rentmaxtimer = 0 
        rentactive = True
        renttimer = 0
        rentgrow = 2
    if(keys[key.R]):
        reset()

    if(keys[key.ESCAPE]):
        pyglet.app.exit()
    if(losttimer > 0 and lost == True):
        losttimer -= 1
    elif(lost == True):
        reset()

    
pyglet.clock.schedule_interval(update, 0.1)
@window.event
def on_draw():
    global points
    global keyToPress
    global shopindex
    global rushActive
    global rentactive
    global rentamount
    global renttimer
    global lost
    global losttimer
    window.clear()
    if (lost == False):
        pointsBox = pyglet.text.Label( f"Points:\n{points.__round__(2)}",
            font_name='Times New Roman',
            font_size=64,
            x=window.width//2, y=window.height - 80,
            anchor_x='center', anchor_y='center',
            multiline=True, width=200,
            align='center')
        pointsBox.draw()
        
        shopBorder = pyglet.shapes.BorderedRectangle(0, 0, width=window.width, height=window.height//2, color=(0, 0, 0), border_color=(255, 255, 255), border=5)
        shopBorder.draw()
        
        for i in range(len(shopitems)):
            # Draw shop items with colored circles at the start of the text
            shopCircle = pyglet.shapes.Circle(window.width//2 - 100, window.height//2 - 50 - i*50, 20, color=shopItemColor[i])
            shopCircle.draw()
            shopItem = pyglet.text.Label( f"{shopitems[i]}: {shopitemscost[i]}",
            font_name='Times New Roman',
            font_size=36,
            x=window.width//2 - 50, y=window.height//2 - 50 - i*50,
            anchor_x='left', anchor_y='center')
            shopItem.draw()
        
        if (rushActive):
            rushBox = pyglet.text.Label( f"Rush Active", 
            font_name='Times New Roman',
            font_size=36,
            x=window.width - 500, y=window.height - 50,
            anchor_x='center', anchor_y='center')
            rushBox.color = (255, 0, 0, 255)
            rushBox.draw()
        
        if (rentactive):
            rentBox = pyglet.text.Label( f"Rent Due: {rentamount.__round__(2)} points in {renttimer/10} seconds",
            font_name='Times New Roman',
            font_size=12,
            # top left corner 
            x=20, y=window.height - 20,
            anchor_x='left', anchor_y='top')
            rentBox.draw()
    else:
        lostBox = pyglet.text.Label( f"YOU LOST", 
            font_name='Times New Roman',
            font_size=52,
            x=window.width//2, y=window.height//2,
            anchor_x='center', anchor_y='center')
        lostBox.draw()
        resetBox = pyglet.text.Label( f"Resetting in {losttimer/10} seconds",
            font_name='Times New Roman',
            font_size=36,
            x=window.width//2, y=window.height//2 - 50,
            anchor_x='center', anchor_y='center')
        resetBox.draw()
    fps_display.draw()

pyglet.app.run()

window.set_visible()