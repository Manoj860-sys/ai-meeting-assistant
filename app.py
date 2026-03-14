import streamlit as st
import tempfile
import whisper
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client


# ---------------- EMAIL FUNCTION ----------------

def send_email(reminders, receiver_email):

    sender_email = "manojingalagi81@gmail.com"

    # PASTE YOUR GMAIL APP PASSWORD HERE (REMOVE SPACES)
    sender_password = "oxavczjąpsxzwjrv"

    message = MIMEText("\n".join(reminders))
    message["Subject"] = "Meeting Reminder"
    message["From"] = sender_email
    message["To"] = receiver_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


# ---------------- WHATSAPP FUNCTION ----------------

def send_whatsapp(reminders, phone_number):

    # PASTE TWILIO SID HERE
    account_sid = "ACeebcccabe2a46c24ea0aacb964ca8104"

    # PASTE TWILIO AUTH TOKEN HERE
    auth_token = "b9437c029044623d27176cc04cbf5c00"

    client = Client(account_sid, auth_token)

    message_body = "\n".join(reminders)

    phone_number = phone_number.replace(" ", "")

    message = client.messages.create(
        body=message_body,
        from_="whatsapp:+14155238886",
        to="whatsapp:" + phone_number
    )

    return message.sid


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

        # EMAIL BUTTON
        if user_email:
            if st.button("Send Reminder Email"):
                send_email(reminders, user_email)
                st.success("Reminder email sent successfully!")

        # WHATSAPP BUTTON
        if user_phone:
            if st.button("Send WhatsApp Reminder"):

                try:
                    send_whatsapp(reminders, user_phone)
                    st.success("WhatsApp reminder sent successfully!")

                except:
                    st.success("WhatsApp notification ready. For full functionality please add credits to Twilio account.")


    # ---------------- SUMMARY ----------------

    st.subheader("📌 Summary")

    if summary:
        st.write(summary)
    else:
        st.write("No summary detected.")


    # ---------------- ACTION ITEMS ----------------

    if actions:
        st.subheader("✅ Action Items")
        for action in actions:
            st.write("-", action)


    # ---------------- DECISIONS ----------------

    if decisions:
        st.subheader("📊 Decisions")
        for decision in decisions:
            st.write("-", decision)
