#	Imports Python’s random module (used later to choose a tip for the simulated AI assistant
#	Imports Tkinter GUI toolkit and aliases it tk for shorter references
#	Imports messagebox (dialogs like showerror) and ttk (themed widgets such as Combobox) from Tkinter
import random
import tkinter as tk
from tkinter import messagebox, ttk

"""
AI Encoder–Decoder GUI

PEP8-style cleaned version of the original main.py.
Preserves original behavior (Shift cipher + Morse encode/decode)
and the simple simulated AI assistant.
"""

#MORSE_CODE_DICT = { 'A': '.-', ... ' ': '/', }
#	A dictionary mapping characters (A–Z, 0–9, punctuation and space) to their Morse-code string
#  equivalents. Space is mapped to '/' (used later to separate words).
#	This is the core lookup for encoding text to Morse.
#  MORSE_TO_TEXT = {v: k for k, v in MORSE_CODE_DICT.items()}
#  Builds the reverse mapping (Morse pattern → character) via dictionary comprehension. Used for decoding Morse back to text


#  Morse Code Dictionary

MORSE_CODE_DICT = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    ',': '--..--',
    '.': '.-.-.-',
    '?': '..--..',
    '/': '-..-.',
    '-': '-....-',
    '(': '-.--.',
    ')': '-.--.-',
    ' ': '/',
}

MORSE_TO_TEXT = {v: k for k, v in MORSE_CODE_DICT.items()}


# --- Encoding/Decoding Functions ---
#	Defines a function that applies a simple shift cipher (but note: it shifts Unicode codepoints, not alphabet positions)

def encode_shift(message, key):
    """Encode a message by shifting character codepoints by key."""
    return ' '.join(str(ord(c) + key) for c in message)


def decode_shift(encoded_text, key):
    """
    Decode a shift-encoded string of numbers separated by spaces.

    Returns an empty string and shows a messagebox on invalid input.
    """
#•	Starts try/except to catch non-integer tokens in the input
    try:
        numbers = list(map(int, encoded_text.split()))
        return ''.join(chr(num - key) for num in numbers)

#	If conversion fails, shows an error dialog (messagebox.showerror) and returns empty string. This informs the user and prevents crashes.

    except ValueError:
        messagebox.showerror(
            "Error", "Invalid numeric input for shift decoding."
        )
        return ""


def encode_morse(message):
    """Encode text to Morse code (unknown chars become '?')."""
#•	Uppercases input so lookup is simpler (MORSE_CODE_DICT keys are uppercase letters)
    message = message.upper()
    return ' '.join(MORSE_CODE_DICT.get(char, '?') for char in message)


def decode_morse(encoded_text):
    """Decode Morse code (words separated with ' /')."""
    words = encoded_text.split(' / ')
    decoded_words = []
    for word in words:
        letters = word.split()
        decoded = ''.join(MORSE_TO_TEXT.get(letter, '?') for letter in letters)
        decoded_words.append(decoded)
    return ' '.join(decoded_words)


# --- AI Text Assistant (Simulated) ---
#	Simulated assistant that offers hints based on the text content. Not a real ML model — deterministic checks + random tips

def ai_assistant_response(text):
    """Simulate AI suggestions or insights based on the text."""
    if not text.strip():
        return "🤖 Please enter some text first!"

    if text.isupper():
        return "🤖 Tip: Your text is in uppercase — ideal for Morse encoding!"
    if text.islower():
        return (
            "🤖 Your text is lowercase — you might want to convert to "
            "uppercase for Morse."
        )
    if text.isdigit():
        return "🤖 That looks like numeric data — use Shift Cipher for best results."
    if any(char in text for char in ['.', '?', '!']):
        return "🤖 This seems like a sentence — consider encoding it in Morse for readability."

    hints = [
        "🤖 Try a higher key for more secure encoding!",
        "🤖 Did you know you can mix Morse and Shift Cipher for fun?",
        "🤖 Keep your message short and simple for clean Morse output.",
        "🤖 Add a numeric key to strengthen your cipher encoding.",
    ]
    return random.choice(hints)


# --- GUI Functions ---


def encode_message():
    """Handler for the Encode button."""
#	Reads the full contents from input_text Tkinter Text widget (from line 1.0 to END) and strips
# surrounding whitespace/newlines. This is the text to encode
    message = input_text.get("1.0", tk.END).strip()
    mode = mode_var.get()

    if mode == "Shift Cipher":
        key = key_entry.get()
        if not key.isdigit():
            messagebox.showerror("Error", "Key must be an integer!")
            return
        key_int = int(key)
        result = encode_shift(message, key_int)

    elif mode == "Morse Code":
        result = encode_morse(message)

    else:
        messagebox.showerror("Error", "Unknown encoding mode.")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

#	Update the AI assistant label (StringVar) with response based on the original message
    ai_text.set(ai_assistant_response(message))


def decode_message():
    """Handler for the Decode button."""
    message = input_text.get("1.0", tk.END).strip()
    mode = mode_var.get()

    if mode == "Shift Cipher":
        key = key_entry.get()
        if not key.isdigit():
            messagebox.showerror("Error", "Key must be an integer!")
            return
        key_int = int(key)
        result = decode_shift(message, key_int)

    elif mode == "Morse Code":
        result = decode_morse(message)

    else:
        messagebox.showerror("Error", "Unknown decoding mode.")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    ai_text.set(ai_assistant_response(result))


def clear_all():
    """Clear input, output, key, and reset AI assistant text."""
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    key_entry.delete(0, tk.END)
    ai_text.set("🤖 AI Assistant ready to help!")


# --- GUI Layout ---
root = tk.Tk()
root.title("AI Encoder–Decoder with Morse Code")
root.geometry("800x800")
root.config(bg="silver")

# Title
# Creates a big title label "AI Encoder–Decoder" with font and background and packs it with vertical padding
tk.Label(
    root,
    text="AI Encoder–Decoder",
    font=("San Serif", 24, "bold"),
    bg="#e6f0ff",
).pack(pady=10)

# Mode selection
mode_frame = tk.Frame(root, bg="#e6f0ff")
mode_frame.pack(pady=5)
tk.Label(
    mode_frame, text="Select Mode:", bg="#e6f0ff", font=("San Serif", 18)
).pack(side=tk.LEFT, padx=5)

mode_var = tk.StringVar(value="Shift Cipher")
mode_menu = ttk.Combobox(
    mode_frame,
    textvariable=mode_var,
    values=["Shift Cipher", "Morse Code"],
    width=20,
    state="readonly",
)
mode_menu.pack(side=tk.LEFT)

# Key input (for shift cipher)
key_frame = tk.Frame(root, bg="#e6f0ff")
key_frame.pack(pady=5)
tk.Label(
    key_frame,
    text="Enter Key (number):",
    bg="#e6f0ff",
    font=("San Serif", 18),
).pack(side=tk.LEFT, padx=5)

key_entry = tk.Entry(key_frame, width=10, font=("San Serif", 18))
key_entry.pack(side=tk.LEFT)

# Input text
tk.Label(
    root,
    text="Input Message:",
    bg="#e6f0ff",
    font=("San Serif", 18, "bold"),
).pack(pady=5)

input_text = tk.Text(root, height=5, width=70, font=("San Serif", 18))
input_text.pack()

# Buttons
button_frame = tk.Frame(root, bg="royalblue")
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Encode",
    command=encode_message,
    width=12,
    bg="white",
).pack(side=tk.LEFT, padx=10)

tk.Button(
    button_frame,
    text="Decode",
    command=decode_message,
    width=12,
    bg="white",
).pack(side=tk.LEFT, padx=10)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_all,
    width=12,
    bg="white",
).pack(side=tk.LEFT, padx=10)

# Output text
tk.Label(
    root,
    text="Output Message:",
    bg="#e6f0ff",
    font=("San Serif", 18, "bold"),
).pack(pady=5)

output_text = tk.Text(root, height=5, width=70, font=("San Serif", 18))
output_text.pack()

# AI Assistant area
tk.Label(
    root,
    text="AI Assistant:",
    bg="#e6f0ff",
    font=("San Serif", 14, "bold"),
).pack(pady=5)

ai_text = tk.StringVar(value="🤖 AI Assistant ready to help!")
ai_label = tk.Label(
    root,
    textvariable=ai_text,
    wraplength=600,
    justify="left",
    bg="royalblue",
    font=("San Serif", 18),
)
ai_label.pack(padx=10, pady=5, fill="x")

root.mainloop()
