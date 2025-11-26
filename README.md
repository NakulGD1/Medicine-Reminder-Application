## 💊 MedRem V2 — Smart Medication Reminder App

A simple yet powerful Streamlit-based medication tracking system with real-time desktop notifications, automatic refresh, and an easy database-backed UI for daily medication management.

## 🚀 Features
- 🔔 Smart Notifications

Sends real-time browser notifications when medication time matches the current time.

Works even when the app is in the background (as long as browser permissions are enabled).

- 📅 Daily Tracking

Tracks medication status:

⏰ Upcoming

🔴 Missed

✅ Taken

Auto-updates every 60 seconds using streamlit_autorefresh.

- 🧠 SQLite Database

Stores all medication details in medication.db

Saves:

Name

Dosage

Time

Meal timing

Last taken date

- 🛠 CRUD Operations

➕ Add medication

✏️ Modify medication

❌ Remove medication

👀 View all medication schedules with status indicators

- 🖥 Streamlit UI

Clean and interactive interface

Forms for adding or editing entries

Gradient-colored status boxes

- 📂 Project Structure
```bash
MedRemV2/
│── MedRemV2.py          # Main Streamlit App
│── medication.db        # SQLite Database
│── Notify.mp3           # (Optional) Notification sound, if you want to integrate
│── README.md            # Project Documentation
```
🛠 How It Works
1️⃣ Start the App

Run:
```bash
streamlit run MedRemV2.py
```
2️⃣ Allow Browser Notifications

On first load, your browser will ask permission → click Allow.

3️⃣ Add Your Medicines

Use the sidebar menus to Add, Modify, Remove, or View All.

4️⃣ Automatic Reminder

Every minute, the system checks:

If medicine.time == current_time AND last_taken != today
      Trigger notification

🗄 Database Schema
```bash
Column	Type	Description
id	INTEGER	Primary key
name	TEXT	Medication name
dosage	TEXT	e.g., “2 tablets”
time	TEXT	“HH:MM” format
meal_time	TEXT	Before or After meal
last_taken	TEXT	ISO date (YYYY-MM-DD)
```

📸 UI Snapshots


🧩 Future Enhancements

Mobile-friendly PWA version

Sound-based notifications

Weekly schedule export

Email/SMS reminders

Multi-user support

🤝 Contributing

Open to pull requests. Feel free to improve UI, logic, or notification handling.

📜 License

MIT License. Free to use and modify.
