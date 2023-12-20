import cv2
import pickle 
import numpy as np
import os
vid=cv2.VideoCapture(0)
face=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

face_data=[]

i=0
name=input("Enter your Name:")
while True:
    working_or_not,frame=vid.read()
    scale=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face_fc=face.detectMultiScale(scale,1.3,3)
    for (x,y,w,h) in face_fc:
         image_cropping=frame[y:y+h,x:x+w,:]
         img_resize=cv2.resize(image_cropping,(50,50))
         if len(face_data)<=20 and i%5==0:
            face_data.append(img_resize)
         i=i+1;
         cv2.putText(frame,str(len(face_data)),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),3)
         cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),1)
    cv2.imshow("Attendance System",frame)
    wait=cv2.waitKey(1)
    if wait==ord('q') or len(face_data)==20:
          break;
vid.release()
cv2.destroyAllWindows()

face_data=np.asarray(face_data)
face_data=face_data.reshape(20,-1)

if 'name.pkl' not in os.listdir('data/'):
     names=[name]*20
     with open('data/name.pkl','wb') as f:
          pickle.dump(names,f)
else:
      with open('data/name.pkl','rb') as f:
          names=pickle.load(f)
      names=names+[name]*20
      with open('data/name.pkl','wb') as f:
          pickle.dump(names,f)


if 'face_info.pkl' not in os.listdir('data/'):
     with open('data/face_info.pkl','wb') as f:
          pickle.dump(face_data,f)
else:
      with open('data/face_info.pkl','rb') as f:
           faces=pickle.load(f)
      faces=np.append(faces,face_data,axis=0)
      with open('data/face_info.pkl','wb') as f:
          pickle.dump(names,f)