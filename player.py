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

        # Has my opponent run out of a suit?
        self.diff_opp = [0, 0, 0, 0]

        # Has my friend run out of a suit?
        self.diff_frd = [0, 0, 0, 0]
        
    def __str__(self):
        """
        Returns a string representation of this player.
        """
        return "(%d, %s, %s)\n" % (self.pid, self.name, Card.hand_to_str(self.hand))
        
    def __repr__(self):
        return self.__str__()   
        
    def winning_card(self, cards):
        """
        Given an array of cards, return the winning card
        """
        if len(cards) == 0:
            return None

        winning = cards[0]
        for i in range(0, len(cards)):
            if cards[i] > winning:
                winning = cards[i]
        return winning
    
    def encode_played_card(self, played_card):
        """
        Encodes the rank of the played card according to
        the format expected by the feature vector.
        """
        output = {
            Rank.seven: 0,
            Rank.eight: 1,
            Rank.nine : 2,
            Rank.queen: 3,
            Rank.king : 4,
            Rank.ten  : 5,
            Rank.ace  : 6,
            Rank.jack : 7
        }[played_card.rank]
        
        if output == 7:
            output= {
                Suit.diamonds: 7,
                Suit.hearts  : 8,
                Suit.spades  : 9,
                Suit.clubs   : 10
            }[played_card.suit]
            
        return output
       
    def examine_suit(self, previous_plays, played_card, rules):
        """
        This method gets called right before this player plays
        a card. 'previous_plays' is a list containing tuples of
        (player, card) pairs representing plays made so 
        far in the round. 'rules' is a BaseRules
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
        # Skip plays where no suit decision was necessary
        if len(previous_plays) > 0:
            # First person played trumps -> we have trumps
            if previous_plays[0].card in rules.trumps and rules.count_trumps(self.hand) > 0:
                return None
            # First person played a suit -> we have cards of that suit
            elif rules.count_suit(previous_plays[0].card.suit, self.hand) > 0:
                return None
        # Only one legal move
        if len([card for card in self.hand 
                if rules.valid(card, self.hand, previous_plays)]) < 2:
            return None

        # Rotate suits so that the trump suit is at
        # the beginning of the list
        suits = [Suit.clubs, Suit.spades, Suit.hearts, Suit.diamonds]
        i = suits.index(rules.trump_suit)        
        suits = suits[i:] + suits[:i]
        
        # Count number of plays made so far in this round
        n_plays = len(previous_plays)
        
        # Count number of cards of each suit, on hand
        n_s1 = rules.count_trumps(self.hand)
        n_s2 = rules.count_suit(suits[1], self.hand)
        n_s3 = rules.count_suit(suits[2], self.hand)
        n_s4 = rules.count_suit(suits[3], self.hand)
                       
        # Find remaining cards in the game
        cur_deck = list(set(self.reference_deck) - set(self.cards_seen))
        for play in previous_plays:
            cur_deck.remove(play.card);

        # Separate remaining cards by suit
        cur_trumps = [card for card in cur_deck if card in rules.trumps] 
        cur_suit1 = cur_trumps
        cur_suit2 = [cd for cd in cur_deck
                     if cd.suit == suits[1] 
                     and cd not in cur_trumps]
        cur_suit3 = [cd for cd in cur_deck 
                     if cd.suit == suits[2] 
                     and cd not in cur_trumps]
        cur_suit4 = [cd for cd in cur_deck 
                     if cd.suit == suits[3] 
                     and cd not in cur_trumps]
                     
        # Count remaining cards (and not in hand) by suit
        n_remain = [len(cur_suit1) - n_s1, 
                    len(cur_suit2) - n_s2, 
                    len(cur_suit3) - n_s3, 
                    len(cur_suit4) - n_s4]
              
        # Determine if player has winning card in each suit
        winning_cards = [self.winning_card(cur_suit1),
                         self.winning_card(cur_suit2),
                         self.winning_card(cur_suit3),
                         self.winning_card(cur_suit4)]
        has_winning = [int(cd in self.hand) for cd in winning_cards];
        
        # Find opponent id
        id_opp = rules.declarer_id
        
        # Find friend id
        id_frd = 6 - self.pid - rules.declarer_id
        
        # Has my opponent or friend run out of a suit?
        if n_plays > 0:
            start_suit = previous_plays[0].card.suit
            for play in previous_plays:
                if play.card.suit != start_suit:
                    if play.pid == id_opp:
                        self.diff_opp[suits.index(start_suit)] = 1
                    elif play.pid == id_frd:
                        self.diff_frd[suits.index(start_suit)] = 1

        # Am I playing first?
        first = int(len(previous_plays) == 0)

        # How many points are on table?
        pts_on_table = sum([int(play.card) for play in previous_plays])
 
        # Has opponent played?
        played_opp = int(any(play.pid == id_opp for play in previous_plays))
        played_frd = int(any(play.pid == id_frd for play in previous_plays))
       
        # Is my team winning?
        winner = rules.winner(previous_plays)
        is_winning = int(winner.pid == id_frd) if winner else 0

        # Do I have "big" points (A or 10) in each suit?
        big_pts = [0, 0, 0, 0]
        for card in self.hand:
            if int(card) >= 10:
                big_pts[suits.index(card.suit)] = 1                                           
        # Find suit of played card (output)
        if played_card.rank == Rank.jack:
            played_suit = suits.index(rules.trump_suit)
        else:
            played_suit = suits.index(played_card.suit);
        
        # Return feature tuple
        return (played_suit,
                n_s1,
                n_s2,
                n_s3,
                n_s4,
                n_remain[0],
                n_remain[1],
                n_remain[2],
                n_remain[3],
                has_winning[0],
                has_winning[1],
                has_winning[2],
                has_winning[3],
                self.diff_opp[0],
                self.diff_opp[1],
                self.diff_opp[2],
                self.diff_opp[3],
                self.diff_frd[0],
                self.diff_frd[1],
                self.diff_frd[2],
                self.diff_frd[3],               
                first,
                pts_on_table,
                played_opp,
                played_frd,
                is_winning,
                big_pts[0],
                big_pts[1],
                big_pts[2],
                big_pts[3])
                
    def examine_rank(self, previous_plays, played_card, rules):
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

        suit = played_card.suit
 
        # Count number of plays made so far in this round
        n_plays = len(previous_plays)
       
        # Rotate suits so that the trump suit is at
        # the beginning of the list
        suits = [Suit.clubs, Suit.spades, Suit.hearts, Suit.diamonds];
        i = suits.index(rules.trump_suit)        
        suits = suits[i:] + suits[:i]

        # Find opponent id
        id_opp = rules.declarer_id
        
        # Find friend id
        id_frd = 6 - self.pid - rules.declarer_id
        
        # Has my opponent or friend run out of a suit?
        if n_plays > 0:
            start_suit = previous_plays[0].card.suit
            for play in previous_plays:
                if play.card.suit != start_suit:
                    if play.pid == id_opp:
                        self.diff_opp[suits.index(start_suit)] = 1
                    elif play.pid == id_frd:
                        self.diff_frd[suits.index(start_suit)] = 1

        # Am I playing first?
        first = int(len(previous_plays) == 0)

        # How many points are on table?
        pts_on_table = sum([int(play.card) for play in previous_plays]);
 
        # Has opponent played?
        played_opp = 0
        played_frd = 0
        opp_card = None
        for play in previous_plays:
            if play.pid == id_opp:
                played_opp = 1
                opp_card = play.card
            elif play.pid == id_frd:
                played_frd = 1
              
        # Is my team winning?
        winner = rules.winner(previous_plays);
        is_winning = int(winner.pid == id_frd) if winner else 0

         # Has my opponent or friend run out of a suit?
        if n_plays > 0:
            start_suit = previous_plays[0].card.suit
            for play in previous_plays:
                if play.card.suit != start_suit:
                    if play.pid == id_opp:
                        self.diff_opp[suits.index(start_suit)] = 1
                    elif play.pid == id_frd:
                        self.diff_frd[suits.index(start_suit)] = 1
                        
        # Find remaining cards in the game
        cur_deck = [card for card in self.reference_deck 
                    if (card not in self.cards_seen) 
                    and (card not in self.hand)]  
        cur_deck_hand = [card for card in self.reference_deck
                         if (card not in self.cards_seen)]
        for play in previous_plays:
            cur_deck.remove(play.card)
            cur_deck_hand.remove(play.card)
        
        # Have this card?
        cur_trumps = [card for card in self.reference_deck 
                      if card in rules.trumps] 
        full_cards = [cd for cd in self.reference_deck 
                      if cd.suit == suits[suits.index(suit)] 
                      and cd not in cur_trumps]
        cur_cards = None
        suit_len = 7
        if suit == rules.trump_suit:
            full_cards = sorted(cur_trumps)
            cur_cards = [cd for cd in cur_deck_hand
                         if cd in rules.trumps]
            suit_len = 11
        else:
            cur_cards = [cd for cd in cur_deck_hand
                         if cd.suit == suits[suits.index(suit)]
                         and cd not in rules.trumps]
            if len(full_cards) != 7:
                full_cards.extend([0] * 4)
                
        highest_card = self.winning_card(cur_cards)

        # Describes the remaining cards of the suit to play.
        # The indices correspond to the cards in the following way:
        #
        # [0, 1, 2, 3, 4, 5,  6,  7,  8,  9, 10]
        # [7, 8, 9, Q, K, 10, A, dB, hB, sB, cB]
        #
        # (win_card[i] == 1) indicates that card is the winning card
        # (has_card[i] == 1) indicates that the player has this card
        # (beat_opp[i] == 1) indicates that the player has this card
        #                    AND it beats the opponennt's played card
        win_card = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        has_card = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        beat_opp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(0,suit_len):
            if full_cards[i] == highest_card:
                win_card[i] = 1
            if full_cards[i] in self.hand:
                has_card[i] = 1
                if opp_card and full_cards[i] > opp_card:
                    beat_opp[i] = 1 

        # Encode played card
        output = self.encode_played_card(played_card)
        
        return tuple([
            output,
            first, 
            pts_on_table, 
            played_opp, 
            played_frd, 
            is_winning,
            self.diff_opp[suits.index(suit)],
            self.diff_frd[suits.index(suit)],
            len(cur_deck)
        ] + has_card + win_card + beat_opp)
    
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
        
