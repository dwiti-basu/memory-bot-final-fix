import streamlit as st
from transformers import pipeline
import json
import random

# ✅ Set Streamlit page config FIRST
st.set_page_config(page_title="💌 My Memory Bot")

# 📖 Load memories from JSON
with open("memories.json", "r", encoding="utf-8") as f:
    memory_data = json.load(f)

# 🚀 Load text generation pipeline from Hugging Face
@st.cache_resource
def load_generator():
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    return pipeline("text-generation", model=model_id)

generator = load_generator()

# 🎨 App UI
st.title("💌 My Memory Bot")
st.write("This bot is on a very emotional mission: to make **Errorgon** finally understand how ridiculously, hopelessly, dramatically much **Romi** loves him. Like, *'please don't leave me, I'm already emotionally deceased'* levels of love. 💀❤️.")

# ✍️ Input from user
emotion = st.text_input("How are you feeling right now? (e.g. sad, angry, missing you)")

# 🧠 Memory matching
def get_memory_by_emotion(emotion):
    matches = [m for m in memory_data["memories"] if emotion.lower() in m["emotion"].lower()]
    return random.choice(matches)["message"] if matches else None

# 🤖 Hugging Face text generation
def generate_reply(emotion, memory):
    prompt = f"""
You are a loving memory bot who knows everything about my love for Errorgon.
Your job is to tell him and express my love when he's feeling {emotion}.
Use the memory below and expand it into a warm, emotional, comforting message full of love and reassurance.

Memory: {memory}
"""
    result = generator(prompt, max_new_tokens=100, do_sample=True)[0]["generated_text"]
    return result.strip()

# 💖 Button logic
if st.button("I love you don't stay angry on me 💖"):
    if not emotion:
        st.warning("Please tell me how you're feeling.")
    else:
        memory = get_memory_by_emotion(emotion)
        if memory:
            reply = generate_reply(emotion, memory)
            st.markdown("### 💬 Memory Response")
            st.success(reply)
        else:
            st.info("I don't have a memory for that emotion yet. You can add one to your memories.json file.")
