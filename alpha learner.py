import tkinter as tk
import os
from datetime import datetime, timedelta

def do_sets():
    flashcards_path = os.path.join(os.path.expanduser("~/Documents"), "Alpha Learner", "flashcards")
    flashcards = [f for f in os.listdir(flashcards_path) if f.endswith('.txt')]
    
    due_flashcards = []
    upcoming_flashcards = []
    for flashcard in flashcards:
        flashcard_path = os.path.join(flashcards_path, flashcard)
        with open(flashcard_path, 'r') as file:
            lines = file.readlines()
            try:
                next_review = datetime.strptime(lines[3].split(": ")[1].strip(), '%Y-%m-%d %H:%M:%S')
                if datetime.now() >= next_review:
                    due_flashcards.append(flashcard)
                else:
                    upcoming_flashcards.append((flashcard, next_review))
            except ValueError:
                pass
    
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    if not due_flashcards:
        message = tk.Label(content_frame, text="No flashcards due for review.")
        message.pack(pady=10)
        
        if upcoming_flashcards:
            upcoming_label = tk.Label(content_frame, text="Upcoming Flashcards:")
            upcoming_label.pack(pady=5)
            
            for flashcard, next_review in upcoming_flashcards:
                flashcard_label = tk.Label(content_frame, text=f"{flashcard}: Next review on {next_review.strftime('%Y-%m-%d %H:%M:%S')}")
                flashcard_label.pack(pady=2)
    else:
        show_flashcard(due_flashcards)

def show_flashcard(flashcards):
    current_flashcard = 0
    flashcard_path = os.path.join(os.path.expanduser("~/Documents"), "Alpha Learner", "flashcards", flashcards[current_flashcard])
    
    with open(flashcard_path, 'r') as file:
        lines = file.readlines()
        question = lines[0].split(": ")[1].strip()
        answer = lines[1].split(": ")[1].strip()

    question_label = tk.Label(content_frame, text=f"Question: {question}")
    question_label.pack(pady=10)
    
    show_answer_button = tk.Button(content_frame, text="Show Answer", command=lambda: show_answer(question_label, answer, flashcard_path))
    show_answer_button.pack(pady=10)

def show_answer(question_label, answer, flashcard_path):
    question_label.destroy()
    
    answer_label = tk.Label(content_frame, text=f"Answer: {answer}")
    answer_label.pack(pady=10)
    
    easy_button = tk.Button(content_frame, text="Easy", command=lambda: update_flashcard(flashcard_path, "easy"))
    easy_button.pack(side="left", padx=5)
    
    medium_button = tk.Button(content_frame, text="Medium", command=lambda: update_flashcard(flashcard_path, "medium"))
    medium_button.pack(side="left", padx=5)
    
    hard_button = tk.Button(content_frame, text="Hard", command=lambda: update_flashcard(flashcard_path, "hard"))
    hard_button.pack(side="left", padx5)
    
    again_button = tk.Button(content_frame, text="Again", command=lambda: update_flashcard(flashcard_path, "again"))
    again_button.pack(side="left", padx5)

def update_flashcard(flashcard_path, difficulty):
    with open(flashcard_path, 'r') as file:
        lines = file.readlines()
        
    last_reviewed = datetime.now()
    if difficulty == "easy":
        interval = timedelta(days=2)
    elif difficulty == "medium":
        interval = timedelta(minutes=10)
    elif difficulty == "hard":
        interval = timedelta(minutes=5)
    elif difficulty == "again":
        interval = timedelta(minutes=1)
    
    next_review = last_reviewed + interval
    
    lines[2] = f"Last Reviewed: {last_reviewed.strftime('%Y-%m-%d %H:%M:%S')}\n"
    lines[3] = f"Next Review: {next_review.strftime('%Y-%m-%d %H:%M:%S')}\n"
    lines[4] = f"Difficulty: {difficulty}\n"
    
    with open(flashcard_path, 'w') as file:
        file.writelines(lines)
    
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    message = tk.Label(content_frame, text="Flashcard updated.")
    message.pack(pady=10)
    do_sets()

def make_edit_flashcards():
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    flashcards_path = os.path.join(os.path.expanduser("~/Documents"), "Alpha Learner", "flashcards")
    flashcards = [f for f in os.listdir(flashcards_path) if f.endswith('.txt')]
    
    flashcards_label = tk.Label(content_frame, text="Existing Flashcards:")
    flashcards_label.pack(pady=5)
    
    for flashcard in flashcards:
        flashcard_label = tk.Label(content_frame, text=flashcard)
        flashcard_label.pack(pady=2)
    
    add_flashcard_button = tk.Button(content_frame, text="Add Flashcard", command=add_flashcard)
    add_flashcard_button.pack(pady=10)

def add_flashcard():
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    question_label = tk.Label(content_frame, text="What is the question for this flashcard?")
    question_label.pack(pady=5)
    question_entry = tk.Entry(content_frame, width=50)
    question_entry.pack(pady=5)
    
    def save_question():
        question = question_entry.get()
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        answer_label = tk.Label(content_frame, text="What is the answer?")
        answer_label.pack(pady=5)
        answer_entry = tk.Entry(content_frame, width=50)
        answer_entry.pack(pady=5)
        
        def save_answer():
            answer = answer_entry.get()
            save_flashcard(question, answer)
            make_edit_flashcards()  # Refresh the flashcards list
        
        save_answer_button = tk.Button(content_frame, text="Save", command=save_answer)
        save_answer_button.pack(pady=10)
    
    save_question_button = tk.Button(content_frame, text="Next", command=save_question)
    save_question_button.pack(pady=10)

def save_flashcard(question, answer):
    flashcards_path = os.path.join(os.path.expanduser("~/Documents"), "Alpha Learner", "flashcards")
    if not os.path.exists(flashcards_path):
        os.makedirs(flashcards_path)
    
    file_name = os.path.join(flashcards_path, f"{question.replace(' ', '_')}.txt")
    with open(file_name, 'w') as file:
        file.write(f"Question: {question}\n")
        file.write(f"Answer: {answer}\n")
        file.write(f"Last Reviewed: Unlearnt\n")
        file.write(f"Next Review: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("Difficulty: Unlearnt\n")
    print(f"Flashcard saved: {file_name}")

# Function to create the storage directory and the flashcards folder
def create_storage_directory():
    documents_path = os.path.expanduser("~/Documents")
    storage_path = os.path.join(documents_path, "Alpha Learner")
    flashcards_path = os.path.join(storage_path, "flashcards")
    
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    
    if not os.path.exists(flashcards_path):
        os.makedirs(flashcards_path)
    
    print(f"Storage directory: {storage_path}")
    print(f"Flashcards directory: {flashcards_path}")

# Create the main window
root = tk.Tk()
root.title("Flashcard Program")

# Create a menu frame
menu_frame = tk.Frame(root)
menu_frame.pack(pady=20)

# 'Do Sets' button
do_sets_button = tk.Button(menu_frame, text="Do Sets", command=do_sets)
do_sets_button.pack(side="left", padx=20)

# 'Make/Edit Flashcards' button
make_edit_flashcards_button = tk.Button(menu_frame, text="Make/Edit Flashcards", command=make_edit_flashcards)
make_edit_flashcards_button.pack(side="left", padx=20)

# Create a content frame for dynamic content
content_frame = tk.Frame(root)
content_frame.pack(pady=20)

# Create the storage directory and flashcards folder
create_storage_directory()

# Run the application
root.mainloop()
