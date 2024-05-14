from collections import Counter

def evaluate_hand_strength(player_hand, community_cards):
    all_cards = player_hand + community_cards
    ranks = [card[0] for card in all_cards]
    suits = [card[1] for card in all_cards]
    
    rank_counter = Counter(ranks)
    flush = len(set(suits)) == 1
    straight = is_straight(ranks)
    pairs = [rank for rank, count in rank_counter.items() if count == 2]
    trips = [rank for rank, count in rank_counter.items() if count == 3]
    quads = [rank for rank, count in rank_counter.items() if count == 4]
    
    if flush and straight:
        return 'Straight Flush'
    elif quads:
        return 'Four of a Kind'
    elif trips and pairs:
        return 'Full House'
    elif flush:
        return 'Flush'
    elif straight:
        return 'Straight'
    elif trips:
        return 'Three of a Kind'
    elif len(pairs) >= 2:
        return 'Two Pair'
    elif pairs:
        return 'One Pair'
    else:
        return 'High Card'

def is_straight(ranks):
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    sorted_ranks = sorted([rank_values[rank] for rank in ranks])
    for i in range(len(sorted_ranks) - 4):
        if sorted_ranks[i:i+5] == list(range(sorted_ranks[i], sorted_ranks[i]+5)):
            return True
    return False
