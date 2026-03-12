
import streamlit as st
import tempfile
import os

st.set_page_config(page_title="AI Meeting Assistant", layout="wide")

st.title("🤖 AI Meeting Assistant")
st.write("Upload meeting audio to generate transcript, summary, and action items.")

uploaded_file = st.file_uploader("Upload meeting audio", type=["wav","mp3","m4a","ogg","opus"])




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

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    st.info("Processing meeting...")

    transcript = transcribe_audio(temp_path)
    summary, actions, decisions = analyze_transcript(transcript)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Transcript")
        st.write(transcript)

        st.subheader("📊 Summary")
        st.write(summary)

    with col2:
        st.subheader("✅ Action Items")
        for a in actions:
            st.write("- " + a)

        st.subheader("📌 Key Decisions")
        for d in decisions:
            st.write("- " + d)

    st.success("Meeting analysis completed!")

st.markdown("---")
st.caption("Hackathon Prototype: Replace placeholder logic with Whisper + LLM for full AI capabilities.")
