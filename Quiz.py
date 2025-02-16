import tkinter as tk
from tkinter import messagebox
import time
from threading import Timer

# Question class to encapsulate a question and its answer
class Question:
    def __init__(self, prompt, options, answer):
        self.prompt = prompt
        self.options = options
        self.answer = answer

# List of 10 questions
questions = [
    Question("Who developed Python programming language?", 
             ["Guido van Rossum", "Dennis Ritchie", "Bjarne Stroustrup", "James Gosling"], "Guido van Rossum"),
    Question("Which keyword is used to define a function in Python?", 
             ["def", "function", "func", "lambda"], "def"),
    Question("What is the output of 2 ** 3 in Python?", 
             ["6", "8", "9", "None of the above"], "8"),
    Question("Which data type is mutable in Python?", 
             ["Tuple", "List", "String", "Integer"], "List"),
    Question("Which method is used to remove whitespaces from a string?", 
             ["strip()", "trim()", "remove()", "split()"], "strip()"),
    Question("What is the default mode of the open() function?", 
             ["write", "append", "read", "binary"], "read"),
    Question("What is the full form of HTML?", 
             ["Hyper Text Markup Language", "High-Level Text Machine Language", 
              "Hyperlink Text Management Language", "None of the above"], "Hyper Text Markup Language"),
    Question("Which CSS property is used to change the text color?", 
             ["font-color", "text-color", "color", "background-color"], "color"),
    Question("Which tag is used to insert an image in HTML?", 
             ["<img>", "<image>", "<picture>", "<src>"], "<img>"),
    Question("Which SQL command is used to retrieve data?", 
             ["INSERT", "DELETE", "SELECT", "UPDATE"], "SELECT")
]

# Timer function
class QuizTimer:
    def __init__(self, duration, callback):
        self.duration = duration
        self.callback = callback
        self.timer = None

    def start(self):
        self.timer = Timer(self.duration, self.callback)
        self.timer.start()

    def cancel(self):
        if self.timer:
            self.timer.cancel()

# GUI Quiz
class QuizApp:
    def __init__(self, root, questions):
        self.root = root
        self.questions = questions
        self.current_question = 0
        self.score = 0
        self.timer = None

        # Configure root window
        self.root.title("Quiz Application")
        self.root.geometry("600x400")

        # Create GUI elements
        self.question_label = tk.Label(root, text="", wraplength=500, font=("Arial", 16), justify="center")
        self.question_label.pack(pady=20)

        self.options_var = tk.StringVar(value="")
        self.options_frame = tk.Frame(root)
        self.options_frame.pack()

        self.submit_button = tk.Button(root, text="Submit", command=self.check_answer, font=("Arial", 14))
        self.submit_button.pack(pady=20)

        self.timer_label = tk.Label(root, text="", font=("Arial", 14))
        self.timer_label.pack()

        self.load_question()

    def load_question(self):
        """Load the current question into the GUI."""
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.config(text=f"Q{self.current_question + 1}) {question.prompt}")
            self.options_var.set("")  # Reset selected option

            # Clear previous options and create new ones
            for widget in self.options_frame.winfo_children():
                widget.destroy()

            for option in question.options:
                tk.Radiobutton(
                    self.options_frame, text=option, variable=self.options_var, value=option, 
                    font=("Arial", 14), wraplength=400
                ).pack(anchor="w", pady=5)

            # Start timer
            self.start_timer(15)  # 15 seconds per question
        else:
            self.end_quiz()

    def check_answer(self):
        """Check the selected answer and proceed to the next question."""
        selected_answer = self.options_var.get()
        correct_answer = self.questions[self.current_question].answer

        if selected_answer == correct_answer:
            self.score += 1

        self.current_question += 1
        self.load_question()

    def start_timer(self, duration):
        """Start the timer for the current question."""
        if self.timer:
            self.timer.cancel()

        self.timer = QuizTimer(duration, self.time_up)
        self.timer.start()
        self.update_timer_label(duration)

    def update_timer_label(self, remaining_time):
        """Update the timer label with the remaining time."""
        if remaining_time > 0:
            self.timer_label.config(text=f"Time Left: {remaining_time} seconds")
            self.root.after(1000, self.update_timer_label, remaining_time - 1)

    def time_up(self):
        """Handle when the time is up for a question."""
        messagebox.showinfo("Time's Up!", "You ran out of time for this question.")
        self.current_question += 1
        self.load_question()

    def end_quiz(self):
        """End the quiz and display the score."""
        if self.timer:
            self.timer.cancel()

        messagebox.showinfo("Quiz Completed", f"You scored {self.score} out of {len(self.questions)}!")
        self.root.quit()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root, questions)
    root.mainloop()
