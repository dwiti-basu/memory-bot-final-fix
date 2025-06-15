import streamlit as st
import json
import random
import requests

st.set_page_config(page_title="💌 My Memory Bot")

# Load memory data
with open("memories.json", "r", encoding="utf-8") as f:
    memory_data = json.load(f)

# Use Hugging Face Inference API (no local model needed)
API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}

def query_hf(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    return "Something went wrong. Try again later."

# UI
st.title("💌 My Memory Bot")
st.write(
    "This bot is here to convince **Errorgon** how much **Romi** loves him. "
    "Truly, madly, deeply. 🥲"
)

emotion = st.text_input("How are you feeling right now? (e.g. sad, missing, angry)")

def get_memory_by_emotion(emotion):
    matches = [m for m in memory_data["memories"] if emotion.lower() in m["emotion"].lower()]
    return random.choice(matches)["message"] if matches else None

def generate_reply(emotion, memory):
    prompt = f"""
You are a loving memory bot who knows everything about my love for Errorgon.
Your job is to tell him and express my love when he's feeling {emotion}.
Use the memory below and expand it into a warm, emotional, comforting message full of love and reassurance.

Memory: {memory}
"""
    return query_hf(prompt)

if st.button("I love you, don’t be mad 💖"):
    if not emotion:
        st.warning("Please enter an emotion.")
    else:
        memory = get_memory_by_emotion(emotion)
        if memory:
            reply = generate_reply(emotion, memory)
            st.markdown("### 💬 Memory Response")
            st.success(reply)
        else:
            st.info("I don't have a memory for that emotion.")
