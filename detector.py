# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care

import cv2
import numpy as np

#sys.path.append('/home/zhangende/projects/darknet/python/')

import darknet as dn

'''
dn.set_gpu(0)
net = dn.load_net("cfg/yolo-thor.cfg", "/home/pjreddie/backup/yolo-thor_final.weights", 0)
meta = dn.load_meta("cfg/thor.data")
r = dn.detect(net, meta, "data/bedroom.jpg")
print r

# And then down here you could detect a lot more images like:
r = dn.detect(net, meta, "data/eagle.jpg")
print r
r = dn.detect(net, meta, "data/giraffe.jpg")
print r
r = dn.detect(net, meta, "data/horses.jpg")
print r
r = dn.detect(net, meta, "data/person.jpg")
print r
'''
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
net = dn.load_net('stop/stop.cfg'.encode("utf-8"),'backup/stop_final.weights'.encode("utf-8"), 0)
meta = dn.load_meta("stop/stop.data".encode("utf-8"))
out = cv2.VideoWriter('stop.MOV',fourcc, 25.0, (320,640))
pre_dis =10000

cap = cv2.VideoCapture("4.mp4")
if cap.isOpened():
    success, img = cap.read()
while success:
    img_resized = cv2.resize(img,(640,320),interpolation=cv2.INTER_AREA)
    cv2.imwrite("img_resized.jpg", img_resized)
    result = dn.detect(net, meta, "./img_resized.jpg".encode("utf-8"))
    if len(result)==1:
        name = result[0][0]
        confidence = result[0][1]
        x = result[0][2][0]
        y = result[0][2][1]
        width = result[0][2][2]
        height = result[0][2][3]
        left = int(x - width / 2)
        right = int(x + width / 2)
        top = int(y - height / 2)
        bottom = int(y + height / 2)
        #print left,right,top,bottom
        cv2.rectangle(img_resized,(left,top),(right,bottom),(255,0,0),2)
        img_resized = np.rot90(img_resized,-1).copy()

        distance = round(20*7.85/(height/320*1080),1)
        if distance >=pre_dis:
            distance = pre_dis
        else:
            pre_dis = distance
        font=cv2.FONT_HERSHEY_SIMPLEX
        #img_resized = img_resized.astype(np.uint8)
        img_resized = cv2.putText(img_resized,str(distance)+"m",(0,60),font,1.5,(255,0,0),2)
        print(distance)
    else :
        img_resized = np.rot90(img_resized,-1)

    #img = cv2.resize(img_resized, (1920,1080), interpolation=cv2.INTER_AREA)
    cv2.imshow("frame",img_resized)
    out.write(img_resized)
    success, img = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()
