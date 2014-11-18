import os
import re
import sys
import collections

from card import *
from player import *
from rules import *

def extract_skat(rule_info, players):
    """
    Extracts the skat from the rule information.
    """
    pattern = re.compile(r"\((\d), ([cshd]+), ([a-zA-Z0-9 ]+)\)")
    results = pattern.match(rule_info).groups()
    
    # Find declarer
    declarer = players[int(results[0])]
    
    # Inflate declarer's final hand
    card_abbrevs = results[2].split()
    hand = []
    for abbrev in card_abbrevs:
        hand.append(Card.from_abbrev(abbrev))

    # Extract skat and give it to the declarer
    full_deck = Card.get_deck()
    cards_dealt = []
    for player in players.values():
        cards_dealt.extend(player.hand)
    skat = set(full_deck) - set(cards_dealt)
    declarer.cards_won.extend(skat)
    
    # Fix declarer's hand
    declarer.hand = hand

def extract_round(round_info):
    """
    This method extracts a round of gameplay from a string
    description and returns a list of tuples like so:
    [(pid, card), (pid, card), (pid, card)]
    """
    pattern = re.compile(r"\(([0-9]+), ([cshd07891QKBA]+)\)")
    results = re.findall(pattern, round_info)
    
    Play = collections.namedtuple('Play', ['pid', 'card'])
    plays = []
    for result in results:
        play = Play(pid = int(result[0]), card = Card.from_abbrev(result[1]))
        plays.append(play)
    return plays

def process_round(plays, suit_file, rank_file, players, rules):
    """
    This method should process a round of gameplay and
    generate features where possible. It should write to
    the given file 'feature-file'
    """
    # Loop over all plays
    for i in range(0, 3):
        
        # Get the current play
        play = plays[i]
        
        # Get the player who made the play
        player = players[play.pid]
        
        if play.pid != rules.declarer_id:   
            # Have the player examine the state of the game
            # before their play and export a tuple of features.
            # If the player did not have to make a decision,
            # 'examine' will return 'None' instead.
            s_features = player.examine_suit(plays[0:i], play.card, rules)
            r_features = player.examine_rank(plays[0:i], play.card, rules)
            
            # Log the features, if it exists
            if s_features:
                suit_file.write(str(s_features)[1:-1] + "\n")
            if r_features:
                rank_file.write(str(r_features)[1:-1] + "\n")
            
        # Remove played card from player's hand
        player.hand.remove(play.card)
        
def process_log_file(log_file_path, suit_file_path, rank_file_path):
    """
    Processes the given log file and writes feature vectors
    from that game out to the given feature file.
    """
    # Open log file
    log_file = open(log_file_path, "r")
        
    # Open suit feature set file
    if not suit_file_path:
        suit_file_path = "feature/suit/" + os.path.basename(log_file_path)
    suit_file = open(suit_file_path, "w")
    
    # Open rank feature set file
    if not rank_file_path:
        rank_file_path = "feature/rank/" + os.path.basename(log_file_path)
    rank_file = open(rank_file_path, "w")
    
    try:
        # Read player info (Lines 1-3)
        players = {}
        for i in range(0, 3):
            player_info = log_file.readline()
            player = Player.from_str(player_info)
            players[player.pid] = player
        
        # Read game rules (Line 4)
        rule_info = log_file.readline()
        rules = BaseRules.from_str(rule_info)
    
        # Extract skat and fix the hand of
        # whoever's playing
        extract_skat(rule_info, players)
    
        # Read gameplay (Lines 5-14)
        for i in range(0, 10):
            round_info = log_file.readline()
            plays = extract_round(round_info)
            process_round(plays, suit_file, rank_file, players, rules)
        
            # Update game state
            winning_play = rules.winner(plays)
            winning_player = players[winning_play.pid]
            winning_player.cards_won.extend([play.card for play in plays])
            for player in players.values():
                player.cards_seen.extend([play.card for play in plays])
        
        # Close feature files
        print("Processed file: " + log_file_path)
        suit_file.close()
        rank_file.close()
        
    # Error? Delete feature file
    except Exception as e:
        print(e)
        print("Error processing file: " + os.path.basename(log_file_path))
        try:
            os.remove(suit_file_path)
            os.remove(rank_file_path)
        except:
            pass
    
    # Close log file
    log_file.close()

def main(argv):
    """
    Parses a game log and and spits out feature vectors for player 
    decisions. The game log format is as follows:
    
    - Lines 1-3: Lists players and hands
      (player ID, player name, player hand)
    
    - Line 4: Lists the teams and rules
      (ID of whoever is playing, trump suit, player hand post-skat)
    
    - Line 5-14: Lists rounds
      [(player ID, card), (player ID, card), (player ID, card),]
    """
    
    # One argument - interpret as command to read all
    # files under log/ directory and write feature vector
    # to files under feature/ directory
    if len(argv) == 1:
        for file_name in os.listdir("log"):
            process_log_file("log/" + file_name, None, None)
                
    # Two arguments - interpret as command to read a
    # specific log file and write feature vectors
    # to a specific feature file
    elif len(argv) == 4:
        process_log_file(argv[1], argv[2], argv[3])
    
    return 0;

if __name__ == "__main__":
    sys.exit(main(sys.argv))
