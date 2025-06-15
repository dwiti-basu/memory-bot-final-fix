import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
import random

# Set Streamlit page config
st.set_page_config(page_title="💌 My Memory Bot")

# Load memory data
with open("memories.json", "r", encoding="utf-8") as f:
    memory_data = json.load(f)

# Load model and tokenizer with caching
@st.cache_resource
def load_generator():
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    return model, tokenizer

model, tokenizer = load_generator()

# App title and intro
st.title("💌 My Memory Bot")
st.write(
    "This bot is on a very emotional mission: to make **Errorgon** finally understand "
    "how ridiculously, hopelessly, dramatically much **Romi** loves him. "
    "Like, *'please don't leave me, I'm already emotionally deceased'* levels of love. 💀❤️."
)

# Emotion input
emotion = st.text_input("How are you feeling right now? (e.g. sad, angry, missing you)")

# Memory filter
def get_memory_by_emotion(emotion):
    matches = [m for m in memory_data["memories"] if emotion.lower() in m["emotion"].lower()]
    return random.choice(matches)["message"] if matches else None

# Text generation logic
def generate_reply(emotion, memory):
    prompt = f"""
You are a loving memory bot who knows everything about my love for Errorgon.
Your job is to tell him and express my love when he's feeling {emotion}.
Use the memory below and expand it into a warm, emotional, comforting message full of love and reassurance.

Memory: {memory}
"""
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids, max_new_tokens=100, do_sample=True)
    result = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return result.strip()

# Button interaction
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
