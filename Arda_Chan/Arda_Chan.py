import keyboard
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.MINIMUM_DURATION = 0.0001

w, h = pyautogui.size()
print(w, h)

while (keyboard.is_pressed("0") != True and keyboard.is_pressed("CTRL") != True):
    while keyboard.is_pressed("SHIFT"):
        print(pyautogui.position())
        
        mx, my = pyautogui.position()
        pyautogui.moveTo(w/2, h/2)
        # pyautogui.click(button='right',duration=0)    
        # pyautogui.moveTo(mx, my, duration=0)