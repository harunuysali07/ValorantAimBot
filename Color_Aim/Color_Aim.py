import keyboard
import time
import ctypes
import PIL.ImageGrab
import winsound 
import serial
import datetime

serialPort = serial.Serial(port = "COM9", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

S_HEIGHT, S_WIDTH = (PIL.ImageGrab.grab().size)
PURPLE_R, PURPLE_G, PURPLE_B = (250, 120, 250)
TOLERANCE = 50
TRIGGER_KEY = "alt"
class triggerBot():
    last_shoot_time = time.time()
    recoil_y = 0;
 
    def __init__(self):
        self.toggled = False
 
    def toggle(self):
        self.toggled = not self.toggled
 
    def click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up
 
    def validate(self, r_list, g_list, b_list):
        values = len(r_list)
        found = False
        for pixel in  range(0, values):
            if self.approx(r_list[pixel], g_list[pixel], b_list[pixel]):
                found = True
        return found
    def approx(self, r, g ,b):
        valid = 0
        if PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE:
            valid += 1
            if PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE:
                valid += 1
                if PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE:
                    valid += 1
        return valid == 3

    
    def scan(self):
        r_list = []
        g_list = []
        b_list = []
        grabzone = 80
        pmap = PIL.ImageGrab.grab(bbox=(S_HEIGHT/2-grabzone, S_WIDTH/2-grabzone - self.recoil_y, S_HEIGHT/2+grabzone, S_WIDTH/2+grabzone - self.recoil_y)).load()
        for y in range(0, grabzone):
            y = y*2
            for x in range(0, grabzone):
                x = x*2
                r, g, b = pmap[x,y]
                if self.approx(r,g,b):
                    write_this = str(x - grabzone) + "X" + str(y - grabzone + self.recoil_y) + "Y"
                    serialPort.write(str.encode(write_this))    
                    print(x , y , write_this, self.recoil_y);
                    if (time.time() - self.last_shoot_time) < 0.3:
                        if self.recoil_y < 21:
                            self.recoil_y += 2 
                    else:
                        self.recoil_y = 0
                    self.last_shoot_time = time.time()
                    time.sleep(0.01)
                    self.click()
                    return

    def recoil(self):
        if (time.time() - self.last_shoot_time) < 0.5:
            if self.recoil_y < 15:
                self.recoil_y += 2 
        else:
            self.recoil_y = 3
        write_this = str(self.recoil_y) + "Y"
        #write_this = str(150) + "X" + str(-150) + "Y" +"\r\n"
        serialPort.write(str.encode(write_this))
        print(write_this, self.recoil_y);
        self.last_shoot_time = time.time()
        time.sleep(0.05)
 
if __name__ == "__main__":
    print("FVAAC alpha Build v0.4")
    print("Features :\n -- SHIFT : Activate Aim Bot")
 
    bot = triggerBot()

    while keyboard.is_pressed("F8") != True:
        while keyboard.is_pressed("SHIFT"):
            bot.scan()

    # while True:
    #     if keyboard.is_pressed(TRIGGER_KEY):
    #         bot.toggle()
    #         if bot.toggled:
    #             print("Activated")
    #             winsound.Beep(440, 75)
    #             winsound.Beep(700, 100)
    #         else:
    #             print("Deactivated")
    #             winsound.Beep(440, 75)
    #             winsound.Beep(200, 100)
    #         while keyboard.is_pressed(TRIGGER_KEY):
    #             pass
    #     if bot.toggled:
    #         bot.scan()
