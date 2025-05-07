from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import tkinter as tk
from tkinter import scrolledtext, messagebox

nltk.download("vader_lexicon")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Load pre-trained GPT-2 model and tokenizer from Hugging Face
model_name = "gpt2"  # Change to another model if desired
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Function to generate song lyrics
def generate_lyrics(theme, emotion, num_verses, max_length=300, num_return_sequences=1):
    prompt = f"Theme: {theme}\nEmotion: {emotion}\nSong Lyrics:\nVerse 1:\n"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Generate lyrics
    output = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,
        temperature=0.7,
        top_k=50,
        top_p=0.85,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    lyrics = [tokenizer.decode(lyrics, skip_special_tokens=True) for lyrics in output]

    formatted_lyrics = []
    for lyric in lyrics:
        verses = lyric.split("Verse")
        if len(verses) >= num_verses + 1:
            formatted_lyric = ""
            for i, verse in enumerate(verses[1:num_verses+1], start=1):
                formatted_lyric += f"Verse {i}:\n{verse.strip()}\n\n"
            formatted_lyrics.append(formatted_lyric.strip())

    return formatted_lyrics or lyrics

# Function for the button action
def generate_lyrics_action():
    theme = theme_entry.get()
    emotion = emotion_entry.get()
    try:
        num_verses = int(verses_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for verses.")
        return

    if not theme or not emotion or not num_verses:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    lyrics = generate_lyrics(theme, emotion, num_verses)
    lyrics_display.delete(1.0, tk.END)
    for i, lyric in enumerate(lyrics, 1):
        lyrics_display.insert(tk.END, f"Generated Lyrics {i}:\n{lyric}\n{'-'*50}\n")

# Set up the GUI window
root = tk.Tk()
root.title("Song Lyrics Generator")
root.geometry("600x600")

# Labels and input fields
tk.Label(root, text="Song Theme:").pack(pady=5)
theme_entry = tk.Entry(root, width=50)
theme_entry.pack(pady=5)

tk.Label(root, text="Emotion:").pack(pady=5)
emotion_entry = tk.Entry(root, width=50)
emotion_entry.pack(pady=5)

tk.Label(root, text="Number of Verses:").pack(pady=5)
verses_entry = tk.Entry(root, width=50)
verses_entry.pack(pady=5)

# Generate Button
generate_button = tk.Button(root, text="Generate Lyrics", command=generate_lyrics_action)
generate_button.pack(pady=10)

# ScrolledText to display the generated lyrics
lyrics_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
lyrics_display.pack(pady=10)

# Start the GUI main loop
root.mainloop()
