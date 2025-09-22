import streamlit as st
from orchestrator import SessionManager

st.set_page_config(page_title="Multi-Agent AI", page_icon="🤖", layout="centered")
st.title("🤖 Multi-Agent AI Assistant")

# Initialize session state
if "manager" not in st.session_state:
    st.session_state.manager = SessionManager()
if "history" not in st.session_state:
    st.session_state.history = []

# Optional Job Description for Interview Agent
st.sidebar.header("Interview Settings")
jd = st.sidebar.text_area("Optional: Paste Job Description here")

# Input box at bottom
user_input = st.chat_input("Type your message...")

if user_input:
    agent, reply = st.session_state.manager.route(user_input, jd=jd if jd.strip() else None)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append((f"{agent.capitalize()} Agent", reply))

# Display conversation
for speaker, text in st.session_state.history:
    with st.chat_message("user" if speaker == "You" else "assistant"):
        st.markdown(f"**{speaker}:** {text}")
