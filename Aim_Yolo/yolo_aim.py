import cv2

import numpy as np
import time
import mss
import ctypes
import pynput
import win32api, win32con
import serial

from grab import grab_screen

cv2.dnn.DNN_TARGET_CUDA
cv2.dnn.DNN_BACKEND_CUDA
#Load YOLO
net = cv2.dnn.readNet("yolov3_custom.weights","yolov3_custom.cfg") # Original yolov3
#net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg") #Tiny Yolo
classes = []
with open("obj.names","r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

SendInput = ctypes.windll.user32.SendInput
colors= np.random.uniform(0,255,size=(len(classes),3))

sct = mss.mss()
Wd, Hd = sct.monitors[1]["width"], sct.monitors[1]["height"]

## serialPort = serial.Serial(port = "COM9", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

ENABLE_AIMBOT = True
ACTIVATION_RANGE = 400
W, H = None, None
origbox = (int(Wd/2 - ACTIVATION_RANGE/2),  int(Hd/2 - ACTIVATION_RANGE/2), int(Wd/2 + ACTIVATION_RANGE/2), int(Hd/2 + ACTIVATION_RANGE/2))
#origbox = (0,  0, 1920, 1080)

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def set_pos(x, y):
    x = 1 + int(x * 65536./Wd)
    y = 1 + int(y * 65536./Hd)
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.mi = pynput._util.win32.MOUSEINPUT(x, y, 0, (0x0001 | 0x8000), 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    command=pynput._util.win32.INPUT(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

                
# Test for GPU support
build_info = str("".join(cv2.getBuildInformation().split()))
if cv2.ocl.haveOpenCL():
    cv2.ocl.setUseOpenCL(True)
    cv2.ocl.useOpenCL()
    print("[OKAY] OpenCL is working!")
else:
    print("[WARNING] OpenCL acceleration is disabled!")
if "CUDA:YES" in build_info:
    print("[OKAY] CUDA is working!")
else:
    print("[WARNING] CUDA acceleration is disabled!")

#loading image
cap=cv2.VideoCapture("B.mp4") #0 for 1st webcam
font = cv2.FONT_HERSHEY_PLAIN
starting_time= time.time()
frame_id = 0

while True:
    key = cv2.waitKey(1) #wait 1ms the loop will start again and we will process the next frame

    if key == 27: #esc key stops the process
        break;

    frame = np.array(grab_screen(region=origbox))
    #_,frame= cap.read() # 
    # if the frame dimensions are empty, grab them
    if W is None or H is None:
        (H, W) = frame.shape[: 2]

    frame_id+=1

    #detecting objects
    blob = cv2.dnn.blobFromImage(frame,0.00392,(160,160),(0,0,0),True,crop=False) #reduce 416 to 320  

        
    net.setInput(blob)
    outs = net.forward(outputlayers)
    #print(outs[1])

    #Showing info on screen/ get confidence score of algorithm in detecting an object in blob
    class_ids=[]
    confidences=[]
    boxes=[]
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                #onject detected
                center_x= int(detection[0]*W)
                center_y= int(detection[1]*H)
                w = int(detection[2]*W)
                h = int(detection[3]*H)

                #cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                #rectangle co-ordinaters
                x=int(center_x - w/2)
                y=int(center_y - h/2)
                #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

                boxes.append([x,y,w,h]) #put all rectangle areas
                confidences.append(float(confidence)) #how confidence was that object detected and show that percentage
                class_ids.append(class_id) #name of the object tha was detected

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

    if len(boxes) > 0:
        bestMatch = confidences[np.argmax(confidences)]

        for i in range(len(boxes)):
            if i in indexes:
                x,y,w,h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence= confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(255,255,255),2)

                
                if ENABLE_AIMBOT and bestMatch == confidences[i]:
                    mouseX = origbox[0] + (x + w/1.5)
                    mouseY = origbox[1] + (y + h/5)
                    #click(int(mouseX), int(mouseY))
                    write_this = str(int(mouseX)) + "X" + str(int(mouseY)) + "Y" +"\r\n"
                    #serialPort.write(str.encode(write_this))
                    #click(0,0);

    elapsed_time = time.time() - starting_time
    fps=frame_id/elapsed_time
    cv2.putText(frame,"FPS:"+str(round(fps,2)),(10,50),font,2,(0,0,0),1)
    
    cv2.imshow("Image",frame)
    
cap.release()    
cv2.destroyAllWindows()