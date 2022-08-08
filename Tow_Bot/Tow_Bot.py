import pygetwindow as gw
import time

import cv2
import mss
import numpy
import pytesseract

from io import StringIO

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

GameWindow = gw.getWindowsWithTitle('Gameroom')[0]

if not GameWindow:
    print("Gameroom Not Found")
    exit()

GameWindow.resizeTo(1150,850)
GameWindow.moveTo(0,0)
GameWindow.restore()
#GameWindow.focus()
print(GameWindow.size)

mon = {'top': 0, 'left': 0, 'width': 1150, 'height': 850}

with mss.mss() as sct:
    while True:
        im = numpy.asarray(sct.grab(mon))
        # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        text_data = pytesseract.image_to_data(im)
        # for yazi in text_data:
        #     print()
        #     if yazi[10] < 70:
        #          text_data.remove(yazi)
        #          print(yazi)
        #     if yazi == "Merhaba":
        #         print("Merhaba !")
        #         pass
        
        print(text_data)

        # One screenshot per second
        time.sleep(1)