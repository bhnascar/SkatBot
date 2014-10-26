import sys
import pickle
import socket
import collections

from card import *
from rules import *
from networking import *

# The game file format is as follows:
#
# Lines 1-3: Lists players and hands
# (player ID, player name, player hand)
#
# Line 4: Lists the teams and rules
# (ID of whoever is playing, trump suit, player hand post-skat)
#
# Line 5-14: Lists rounds
# [(player ID, card), (player ID, card), (player ID, card),]

def main(argv):
    
    # Open log file
    file = open("log", "w")
    
    # Generate hands
    deck = Card.shuffle_deck(Card.get_deck())
    h1 = sorted(deck[0:10])
    h2 = sorted(deck[10:20])
    h3 = sorted(deck[20:30])
    skat = deck[30:32]
    player_to_hand = { 1 : h1, 2 : h2, 3 : h3 }
    
    # Wait for incoming connections from three players
    print("Waiting for players to connect...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 50007))
    server_socket.listen(1)
    
    # Accept connections from players
    conn1, addr1 = server_socket.accept()
    p1 = recv_str(conn1) 
    print(p1 + " connected")
    
    conn2, addr2 = server_socket.accept()
    p2 = recv_str(conn2)
    print(p2 + " connected")
    
    conn3, addr3 = server_socket.accept()
    p3 = recv_str(conn3)
    print(p3 + " connected")
    
    # Map player IDs to name and connetions
    Player = collections.namedtuple("Player", ["name", "pid", "hand", "conn"], 
                                    verbose = False, rename = False)
    players = {1 : Player(name = p1, pid = 1, hand = h1, conn = conn1),
               2 : Player(name = p2, pid = 2, hand = h2, conn = conn2),
               3 : Player(name = p3, pid = 3, hand = h3, conn = conn3)}
    for player in players.values():
        file.write("(%d, %s, %s)\n" % 
                    (player.pid, player.name, Card.hand_to_str(player.hand)))
    
    # Deal hands
    print("\nDealing hands...")
    for player in players.values():
        send_msg(player.conn, pickle.dumps(player.hand))
    
    # Who's playing?
    p1_response = recv_str(players[1].conn)
    p2_response = recv_str(players[2].conn)
    p3_response = recv_str(players[3].conn)
    player = players[1] if p1_response == "y" else None
    player = players[2] if p2_response == "y" else player
    player = players[3] if p3_response == "y" else player
    if not player:
        file.close()
        server_socket.close()
        return 1
    print(player.name + " is playing!")
    
    # Send the skat
    print("\nSending skat to " + player.name + "...")
    send_msg(player.conn, pickle.dumps(skat))
    
    # Receive hidden cards from the person playing
    hidden = pickle.loads(recv_msg(player.conn))
    player.hand.extend(skat)
    player.hand.remove(hidden[0])
    player.hand.remove(hidden[1])
    player.hand.sort()
    
    # Receive trumps from the person playing
    trumps = recv_str(player.conn)
    announce = "\n" + player.name + " is playing " + trumps + "\n"
    print(announce)

    # Log the game parameters
    file.write("(%d, %s, %s)\n" % 
                (player.pid, trumps, Card.hand_to_str(player.hand)))

    # Broadcast the rules
    rules = BaseRules(trumps)
    for player in players.values():
        send_str(player.conn, announce)
        send_msg(player.conn, pickle.dumps(rules))
        
    # Play 10 rounds
    pid = 1
    for r in range(0, 10):
        
        # List of plays so far. It should be in the format
        # [(pid, card), (pid, card), ...]
        plays = []
        for i in range(0, 3):
            
            # Make play
            for player in players.values():
                if player == players[pid]:
                    send_str(player.conn, "Your turn")
                    send_msg(player.conn, pickle.dumps(plays))
                else:
                    announce = "Waiting for " + players[pid].name + " to play..."
                    send_str(player.conn, announce)
                    
            # Receive play
            card = pickle.loads(recv_msg(players[pid].conn))
            plays.append((pid, card))
            
            # Broadcast state of round
            announce = players[pid].name + " played " + str(card)
            print(announce)
            for player in players.values():
                send_str(player.conn, announce)
            
            # Choose next player
            pid += 1
            pid = pid if pid < 4 else 1

        # Next person to start is the winner of this round
        pid = (rules.winner(plays))[0]
        announce = players[pid].name + " won the round!\n"
        print(announce)
        for player in players.values():
            send_str(player.conn, announce)
        
        # Log round
        file.write(str(plays) + "\n")
        file.flush()

    # Finish
    file.close()
    server_socket.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
