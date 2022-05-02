import time
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")


# to activate the emergency communication mode using SMS uncomment the import as needed

#from SMSPi import SendSms1
#from SMSPi import SendSms2
from SMSWin import SendSms1
#from SMSWin import SendSms2 


# Funzione di allarme
def Alarm():
    print('Fall detected!')
    print('Starting help request!')
    #SendSms1("Emergency detected, please make sure everything is alright " + current_time)
    #SendSms2("Emergency detected, please make sure everything is alright " + current_time)
    #time.sleep(5)     # uncomment to stop execution of detection for 5 seconds after a fall has been detected   
    