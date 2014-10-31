import sys

from card import *
from player import *


def process_round(round_info, feature_file, players, rules):
    """
    This method should process a round of gameplay and
    generate features where possible.
    """
    # TODO: implement
    pass

def process_rules(rule_info):
    """
    This method returns a Rules object inflated from the
    rule_info string read from the log file.
    """
    # TODO: implement
    pass

def process_player(player_info):
    """
    This method returns a player object inflated
    from the player_info string read from the log file.
    """
    return Player.from_str(player_info)

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
    if len(argv) < 3:
        print "Usage: python3 feature_extractor.py [log file] [output file]"
        return 0
        
    # Open feature set file
    file = open(argv(2), "w")
    
    # Read player info
    players = {}
    for i in range(0, 3):
        player_info = file.readLine()
        player = process_player(player_info)
        players[player.pid] = player
        
    # Read game rules
    rule_info = file.readLine()
    rules = process_rules(rule_info)
    
    # Read gameplay
    for i in range(0, 10):
        round_info = file.readLine()
        process_round(round_info, file, players, rules)
        
    # Close feature set file
    file.close()
    
    return 0;

if __name__ == "__main__":
    sys.exit(main(sys.argv))
