from hand_evaluation import evaluate_hand_strength
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
from pypokerengine.engine.card import Card

NB_SIMULATION = 1000

def give_advice(player_hand, community_cards, game_stage, opponent_actions):
    hand_strength = evaluate_hand_strength(player_hand, community_cards)
    print(f"Hand Strength: {hand_strength}")  # Debug statement
    winning_percentage = calculate_winning_percentage(player_hand, community_cards)
    print(f"Winning Percentage: {winning_percentage}")  # Debug statement
    opponent_is_bluffing = detect_bluff(opponent_actions)
    print(f"Opponent Bluffing: {opponent_is_bluffing}")  # Debug statement

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
    try:
        # Convert cards to expected format by pypokerengine
        hole_cards = [Card.from_str(card) for card in player_hand]
        community = [Card.from_str(card) for card in community_cards]
        print(f"Hole Cards: {hole_cards}")  # Debug statement
        print(f"Community Cards: {community}")  # Debug statement
        return estimate_hole_card_win_rate(nb_simulation=NB_SIMULATION, nb_player=2, hole_card=hole_cards, community_card=community)
    except Exception as e:
        print(f"Error in calculate_winning_percentage: {e}")  # Debug statement
        return 0

def detect_bluff(opponent_actions):
    # Simplified bluff detection logic: Assume an opponent might be bluffing if they raise often
    raise_count = opponent_actions.count('raise')
    total_actions = len(opponent_actions)
    if total_actions > 0 and (raise_count / total_actions) > 0.5:
        return True
    return False
