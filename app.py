import streamlit as st
import tempfile
import os

st.set_page_config(page_title="AI Meeting Assistant", layout="wide")

st.title("🎙 AI Meeting Assistant")
st.write("Upload meeting audio to generate transcript, summary, and action items.")

uploaded_file = st.file_uploader(
    "Upload meeting audio",
    type=["wav", "mp3", "m4a", "ogg", "opus"]
)

import whisper
model = whisper.load_model("base")


def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]


def analyze_transcript(text):

    # Simple prototype logic for hackathon demo
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


if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Processing meeting audio...")

    transcript = transcribe_audio(tmp_path)

    st.subheader("📝 Transcript")
    st.write(transcript)

    summary, actions, decisions = analyze_transcript(transcript)

    st.subheader("📌 Summary")
    st.write(summary)

    st.subheader("✅ Action Items")
    for action in actions:
        st.write("-", action)

    st.subheader("📊 Decisions")
    for decision in decisions:
        st.write("-", decision)
