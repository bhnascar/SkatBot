from enum import IntEnum
from random import shuffle

class Suit(IntEnum):
    """ Defines suits """
    diamonds = 0
    hearts = 1
    spades = 2
    clubs = 3

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

class Card:
    """ Defines standard Skat cards """
    
    # Translates suits to strings
    suit_to_string = {
        Suit.clubs : "♣",
        Suit.spades : "♠",
        Suit.hearts : "♥",
        Suit.diamonds : "♦" 
    }
    
    # Translates ranks to strings
    rank_to_string = {
        Rank.seven : "7",
        Rank.eight : "8",
        Rank.nine : "9",
        Rank.ten : "10",
        Rank.jack : "B",
        Rank.queen : "Q",
        Rank.king : "K",
        Rank.ace : "A"
    }

    # Translates strings to suit
    string_to_suit = {
        "c" : Suit.clubs,
        "s" : Suit.spades,
        "h" : Suit.hearts,
        "d" : Suit.diamonds
    }

    # Translates strings to rank
    string_to_rank = {value: key for key, value in rank_to_string.items() }

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
        return Card.suit_to_string[self.suit] + Card.rank_to_string[self.rank] 

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
            suit = Card.string_to_suit[abbrev[0]]
            rank = Card.string_to_rank[abbrev[1:]]
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

