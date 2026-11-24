from tkinter import Canvas, PhotoImage, Tk, Button
from pathlib import Path
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
flip_timer = None

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "Data"
IMAGE_DIR = PROJECT_DIR / "images"
WORDS_TO_LEARN_FILE = DATA_DIR / "japanese_words_to_learn.csv"
ORIGINAL_WORDS_FILE = DATA_DIR / "japanese_words.csv"

try:
    data = pandas.read_csv(WORDS_TO_LEARN_FILE)
except FileNotFoundError:
    data = pandas.read_csv(ORIGINAL_WORDS_FILE)

to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer

    if flip_timer is not None:
        window.after_cancel(flip_timer)

    if not to_learn:
        canvas.itemconfig(card_title, text="Finished", fill="black")
        canvas.itemconfig(card_word, text="No words left", fill="black")
        canvas.itemconfig(card_image, image=card_front_image)
        return

    current_card = random.choice(to_learn)
    canvas.itemconfig(card_image, image=card_front_image)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Japanese"], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_image, image=card_back_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def is_known():
    if current_card in to_learn:
        to_learn.remove(current_card)
        pandas.DataFrame(to_learn).to_csv(WORDS_TO_LEARN_FILE, index=False)
    next_card()


window = Tk()
window.title("Japanese Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file=IMAGE_DIR / "card_front.png")
card_back_image = PhotoImage(file=IMAGE_DIR / "card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 32, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 42, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file=IMAGE_DIR / "wrong.png")
unknown_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

right_image = PhotoImage(file=IMAGE_DIR / "right.png")
known_button = Button(image=right_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()
window.mainloop()