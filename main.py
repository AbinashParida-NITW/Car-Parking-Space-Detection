import numpy as np
import cv2
import pickle
import cvzone
from PIL.ImageChops import offset

# Open the video file
cap = cv2.VideoCapture('carPark.mp4')
width,height=107,48

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgPro):

    spaceCounter=0

    for pos in posList:
        x,y=pos

        imgCrop=imgPro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgCrop)
        count=cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2,offset=0,colorR=(0,0,225))

        if count<850:
            color=(0,255,0)
            thickness=3
            spaceCounter+=1
        else:
            color=(0,0,255)
            thickness=2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(img, f'Free:{spaceCounter}/{len(posList)}', (100,50),
                       scale=3, thickness=5, offset=20, colorR=(0, 200, 0))
# Loop through the video frames
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    imageGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert bgr to gray
    imgBlur=cv2.GaussianBlur(imageGray,(3,3),1)
    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV,25,16)
    imgMedian=cv2.medianBlur(imgThreshold,5)
    kernel=np.ones((3,3),np.int8)
    imgDilate=cv2.dilate(imgMedian,kernel,iterations=1)

    checkParkingSpace(imgDilate)
    #for pos in posList:


    # Check if the frame was read correctly
    if not success:
        print("Error: Failed to read frame from video.")
        break

    # Display the frame
    cv2.imshow("Image", img)
    #cv2.imshow('ImageBlur',imgBlur)
    #cv2.imshow('ImageThreshold', imgThreshold)
    #cv2.imshow('ImageMedian', imgMedian)

    # Exit the loop if the 'a' key is pressed
    if cv2.waitKey(10) & 0xFF == ord('a'):
        break

# Release video capture object and close windows
cap.release()
cv2.destroyAllWindows()
