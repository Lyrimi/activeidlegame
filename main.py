import keyboard
import time

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
    
while True:
    time.sleep(0.1)
    if (getkeynum() != None):
        print(getkeynum())