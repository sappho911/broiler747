import time
from db import get_random_quiz  #DB function returning a Quiz dict
from quiz import Quiz  #Quiz class

"""
QuizController class to manage quiz flow and scoring without timing.
Some methods are prefixed with an underscore to indicate they are internal.

"""

class QuizController:
    def __init__(self, num_questions=10):
        self.num_questions = num_questions
        self.score = 0
        self.correct_count = 0
        self.streak = 0

    def start_quiz(self):
        print("\n Welcome to the Flight Quiz Challenge!")
        print("Answer each question by typing A, B, C, or D.\n")

        for i in range(1, self.num_questions + 1):
            q_data = get_random_quiz()
            # Unpack quiz data with some python sugar
            # (using ** to unpack dict to parameters)
            quiz = Quiz(**q_data)

            # Display the question
            print(f"Q{i}: {quiz.question}")
            print(f"A) {quiz.choice_a}")
            print(f"B) {quiz.choice_b}")
            print(f"C) {quiz.choice_c}")
            print(f"D) {quiz.choice_d}")

            # Get the player's answer + Ctrl-C handling
            try:
                answer = input("> ").strip().upper()
            except KeyboardInterrupt:
                print("\n\nQuiz interrupted. Exiting...")
                return

            if not answer or answer not in ["A", "B", "C", "D"]:
                print("Invalid input! Moving to next question.\n")
                self.streak = 0
                continue

            # Evaluate answer
            if quiz.is_correct(answer):
                print("Correct!")
                self.correct_count += 1
                self.streak += 1
                self.score += 10

                # Streak bonus every 3 correct answers
                if self.streak %3 == 0:
                    print("🔥 Streak bonus +5 points!")
                    self.score += 5
            else:
                print(f" Wrong! The correct answer was {quiz.correct_choice}.")
                self.streak = 0

            time.sleep(1.2)  # short pause for readability
            print()

        self._show_results()

    def _show_results(self):
        print("\n Quiz Over!")
        print(f" Correct Answers: {self.correct_count}/{self.num_questions}")
        print(f" Final Score: {self.score}\n")
