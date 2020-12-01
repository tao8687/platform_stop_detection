# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care

import sys, os
import cv2
sys.path.append('/home/zhangende/projects/darknet/python/')

sys.path.append(os.path.join(os.getcwd(),'python/'))
import darknet as dn

net = dn.load_net("stop/stop.cfg", "weights/stop_final.weights", 0)
meta = dn.load_meta("stop/stop.data")
out = cv2.VideoWriter('stop.MOV',fourcc, 25.0, (1920,1080))

cap = cv2.VideoCapture("/repository/darknet/2.MOV")
if cap.isOpened():
	success = True
else:
	success = False
	print('读取失败！')
while success:
    print(1)
    success,img = cap.read()
    img_resized = cv2.resize(img,(640,320),interpolation=cv2.INTER_AREA)
    result = dn.detect(net, meta,img_resized)
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
        print left,right,top,bottom
        cv2.rectangle(img_resized,(left,top),(right,bottom),(255,0,0),10)
        cv2.putText(img_resized,str(x),(10,10),cv2.FONT_HERSHEY_SIMPLEX,4,(255,0,0),2)

    img = cv2.resize(img_resized, (1920,1080), interpolation=cv2.INTER_AREA)
    out.write(img)

cap.release()
out.release()
cv2.destoryAllWindows()
