import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import streamlit.components.v1 as components

st.set_page_config(page_title="Shared Clipboard", layout="wide")

# ---------------- Firebase Setup from Secrets ----------------
firebase_secret = st.secrets["FIREBASE"]
cred = credentials.Certificate(firebase_secret)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://clip-board-10d45-default-rtdb.firebaseio.com/"
    })

ref = db.reference("sharedClipboard")

# ---------------- Load Data ----------------
data = ref.get() or {"q1": "", "q2": "", "q3": "", "q4": ""}

# ---------------- Clipboard Copy Function ----------------
def copy_clip(text):
    components.html(
        f"""
        <script>
        const temp = document.createElement('textarea');
        temp.value = `{text}`;
        document.body.appendChild(temp);
        temp.select();
        document.execCommand('copy');
        document.body.removeChild(temp);
        </script>
        """,
        height=0,
    )

st.title("📋 Shared Clipboard (4 Questions Sync)")
st.write("Paste, Save, Copy — Live shared clipboard between you and your friend.")

# ---------------- COPY ALL BUTTON ----------------
st.subheader("Copy ALL Questions")

all_codes = f"""
------ Question 1 ------
{data['q1']}

------ Question 2 ------
{data['q2']}

------ Question 3 ------
{data['q3']}

------ Question 4 ------
{data['q4']}
"""

if st.button("COPY ALL (TOP)"):
    copy_clip(all_codes)
    st.success("Copied ALL!")

st.write("---")

# ---------------- Question Block Function ----------------
def question_block(title, key, value):

    st.write(f"### {title}")

    col1, col2, col3, col4 = st.columns([5, 1.2, 1.2, 1.2])

    with col1:
        new_text = st.text_area("", value, key=key, height=150)

    with col2:
        if st.button("Save", key=f"{key}_save"):
            ref.child(key).set(new_text)
            st.success("Saved!")

    with col3:
        if st.button("Copy", key=f"{key}_copy"):
            copy_clip(new_text)
            st.success("Copied!")

    with col4:
        if st.button("Clear", key=f"{key}_clear"):
            ref.child(key).set("")
            st.success("Cleared! Refresh page.")

    st.write("---")

# ---------------- 4 Questions ----------------
question_block("Question 1", "q1", data["q1"])
question_block("Question 2", "q2", data["q2"])
question_block("Question 3", "q3", data["q3"])
question_block("Question 4", "q4", data["q4"])
