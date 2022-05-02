#Import all important functionalities
import time
import cv2
import mediapipe as mp
from Alarm import Alarm
import numpy as np

''' 
    #from SMSPi import SendSms1
    #from SMSPi import SendSms2
    from SMSWin import SendSms1
    from SMSWin import SendSms2
    from datetime import datetime
    import serial as io
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    gsm = io.Serial('/dev/ttyUSB0',9600, timeout=0.5)
    gsm.flush()

''' 
cap=cv2.VideoCapture(0)             # choose the argument of VideoCapture accordingly to which is the number of your camera. If you are using the embedded one it will most probably be 0
#Initialise Media Pipe Pose features
mp_pose=mp.solutions.pose
mpDraw=mp.solutions.drawing_utils
pose=mp_pose.Pose(model_complexity
= 1, min_detection_confidence=0.9,
    min_tracking_confidence=0.9)





#Start endless loop to create video frame by frame Add details about video size and image post-processing to better identify bodies
def FallDetection():
    # starting of the fall detection function
    # Start endless loop to create video frame by frame Add details about video size and image post-processing to better identify bodies
    ret,frame=cap.read()
    flipped=cv2.flip(frame,flipCode= 1)   # change flipCode accordingly to your needs
    frame1 = cv2.resize(flipped,(640,480))
    rgb_img=cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB) # Mediapipe works in RGB while Opencv in BGR so this conversion is needed
    result=pose.process(rgb_img)
    mpDraw.draw_landmarks(rgb_img,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
    #cv2.imshow('frame',rgb_img)
    key = cv2.waitKey(1) & 0xFF
    CoGArchive = [0,0] # initialization of CoG archive to keep track of the changes
    dv = 0             # initialization of instant velocity
    while True:                
        try:
            start = time.time()
            LeftHipHeight = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * 480
            RightHipHeight = result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * 480
            NoseHeight = result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * 480
            ret,frame=cap.read()
            flipped=cv2.flip(frame,flipCode= 1)    # change flipCode accordingly to your needs
            frame1 = cv2.resize(flipped,(640,480))  
            rgb_img=cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)   # Mediapipe works in RGB while Opencv in BGR so this conversion is needed
            result=pose.process(rgb_img)
            mpDraw.draw_landmarks(rgb_img,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
            cv2.imshow('Frame: ',rgb_img)
            key = cv2.waitKey(1) & 0xFF
            if(((result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].visibility) > 0.9)
            and ((result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].visibility) > 0.9)
            and ((result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].visibility) > 0.9)):
                #print('Detection mode!')
                CoGHeight = (LeftHipHeight + RightHipHeight + NoseHeight)/3
                CoGArchive.append(CoGHeight)
                #print(CoGArchive)
                #print('Center of gravity height values are: ', CoGArchive)
                dv = (CoGArchive[-2] - CoGArchive[-1])
                
                print('Center of gravity height is: ' , CoGHeight)
                print('Instant velocity is: ', dv)
                
                #print('mean of latter 100 CoG values is: ', np.mean(CoGArchive[-100:-1]))                
                if dv < -10 and len(CoGArchive) > 60:  
                    return Alarm()
                
                elif len(CoGArchive) > 150 and np.mean(CoGArchive[-150:-1]) > 300: 
                    return Alarm()
                
                elif len(CoGArchive) == 500000:
                    CoGArchive = []
                    print('RESET RESET RESET RESET RESET')          # this is made to avoid the overflow of the list 
                
                else: 
                    end = time.time()
                    totalTime = end - start
                    fps = 1 / totalTime
                    print('FPS: ', fps)
                    continue    

            else:
                print('Cannot detect enire body!')
                CoGArchive = []
        except:
            print('Insufficient visibility!')
            break

                        
    FallDetection() 
            

if __name__ == '__main__':
    FallDetection()
        
                