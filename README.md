# Medicine Reminder Application
This is a simple Python script that helps you set up reminders to take your medicine at a specified time each day. The script uses the 'plyer' library to send desktop notifications and the datetime library to check the current time.

**Installation**

1. Install the required library using pip:
```
pip install plyer
```

2. Save an icon file for the notification (e.g., MRlogo.ico) in a known location. Update the script with the correct path to this icon.
```
app_icon = "C:/path/to/your/MRlogo.ico",
```
**Usage**
1. Run the script.

2. When prompted, enter the hour and minute for the reminder.

3. The script will continuously run and check the current time every minute. When the current time matches the specified time, a notification will be triggered, and the current day of the week will be displayed in the console.
