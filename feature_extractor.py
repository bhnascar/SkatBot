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

def process_round(plays, feature_file, players, rules):
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
        
        # Have the player examine the state of the game
        # before their play and export a tuple of features.
        # If the player did not have to make a decision,
        # 'examine' will return 'None' instead.
        features = player.examine(plays[0:i], rules)
        
        # Log the features, if it exists
        if features:
            feature_file.write(str(features) + "\n")
            
        # Remove played card from player's hand
        player.hand.remove(play.card)

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
    
    if len(argv) < 3:
        print("Usage: python3 feature_extractor.py [log file] [output file]")
        return 0
        
    # Open log file
    log_file = open(argv[1], "r")
        
    # Open feature set file
    feature_file = open(argv[2], "w")
    
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
        process_round(plays, feature_file, players, rules)
        
        # Update game state
        winning_play = rules.winner(plays)
        winning_player = players[winning_play.pid]
        winning_player.cards_won.extend([play.card for play in plays])
        for player in players.values():
            player.cards_seen.extend([play.card for play in plays])
        
    # Close feature set file
    feature_file.close()
    
    # Close log file
    log_file.close()
    
    return 0;

if __name__ == "__main__":
    sys.exit(main(sys.argv))
