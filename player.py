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
        
        