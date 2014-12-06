import re
import abc
import pickle
import random

from card import *
from rules import *
from globals import *
from networking import *

class Player:
    """
    An abstract class outlining the methods required of any
    player, human or computer.
    
    Also provides instance variables to maintain player state
    information. This includes the player's hand and cards 
    won by the player so far.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, pid, hand):
        """
        At minimum, a player must be given an ID and a hand
        """
        # The player's ID
        self.pid = pid
        
        # The player's hand
        self.hand = hand
        
        # The player's name
        self.name = "Fish"
        
        # Cards won by this player so far
        self.cards_won = []

    @abc.abstractmethod
    def get_bet(self):
        """
        Retrieves a player's pre-game bet over the network.
        Used to decide if the player gets to declare the game.
        """
        pass
    
    @abc.abstractmethod
    def hide_cards(self, skat):
        """
        If this player is declaring the game, this method lets
        the player pick which cards to hide.
        
        'skat' is a list of cards representing the original skat.
        """
        pass
        
    @abc.abstractmethod
    def get_rules(self):
        """
        If this player is declaring the game, this method should
        return a rules object indicating the suit the player would
        like to play.
        """
        pass
    
    @abc.abstractmethod
    def get_play(self, previous_plays, rules):
        """
        Retrieves a play from over the player given a list of
        previous plays in the round and the rules of the game.
        
        'previous_plays' is a list containing tuples of
        (player, card) pairs representing plays made so 
        far in the round.
        
        'rules' is a BaseRules object (see rules.py).
        """
        pass
        
    def __str__(self):
        """
        Returns a string representation of this player.
        """
        return "(%d, %s, %s)\n" % (self.pid, self.name, 
                                   Card.hand_to_str(self.hand))
                                   
    def __repr__(self):
        return self.__str__()

class HumanPlayer(Player):
    """
    A human Skat player. Connects using the Skat client (see
    skat_client.py) from over the network.
    """
    
    def __init__(self, pid, hand, conn):
        """
        Initializes a human player with an ID and hand.
        Human players additionally require a network
        connection from which the game server will receive
        input.
        """
        super(HumanPlayer, self).__init__(pid, hand)
        
        # This player's connection
        self.conn = conn
        
        # This player's name
        self.name = recv_str(self.conn)
        
        # Send hand to player client
        send_msg(self.conn, pickle.dumps(self.hand))
    
    def get_bet(self):
        """
        Retrieves a player's pre-game bet over the network.
        Used to decide if the player gets to play.
        """
        if not self.conn:
            print("No op!")
            return None
        bet = recv_str(self.conn)
        print("Received " + bet + " from " + self.name)
        return bet
    
    def hide_cards(self, skat):
        """
        If this player is declaring the game, this method lets
        the player pick which cards to hide.
        """
        if not self.conn:
            print("No op!")
            return None
            
        print("\nSending skat to " + self.name + "...")
        send_msg(self.conn, pickle.dumps(skat))
    
        # Receive hidden cards from the player client
        hidden = pickle.loads(recv_msg(self.conn))
        self.hand.extend(skat)
        self.hand.remove(hidden[0])
        self.hand.remove(hidden[1])
        self.hand.sort()
    
        # Add the hidden cards to player's cards won
        self.cards_won.extend(hidden)
        
    def get_rules(self):
        """
        If this player is declaring the game, this method should
        return a rules object indicating the suit the player would
        like to play.
        """
        if not self.conn:
            print("No op!")
            return None
        trumps = recv_str(self.conn)
        rules = BaseRules(self.pid, trumps)
        return rules
    
    def get_play(self, previous_plays, rules):
        """
        Retrieves a card from over the network in a Skat game.
        """
        if not self.conn:
            print("No op!")
            return None
        send_str(self.conn, "Your turn")
        send_msg(self.conn, pickle.dumps(previous_plays))
        card = pickle.loads(recv_msg(self.conn))
        self.hand.remove(card)
        return card
        
class BotPlayer(Player):
    """
    A computer Skat player. Overrides methods expecting user
    input and returns computer-predicted values instead.
    """
    
    def __init__(self, pid, hand, name):
        """
        Initializes a computer player with an ID and hand.
        """
        super(BotPlayer, self).__init__(pid, hand)
        
        self.name = name
        
        # Cards seen by this player so far
        # (Excludes cards on player's hand and
        # cards in current round)
        self.cards_seen = []
        
        # A reference deck of all Skat cards
        self.reference_deck = Card.get_deck()
        
        # Has my opponent run out of a suit?
        self.diff_opp = [0, 0, 0, 0]

        # Has my friend run out of a suit?
        self.diff_frd = [0, 0, 0, 0]
    
    @staticmethod
    def from_str(player_info):
        """
        Creates a BotPlayer object from a string description from a
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
        return BotPlayer(int(results[0]), hand, results[1])
    
    def get_bet(self):
        """
        A computer never plays.
        """
        return 'n'
        
    def hide_cards(self, skat):
        """
        A computer should never play, so it will never need to
        hide cards.
        """
        pass

    def get_rules(self):
        """
        A computer should never play. Returns a dummy value.
        """
        return BaseRules(self.pid, "s")
    
    def get_play(self, previous_plays, rules):
        """
        Generates suit and rank feature vectors and writes it
        to a file (lolz...). Invokes Matlab on the file to generate 
        a prediction and receives the result back from Matlab.
        This is what happens when you have a multi-person project
        and are too lazy to rewrite Matlab stuff with numpy...
        """
        print("lala")
        print("lala")
        valid_cards = [card for card in self.hand 
                       if rules.valid(card, self.hand, previous_plays)]
        card = random.choice(valid_cards)
        self.hand.remove(card)

		# Get suit features
        s_features = self.examine_suit(previous_plays, None, rules)
        if (s_features):
            print("\n" + str(s_features)[1:-1])

            # Talk to Matlab
            args = {}
            for i in range(0, len(s_features)):
                args['arg' + str(i + 1)] = s_features[i]
            print('Foobar')
            res = mlab.run('Matlab/PythonInterface/PredictSuitSoftmax.m', args)
            print('Baz')
            print(res['result'])

		# Get rank features
        r_features = self.examine_rank(previous_plays, None, rules, chosen_suit = card.suit)
        if (r_features):
            print("foo1")
            print(str(r_features)[1:-1])
            print("foo2")

            # Talk to Matlab
            args = {}
            for i in range(0, len(r_features)):
                args['arg' + str(i + 1)] = r_features[i]
            res = mlab.run('Matlab/PythonInterface/PredictRankSVM.m', args)
            print(res['result'])

        return card
    
    def encode_card_rank(self, card):
        """
        Encodes the rank of the given card according to
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
        }[card.rank]
        
        if output == 7:
            output = {
                Suit.diamonds: 7,
                Suit.hearts  : 8,
                Suit.spades  : 9,
                Suit.clubs   : 10
            }[card.suit]
            
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
            
            # First person played trumps and we have trumps
            if (previous_plays[0].card in rules.trumps and 
                rules.count_trumps(self.hand) > 0):
                return None
                
            # First person played a suit and we have cards of that suit
            elif rules.count_suit(previous_plays[0].card.suit, self.hand) > 0:
                return None
            
        # Only one suit left
        # (This also catches the case of only one card left)
        if len(set([card.suit for card in self.hand])) == 1:
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
        winning_cards = [rules.winning_card(cur_suit1),
                         rules.winning_card(cur_suit2),
                         rules.winning_card(cur_suit3),
                         rules.winning_card(cur_suit4)]
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
        winner = rules.winning_play(previous_plays)
        is_winning = int(winner.pid == id_frd) if winner else 0

        # Do I have "big" points (A or 10) in each suit?
        big_pts = [0, 0, 0, 0]
        for card in self.hand:
            if int(card) >= 10:
                big_pts[suits.index(card.suit)] = 1 

        # Find suit of played card (output)
        if not played_card:
            played_suit = 0
        elif played_card.rank == Rank.jack:
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
                
    def examine_rank(self, previous_plays, played_card, rules, chosen_suit = Suit.clubs):
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

        # Determine suit of played_card
        if played_card:
            if played_card in rules.trumps:
                suit = rules.trump_suit
                if rules.count_trumps(self.hand) == 1:
                    return None
            else:
                suit = played_card.suit
                if rules.count_suit(suit, self.hand) == 1:
                    return None
        else:
            suit = chosen_suit
 
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
        winner = rules.winning_play(previous_plays);
        is_winning = int(winner.pid == id_frd) if winner else 0
                        
        # Find remaining cards in the game (including hand)
        cur_deck_hand = [card for card in self.reference_deck
                         if (card not in self.cards_seen)]
        for play in previous_plays:
            cur_deck_hand.remove(play.card)
        
        # What's the highest card of the given suit?
        if played_card in rules.trumps:
            suit_len = 11
            full_cards = rules.trumps
            cur_cards = [cd for cd in cur_deck_hand if cd in rules.trumps]
        else:
            suit_len = 7
            full_cards = [cd for cd in self.reference_deck 
                          if cd.suit == suits[suits.index(suit)] 
                          and cd not in rules.trumps]
            cur_cards = [cd for cd in cur_deck_hand
                         if cd.suit == suits[suits.index(suit)]
                         and cd not in rules.trumps]
            full_cards.extend([0] * 4)
                
        highest_card = rules.winning_card(cur_cards)

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

        # How many cards are left in the game?
        num_cards_left = len([card for card in cur_deck_hand 
                              if card not in self.hand])

        # Encode played card
        if not played_card:
            output = 0
        else:
            output = self.encode_card_rank(played_card)
        
        # Uncomment to debug feature variables
        print("Highest card (" + str(suit) + "): " + str(highest_card))
        print("Previous plays: " + str(previous_plays))
        print("Going first: " + str(first))
        print("Points on table: " + str(pts_on_table))
        print("Has opponent played: " + str(played_opp))
        print("Has friend played: " + str(played_frd))
        print("Is winning: " + str(is_winning))
        print("Hand: " + str(self.hand))
        print("Winning card: (" + str(suit) + ") " + str(win_card))
        print("Has card: (" + str(suit) + ") " + str(has_card))
        print("Beat opp: (" + str(suit) + ") " + str(beat_opp))
        print("Num. cards left: " + str(num_cards_left))
        
        return tuple([
            output,
            first, 
            pts_on_table, 
            played_opp, 
            played_frd, 
            is_winning,
            self.diff_opp[suits.index(suit)],
            self.diff_frd[suits.index(suit)],
            num_cards_left,
        ] + has_card + win_card + beat_opp)
