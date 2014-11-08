import sys
import platform

from enum import IntEnum
from random import shuffle
from functools import reduce

class Suit(IntEnum):
    """ Defines suits """
    diamonds = 0
    hearts = 1
    spades = 2
    clubs = 3
    
    def __str__(self):
        if platform.system() != "Windows" or "idlelib" in sys.modules:
            return {
                "diamonds": "♦",
                "hearts"  : "♥",
                "spades"  : "♠",
                "clubs"   : "♣"
            }[self.name]
        else:
            return {
                "diamonds": chr(4),
                "hearts"  : chr(3),
                "spades"  : chr(6),
                "clubs"   : chr(5)
            }[self.name]
    
    def __repr__(self):
        return {
            "diamonds": "d",
            "hearts"  : "h",
            "spades"  : "s",
            "clubs"   : "c"
        }[self.name]
        
    @classmethod
    def from_str(cls, str):
        return {
            "d": cls.diamonds,
            "h": cls.hearts,
            "s": cls.spades,
            "c": cls.clubs
        }[str]

class Rank(IntEnum):
    """ Defines card ranks """
    seven = 0
    eight = 1
    nine = 2
    queen = 3
    king = 4
    ten = 5
    ace = 6
    jack = 7
    
    def __str__(self):
        return {
            "seven": "7",
            "eight": "8",
            "nine" : "9",
            "queen": "Q",
            "king" : "K",
            "ten"  : "10",
            "ace"  : "A",
            "jack" : "B"
        }[self.name]
    
    def __repr__(self):
        return self.__str__()
        
    def __int__(self):
        return {
            "seven": 0,
            "eight": 0,
            "nine" : 0,
            "queen": 3,
            "king" : 4,
            "ten"  : 10,
            "ace"  : 11,
            "jack" : 2,
        }[self.name]
        
    @classmethod
    def from_str(cls, str):
        return {
            "7" : cls.seven,
            "8" : cls.eight,
            "9" : cls.nine,
            "Q" : cls.queen,
            "K" : cls.king,
            "10": cls.ten,
            "A" : cls.ace,
            "B" : cls.jack
        }[str]
        
class Card:
    """ Defines standard Skat cards """

    def __init__(self, suit, rank):
        """
        Card constructor.
        """
        self.suit = suit
        self.rank = rank    

    def __eq__(self, other):
        """
        Compares two cards for equality.
        """
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank

    def __ne__(self, other):
        """
        Compares two cards for inequality.
        """
        return not __eq__(self, other)

    def __lt__(self, other):
        """
        Defines a general ordering over cards. This is 
        specific to Skat.
        """
        if self.rank == Rank.jack and other.rank == Rank.jack:
            return self.suit < other.suit
        elif self.rank == Rank.jack:
            return False
        elif other.rank == Rank.jack:
            return True
        if self.suit == other.suit:
            return self.rank < other.rank
        return self.suit < other.suit

    def __hash__(self):
        """
        Returns a hash value for the card.
        """
        return 8 * self.suit + self.rank

    def __str__(self):
        """
        Returns a string representation of this card.
        """
        return str(self.suit) + str(self.rank)
        
    def __repr__(self):
        return repr(self.suit) + repr(self.rank)
        
    def __int__(self):
        """
        Returns the points value of this card.
        """
        return int(self.rank)

    # General functions for manipulating a hand or deck,
    # (which are simply lists of Cards). Just using the
    # Card class like a namespace here, because it makes
    # the most sense to stuff these methods here if we're
    # not creating another utility file or some Hand/Deck
    # class

    @staticmethod
    def hand_to_str(hand):
        """
        Turns a hand into a string. The hand should be given
        as a list of cards.
        """
        return " ".join(str(card) for card in hand)
    
    @staticmethod
    def hand_to_repr(hand):
        """
        Turns a hand into a repr. The hand should be given
        as a list of cards.
        """
        return " ".join(repr(card) for card in hand)

    @staticmethod
    def print_hand(hand):
        """
        Prints a hand on one line. The hand should be given
        as a list of cards.
        """
        for card in hand: print(card, end = " ")
        
    @staticmethod
    def from_abbrev(abbrev):
        """
        Returns a card corresponding to an abbreviation.
        The abbreviation should be a two character string
        with the following format.
    
        The first character denotes the suit. It can be one
        of:
        'c' - Clubs
        's' - Spades
        'h' - Hearts
        'd' - Diamonds

        The second character denotes the card rank. It can
        be one of:
        '7' - Seven
        '8' - Eight
        '9' - Nine
        '10' - Ten
        'B' - Jack
        'Q' - Queen
        'K' - King
        'A' - Ace

        Returns none on failure.
        """
        try:
            suit = Suit.from_str(abbrev[0])
            rank = Rank.from_str(abbrev[1:])
        except:
            return None
        return Card(suit, rank)

    @staticmethod
    def get_deck():
        """
        Generates a sorted deck of Skat cards.
        """
        deck = []
        for suit in range(0, 4):
            for rank in range(0, 8):
                deck.append(Card(Suit(suit), Rank(rank)))
        return deck

    @staticmethod
    def shuffle_deck(deck):
        """
        Shuffles a Skat deck.
        """
        assert len(deck) == 32
        for card in deck:
            assert isinstance(card, Card)
        shuffle(deck)
        return deck