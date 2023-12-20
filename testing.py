from sklearn.neighbors import KNeighborsClassifier
import pyttsx3
import cv2
import speech_recognition as sp
import pickle 
import numpy as np
import os
import csv
import time
import datetime
from win32com.client import Dispatch
from datetime import datetime

vid=cv2.VideoCapture(0)
face=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')

def speak(str1):
      speak=Dispatch("SAPI.SpVoice")
      speak.Speak(str1)

with open('data/name.pkl','rb') as f:
        Labels=pickle.load(f)
with open('data/face_info.pkl','rb') as f:
        Labels1=pickle.load(f)

knn=KNeighborsClassifier(n_neighbors=10)
knn.fit(Labels1,Labels)

column_info=['Name','Time','Date']


def takeCommand():
    r=sp.Recognizer()
    with sp.Microphone() as source:
        print("Listening....")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        print("Recognizing....")
        query=r.recognize_google(audio,language='en-in')
        print(f"User said:{query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

while True:
    working_or_not,frame=vid.read()
    scale=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face_fc=face.detectMultiScale(scale,1.3,3)
         
    for (x,y,w,h) in face_fc:
         image_cropping=frame[y:y+h,x:x+w,:]
         img_resize=cv2.resize(image_cropping,(50,50)).flatten().reshape(1,-1)
         output_obt=knn.predict(img_resize)
         time_info=time.time()
         date=datetime.fromtimestamp(time_info).strftime("%d-%m-%Y")
         found=os.path.isfile("Attendance_details/Attendance_info"+date+".csv")
         time_stamp=datetime.fromtimestamp(time_info).strftime("%H:%M:%S")
         cv2.putText(frame,str(output_obt[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
         cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),3)
         attendance=[str(output_obt[0]),str(time_stamp),str(date)]
    cv2.imshow("Attendance System",frame)
    wait=cv2.waitKey(1)
    if takeCommand().__eq__("mark the attendance"):
          speak("Attendance is Marked")
          if found:
                with open("Attendance_details/Attendance_info"+date+".csv","+a") as csvfile:
                      write=csv.writer(csvfile)
                      write.writerow(attendance)
                csvfile.close()
                break;
          else:
                with open("Attendance_details/Attendance_info"+date+".csv","+a") as csvfile:
                      write=csv.writer(csvfile)
                      write.writerow(column_info)
                      write.writerow(attendance)
                csvfile.close()
                break;
    else:
          speak("Speak valid statement and mark your attendance again..")
          break;
vid.release()
cv2.destroyAllWindows()