import tkinter as tk
from tkinter import messagebox, ttk
import random

# --- Morse Code Dictionary ---
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
    '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

MORSE_TO_TEXT = {v: k for k, v in MORSE_CODE_DICT.items()}

# --- Encoding/Decoding Functions ---
def encode_shift(message, key):
    return ' '.join(str(ord(c) + key) for c in message)

def decode_shift(encoded_text, key):
    try:
        numbers = list(map(int, encoded_text.split()))
        return ''.join(chr(num - key) for num in numbers)
    except ValueError:
        messagebox.showerror("Error", "Invalid numeric input for shift decoding.")
        return ""

def encode_morse(message):
    message = message.upper()
    return ' '.join(MORSE_CODE_DICT.get(char, '?') for char in message)

def decode_morse(encoded_text):
    words = encoded_text.split(' / ')
    decoded_words = []
    for word in words:
        letters = word.split()
        decoded = ''.join(MORSE_TO_TEXT.get(letter, '?') for letter in letters)
        decoded_words.append(decoded)
    return ' '.join(decoded_words)

# --- AI Text Assistant (Simulated) ---
def ai_assistant_response(text):
    """Simulates AI suggestions or insights based on the text."""
    if not text.strip():
        return "🤖 Please enter some text first!"

    if text.isupper():
        return "🤖 Tip: Your text is in uppercase — ideal for Morse encoding!"
    elif text.islower():
        return "🤖 Your text is lowercase — you might want to convert to uppercase for Morse."
    elif text.isdigit():
        return "🤖 That looks like numeric data — use Shift Cipher for best results."
    elif any(char in text for char in ['.', '?', '!']):
        return "🤖 This seems like a sentence — consider encoding it in Morse for readability."
    else:
        hints = [
            "🤖 Try a higher key for more secure encoding!",
            "🤖 Did you know you can mix Morse and Shift Cipher for fun?",
            "🤖 Keep your message short and simple for clean Morse output.",
            "🤖 Add a numeric key to strengthen your cipher encoding."
        ]
        return random.choice(hints)

# --- GUI Functions ---
def encode_message():
    message = input_text.get("1.0", tk.END).strip()
    mode = mode_var.get()

    if mode == "Shift Cipher":
        key = key_entry.get()
        if not key.isdigit():
            messagebox.showerror("Error", "Key must be an integer!")
            return
        key = int(key)
        result = encode_shift(message, key)

    elif mode == "Morse Code":
        result = encode_morse(message)
    else:
        messagebox.showerror("Error", "Unknown encoding mode.")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    ai_text.set(ai_assistant_response(message))

def decode_message():
    message = input_text.get("1.0", tk.END).strip()
    mode = mode_var.get()

    if mode == "Shift Cipher":
        key = key_entry.get()
        if not key.isdigit():
            messagebox.showerror("Error", "Key must be an integer!")
            return
        key = int(key)
        result = decode_shift(message, key)

    elif mode == "Morse Code":
        result = decode_morse(message)
    else:
        messagebox.showerror("Error", "Unknown decoding mode.")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    ai_text.set(ai_assistant_response(result))

def clear_all():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    key_entry.delete(0, tk.END)
    ai_text.set("🤖 AI Assistant ready to help!")

# --- GUI Layout ---
root = tk.Tk()
root.title("AI Encoder–Decoder with Morse Code")
root.geometry("700x600")
root.config(bg="#e6f0ff")

# Title
tk.Label(root, text="AI Encoder–Decoder", font=("Arial", 20, "bold"), bg="#e6f0ff").pack(pady=10)

# Mode selection
mode_frame = tk.Frame(root, bg="#e6f0ff")
mode_frame.pack(pady=5)
tk.Label(mode_frame, text="Select Mode:", bg="#e6f0ff", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
mode_var = tk.StringVar(value="Shift Cipher")
mode_menu = ttk.Combobox(mode_frame, textvariable=mode_var, values=["Shift Cipher", "Morse Code"], width=20, state="readonly")
mode_menu.pack(side=tk.LEFT)

# Key input (for shift cipher)
key_frame = tk.Frame(root, bg="#e6f0ff")
key_frame.pack(pady=5)
tk.Label(key_frame, text="Enter Key (number):", bg="#e6f0ff", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
key_entry = tk.Entry(key_frame, width=10, font=("Arial", 12))
key_entry.pack(side=tk.LEFT)

# Input text
tk.Label(root, text="Input Message:", bg="#e6f0ff", font=("Arial", 12, "bold")).pack(pady=5)
input_text = tk.Text(root, height=5, width=70, font=("Arial", 12))
input_text.pack()

# Buttons
button_frame = tk.Frame(root, bg="#e6f0ff")
button_frame.pack(pady=10)
tk.Button(button_frame, text="Encode", command=encode_message, width=12, bg="#cce5ff").pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Decode", command=decode_message, width=12, bg="#cce5ff").pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Clear", command=clear_all, width=12, bg="#ffcccc").pack(side=tk.LEFT, padx=10)

# Output text
tk.Label(root, text="Output Message:", bg="#e6f0ff", font=("Arial", 12, "bold")).pack(pady=5)
output_text = tk.Text(root, height=5, width=70, font=("Arial", 12))
output_text.pack()

# AI Assistant area
tk.Label(root, text="AI Assistant:", bg="#e6f0ff", font=("Arial", 12, "bold")).pack(pady=5)
ai_text = tk.StringVar(value="🤖 AI Assistant ready to help!")
ai_label = tk.Label(root, textvariable=ai_text, wraplength=600, justify="left", bg="#f0f8ff", font=("Arial", 11))
ai_label.pack(padx=10, pady=5, fill="x")

root.mainloop()

