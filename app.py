# app.py

import streamlit as st
from tutor_core import ask_tutor
import datetime

st.set_page_config(page_title="🤖 AI Python Tutor", layout="centered")
st.title("🤖 AI Python Tutor")

if "question" not in st.session_state:
    st.session_state.question = ""

st.sidebar.title("🛠️ How It Works")
st.sidebar.write("""
1. Ask any Python question  
2. Click **Get Answer**  
3. Read, copy, learn!
""")

st.sidebar.title("💡 Examples")
examples = [
    "What is a list comprehension?",
    "Explain Python decorators.",
    "Debug this code: `for i in range(5) print(i)`"
]
for ex in examples:
    if st.sidebar.button(ex):
        st.session_state.question = ex

st.sidebar.markdown("🗑️ **Clear Memory**")
if st.sidebar.button("Clear All Memory"):
    from pathlib import Path
    mem_file = Path(__file__).parent / "memory.json"
    if mem_file.exists():
        mem_file.unlink()
   

st.markdown("Ask me anything about **Python** below and I'll explain it clearly!")
question = st.text_area(
    "Your Question:",
    value=st.session_state.question,
    height=150,
    placeholder="e.g., What is a list comprehension in Python?"
)

get_btn = st.button("Get Answer", disabled=not question.strip())

if get_btn:
    with st.spinner("Thinking..."):
        try:
            answer = ask_tutor(question)
        except Exception as e:
            st.error(f"Oops—something went wrong: {e}")
        else:
            st.markdown(f"### 💡 Answer ({datetime.datetime.now().strftime('%H:%M:%S')}):")
            st.write(answer)
            st.session_state.question = ""
