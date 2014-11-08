import re

from card import *

class BaseRules:
    """
    This class implements the rules for a basic game. The three
    main parts of gameplay governed by the rules are:
    
    (1) which cards are trumps
    (2) which plays are legal
    (3) which card wins
    
    This class keeps track of trumps and exports the methods
    valid(...) and winner(...) to determine (2) and (3).
    """
    
    def __init__(self, declarer_id, trumps):
        deck = Card.get_deck()
        self.declarer_id = declarer_id
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

    @staticmethod
    def from_str(rules_info):
        """
        Creates a BaseRules object from a string description
        from a log file.
        """
        pattern = re.compile(r"\((\d), ([cshd]+), ([a-zA-Z0-9 ]+)\)")
        results = pattern.match(rules_info).groups()
        
        # Return rules
        return BaseRules(results[0], results[1])

    def __str__(self):
        """
        Returns a string description of this game.
        """
        return self.trump_suit
        
    def count_points(self, hand):
        """
        Returns the number of points in the given hand
        """
        return reduce(lambda card_1, card_2: int(card_1) + int(card_2), hand)

    def count_suit(self, suit, hand):
        """
        Counts the number of cards with the given suit
        on the given hand, excluding Jacks.
        """
        return len([card for card in hand if (card.suit == suit and
                                              card.rank != Rank.jack)])

    def count_trumps(self, hand):
        """
        Counts the number of trumps on a given hand.
        """
        return len(set(hand).intersection(set(self.trumps)))

    def winner(self, plays):
        """ 
        Returns the winner of a sequence of plays.
        
        Plays is a sequence of tuples like so:
        [(player, card), (player, card), (player, card)]
        """
        if len(plays) == 0:
            return None
        
        trump_plays = [play for play in plays if play[1] in self.trumps]
        
        # If trumps were played, the winner will be one of them
        if len(trump_plays) > 0:
            winner = trump_plays[0]
            for i in range(1, len(trump_plays)):
                trump_play = trump_plays[i]
                winner = trump_play if trump_play[1] > winner[1] else winner
        
        # If trumps were not played...
        else:
            winner = plays[0]
            for i in range(1, len(plays)):
                play = plays[i]
                if play[1] > winner[1] and play[1].suit == winner[1].suit:
                    winner = play
                
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
            
            # If we do have trumps, then the play is valid
            # if it the given card is indeed a trump
            if self.count_trumps(hand) != 0:
                return card in self.trumps
            
            # Otherwise, we don't have trumps => any card
            # on our hand is valid 
            return True;
        
        # Do we have to play a suit?
        # The play is valid if either:
        # (1) We play a card of the starting suit
        # (2) (1) is false but we don't have any more cards
        #     of the starting suit
        return ((card.suit == plays[0][1].suit and card.rank != Rank.jack) or
                self.count_suit(plays[0][1].suit, hand) == 0)
