from card import *
from rules import *

def hide(cards, hand, skat):
    # Sanity check
    try:
        cards = [Card.from_abbrev(abbrev) for abbrev in cards.split(" ")]
    except:
        return False
    
    # Check card selections
    if len(set(cards) & (set(hand) | set(skat))) != 2:
        return False

    # Perform swap
    hand.extend(skat)
    hand.remove(cards[0])
    hand.remove(cards[1])
    hand.sort()
    return True 

def play_card(player, hand, plays, rules):
    # Print player's hand
    print("\n(Player " + str(player) + ")", end = " ") 
    for card in hand:
        print(card, end = " ")

    # Prompt player to make a choice
    card = Card.from_abbrev(input("\nChoose a card to play:\n"))
    while not rules.valid(card, hand, plays):
        print("You can't play that card!")
        card = Card.from_abbrev(input("Choose a card to play:\n"))

    # Remove and return the played card
    hand.remove(card)
    return card

def main():
    # Generate hand
    deck = Card.shuffle_deck(Card.get_deck())
    
    # Deal cards
    h1 = sorted(deck[0:10])
    h2 = sorted(deck[10:20])
    h3 = sorted(deck[20:30])
    skat = deck[30:32]
    player_to_hand = { 1 : h1, 2 : h2, 3 : h3 }
    
    # Print hands
    print("Player 1: ")
    for card in h1: print(card, end = " ")
    print("\nPlayer 2: ")
    for card in h2: print(card, end = " ")
    print("\nPlayer 3: ")
    for card in h3: print(card, end = " ")
    print()

    # Who plays?
    player = int(input("\nWho is playing? (1, 2, 3)\n"))
    while (player not in range(1, 4)):
        print("Must be 1, 2, or 3!")
        player = int(input("Who is playing? (1, 2, 3)\n"))
    hand = player_to_hand[player]

    # Pick cards
    print("\n(Player " + str(player) + ") The skat was [", end = " ")
    for card in skat: 
        print(card, end = " ")
    cards = input("]\nWhat do you want to hide?\n")
    while not hide(cards, hand, skat):
        print("You must provide two valid cards!")
        cards = input("What do you want to hide?\n")
    print("\n(Player " + str(player) + ") Your hand is now:")
    for card in hand: print(card, end = " ")

    # What's trumps?
    trumps = input("\n\n(Player " + str(player) + ") Which suit is trumps? (c, s, h, d)\n")
    while (trumps not in ["c", "s", "h", "d"]):
        print("Must be c, s, h, or d!")
        trumps = input("Which suit is trumps? (c, s, h, d)\n")
    rules = BaseRules(trumps)

    # Play 10 rounds
    for i in range(0, 10):
        plays = []

        # Make plays in clockwise order
        plays.append((player, play_card(player, hand, plays, rules)))
        player = player + 1 if player < 3 else 1
        hand = player_to_hand[player]

        plays.append((player, play_card(player, hand, plays, rules)))
        player = player + 1 if player < 3 else 1
        hand = player_to_hand[player]

        plays.append((player, play_card(player, hand, plays, rules)))

        # Next person to start is the winner of this round
        player = (rules.winner(plays))[0]
        hand = player_to_hand[player]
        print("\nPlayer " + str(player) + " won the round!")

if __name__ == "main":
    main()

main()
