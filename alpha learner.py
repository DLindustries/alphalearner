import tkinter as tk
import os
from datetime import datetime, timedelta

current_flashcard = 0
intervals = [timedelta(days=1), timedelta(days=2), timedelta(days=4), timedelta(days=8)]

def do_sets():
    global current_flashcard
    flashcards_path = os.path.join(os.path.expanduser("~/Documents"), "Alpha Learner", "flashcards")
    if not os.path.exists(flashcards_path):
        tk.Label(content_frame, text="Flashcards directory not found.").pack(pady=10)
        return

    flashcards = [f for f in os.listdir(flashcards_path) if f.endswith('.txt')]
    due_flashcards, upcoming_flashcards = [], []

    for flashcard in flashcards:
        flashcard_path = os.path.join(flashcards_path, flashcard)
        try:
            with open(flashcard_path, 'r') as file:
                lines = file.readlines()
                next_review = datetime.strptime(lines[3].split(": ")[1].strip(), '%Y-%m-%d %H:%M:%S')
                if datetime.now() >= next_review:
                    due_flashcards.append(flashcard)
                else:
                    upcoming_flashcards.append((flashcard, next_review))
        except Exception as e:
            print(f"Error processing {flashcard}: {e}")

    for widget in content_frame.winfo_children():
        widget.destroy()

    if not due_flashcards:
        tk.Label(content_frame, text="No flashcards due for review.").pack(pady=10)
        if upcoming_flashcards:
            tk.Label(content_frame, text="Upcoming Flashcards:").pack(pady=5)
            for flashcard, next_review in upcoming_flashcards:
                tk.Label(content_frame, text=f"{flashcard}: Next review on {next_review.strftime('%Y-%m-%d %H:%M:%S')}").pack(pady=2)
    else:
        current_flashcard = 0
        show_flashcard(due_flashcards)

def show_flashcard(flashcards):
    global current_flashcard
    for widget in content_frame.winfo_children():
        widget.destroy()

    if current_flashcard >= len(flashcards):
        tk.Label(content_frame, text="No more flashcards to review.").pack(pady=10)
        return

    flashcard_path = os.path.join(os.path.expanduser("~/Documents"), "Alpha Learner", "flashcards", flashcards[current_flashcard])
    with open(flashcard_path, 'r') as file:
        lines = file.readlines()
        question = lines[0].split(": ")[1].strip()
        answer = lines[1].split(": ")[1].strip()

    tk.Label(content_frame, text=f"Question: {question}").pack(pady=10)
    tk.Button(content_frame, text="Show Answer", command=lambda: show_answer(answer, flashcard_path, flashcards)).pack(pady=10)

def show_answer(answer, flashcard_path, flashcards):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text=f"Answer: {answer}").pack(pady=10)
    for difficulty, text in [("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard"), ("again", "Again")]:
        tk.Button(content_frame, text=text, command=lambda d=difficulty: update_flashcard(flashcard_path, d, flashcards)).pack(side="left", padx=5)

def update_flashcard(flashcard_path, difficulty, flashcards):
    global current_flashcard
    with open(flashcard_path, 'r') as file:
        lines = file.readlines()

    last_reviewed = datetime.now()
    stage = int(lines[4].split(": ")[1].strip())  

    if difficulty == "easy":
        stage = min(stage + 1, len(intervals) - 1)  
        next_review = last_reviewed + intervals[stage]
    elif difficulty == "medium":
        next_review = last_reviewed + intervals[stage]  
    elif difficulty == "hard":
        next_review = last_reviewed + timedelta(minutes=5)  
    elif difficulty == "again":
        stage = 0  
        next_review = last_reviewed + intervals[stage]

    lines[2] = f"Last Reviewed: {last_reviewed.strftime('%Y-%m-%d %H:%M:%S')}\n"
    lines[3] = f"Next Review: {next_review.strftime('%Y-%m-%d %H:%M:%S')}\n"
    lines[4] = f"Stage: {stage}\n"  

    with open(flashcard_path, 'w') as file:
        file.writelines(lines)

    current_flashcard += 1
    show_flashcard(flashcards)

root = tk.Tk()
root.title("Flashcard Review")

content_frame = tk.Frame(root)
content_frame.pack(pady=20)

do_sets()
root.mainloop()
