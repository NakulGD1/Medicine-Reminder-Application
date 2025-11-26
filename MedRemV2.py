import sqlite3
import datetime
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# --------- Database setup ---------
def init_db():
    update_db_schema()
    conn = sqlite3.connect("medication.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            time TEXT NOT NULL,
            meal_time TEXT NOT NULL,
            last_taken TEXT
        )
    """)
    conn.commit()
    conn.close()
def update_db_schema():
    conn = sqlite3.connect("medication.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=off;")
    try:
        c.execute("ALTER TABLE medications ADD COLUMN meal_time TEXT;")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE medications ADD COLUMN last_taken TEXT;")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def mark_as_taken(med_id):
    today = datetime.date.today().isoformat()
    conn = sqlite3.connect("medication.db")
    c = conn.cursor()
    c.execute("UPDATE medications SET last_taken = ? WHERE id = ?", (today, med_id))
    conn.commit()
    conn.close()
    
def undo_taken(med_id):
    conn = sqlite3.connect("medication.db")
    c = conn.cursor()
    c.execute("UPDATE medications SET last_taken = NULL WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()

# --------- Database functions ---------
def add_medication(name, dosage, time_str, meal_time):
    conn = sqlite3.connect("medication.db")
    c = conn.cursor()
    c.execute("INSERT INTO medications (name, dosage, time, meal_time) VALUES (?, ?, ?, ?)", 
              (name, dosage, time_str, meal_time))
    conn.commit()
    conn.close()

def modify_medication(med_id, name, dosage, time_str, meal_time):
    conn = sqlite3.connect("medication.db")
    c = conn.cursor()
    c.execute("UPDATE medications SET name = ?, dosage = ?, time = ?, meal_time = ? WHERE id = ?", 
              (name, dosage, time_str, meal_time, med_id))
    conn.commit()
    conn.close()

def remove_medication(med_id):
    conn = sqlite3.connect("medication.db")
    c = conn.cursor()
    c.execute("DELETE FROM medications WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()

def get_medications():
    conn = sqlite3.connect("medication.db")
    c = conn.cursor()
    c.execute("SELECT * FROM medications")
    meds = c.fetchall()
    conn.close()
    return meds

# --------- UI Reminder ---------
def check_for_reminders():
    current_time = datetime.datetime.now().strftime("%H:%M")
    today = datetime.date.today().isoformat()
    meds = get_medications()
    for med in meds:
        if med[3] == current_time and med[5] != today:
            push_notification(f"Time to take {med[1]} ({med[2]}) - {med[4]}")


def push_notification(message):
    js = f"""
    <script>
    if (Notification.permission === "granted") {{
        var notification = new Notification("💊 Medication Reminder", {{
            body: "{message}",
        }});
    }} else {{
        Notification.requestPermission().then(function(permission) {{
            if (permission === "granted") {{
                var notification = new Notification("💊 Medication Reminder", {{
                    body: "{message}",
                }});
            }}
        }});
    }}
    </script>
    """
    components.html(js)


# --------- Streamlit App ---------
def app():
    st.set_page_config(page_title="Medication Reminder", page_icon="💊")
    st.title("💊 Medication Reminder")

    st_autorefresh(interval=60000, key="refresh")  # Refresh every 60 seconds
 
    init_db()
    
    check_for_reminders()
    
    #Debug Notification
    if st.button("🔔 Check Reminder"):
        meds = get_medications()
        for med in meds:
            push_notification(f"Time to take {med[1]} ({med[2]}) - {med[4]}")    
    
    st.subheader("Manage Medications")
    menu = st.selectbox("Choose Action", ["Add", "Modify", "Remove", "View All"])
        
    if menu == "Add":
        with st.form("add_form"):
            name = st.text_input("Medication Name")
            dosage = st.text_input("Dosage (e.g., 2 tablets)")
            med_time = st.time_input("Time (24H format)")
            meal_time = st.radio("Meal Timing", ["Before Meal", "After Meal"])
            submitted = st.form_submit_button("Add")
            if submitted:
                if name and dosage:
                    add_medication(name, dosage, med_time.strftime("%H:%M"), meal_time)
                    st.success(f"{name} added successfully!")

    elif menu == "Modify":
        meds = get_medications()
        if meds:
            med_display = [f"{m[1]} - {m[2]} at {m[3]} ({m[4]})" for m in meds]
            selected = st.selectbox("Select to Modify", med_display)
            med_id = meds[med_display.index(selected)][0]

            with st.form("modify_form"):
                med_data = meds[med_display.index(selected)]
                new_name = st.text_input("New Name", value=med_data[1])
                new_dosage = st.text_input("New Dosage", value=med_data[2])
                new_time = st.time_input("New Time", value=datetime.datetime.strptime(med_data[3], "%H:%M").time())
                new_meal_time = st.radio("Meal Timing", ["Before Meal", "After Meal"], index=0 if med_data[4] == "Before Meal" else 1)
                submit_edit = st.form_submit_button("Update")
                if submit_edit:
                    modify_medication(med_id, new_name, new_dosage, new_time.strftime("%H:%M"), new_meal_time)
                    st.success("Updated successfully!")

    elif menu == "Remove":
        meds = get_medications()
        if meds:
            med_display = [f"{m[1]} - {m[2]} at {m[3]} ({m[4]})" for m in meds]
            selected = st.selectbox("Select to Remove", med_display)
            med_id = meds[med_display.index(selected)][0]
            if st.button("Delete"):
                remove_medication(med_id)
                st.success("Medication removed.")

    elif menu == "View All":
        meds = get_medications()
        if meds:
            st.subheader("📝 Scheduled Medications")
            now = datetime.datetime.now()
            for med in meds:
                med_id, name, dosage, time_str, meal_time, last_taken = med
                med_time = datetime.datetime.strptime(time_str, "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day
                )
                taken_today = last_taken == datetime.date.today().isoformat()

                if taken_today:
                    status = "✅ Taken"
                    color = "green"
                elif now > med_time:
                    status = "🔴 Missed"
                    color = "red"
                else:
                    status = "⏰ Upcoming"
                    color = "orange"

                st.markdown(f"""
                <div style='border:1px solid #{color};padding:10px;border-radius:8px;margin-bottom:10px'>
                <b>Name:</b> {name} <br>
                <b>Dosage:</b> {dosage} <br>
                <b>Time:</b> {time_str} <br>
                <b>Meal Time:</b> {meal_time} <br>
                <b>Status:</b> <span style='color:{color};font-weight:bold'>{status}</span><br>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns([1, 1])
                with col1:
                    if not taken_today:
                        if st.button(f"✅ Mark as Taken: {name} ({time_str})", key=f"take_{med_id}"):
                            mark_as_taken(med_id)
                            st.success(f"{name} marked as taken!")
                            st.experimental_rerun()
                with col2:
                    if taken_today:
                        if st.button(f"↩️ Undo Taken: {name} ({time_str})", key=f"undo_{med_id}"):
                            undo_taken(med_id)
                            st.warning(f"{name} marked as not taken.")
                            st.experimental_rerun()
    else:
        st.info("No medications scheduled yet.")

# Run app
if __name__ == "__main__":
    app()
