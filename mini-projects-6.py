# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = ""
        for i in range(len(self.cards)):
            ans += self.cards[i].suit + self.cards[i].rank + ' '
        return ans

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        has_Aces = False
        value = 0
        for card in self.cards:
            if card.rank == 'A':
                has_Aces = True
            value += VALUES[card.rank]
        if has_Aces and value + 10 <= 21:
            return value+10
        else:
            return value
    def draw(self, canvas, pos):
        i = 0
        for card in self.cards:
            if i<5:
                card.draw(canvas, [i*100 + pos[0], pos[1]])
                i +=1
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
                
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(-1)
    
    def __str__(self):
        ans = ''
        for i in range(len(self.cards)):
            ans += self.cards[i].suit + self.cards[i].rank + ' '
        return ans



#define event handlers for buttons
def deal():
    global outcome, in_play
    global deck, dealer, player, score
    deck = Deck()
    deck.shuffle()
    dealer = Hand()
    player = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    if in_play:
        outcome = 'you lost. Hit or stand?'
        score -= 1
    else:
        outcome = 'Hit or stand?'
    in_play = True

def hit():
    global outcome, in_play
    global deck, dealer, player, score
    if in_play:
        if player.get_value()<=21:
            player.add_card(deck.deal_card())
        if player.get_value()>21:
            outcome = 'You have busted. New game?'
            in_play = False
            score -= 1
            

def stand():
    global outcome, in_play
    global deck, dealer, player, score
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() < player.get_value() or dealer.get_value()>21:
            outcome = 'you win. New deal?'
            score += 1
        else:
            outcome = 'you lost. New deal?'
            score -= 1
    in_play = False
    
    

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, in_play
    global deck, dealer, player
    dealer.draw(canvas, [100, 200])
    player.draw(canvas, [100, 400])
    canvas.draw_text('Blackjack', (200, 100), 40, 'Pink')
    canvas.draw_text('Dealer', (100, 180), 20, 'Black')
    canvas.draw_text('Player', (100, 380), 20, 'Black')
    canvas.draw_text('Score: '+str(score), (500, 50), 20, 'white')
    canvas.draw_text(outcome, (300, 380), 20, 'white')
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER,
                          CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
