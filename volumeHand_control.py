import cv2 as cv
import mediapipe as mp
import numpy as np 
import time
import hand_module as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv.VideoCapture(0)
detector = htm.HandDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
pTime = 0
while True:
    success , img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img , draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        
        x1 , y1 = lmList[4][1] , lmList[4][2]
        x2 , y2 = lmList[8][1] , lmList[8][2]
        cx , cy = (x1+x2)//2 , (y1+y2)//2
    
        cv.circle(img , (x1,y1), 15, (255,0,0) , cv.FILLED)
        cv.circle(img , (x2,y2), 15, (255,0,0) , cv.FILLED)
        cv.line(img, (x1,y1),(x2,y2), (255,0,0),2)
        cv.circle(img , (cx,cy), 8, (255,0,0) , cv.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)
        
        vol = np.interp(length,[50,300],[minVol,maxVol])
        volBar = np.interp(length,[50,300],[400,150])
        volPer = np.interp(length,[50,300],[0,100])

        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        if length<50:
            cv.circle(img , (cx,cy), 8, (0,255,0) , cv.FILLED)
            
        
    cv.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv.FILLED)
    cv.putText(img , f'{int(volPer)}%', (40,450),cv.FONT_HERSHEY_SIMPLEX, 1 , (0,255,0),3)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv.putText(img , str(int(fps)), (40,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv.imshow("Img",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()   
    