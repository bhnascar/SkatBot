from card import *

class Player:
    """
    A class to maintain player state information. This includes
    data such as the player's hand, cards won by the player, cards 
    known to that player, etc.
    """
    
    # Player IDs
    pid = 0
    
    def __init__(self, pid, name, hand, conn = None):
        """
        Initializes player information
        """
        self.pid = pid
        self.name = name
        self.hand = hand
        self.conn = conn
        self.cards_won = []
        
    def __str__(self):
        """
        Returns a string representation of this player.
        """
        return "(%d, %s, %s)\n" % (self.pid, self.name, Card.hand_to_str(self.hand))
        
    def __repr__(self):
        return self.__str__()    
    
    @staticmethod
    def from_str(player_info):
        info = parse("(%d, %s, %s)\n")
        
        # Inflate hand
        card_abbrevs = info.split()
        hand = []
        for abbrev in card_abbrevs:
            hand.append(Card.from_abbrev(abbrev))
        
        # Return player
        return Player(info[0], info[1], hand)
        