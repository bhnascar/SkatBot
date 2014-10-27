from card import *

class BaseRules:
    """
    This class implements the rules for a basic game. The three
    main parts of gameplay governed by the rules is.
    
    (1) which cards are trumps
    (2) which plays are legal
    (3) which card wins
    
    This class keeps track of trumps and exports the methods
    valid(...) and winner(...) to determine (2) and (3).
    """
    
    def __init__(self, trumps):
        deck = Card.get_deck()
        self.trump_suit = trumps
        
        # Get trumps from the given suit
        trump_suit = {
            "c": Suit.clubs,
            "s": Suit.spades,
            "h": Suit.hearts,
            "d": Suit.diamonds
        }[trumps]
        self.trumps = [card for card in deck if card.suit == trump_suit]

        # Add jacks, which are always trumps
        self.trumps.extend([card for card in deck if card.rank == Rank.jack])
        self.trumps = list(set(self.trumps))

    def __str__(self):
        """
        Returns a string description of this game.
        """
        return self.trump_suit

    def winner(self, plays):
        """ 
        Returns the winner of a sequence of plays.
        
        Plays is a sequence of tuples like so:
        [(player, card), (player, card), (player, card)]
        """
        trumps = [play for play in plays if play[1] in self.trumps]
        
        # If trumps were played, the winner will be one of them
        if len(trumps) > 0:
            winner = trumps[0]
            for i in range(1, len(trumps)):
                winner = trumps[i] if trumps[i][1] > winner[1] else winner
        
        # If trumps were not played...
        else:
            winner = plays[0]
            if plays[1][1] > winner[1] and plays[1][1].suit == winner[1].suit:
                winner = plays[1]
            if plays[2][1] > winner[1] and plays[2][1].suit == winner[1].suit:
                winner = plays[2] 
        return winner

    def valid(self, card, hand, plays):
        """ 
        Returns whether or not a selected card represents a
        valid play, given the player's hand and plays that
        have been made so far.
        """
        if not card or card not in hand:
            return False

        # If no one has played yet, we can do what we want
        if len(plays) == 0:
            return True

        # Do we have to play trumps?
        if plays[0][1] in self.trumps:
            if len(set(hand).intersection(set(self.trumps))) != 0:
                return card in self.trumps
            return True;
        
        # Do we have to play a suit?
        # Yes, unless we don't have cards of that suit beside
        # a Jack, which is trumps
        return ((card.suit == plays[0][1].suit and card.rank != Rank.jack) or
                len([cd for cd in hand if cd.suit == plays[0][1].suit and cd.rank != Rank.jack]) == 0)
