# implementation of card game - Memory

import simplegui
import random

cards = range(8)
cards.extend(range(8))
exposed = [n<0 for n in cards]

# helper function to initialize globals
def new_game():
    random.shuffle(cards)
    global state, caed_1, card_2, truns_conuter, exposed
    state = 0
    card_1 = 0
    card_2 = 0
    truns_conuter = 0
    exposed = [n<0 for n in cards]
    label.set_text("Turns = " + str(truns_conuter))
    
# define event handlers
def mouseclick(pos):
    global state, card_1, card_2, truns_conuter
    i = pos[0] / 50

    if exposed[i] == False:
        exposed[i] = True
        if state == 0:
            state = 1
        elif state == 1:
            state = 2
        else:
            state = 1
            if cards[card_1] != cards[card_2]:
                exposed[card_1] = False
                exposed[card_2] = False
        card_1 = card_2
        card_2 = i
        if state == 1:
            truns_conuter += 1
            label.set_text("Turns = " + str(truns_conuter))
                 
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i]:
            canvas.draw_polygon([[i*50, 0], [50+i*50, 0], [50+i*50, 100], [i*50, 100]], 1, 'Yellow', 'Green')
            canvas.draw_text(str(cards[i]), (i*50+10, 70), 60, 'White')
        else:
            canvas.draw_polygon([[i*50, 0], [50+i*50, 0], [50+i*50, 100], [i*50, 100]], 1, 'Yellow', 'Black')
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric