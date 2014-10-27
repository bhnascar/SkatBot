import sys
import socket
import pickle

from card import *
from rules import *
from networking import *

def hide(cards, hand, skat, server_socket):
    """
    Hides the card the player indicated in the skat.
    """
    # Sanity check
    try:
        cards = [Card.from_abbrev(abbrev) for abbrev in cards.split()]
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
    
    # Send hidden cards to server
    send_msg(server_socket, pickle.dumps(cards))
    
    return True
    
def choose_game(hand, server_socket):
    """
    Prompts the player to examine the skat and choose
    what game to play. Requires a server socket to
    communicate the player's choice to the game
    server.
    """
    # Receive skat
    skat = pickle.loads(recv_msg(server_socket))
    print("\nThe skat was [%s]" % Card.hand_to_str(skat))
        
    # Hide cards
    cards = input("What do you want to hide?\n")
    while not hide(cards.strip(), hand, skat, server_socket):
        print("You must provide two valid cards!")
        cards = input("What do you want to hide?\n")
    print("\nYour hand is now:\n" + Card.hand_to_str(hand))
    
    # What's trumps?
    trumps = input("\nWhich suit should be trumps? (c, s, h, d)\n")
    while (trumps.strip() not in ["c", "s", "h", "d"]):
        print("Must be c, s, h, or d!")
        trumps = input("Which suit should be trumps? (c, s, h, d)\n")
    send_str(server_socket, trumps)

def play_card(hand, plays, rules, server_socket):
    """
    Prompts the player to play a card from their hand.
    Checks the selection against the game rules.
    """
    # Print player's hand
    print("Your hand:", end = " ") 
    for card in hand:
        print(card, end = " ")

    # Prompt player to make a choice
    card = Card.from_abbrev(input("\nChoose a card to play:\n"))
    while not rules.valid(card, hand, plays):
        print("You can't play that card!")
        card = Card.from_abbrev(input("Choose a card to play:\n"))

    # Remove and return the played card
    hand.remove(card)
    
    # Send the played card to the server
    send_msg(server_socket, pickle.dumps(card))

def main(argv):
    if len(argv) != 3:
        print("Usage: python3 [host IP address] [host port]")
        sys.exit(0)
    
    # Connect to server
    host = argv[1]
    port = int(argv[2])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))
    send_str(server_socket, input("\nUsername: ").strip())
    print("Connecting to server...")
    
    # Receive hand
    hand = pickle.loads(recv_msg(server_socket))
    print("\nReceived hand:\n" + Card.hand_to_str(hand))
    
    # Playing?
    playing = input("\nAre you playing? (y/n)\n")
    send_str(server_socket, playing)
    print(recv_str(server_socket))
    
    # If playing...
    if playing == "y":
        choose_game(hand, server_socket)
    
    # Receive game announcement and rules
    print(recv_str(server_socket))
    rules = pickle.loads(recv_msg(server_socket))
    
    # Play 10 rounds
    for i in range(0, 10):
        
        # 3 people play per round
        for i in range(0, 3):
            # Receive message about who's going to play
            announce = recv_str(server_socket)
            print("\n" + announce)
        
            # Are we up?
            if announce == "Your turn":
                plays = pickle.loads(recv_msg(server_socket))
                play_card(hand, plays, rules, server_socket)
        
            # Receive message about play
            print(recv_str(server_socket), end = "")
            print(str(pickle.loads(recv_msg(server_socket))))
        
        # Receive message about who won the round
        print("\n" + recv_str(server_socket))
    
    # Close socket
    server_socket.close()
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))