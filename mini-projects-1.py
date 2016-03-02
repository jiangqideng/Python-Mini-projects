# Rock-paper-scissors-lizard-Spock template
import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        print 'error: name_to_number(name) saw an invalid name.'
        
def number_to_name(number):
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        print 'error: number_to_name(number) saw an invalid number.'
    
def rpsls(player_choice): 
    print 'Player chooses', player_choice
    player_number = name_to_number(player_choice)
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print 'Computer chooses', comp_choice
    diff = (comp_number - player_number) % 5
    if diff==0:
        print 'Player and computer tie!\n'
    elif diff==1 or diff==2:
        print 'Computer wins!\n'
    elif diff==3 or diff==4:
        print 'Player wins!\n'
    else:
        print 'error in rpsls(player_choice)\n'

# test 
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")



