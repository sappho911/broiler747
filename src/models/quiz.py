class Quiz:
    def __init__(self):
        self.id = id
        self.question = None
        self.choice_a = None
        self.choice_b = None
        self.choice_c = None
        self.choice_d = None
        self.correct_choice = None

    def is_correct(self, answer: str) -> bool:
        return answer.strip().lower() == self.correct_choice.strip().lower()
    """
    def calculate_score(self, correct: bool, streak: int) -> int:
        if correct:
            return 10 + (streak * 2)
        return 0
    """