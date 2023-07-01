import random

def stats():
    print("\nCurrent Standing => Player 1: ", player_1, "--- Player 2: ", player_2)

def strength_attack(player_to_attack, player_to_be_attacked):
    attacked_dice = input("Which dice would you like to attack (4/6/8/10/12/20): ")
    attacked_dice_value = player_to_be_attacked[attacked_dice]
    print(f'You chose to attack the {attacked_dice} sided dice with value {attacked_dice_value}')
    attacker_dice = input("Which dice are you using to attack (4/6/8/10/12/20): ")
    if player_to_attack[attacker_dice] >= player_to_be_attacked[attacked_dice]:
        player_to_be_attacked[attacked_dice] = "X"
        player_to_attack[attacker_dice] = random.randint(1, int(attacker_dice))
        new_value = player_to_attack[attacker_dice]
        print(attacker_dice,'sided dice has now been rerolled to a', new_value)
        stats()

def mind_attack(player_to_attack, player_to_be_attacked):
    attacked_dice = input("Which dice would you like to attack (4/6/8/10/12/20): ")
    attacked_dice_value = player_to_be_attacked[attacked_dice]
    print(f'You chose to attack the {attacked_dice} sided dice with value {attacked_dice_value}')
    attacker_dices = input("Which dices are you using to attack (4/6/8/10/12/20) (Enter separated by a comma): ").split(',')
    attacker_dices_value = [player_to_attack[num] for num in attacker_dices]
    print('You chose dices', attacker_dices, "with values", attacker_dices_value)
    expression = eval(str(input(f'Enter expression using the values {attacker_dices_value} equal to {attacked_dice_value}: ')))
    if expression == attacked_dice_value:
        player_to_be_attacked[attacked_dice] = "X"
    for dice in attacker_dices:
        player_to_attack[dice] = random.randint(1, int(dice))
        new_value = player_to_attack[dice]
        print(dice,'sided dice has now been rerolled to a', new_value)      
    stats()

#set initial dice values
print("ROLLING RANDOM VALUES")
player_1 = {"4":random.randint(1, 4), "6":random.randint(1, 6), "8":random.randint(1, 8), "10":random.randint(1, 10), "12":random.randint(1, 12), "20":random.randint(1, 20)}
player_2 = {"4":random.randint(1, 4), "6":random.randint(1, 6), "8":random.randint(1, 8), "10":random.randint(1, 10), "12":random.randint(1, 12), "20":random.randint(1, 20)}
print("Player 1: ", player_1, "--- Player 2: ", player_2)

# turn_flag true = player 1 , turn_flag false = player 2
turn_flag = None

#who goes first
player_1_values = sorted(list(player_1.values()))
player_2_values = sorted(list(player_2.values()))
for num in range(len(player_1_values)):
    if player_1_values[num] > player_2_values[num]:
        print('Player 2 goes first and has the penalty card')
        turn_flag = False
        break
    elif player_1_values[num] < player_2_values[num]:
        print('Player 1 goes first and has the penalty card')
        turn_flag = True
        break

while True:
    # turn_flag true = player 1 , turn_flag false = player 2
    if turn_flag == True:
        kind_of_attack = input(f"\nPlayer 1 Turn\nEnter kind of attack (S/M): ")
        if kind_of_attack.upper() == "S":
            strength_attack(player_1,player_2)
        elif kind_of_attack.upper() == "M":
            mind_attack(player_1,player_2)
    else:
        kind_of_attack = input(f"\nPlayer 2 Turn\nEnter kind of attack (S/M): ")
        if kind_of_attack.upper() == "S":
            strength_attack(player_2,player_1)
        elif kind_of_attack.upper() == "M":
            mind_attack(player_2,player_1)
    turn_flag = not(turn_flag)
