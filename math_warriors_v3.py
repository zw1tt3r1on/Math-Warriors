import random
import easygui
from tabulate import tabulate
import time
import threading

def stats(stop):
    while True:
        if stop():
            break
        table = tabulate([player_1.values(), player_2.values()], headers=('Dice 4', 'Dice 6', 'Dice 8', 'Dice 10', 'Dice 12', 'Dice 20'), tablefmt="grid")
        easygui.codebox("MATH WARRIORS by John Lester Tan", "MATH WARRIORS by John Lester Tan", table)
        time.sleep(1)

def game_win_checker():
    K = 'X'
    res = all(x == K for x in player_1.values())
    if res == True:
        easygui.msgbox('Player 2 Wins!')
        exit()
    res = all(x == K for x in player_2.values())
    if res == True:
        easygui.msgbox('Player 1 Wins!')
        exit()

def strength_attack(player_to_attack, player_to_be_attacked):
    active_attacker_dices = [str(sides) for sides, dice_value in player_to_attack.items() if dice_value != 'X']
    active_to_be_attacked_dices = [str(sides) for sides, dice_value in player_to_be_attacked.items() if dice_value != 'X']

    attacked_dice = easygui.buttonbox(msg = f"Which sided dice would you like to attack? ", choices = active_to_be_attacked_dices)
    attacked_dice = str(attacked_dice)
    attacked_dice_value = player_to_be_attacked[attacked_dice]
    easygui.msgbox(f'You chose to attack the {attacked_dice} sided dice with value {attacked_dice_value}')

    attacker_dice = easygui.buttonbox(msg = f"Which dice are you using to attack?", choices = active_attacker_dices)
    attacker_dice = str(attacker_dice)

    if player_to_attack[attacker_dice] >= player_to_be_attacked[attacked_dice]:
        value_to_attack = player_to_attack[attacker_dice]
        value_to_be_attacked = player_to_be_attacked[attacked_dice]
        player_to_attack[attacker_dice] = random.randint(1, int(attacker_dice))
        new_value = player_to_attack[attacker_dice]
        easygui.msgbox(msg = f'The {attacked_dice}-sided dice was strength attacked by the {attacker_dice}-sided dice\n\
Since {value_to_attack} is greater than {value_to_be_attacked}\n\
The attacked {attacked_dice}-sided dice is now conquered and replaced with an X\n\
The used dice has now been rerolled')
        player_to_be_attacked[attacked_dice] = "X"

def mind_attack(player_to_attack, player_to_be_attacked):
    active_attacker_dices = [str(sides) for sides, dice_value in player_to_attack.items() if dice_value != 'X']
    active_to_be_attacked_dices = [str(sides) for sides, dice_value in player_to_be_attacked.items() if dice_value != 'X']

    attacked_dice = easygui.buttonbox(msg = f"Which sided dice would you like to attack? ", choices = active_to_be_attacked_dices)
    attacked_dice_value = str(player_to_be_attacked[attacked_dice])
    easygui.msgbox(f'You chose to attack the {attacked_dice} sided dice with value {attacked_dice_value}')

    attacker_dices = easygui.enterbox(msg = f"Which dices are you using to attack?\nAvailable Dices: [{' / '.join(active_attacker_dices)}]\nEnter separated by a comma").split(',')
    attacker_dices_value = [player_to_attack[num] for num in attacker_dices]
    # easygui.msgbox('You chose dices', str(attacker_dices), "with values", str(attacker_dices_value))
    expression = eval(str(easygui.enterbox(f'Enter expression using the values {attacker_dices_value} equal to {attacked_dice_value}: ')))
    if expression == int(attacked_dice_value):
        easygui.msgbox(msg = f'The {attacked_dice}-sided dice was mind attacked by the {attacker_dices}-sided dices\n\
Since {expression} is equal to {attacked_dice_value}\n\
The attacked {attacked_dice}-sided dice is now conquered and replaced with an X\n\
Used dices are now being rerolled')
        player_to_be_attacked[attacked_dice] = "X"

    for dice in attacker_dices:
        player_to_attack[dice] = random.randint(1, int(dice))
        new_value = player_to_attack[dice]
        # print(dice,'sided dice has now been rerolled to a', new_value)


# set initial dice values
player_1 = {"4": random.randint(1, 4), "6": random.randint(1, 6), "8": random.randint(1, 8),
            "10": random.randint(1, 10), "12": random.randint(1, 12), "20": random.randint(1, 20)}
player_2 = {"4": random.randint(1, 4), "6": random.randint(1, 6), "8": random.randint(1, 8),
            "10": random.randint(1, 10), "12": random.randint(1, 12), "20": random.randint(1, 20)}

# turn_flag true = player 1 , turn_flag false = player 2
turn_flag = None

# check who goes first
player_1_values = sorted(list(player_1.values()))
player_2_values = sorted(list(player_2.values()))
for num in range(len(player_1_values)):
    if player_1_values[num] > player_2_values[num]:
        easygui.msgbox('Player 2 goes first and has the penalty card')
        turn_flag = False
        break
    elif player_1_values[num] < player_2_values[num]:
        easygui.msgbox('Player 1 goes first and has the penalty card')
        turn_flag = True
        break

while True:
    stop_threads = False
    update_thread = threading.Thread(target=stats, args =(lambda : stop_threads, ))
    update_thread.start()

    if turn_flag == True:
        kind_of_attack = easygui.buttonbox(msg="\nPlayer 1 Turn\nEnter kind of attack?\n1. Strength Attack\n2. Mind Attack\n3. Pass",
                                           choices=['Strength', 'Mind', 'Pass'])
        if kind_of_attack == "Strength":
            strength_attack(player_1, player_2)
        elif kind_of_attack == "Mind":
            mind_attack(player_1, player_2)
        elif kind_of_attack == "Pass":
            easygui.msgbox("Player 1 passes this turn")
    elif turn_flag == False:
        kind_of_attack = easygui.buttonbox(msg="\nPlayer 2 Turn\nEnter kind of attack?\n1. Strength Attack\n2. Mind Attack\n3. Pass",
                                           choices=['Strength', 'Mind', 'Pass'])
        if kind_of_attack == "Strength":
            strength_attack(player_2, player_1)
        elif kind_of_attack == "Mind":
            mind_attack(player_2, player_1)
        elif kind_of_attack == "Pass":
            easygui.msgbox("Player 2 passes this turn")
    
    stop_threads = True
    update_thread.join()
    # -------- restart the thread on the while true

    game_win_checker()
    turn_flag = not (turn_flag)

