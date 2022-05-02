#Import all important functionality
import time
import cv2
import mediapipe as mp
from Alarm import Alarm
import numpy as np 

#Start cv2 video capturing through CSI port

for i in range(1,31,1): # choose range accordingly to your subset
    cap=cv2.VideoCapture('{pathofvideosdataset} (%d).avi'%i) # insert path of the videos indexed by i
    
    #Initialise Media Pipe Pose features
    
    mp_pose=mp.solutions.pose
    mpDraw=mp.solutions.drawing_utils
    pose=mp_pose.Pose(model_complexity
    = 1, min_detection_confidence=0.9,
        min_tracking_confidence=0.9)

    # Communication initialization
    
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



    # Start endless loop to create video frame by frame Add details about video size and image post-processing to better identify bodies
    
    def FallDetection():
        # starting of the fall detection function
        try:
            ret,frame=cap.read()
            flipped=cv2.flip(frame,flipCode= 1)     # change flipCode accordingly to your needs
            frame1 = cv2.resize(flipped,(640,480))
            rgb_img=cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB) # Mediapipe works in RGB while Opencv in BGR so this conversion is needed
            result=pose.process(rgb_img)
            mpDraw.draw_landmarks(rgb_img,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
            cv2.imshow('frame',rgb_img)
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
                    flipped=cv2.flip(frame,flipCode= 1)
                    frame1 = cv2.resize(flipped,(640,480))
                    rgb_img=cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)          # Mediapipe works in RGB while Opencv in BGR so this conversion is needed
                    result=pose.process(rgb_img)
                    mpDraw.draw_landmarks(rgb_img,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
                    cv2.imshow('frame',rgb_img)
                    key = cv2.waitKey(1) & 0xFF
                    if(((result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].visibility) > 0.9)
                    and ((result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].visibility) > 0.9)
                    and ((result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].visibility) > 0.9)):
                        #print('Detection mode!')
                        CoGHeight = (LeftHipHeight+RightHipHeight+NoseHeight)/3
                        CoGArchive.append(CoGHeight)
                        #print(CoGArchive)
                        #print('Center of gravity height values are: ', CoGArchive)
                        dv = (CoGArchive[-2] - CoGArchive[-1])
                        
                        print('The center of gravity height is: ' , CoGHeight)
                        print('Instant velocity is: ', dv)
                        
                        #print('The mean of the 100 latter CoG values is: ', np.mean(CoGArchive[-100:-1]))    
                        
                        if dv < -9 and len(CoGArchive) > 60:  
                            Results= open('pathoffileyouwanttowriteon.txt', 'a')     # change path accordingly to the file you chose to write on the results 
                            Results.write('\nFall detected on video number %d'%i)
                            Results.close()
                            return Alarm()
                        elif len(CoGArchive) > 150 and np.mean(CoGArchive[-150:-1]) > 300: 
                            Results= open('pathoffileyouwanttowriteon.txt', 'a')
                            Results.write('\nFall detected on video number %d'%i)
                            Results.close()
                            return Alarm()
                        elif len(CoGArchive) == 500000:
                            CoGArchive = []                             # this is made to avoid the overflow of the list
                            print('RESET RESET RESET RESET RESET')          
                        else: 
                            end = time.time()
                            totalTime = end - start
                            fps = 1 / totalTime
                            print('FPS: ', fps)
                            continue    

                    else:
                        print('Cannot detect entire body!')
                        CoGArchive = []
                except:
                    print('Insufficient visibility!')
                    break
        except:
            Results = open('pathoffileyouwanttowriteon.txt', 'a')   # change path accordingly to the file you chose to write on the results
            Results.write('\n No fall detected on video number %d'%i)
            Results.close()
            return 1  # returns success and goes to test next video
        
                        
        FallDetection()                 
            

    
    if __name__ == "__main__":
        FallDetection()            

                
                            
