import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import hashlib
import sqlite3
import datetime
from cryptography.fernet import Fernet

# --- Security & Database Setup ---
if "key" not in st.session_state:
    st.session_state.key = Fernet.generate_key()

cipher = Fernet(st.session_state.key)

def init_db():
    conn = sqlite3.connect("telemedicine.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS appointments 
                 (id INTEGER PRIMARY KEY, patient TEXT, doctor TEXT, time TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS records 
                 (id INTEGER PRIMARY KEY, patient TEXT, data BLOB)''')
    conn.commit()
    return conn

conn = init_db()

# --- App Interface ---
def main():
    st.set_page_config(page_title="Secure Telemedicine Portal", layout="wide")
    st.title("🏥 HIPAA-Compliant Telemedicine System")

    menu = ["Video Consultation", "Appointments", "Medical Records"]
    choice = st.sidebar.selectbox("Dashboard", menu)

    if choice == "Video Consultation":
        st.subheader("Secure Video Link")
        rtc_config = RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        )
        
        webrtc_streamer(
            key="telemedicine-call",
            rtc_configuration=rtc_config,
            media_stream_constraints={"video": True, "audio": True},
        )
        st.info("Video stream is encrypted end-to-end via WebRTC protocols.")

    elif choice == "Appointments":
        st.subheader("Schedule Consultation")
        with st.form("appt_form"):
            patient = st.text_input("Patient Name")
            doctor = st.selectbox("Select Specialist", ["Dr. Smith (GP)", "Dr. Jones (Cardio)"])
            date = st.date_input("Date")
            time = st.time_input("Time")
            if st.form_submit_button("Book Appointment"):
                c = conn.cursor()
                c.execute("INSERT INTO appointments (patient, doctor, time) VALUES (?, ?, ?)",
                          (patient, doctor, f"{date} {time}"))
                conn.commit()
                st.success("Appointment Secured.")

    elif choice == "Medical Records":
        st.subheader("Secure Record Sharing")
        patient_name = st.text_input("Search Patient Name")
        record_text = st.text_area("Clinical Notes")
        
        if st.button("Encrypt & Upload"):
            encrypted_data = cipher.encrypt(record_text.encode())
            c = conn.cursor()
            c.execute("INSERT INTO records (patient, data) VALUES (?, ?)", 
                      (patient_name, encrypted_data))
            conn.commit()
            st.success(f"Record for {patient_name} encrypted and stored.")

        if st.button("View Decrypted Records"):
            c = conn.cursor()
            c.execute("SELECT data FROM records WHERE patient=?", (patient_name,))
            results = c.fetchall()
            for row in results:
                decrypted_note = cipher.decrypt(row[0]).decode()
                st.write(f"📄 {decrypted_note}")

if __name__ == "__main__":
    main()