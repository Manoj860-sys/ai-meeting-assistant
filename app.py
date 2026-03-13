import streamlit as st
import tempfile
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


# ---------------- ANALYSIS FUNCTION ----------------

def analyze_transcript(text):

    sentences = text.split(".")

    actions = []
    decisions = []
    summary_sentences = []

    for s in sentences:

        s = s.strip()

        if any(word in s.lower() for word in ["will", "prepare", "submit", "complete", "implement"]):
            actions.append(s)

        elif any(word in s.lower() for word in ["decided", "decision", "agree", "approved"]):
            decisions.append(s)

        else:
            summary_sentences.append(s)

    summary = ". ".join(summary_sentences[:3])

    return summary, actions, decisions


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

    summary, actions, decisions = analyze_transcript(transcript)

    # ---------------- REMINDERS ----------------

    if reminders:

        st.subheader("🔔 Detected Reminders")

        for r in reminders:
            st.write("•", r)

        if user_email:
            if st.button("Send Reminder Email"):

                send_email(reminders, user_email)

                st.success("Reminder email sent successfully!")

    # ---------------- SUMMARY (ALWAYS SHOW) ----------------

    st.subheader("📌 Summary")

    if summary:
        st.write(summary)
    else:
        st.write("No summary detected.")


    # ---------------- ACTION ITEMS (ONLY IF EXISTS) ----------------

    if actions:
        st.subheader("✅ Action Items")

        for action in actions:
            st.write("-", action)


    # ---------------- DECISIONS (ONLY IF EXISTS) ----------------

    if decisions:
        st.subheader("📊 Decisions")

        for decision in decisions:
            st.write("-", decision)
