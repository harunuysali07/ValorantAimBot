import mss
import cv2
import numpy as np
from collections import namedtuple
from win32 import win32api
import pyautogui

#   Written by Zubair Sidhu
#   github.com/ZubairSidhu

#   Python 3.6.5
#   Plays Piano Tiles automatically
#   Game link: http://tanksw.com/piano-tiles/
#   Uses OpenCV to detect tiles and pyautogui to click tiles

#   Steps:
#   1) Run file
#   2) Click top left corner of play area
#   3) Click bottom right corner of play area
#   4) Sit back and watch

# ===High Scores Arcade Mode===
#           1) 414
#           2) 409
#           3) 408


def set_window():
    click_count = 0
    state_left = win32api.GetKeyState(0x01)  # Default mouse state
    # Checks for left click
    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left:  # Button state changed
            state_left = a

            # If left mouse is clicked
            if a < 0:
                # First click
                if click_count == 0:
                    # Stores mouse position
                    firstX, firstY = win32api.GetCursorPos()
                    print('Top Left Corner Selected: ', firstX, firstY)
                    click_count = click_count + 1

                # Second click
                elif click_count == 1:
                    secondX, secondY = win32api.GetCursorPos()
                    print('Bottom Right Corner Selected: ', secondX, secondY)
                    click_count = click_count + 1
                    break

    # Finds width and height of area clicked
    width, height = abs(firstX - secondX), abs(firstY - secondY)

    # Creates a namedtuple() to store play area dimensions
    Dimensions = namedtuple('dimensions', ['x', 'y', 'w', 'h'])
    dims = Dimensions(firstX, firstY, width, height)
    
    return dims


def screencapture(dims):
    with mss.mss() as sct:

        # The screen part to capture
        monitor = {'top': dims.y, 'left': dims.x, 'width': dims.w, 'height': dims.h}
        count = 0

        while True:

            img = sct.grab(monitor)
            output = mss.tools.to_png(img.rgb, img.size)
            img = cv2.imdecode(np.frombuffer(output, np.uint8), cv2.IMREAD_COLOR)

            # Converts image to HSV so it can be used with OpenCV
            hsv_output = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Mask black tiles
            lower_color = np.array([0, 0, 10])
            upper_color = np.array([0, 0, 20])
            tile_mask = cv2.inRange(hsv_output, lower_color, upper_color)

            # Smooths image for easier rectangle detection
            median = cv2.medianBlur(tile_mask, 151)

            # Finds contours in masked image
            ret, thresh = cv2.threshold(median, 127, 255, 0)
            _, contours, hierarchy = cv2.findContours(thresh, 1, 2)

            # Checks if any contours have been detected
            if not contours:
                continue
            else:
                cnt = contours[0]

            # Loops through detected contours (if there are any), finds rectangles, then clicks the center of each one    
            for cnt in contours:
                epsilon = 0.2*cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
        
                x, y, w, h = cv2.boundingRect(cnt)

                # Finds center of detected rectangle
                cx = int((x + (w/2)))
                cy = int((y + (h/2)))

                # Clicks center
                pyautogui.click((cx + dims.x), (cy + dims.y))
                count = count + 1
                print("Click: " + str(count) + " cx: " + str(cx))
                
                
screencapture(set_window())