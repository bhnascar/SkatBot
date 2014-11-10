import re

from card import *
from rules import *

class Player:
    """
    A class to maintain player state information. This includes
    data such as the player's hand, cards won by the player, cards 
    known to that player, etc.
    """
    
    def __init__(self, pid, name, hand, conn = None):
        """
        Initializes player information
        """
        # This player's player ID
        self.pid = pid
        
        # This player's name
        self.name = name
        
        # This player's hand
        self.hand = hand
        
        # Cards won by this player so far
        self.cards_won = []
        
        # Cards seen by this player so far
        # (Excludes cards on player's hand and
        # cards in current round)
        self.cards_seen = []
        
        # A reference deck of all Skat cards
        self.reference_deck = Card.get_deck()
        
        # This player's network connection (ignore)
        self.conn = conn
        
    def __str__(self):
        """
        Returns a string representation of this player.
        """
        return "(%d, %s, %s)\n" % (self.pid, self.name, Card.hand_to_str(self.hand))
        
    def __repr__(self):
        return self.__str__()   
        
    def examine_suit(self, previous_plays, rules):
        """
        This method gets called right before this player plays
        a card. 'previous_plays' is a list containing Cards 
        played so far in the round. 'rules' is a BaseRules
        object representing the rules in effect for this game.
        This method should output features for deciding what
        suit to play.
        
        If there is no decision to be made for this play, this
        method should return 'None' (the Python equivalent of
        NULL). If there is a decision to be made, this method
        should return a tuple representing the features for this
        decision. The framework that calls this code will handle 
        writing the tuple to the feature file.
        
        Tuples can be declared like so:
        foo = (1, 2)
        bar = ("hello", 3, True)
        Notice you can stuff different types into them.
        
        Useful information for calculating features:
        - Players keep track of game state information
          See instance variables declared in __init__
        - BaseRules provides a bunch of useful methods
          for game state information related to the game
          rules - for instance, counting the number of
          trumps on a hand.
        """
        if len([card for card in self.hand 
                if rules.valid(card, self.hand, previous_plays)]) < 2:
            return None
            
        # Count number of trumps
        num_trumps = rules.count_trumps(self.hand)
        
        # Count number of cards of each suit
        num_clubs = rules.count_suit(Suit.clubs, self.hand)
        num_spades = rules.count_suit(Suit.spades, self.hand)
        num_hearts = rules.count_suit(Suit.hearts, self.hand)
        num_diamonds = rules.count_suit(Suit.diamonds, self.hand)
        
        # Return feature tuple
        return (num_trumps,
                num_clubs,
                num_spades,
                num_hearts,
                num_diamonds)
                
    def examine_rank(self, suit, previous_plays, rules):
        """
        This method gets called right after examine_suit. 'suit'
        contains the suit chosen by the player. 'previous_plays' 
        is a list containing Cards played so far in the round. 
        'rules' is a BaseRules object representing the rules in 
        effect for this game. This method should output features 
        for deciding what rank card to play.
        
        If there is no decision to be made for this play, this
        method should return 'None'. If there is a decision to be 
        made, this method should return a tuple representing the 
        features for this decision. The framework that calls this 
        code will handle writing the tuple to the feature file.
        """
        if len([card for card in self.hand 
                if rules.valid(card, self.hand, previous_plays)]) < 2:
            return None
        
        # Return feature tuple
        return (0, 0)
    
    @staticmethod
    def from_str(player_info):
        """
        Creates a Player object from a string description from a
        log file.
        """
        pattern = re.compile(r"\((\d), ([a-zA-Z0-9]+), ([a-zA-Z0-9 ]+)\)")
        results = pattern.match(player_info).groups()
        
        # Inflate hand
        card_abbrevs = results[2].split()
        hand = []
        for abbrev in card_abbrevs:
            hand.append(Card.from_abbrev(abbrev))
        
        # Return player
        return Player(int(results[0]), results[1], hand)
        