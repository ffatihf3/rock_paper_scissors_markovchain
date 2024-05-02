from tabulate import tabulate
from enum import Enum
import numpy as np

class MarkovChain:

    class rps(Enum):
        ROCK = 0
        PAPER = 1
        SCISSORS = 2

    game_rules = {
        rps.SCISSORS: rps.ROCK,
        rps.ROCK: rps.PAPER,
        rps.PAPER: rps.SCISSORS
    }

    def __init__(self, target_score):
        self.target_score = target_score

    def start_new_game(self):
        self.match_count = 0
        self.current_score = 0
        self.initial_matrix = self.init_markov_model()
        self.round_results = [['Round', 'Hoooman vs Mr.Computer', 'Match Result']]
        self.play_game()
    
    def init_markov_model(self):
        return {
            self.rps.ROCK.name: [1, 1, 1],
            self.rps.SCISSORS.name: [1, 1, 1],
            self.rps.PAPER.name: [1, 1, 1]
        }

    def play_game(self):
        previous_user_input = None
        while -self.target_score < self.current_score < self.target_score:
            previous_user_input = self.play_round(previous_user_input)
        final_result_message = f'\n[Your Score / Your Target]: {self.current_score} / {self.target_score}\nYou ' + ('Win 🏅' if self.target_score == self.current_score else 'Lose 🤡')
        print(tabulate(self.round_results, tablefmt="fancy_grid"))
        print(final_result_message)
        print("Press Enter To Exit..")
        input()
        print("Thank You For Playing With Us! 🗿")
        quit()
    
    def play_round(self, previous_user_input):
        self.match_count += 1
        computer_input = self.handle_computer_input(previous_user_input)
        user_input = self.handle_player_input()

        self.current_score += self.check_round_results(user_input, computer_input)
        self.learn(previous_user_input, user_input)

        user_choice_emoji = self.get_emoji(user_input)
        computer_choice_emoji = self.get_emoji(computer_input)

        round_result = "Win " if self.check_round_results(user_input, computer_input) == 1 else (
            "Lose " if self.check_round_results(user_input, computer_input) == -1 else "Draw "
        )

        self.round_results.append([f'{self.match_count}', f"{user_choice_emoji} - {computer_choice_emoji}", f"{round_result}"])
        print(f"[👨🏻‍💼 / 👾 ]: {user_choice_emoji} - {computer_choice_emoji}\nResult: {round_result}")

        previous_user_input = user_input
        return previous_user_input

    def predict_next_user_input(self, user_input):
        pred_sum = sum(self.initial_matrix[user_input.name])
        probability = [el / pred_sum for el in self.initial_matrix[user_input.name]]
        return np.random.choice(list(self.rps), replace=True, p=probability)

    def learn(self, previous_user_input, user_input):
        if previous_user_input is None:
            return
        self.initial_matrix.get(previous_user_input.name)[user_input.value] += 1

    def check_round_results(self, user_input, computer_input):
        if self.game_rules.get(user_input) == computer_input:
            return -1
        if user_input == computer_input:
            return 0
        return 1

    def handle_player_input(self):
        print_rps_options()
        user_input = input(f'{self.match_count}) Enter your choice (1, 2, or 3): ')
        while user_input not in ['1', '2', '3']:
            print("Invalid entry. Please try again.")
            print_rps_options()
        return self.rps(int(user_input) - 1)

    def handle_computer_input(self, user_input):
        if self.match_count < 1 or user_input is None:
            return np.random.choice(list(self.rps))
        prediction = self.predict_next_user_input(user_input)
        computer_input = self.game_rules[prediction]
        return computer_input
    
    def get_emoji(self, choice):
        if choice == self.rps.ROCK:
            return "👊"
        elif choice == self.rps.PAPER:
            return "✋"
        else:
            return "🖖"

def print_rps_options():
    print("Choose Your Element:")
    print("👊 (1)")
    print("✋ (2)")
    print("🖖 (3)")

if __name__ == "__main__":
    while True:
        target_score_input = input("Enter Target Score: ")
        try:
            target_score = int(target_score_input)
            if target_score > 0:
                break
            else:
                print("The target score must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a positive number.")

    MarkovChain = MarkovChain(target_score)
    MarkovChain.start_new_game()