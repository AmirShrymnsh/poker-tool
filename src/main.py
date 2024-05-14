class CombinedPokerHandEvaluator:
    def __init__(self):
        self.two_plus_two_evaluator = TwoPlusTwoEvaluator()
        self.cactus_kev_evaluator = CactusKevEvaluator()
        self.henry_lee_evaluator = HenryLeeEvaluator()

    def evaluate_hand(self, hand):
        if len(hand) == 5:
            return self.cactus_kev_evaluator.evaluate_hand(hand)
        elif len(hand) == 7:
            return self.two_plus_two_evaluator.evaluate_hand(hand)
        elif len(hand) in [6, 9]:  # Omaha or other variants
            return self.henry_lee_evaluator.evaluate_hand(hand)
        else:
            raise ValueError("Unsupported hand size or poker variant")


class TwoPlusTwoEvaluator:
    def __init__(self):
        self.hand_ranks = {"AH KH QH JH TH": 10, "AS KS QS JS TS": 10}  # Example entries

    def evaluate_hand(self, hand):
        hand_str = " ".join(sorted([f"{r}{s}" for r, s in hand], key=lambda x: x[0]))  # Sort hand for lookup
        return self.hand_ranks.get(hand_str, 1)  # Default to "High Card" if not found


class CactusKevEvaluator:
    def __init__(self):
        self.flushes = self._init_flushes()
        self.unique5 = self._init_unique5()

    def _init_flushes(self):
        return {31: 9, 7808: 323}

    def _init_unique5(self):
        return {3968: 1601, 47: 7462}

    def evaluate_hand(self, hand):
        suits = [self.get_suit(card) for card in hand]
        values = [self.get_value(card) for card in hand]

        if len(set(suits)) == 1:
            return self.flushes.get(self.compute_flush_hash(values), 1)

        return self.unique5.get(self.compute_non_flush_hash(values), 1)

    def get_suit(self, card):
        return card[1]

    def get_value(self, card):
        value_str_to_int = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return value_str_to_int[card[0]]

    def compute_flush_hash(self, values):
        return sum([1 << value for value in values])

    def compute_non_flush_hash(self, values):
        return sum([1 << value for value in values]) >> 16


class HenryLeeEvaluator:
    def __init__(self):
        self.perfect_hash_table = {"AH KH QH JH TH": 10}

    def evaluate_hand(self, hand):
        hand_str = " ".join(sorted([f"{r}{s}" for r, s in hand], key=lambda x: x[0]))  # Sort hand for lookup
        return self.perfect_hash_table.get(hand_str, 1)  # Default to "High Card" if not found


def get_user_hand():
    hand_input = input("Enter your hand (e.g., 'AH KH'): ")
    hand = []
    for card_str in hand_input.split():
        rank = card_str[0]
        suit = card_str[1]
        hand.append((rank, suit))
    return hand


def get_community_cards():
    community_input = input("Enter community cards (e.g., '2h 7d Ts'): ")
    community = []
    for card_str in community_input.split():
        rank = card_str[0]
        suit = card_str[1]
        community.append((rank, suit))
    return community


def get_game_stage():
    stage = input("Enter game stage (pre-flop, flop, turn, river): ").strip().lower()
    return stage


def get_opponent_actions():
    actions = input("Enter opponent actions (comma separated, e.g., 'call, raise'): ").strip().lower().split(', ')
    return actions


def calculate_winning_percentage(hand, community):
    # Placeholder for calculating winning percentage
    # You can implement your own logic or use an existing library
    return 50.0  # Example fixed winning percentage


def determine_bluffing(actions):
    # Placeholder for determining bluffing based on actions
    # Implement your own logic or use an existing model
    return "True" if "raise" in actions else "False"


def provide_advice(winning_percentage, bluffing):
    if winning_percentage > 70:
        return "Raise"
    elif winning_percentage > 40:
        return "Call"
    else:
        return "Fold"


def main():
    evaluator = CombinedPokerHandEvaluator()
    print("Welcome to the Poker Advisor!")

    user_hand = get_user_hand()
    community_cards = get_community_cards()
    game_stage = get_game_stage()
    opponent_actions = get_opponent_actions()

    if game_stage == 'pre-flop':
        full_hand = user_hand
    else:
        full_hand = user_hand + community_cards

    try:
        hand_strength = evaluator.evaluate_hand(full_hand)
        winning_percentage = calculate_winning_percentage(user_hand, community_cards)
        bluffing = determine_bluffing(opponent_actions)
        advice = provide_advice(winning_percentage, bluffing)

        print(f"Hand Strength: {hand_strength}")
        print(f"Winning Percentage: {winning_percentage}%")
        print(f"Opponent Bluffing: {bluffing}")
        print(f"Advice: {advice}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
