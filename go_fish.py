import random

class Card(object):
    suit_names = ["Diamonds", "Clubs", "Hearts", "Spades"]
    rank_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    faces = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}

    def __init__(self, suit=0, rank=2):
        self.suit = self.suit_names[suit]
        if rank in self.faces:  # self.rank handles printed representation
            self.rank = self.faces[rank]
        else:
            self.rank = rank

        self.rank_num = rank  # To handle winning comparison

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck(object):
    def __init__(self):  # Don't need any input to create a deck of cards
        # This working depends on Card class existing above
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)  # appends in a sorted order

    def __str__(self):
        total = []
        for card in self.cards:
            total.append(card.__str__())
        # shows up in whatever order the cards are in
        return "\n".join(total)  # returns a multi-line string listing each card

    def pop_card(self, i=-1):
        # removes and returns a card from the Deck
        # default is the last card in the Deck
        return self.cards.pop(i)  # this card is no longer in the deck -- taken off

    def shuffle(self):
        random.shuffle(self.cards)

    def replace_card(self, card):
        card_strs = []  # forming an empty list
        for c in self.cards:  # each card in self.cards (the initial list)
            card_strs.append(c.__str__())  # appends the string that represents that card to the empty list
        if card.__str__() not in card_strs:  # if the string representing this card is not in the list already
            self.cards.append(card)  # append it to the list

    def sort_cards(self):
        # Basically, remake the deck in a sorted way
        # This is assuming you cannot have more than the normal 52 cars in a deck
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    # Deal out specified number of cards to number of hands
    # If per_hand is -1, deal all cards in deck, regardless if unequal hands
    def deal(self, num_hands, per_hand):
        list_hands = []

        for x in range(0, num_hands):
            list_hands.append(Hand([]))

        if per_hand != -1:
            for x in range(0, per_hand):
                for hand in list_hands:
                    hand.draw(self)

            return list_hands
        else:
            while len(self.cards) != 0:
                for hand in list_hands:
                    try:
                        hand.draw(self)
                    except:
                        pass

            return list_hands


class Hand(object):
    # create the Hand with an initial set of cards
    # param: a list of cards
    def __init__(self, init_cards):
        self.hand = init_cards

    # add a card to the hand
    # silently fails if the card is already in the hand
    # param: the card to add
    # returns: nothing
    def add_card(self, card):
        if card not in self.hand:
            self.hand.append(card)

        # remove a card from the hand
        # param: the card to remove
        # returns: the card, or None if the card was not in the Hand

    def remove_card(self, card):
        if card in self.hand:
            return self.hand.pop(self.hand.index(card))
        else:
            return None

        # draw a card from a deck and add it to the hand
        # side effect: the deck will be depleted by one card
        # param: the deck from which to draw
        # returns: nothing

    def draw(self, deck):
        self.add_card(deck.pop_card())


def play_human_go_fish():
    # Initialiing components of game
    deck = Deck()
    deck.shuffle()

    hands = deck.deal(2, 7)
    book_player_1 = []
    book_player_2 = []

    # Loop till all books are not formed
    while is_game_ended(book_player_1, book_player_2):
        rank_in_hand_a = list(map(lambda x: x.rank_num, hands[0].hand))
        rank_in_hand_b = list(map(lambda x: x.rank_num, hands[1].hand))
        print("######")
        print("Game Status")
        print("Player A Ranks - " + str(sorted(rank_in_hand_a)))
        print("Player B Ranks - " + str(sorted(rank_in_hand_b)))
        print("player A Book - " + str(sorted(book_player_1)))
        print("player B Book - " + str(sorted(book_player_2)))
        print("######")
        # starting with player A
        # get card which player A wants to ask to B
        player_a_card_rank = ask_player(hands[0].hand, "B")

        # check with player B and get matching rank cards
        matching_rank_player_b_cards = matching_rank(hands[1], player_a_card_rank)

        # if player B had matching rank card add them to player A hand else tell player A to go fish
        if len(matching_rank_player_b_cards) == 0:
            print("Go Fish player A")
            go_fish(hands[0],deck, player_a_card_rank)
        else:
            for card in matching_rank_player_b_cards:
                hands[0].add_card(card)

        # B turn
        player_b_card_rank = ask_player(hands[1].hand, "A")
        # check with player A and get matching rank cards
        matching_rank_player_a_cards = matching_rank(hands[0], player_b_card_rank)

        # if player A had matching rank card add them to player B hand else tell player B to go fish
        if len(matching_rank_player_a_cards) == 0:
            print("Go Fish player B")
            go_fish(hands[1], deck, player_b_card_rank)
        else:
            for card in matching_rank_player_a_cards:
                hands[1].add_card(card)

        # check for books in both players hand
        check_book(hands[0], book_player_1)
        check_book(hands[1], book_player_2)

        # if one player runs out of card, the remaining card in deck should be given to other player and again do book check
        if len(hands[0].hand) == 0 and len(deck.cards) != 0:
            cards_in_deck = len(deck.cards)
            for i in range(cards_in_deck):
                card = deck.pop_card()
                hands[0].add_card(card)
            check_book(hands[0], book_player_1)

        if len(hands[1].hand) == 0 and len(deck.cards) != 0:
            cards_in_deck = len(deck.cards)
            for i in range(cards_in_deck):
                card = deck.pop_card()
                hands[1].add_card(card)
            check_book(hands[1], book_player_2)

    if len(book_player_1) > len(book_player_2):
        print("player A Book - " + str(sorted(book_player_1)))
        print("player B Book - " + str(sorted(book_player_2)))
        print("Player A won")
    elif len(book_player_1) < len(book_player_2):
        print("player A Book - " + str(sorted(book_player_1)))
        print("player B Book - " + str(sorted(book_player_2)))
        print("Player B won")
    else:
        print("player A Book - " + str(sorted(book_player_1)))
        print("player B Book - " + str(sorted(book_player_2)))
        print("Game was tied")

# checks for books in the hand object, removes book formed ranks from hand and appends book to book list passed
def check_book(hand_object, book):
    hand = hand_object.hand
    rank_in_hand = list(map(lambda x: x.rank_num, hand)) # Need to cast the map return value as a list for .count() to work
    for i in range(1,14):
        rank_count = rank_in_hand.count(i)
        if rank_count == 4:
            # book is formed, remove these rank card from hand and add this rank to book list
            print("Book formed for rank - " + str(i))
            card_to_remove = []
            for card in hand_object.hand:
                if card.rank_num == i:
                    card_to_remove.append(card)
            for card in card_to_remove:
                hand_object.remove_card(card)
            book.append(i)

# get one card from deck, if rank matches the rank asked then fish again
def go_fish(hand, deck, rank_to_check):
    # only fish if deck has cards
    if len(deck.cards) > 0:
        card = deck.pop_card()
        # if card is not equal to rank
        if card.rank_num != rank_to_check:
            print("Fished - " + str(card.rank_num))
            hand.add_card(card)
        else:
            # keep fishing till a non matching rank card is drawn from deck
            print("I found a matching rank card, fishing again")
            hand.add_card(card)
            go_fish(hand, deck,rank_to_check)
    else:
        print("Deck is finished")

# return cards which match the passed rank after removing them from the hand
def matching_rank(hand_object, card_rank_to_check):
    # append all matching rank cards to list
    cards_to_remove = []
    for card in hand_object.hand:
        if card.rank_num == card_rank_to_check:
            cards_to_remove.append(card)
    for card in cards_to_remove:
        hand_object.remove_card(card)
    # these removed cards will be given to other player
    return cards_to_remove

# function to get rank of card which one player wants to ask other, he should atleast have one card of rank he is asking
def ask_player(hand, player_to_ask):
    card_a = int(input("What card rank do you want from Player " + player_to_ask + "?"))
    # this card rank should be present in player A hand else ask again
    rank_in_hand = map(lambda x: x.rank_num, hand)
    if card_a not in rank_in_hand:
        print("You should have at least one card of the rank you requested")
        # again ask
        return ask_player(hand, player_to_ask)
    else:
        return card_a


# Game ends when we have made books for all the ranks (1 to 13)
def is_game_ended(book1, book2):
    return len(book1) + len(book2) != 13


def main():
   #play actual game
    play_human_go_fish()


if __name__ == "__main__":
    # execute only if run as a script
    main()
