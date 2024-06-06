from datetime import datetime
import time
from plyer import notification
sch=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

def reminder():
    notification.notify(
        title = "Reminder",
        message = "Its time to take your medicine",
        app_icon = "C:/Users/hp/Downloads/MRlogo (1).ico",
    )
  
h=int(input("Enter the hour:"))
m=int(input("Enter the minutes:"))

while True:
    dt=datetime.now()
    x=dt.weekday()
    
    time1=datetime.now().time()
    if time1.hour== h and time1.minute==m:
        print("Today is ",sch[x])
        reminder()
    time.sleep(60)