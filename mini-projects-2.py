# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

num_range = 100


# helper function to start and restart the game
def new_game():
    global secret_number
    global num_remaining
    secret_number = random.randrange(0, num_range)
    num_remaining = int(math.ceil(math.log(num_range, 2)))
    print "\nNew game. Range is from 0 to", num_range
    print "Number of remaining guesses is", num_remaining
    
# define event handlers for control panel
def range100():
    global num_range
    num_range = 100
    new_game()

def range1000():
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    global num_remaining
    if guess.isdigit():
        input_number = int(guess)
    else:
        print "\ninvalid input!"
        return
    print "\nGuess was",int(input_number)
    num_remaining -= 1
    print "Number of remaining guesses is", num_remaining

    if input_number > secret_number:
        print "Too high"
    elif input_number < secret_number:
        print "Too Low"
    else:
        print "Correct!"
        new_game()
        
    if num_remaining==0 and input_number != secret_number:
        print "\n :( you lose\n"
        new_game()
    
# create frame
f = simplegui.create_frame('Testing', 200, 200)

# register event handlers for control elements and start frame
f.add_button("Range: 0 - 100", range100, 200)
f.add_button("Range: 0 - 1000", range1000, 200)
f.add_input("input_guess", input_guess, 200)
f.start

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
