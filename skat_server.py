import os
import sys
import pickle
import socket
import datetime
import traceback

from card import *
from rules import *
from player import *
from globals import *
from networking import *

def accept_players(server_socket, hands, player_args):
    """
    Accepts three players for this game of Skat. Deals out
    their hands. Returns a dictionary that maps player IDs
    to Player objects.
    """
    # Count bots
    if '-b' in player_args:
        index = player_args.index('-b');
        num_bots = max(2, int(player_args[index + 1]))
        mlab.start()
    else:
        num_bots = 0

    # See if bot algorithm has been provided
    suit_algo = None
    rank_algo = None
    if '-sa' in player_args:
        index = player_args.index('-sa');
        suit_algo = player_args[index + 1]
    if '-ra' in player_args:
        index = player_args.index('-ra');
        rank_algo = player_args[index + 1]

    # Accept human players connecting from the Skat client
    # program
    players = {}
    for i in range(0, 3 - num_bots):
        # Create player
        conn, addr = server_socket.accept()
        player = HumanPlayer(i + 1, hands[i], conn)
        players[i + 1] = player
        
        # Log connection
        print(player.name + " connected")
    
    # Add bot players
    for i in range(3 - num_bots, 3):
        players[i + 1] = BotPlayer(i + 1, hands[i], "Bot", 
                                   suit_algo = suit_algo,
                                   rank_algo = rank_algo)
    return players
    
def decide_declarer(players):
    """
    Determine who will declare the game. Right now this has
    to be decided verbally and each player will have to send
    their response through the client program. The declarer
    is simply whoever responds "y" (yes).
    """
    declarer = None
    for player in players.values():
        response = player.get_bet()
        declarer = player if response == "y" else declarer
    return declarer

def decide_game(declarer, skat):
    """
    Prompts the declarer to decide what game to play. Sends
    the skat to the declarer and receives back the cards
    to hide and the trump suit. Returns a Rules object
    indicating the game to play.
    """
    declarer.hide_cards(skat)
    return declarer.get_rules()

def open_log_file(file_args):
    """
    Opens a log file according to the given file arguments.
    Returns the opened file.

    Arguments are:
    'd' - Use "debug.txt" in the project root directory
    'l [folder]' - Write to a date-named file in the given 
                   folder
    Nothing (default) - Write to a date-named file in the
                        log/ directory
    ________________________________________________________

    The game file format is as follows:

    Lines 1-3: Lists players and hands
    (player ID, player name, player hand)

    Line 4: Lists the teams and rules
    (ID of whoever is playing, trump suit, player hand post-skat)

    Line 5-14: Lists rounds
    [(player ID, card), (player ID, card), (player ID, card),]
    """
    # Use debug file in root directory
    if '-d' in file_args:
        file = open("debug.txt", "w")

    # Write a new file in the user-given directory
    elif '-l' in file_args:
        index = file_args.index('-l');
        log_folder = str(file_args[index + 1])
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        file = open(log_folder + "/" + time + ".txt", "a")

    # Write a new file in the default log directory
    else:
        time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        file = open("log/" + time + ".txt", "a")

    return file

def main(argv):
    """
    Main function...

    Arguments are:
    Folder arguments - see open_log_file
    'b [number]' - Play with a given number of bots
    """

    # Open log file
    file = open_log_file(argv)

    # Generate hands
    deck = Card.shuffle_deck(Card.get_deck())
    hands = [sorted(deck[0:10]), sorted(deck[10:20]), sorted(deck[20:30])]
    skat = deck[30:32]
    
    # Wait for incoming connections from three players
    print("Waiting for players to connect...")
    server_socket = open_socket(50007)
    
    # Accept players
    players = accept_players(server_socket, hands, argv)
    conns = [player.conn for player in players.values() if isinstance(player, HumanPlayer)]
    for player in players.values():
        file.write("(%d, %s, %s)\n" % 
                    (player.pid, player.name, Card.hand_to_repr(player.hand)))
    
    # Who's playing?
    declarer = decide_declarer(players)
    if not declarer:
        file.close()
        server_socket.close()
        mlab.stop()
        return 1
    broadcast_str(conns, declarer.name + " is playing!", log = True)
    
    # What are we playing?
    rules = decide_game(declarer, skat)
    announce = "\n" + declarer.name + " is playing " + str(rules) + "\n"
    broadcast_str(conns, announce, log = True)
    broadcast_msg(conns, pickle.dumps(rules))

    # Log the game parameters
    file.write("(%d, %s, %s)\n" % 
                (declarer.pid, str(rules), Card.hand_to_repr(declarer.hand)))
        
    # Play 10 rounds
    pid = 1
    for r in range(0, 10):
        
        # List of plays so far. It should be in the format
        # [(pid, card), (pid, card), (pid, card)]
        plays = []
        for i in range(0, 3):
            
            # Make play
            for player in players.values():
                if player == players[pid]:
                    card = player.get_play(plays, rules)
                elif isinstance(player, HumanPlayer):
                    announce = "Waiting for " + players[pid].name + " to play..."
                    send_str(player.conn, announce)
                    
            # Receive play
            plays.append(Play(pid = pid, card = card))
            
            # Broadcast state of round
            broadcast_str(conns, players[pid].name + " played ", log = True)
            broadcast_msg(conns, pickle.dumps(card))
            
            # Choose next player
            pid = (pid + 1) if (pid + 1) < 4 else 1

        # Who won the round?
        winning_play = rules.winning_play(plays)
        winner = players[winning_play.pid]
        announce = winner.name + " won the round!\n"
        broadcast_str(conns, announce, log = True)
        
        # Next person to start is the winner of this round
        winner.cards_won.extend([play.card for play in plays])
        pid = winner.pid
        
        # Update cards seen
        for player in players.values():
	        if isinstance(player, BotPlayer):
		        player.cards_seen.extend([play.card for play in plays])
        
        # Log round
        file.write("[")
        for i in range(0, len(plays)):
            play = plays[i]
            file.write("(%d, %s)" % (play.pid, repr(play.card)))
            if i != len(plays) - 1:
                file.write(", ")
        file.write("]\n")
        file.flush()

    # Print points won
    for player in players.values():
        points = rules.count_points(player.cards_won)
        announce = player.name + " won " + str(points) + " points"
        broadcast_str(conns, announce, log = True)

    # Finish
    file.close()
    server_socket.close()
    mlab.stop()

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception:
        # Always stop the Matlab server, especially if we crash
        traceback.print_exc(file = sys.stdout)
        mlab.stop()
