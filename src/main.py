from hand_evaluation import evaluate_hand_strength
from strategy import give_advice

def get_user_input():
    player_hand = input("Enter your hand (e.g., 'As Ks'): ").strip().upper().split()
    community_cards = input("Enter community cards (e.g., '2h 7d Ts'): ").strip().upper().split()
    game_stage = input("Enter game stage (pre-flop, flop, turn, river): ").strip().lower()
    opponent_actions = input("Enter opponent actions (comma separated, e.g., 'call, raise'): ").strip().lower().split(', ')
    return player_hand, community_cards, game_stage, opponent_actions

def main():
    print("Welcome to the Poker Advisor!")
    player_hand, community_cards, game_stage, opponent_actions = get_user_input()
    advice, winning_percentage = give_advice(player_hand, community_cards, game_stage, opponent_actions)
    print(f"Advice: {advice}")
    print(f"Winning Percentage: {winning_percentage * 100:.2f}%")

if __name__ == "__main__":
    main()
