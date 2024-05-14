from hand_evaluation import evaluate_hand_strength
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

NB_SIMULATION = 1000

def give_advice(player_hand, community_cards, game_stage, opponent_actions):
    hand_strength = evaluate_hand_strength(player_hand, community_cards)
    winning_percentage = calculate_winning_percentage(player_hand, community_cards)
    opponent_is_bluffing = detect_bluff(opponent_actions)

    if game_stage == 'pre-flop':
        advice = pre_flop_strategy(player_hand, opponent_is_bluffing)
    elif game_stage == 'flop':
        advice = post_flop_strategy(hand_strength, winning_percentage, opponent_is_bluffing, opponent_actions)
    elif game_stage == 'turn':
        advice = turn_strategy(hand_strength, winning_percentage, opponent_is_bluffing, opponent_actions)
    elif game_stage == 'river':
        advice = river_strategy(hand_strength, winning_percentage, opponent_is_bluffing, opponent_actions)

    return advice, winning_percentage

def pre_flop_strategy(player_hand, opponent_is_bluffing):
    strong_hands = [('A', 'A'), ('K', 'K'), ('Q', 'Q'), ('J', 'J'), ('A', 'K'), ('A', 'Q')]
    if tuple(player_hand) in strong_hands:
        return "Raise"
    elif opponent_is_bluffing:
        return "Call"
    else:
        return "Fold"

def post_flop_strategy(hand_strength, winning_percentage, opponent_is_bluffing, opponent_actions):
    if hand_strength in ['Straight Flush', 'Four of a Kind', 'Full House']:
        return "Bet/Raise"
    elif winning_percentage > 80:
        return "Bet/Raise"
    elif winning_percentage > 60:
        return "Bet/Call"
    elif winning_percentage > 40:
        if 'raise' in opponent_actions:
            if opponent_is_bluffing:
                return "Call"
            else:
                return "Fold"
        else:
            return "Check/Call"
    else:
        return "Fold"

def turn_strategy(hand_strength, winning_percentage, opponent_is_bluffing, opponent_actions):
    return post_flop_strategy(hand_strength, winning_percentage, opponent_is_bluffing, opponent_actions)

def river_strategy(hand_strength, winning_percentage, opponent_is_bluffing, opponent_actions):
    return post_flop_strategy(hand_strength, winning_percentage, opponent_is_bluffing, opponent_actions)

def calculate_winning_percentage(player_hand, community_cards):
    # Ensure cards are in the correct format
    hole_cards = gen_cards([card.upper() for card in player_hand])
    community = gen_cards([card.upper() for card in community_cards])
    return estimate_hole_card_win_rate(nb_simulation=NB_SIMULATION, nb_player=2, hole_card=hole_cards, community_card=community)

def detect_bluff(opponent_actions):
    # Simplified bluff detection logic: Assume an opponent might be bluffing if they raise often
    raise_count = opponent_actions.count('raise')
    total_actions = len(opponent_actions)
    if total_actions > 0 and (raise_count / total_actions) > 0.5:
        return True
    return False
