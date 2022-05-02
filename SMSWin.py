import serial as io
import time
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
gsm = io.Serial("COM6",9600, timeout=0.5)           # to be changed accordingly to the serial port you wish to use
gsm.flush()

def SendSms1(msg,):
    print("Sending SMS\n")
    gsm.flush()
    gsm.write(b'\r\n')
    gsm.write(b'AT+CMGF=1\r\n')
    time.sleep(0.5)
    gsm.write(b'AT+CMGS=\"{insert phone number without prefixes}" \r\n')
    #serialcmd = args["{insert phone number without prefixes}"]
    #gsm.write(serialcmd.encode())
    #gsm.write(b'\"\r\n')
    time.sleep(0.5)
    data = msg
    gsm.write(data.encode())
    gsm.write(b'\x1A')
    time.sleep(3)



if __name__ == "__main__":
    SendSms1("Emergency detected, please make sure everything is alright " + current_time)



def SendSms2(msg,):
    print("Sending SMS\n")
    gsm.flush()
    gsm.write(b'\r\n')
    gsm.write(b'AT+CMGF=1\r\n')
    time.sleep(0.5)
    gsm.write(b'AT+CMGS=\"{insert phone number without prefixes}" \r\n')
    #serialcmd = args["{insert phone number without prefixes}"]
    #gsm.write(serialcmd.encode())
    #gsm.write(b'\"\r\n')
    time.sleep(0.5)
    data = msg
    gsm.write(data.encode())
    gsm.write(b'\x1A')
    time.sleep(3)
