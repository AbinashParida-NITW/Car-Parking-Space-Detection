import cv2
import pickle


width,height=107,48
try:
    with open('CarParkPos','rb') as f:
        posList=pickle.load(f)
except:
    posList=[]

def mouseClick(events,x,y,flags,parms):
    if events==cv2.EVENT_LBUTTONDOWN:#when click left button of mouse
        posList.append((x,y))# x and y are the position or the left corner point
    if events==cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)

    with open('CarParkPos','wb') as f: # open('CarParkPos', 'wb'): This line opens a file named CarParkPos in write-binary mode (wb). If the file doesn't exist, it will create one
        pickle.dump(posList,f)



while True:
    img = cv2.imread('carParkImg.png')
    #cv2.rectangle(img,(50,192),(159,240),(0,0,255),2) # create a rectangle box. then calculate manually the values of the points
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+width,pos[1]+height), (255, 0, 255), 2)


    cv2.imshow('Image',img)
    cv2.setMouseCallback('Image',mouseClick)
    if cv2.waitKey(1)  & 0xFF==ord('a'):
        break
