import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Shared Clipboard", layout="wide")

# ---------------- FIREBASE LOAD FROM RENDER ENV VARIABLES ----------------
firebase_config = {
    "type": os.environ["FIREBASE_TYPE"],
    "project_id": os.environ["FIREBASE_PROJECT_ID"],
    "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
    "client_id": os.environ["FIREBASE_CLIENT_ID"],
    "auth_uri": os.environ["FIREBASE_AUTH_URI"],
    "token_uri": os.environ["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["FIREBASE_AUTH_PROVIDER"],
    "client_x509_cert_url": os.environ["FIREBASE_CLIENT_CERT"],
}

cred = credentials.Certificate(firebase_config)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://clip-board-10d45-default-rtdb.firebaseio.com/"
    })

ref = db.reference("sharedClipboard")

# ---------------- FETCH EXISTING DATA ----------------
data = ref.get() or {"q1": "", "q2": "", "q3": "", "q4": ""}

# ---------------- JS COPY TO CLIPBOARD ----------------
def copy_clip(text):
    components.html(
        f"""
        <script>
            const el = document.createElement('textarea');
            el.value = `{text}`;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
        </script>
        """, height=0
    )

# ---------------- UI HEADER ----------------
st.title("📋 Shared Clipboard (4 Questions Sync)")
st.write("Paste code → Save → Copy → Clear")

# ---------------- COPY ALL TOP BUTTON ----------------
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

# ---------------- QUESTION BLOCK FUNCTION ----------------
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
            st.success("Cleared!")

    st.write("---")

# ---------------- RENDER 4 QUESTIONS ----------------
question_block("Question 1", "q1", data["q1"])
question_block("Question 2", "q2", data["q2"])
question_block("Question 3", "q3", data["q3"])
question_block("Question 4", "q4", data["q4"])
