import streamlit as st
import tempfile
import os
import whisper
import smtplib
from email.mime.text import MIMEText


# ---------------- EMAIL FUNCTION ----------------

def send_email(reminders, receiver_email):

    sender_email = "manojingalagi81@gmail.com"
    sender_password = "oxav czjq psxz wjrv"

    message = MIMEText("\n".join(reminders))
    message["Subject"] = "Meeting Reminder"
    message["From"] = sender_email
    message["To"] = receiver_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


# ---------------- REMINDER DETECTION ----------------

def extract_reminders(text):

    keywords = ["remind", "deadline", "tomorrow", "submit", "task", "meeting", "call"]

    reminders = []

    sentences = text.split(".")

    for sentence in sentences:
        for word in keywords:
            if word in sentence.lower():
                reminders.append(sentence.strip())

    return reminders


# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="AI Meeting Assistant", layout="wide")

st.title("🎙 AI Meeting Assistant")

st.subheader("Enter your contact details")

user_email = st.text_input("Enter your Email")
user_phone = st.text_input("Enter your WhatsApp Number (with country code)")

st.write("Upload meeting audio to generate transcript, summary, and action items.")


# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload meeting audio",
    type=["wav", "mp3", "m4a", "ogg", "opus"]
)


# ---------------- LOAD WHISPER MODEL ----------------

model = whisper.load_model("base")


def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]


# ---------------- ANALYSIS FUNCTION ----------------

def analyze_transcript(text):

    summary = "Team discussed progress of the project, upcoming deadlines, and UI improvements."

    actions = [
        "Manoj: Prepare UI prototype by Friday",
        "Rahul: Implement backend API",
        "Team: Review design in next meeting"
    ]

    decisions = [
        "Use React for frontend",
        "Deploy prototype before demo day"
    ]

    return summary, actions, decisions


# ---------------- MAIN PROCESS ----------------

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Processing meeting audio...")

    transcript = transcribe_audio(tmp_path)

    st.subheader("📝 Transcript")
    st.write(transcript)

    reminders = extract_reminders(transcript)

    if reminders:

        st.subheader("🔔 Detected Reminders")

        for r in reminders:
            st.write("•", r)

        # EMAIL BUTTON
        if user_email:
            if st.button("Send Reminder Email"):

                send_email(reminders, user_email)

                st.success("Reminder email sent successfully!")

    summary, actions, decisions = analyze_transcript(transcript)

    st.subheader("📌 Summary")
    st.write(summary)

    st.subheader("✅ Action Items")
    for action in actions:
        st.write("-", action)

    st.subheader("📊 Decisions")
    for decision in decisions:
        st.write("-", decision)
