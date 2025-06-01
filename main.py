import os
import random
import time

# COLORS:
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
RESET = "\033[0m"

# VARIABLES HERE
city_name = random.choice(["Seattle","Boston","New York", "London", "Paris"])  # REPLACE THESE LATER
country_name = random.choice(["USA","France","UK","Brazil","North Korea"])  # REPLACE THESE LATER
coords = [random.choice([-12.125,55.2,92.4]),random.choice([-85.2,-15.6,2.5])]  # REPLACE THESE LATER
# guesses = [["Seattle", "USA", [-13.125,55.2]]]
guesses = []
guess = []
gnum = 0

def past_guesses():
    global guesses
    global country_name
    global coords
    global city_name
    global GREEN
    global YELLOW
    info = []
    # os.system('cls')
    for i in range(len(guesses)):
        for l in range(len(guesses[i])):
            if l == 0:
                if guesses[i][l] == city_name:
                    info.append(GREEN)
                else:
                    info.append(RESET)
            elif l == 1:
                if guesses[i][l] == country_name:
                    info.append(GREEN)
                    # HOW ARE WE GONNA DO COUNTRIES THAT BORDER EACH OTHER?
                else:
                    info.append(RESET)
            elif l == 2:
                if guesses[i][l] == coords:
                    info.append(GREEN)
                elif abs((guesses[i][l][0] + guesses[i][l][1]) - (coords[0] + coords[1])) < 2:
                    info.append(YELLOW)
                else:
                    info.append(RESET)
            # print(guesses[i][l])
            info.append(str(guesses[i][l]))
            info.append(" ")
        info.append("\n")
        info.append(RESET)
    return info

def get_guess():
    global gnum
    global GREEN
    global RESET
    gnum -=-1
    while True:
        guess = input("Guess a city!\n").lower()
        if guess.isalpha() == True:
            break
        else:
            print("Please input the name of a city.")
    if guess == "help":
        pass # MAYBE PUT ALL OF THE POSSIBLE CITIES HERE JUST IN CASE, YOU NEVER KNOW.
    elif guess == city_name.lower():
        print(GREEN+"YOU WIN!!!!!!!! OMG YOU so GOOD"+RESET)
        exit()
    
    # Make guess into a list with index 0 being city, 1 being country, 2 being a list of coordinates.
    for_guess = [guess,"USA",[-12.125,-85.2]]

    return guess

while True:
    guesses.append(guess)
    guess = get_guess()
    print("IMAGE OF", city_name)
    time.sleep(5)
    os.system('cls')
    time.sleep(5)
    print("".join(past_guesses()))
    time.sleep(5)
    # break











