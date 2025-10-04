import threading
import time
import sys
from db import get_random_quiz  #DB function returning a Quiz object or dict
from quiz import Quiz  # Quiz class


"""
QuizController class to manage quiz flow, timing, and scoring.
We use threading to implement a countdown timer for each question.
Some methods are prefixed with an underscore to indicate they are internal.
Threading is used to allow the timer to run concurrently with user input.
"""
class QuizController:
    def __init__(self, num_questions=5, time_limit=30):
        """
        Initialize a QuizController object.

        Args:
            num_questions (int): The number of questions to ask in a quiz.
                Defaults to 5.
            time_limit (int): The time limit in seconds for each question.
                Defaults to 30.
        """
        self.num_questions = num_questions
        self.time_limit = time_limit
        self.score = 0
        self.correct_count = 0
        self.streak = 0

    def _progress_bar(self, seconds, stop_event):
        """Show countdown progress bar."""
        total = seconds
        for remaining in range(total, 0, -1):
            if stop_event.is_set():
                return
            bar_length = 20
            filled = int((remaining / total) * bar_length)
            bar = "#" * filled + "-" * (bar_length - filled)

            sys.stdout.write(f"\r[{bar}] {remaining:2d}s left ")
            sys.stdout.flush()
            time.sleep(1)
        print("\n Time’s up!")

    def _timed_input(self, prompt):
        """Input with a visible countdown timer."""
        stop_event = threading.Event()
        timer_thread = threading.Thread(target=self._progress_bar, args=(self.time_limit, stop_event))
        timer_thread.start()

        start = time.time()
        try:
            answer = input(f"\n{prompt}\n> ").strip().upper()
        except EOFError:
            answer = None

        stop_event.set()
        timer_thread.join()

        elapsed = time.time() - start
        if elapsed > self.time_limit or not answer:
            return None
        return answer

    def start_quiz(self):
        """
        Start a quiz with a given number of questions and time limit.

        Print a welcome message, then loop through the given number of questions.
        For each question, print the question text and options, then ask the user for an answer.
        If the user answers correctly, print a success message and increment the score and correct count.
        If the user answers incorrectly or runs out of time, print a failure message and reset the streak.
        After all questions have been asked, print the final score and number of correct answers.
        """
        print("\n Welcome to the Flight Quiz Challenge!")
        print(f"You will have {self.time_limit} seconds per question.\n")

        for i in range(1, self.num_questions + 1):
            q_data = get_random_quiz()
            quiz = Quiz(**q_data)

            question_text = (
                f"Q{i}: {quiz.question}\n"
                f"A) {quiz.choice_a}\n"
                f"B) {quiz.choice_b}\n"
                f"C) {quiz.choice_c}\n"
                f"D) {quiz.choice_d}\n"
            )

            answer = self._timed_input(question_text)

            if answer is None:
                print("❌ You ran out of time!")
                self.streak = 0
                continue

            if quiz.is_correct(answer):
                print("✅ Correct!")
                self.correct_count += 1
                self.streak += 1
                self.score += 10

                # Streak bonus every 3 correct answers
                if self.streak == 3:
                    print("🔥 Streak bonus +5 points!")
                    self.score += 5
                    self.streak = 0
            else:
                print(f"❌ Wrong! The correct answer was {quiz.correct_choice}.")
                self.streak = 0

            time.sleep(1.2)  # short pause before next question

        self._show_results()

    def _show_results(self):
        """
        Prints out the final results of the quiz, including the number of correct answers and the final score.
        """
        print("\n Quiz Over!")
        print(f" Correct Answers: {self.correct_count}/{self.num_questions}")
        print(f" Final Score: {self.score}\n")
