'''
The backend for the double trouble game.
'''

# Put any global variables your implementation needs here
pile = []

def flip_card(card_obj):
    '''
    Takes in a card_obj which is a python dictionary consistsing of two keys:
     suit: Either "Hearts", "Spades", "Diamonds", or "Clubs"
     number: '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K'

    E.G. {"suit": "Hearts", "number": "5"}

    This card is then added to the pile.

    If the card already exists in the pile, it will not be added.
    '''
    global pile
    # check if card exists
    if not card_obj in pile:
        pile.append(card_obj)

def is_double_trouble():
    '''
    Returns true if the last two cards were the same number. False otherwise.
    If this function is called whilst true, the pile is reset to empty.
    '''
    global pile
    if len(pile) <= 1:
        return False
    if pile[-1]['number'] == pile[-2]['number']:
        clear()
        return True
    return False

def is_trouble_double():
    '''
    Returns true if the last four cards had the same suit. False otherwise.
    If this function is called whilst true, the pile is reset to empty.
    '''
    global pile
    if len(pile) <= 3:
        return False
    if pile[-1]['suit'] == pile[-2]['suit'] and pile[-2]['suit'] == pile[-3]['suit'] and pile[-3]['suit'] == pile[-4]['suit']:
        clear()
        return True
    return False

def is_empty():
    '''
    Returns a boolean that is true if the pile of cards is empty, false if it is not empty
    '''
    global pile
    if pile == []:
        return True
    return False

def clear():
    '''
    Clears the pile and resets the game
    '''
    global pile
    pile = []