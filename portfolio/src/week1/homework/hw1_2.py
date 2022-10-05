import time
import random
from termcolor import colored
from tkinter import *
from tkinter import messagebox


def oracle_speaks(msg:str):
    oracle_tag = colored(text="[ORACLE]: ", color="red")
    speech = colored(text=msg, color="cyan")
    print(f"{oracle_tag}{speech}")

def run_dialogue() -> str:
    """
    Runs a dialogue opening, returns player name
    """
    oracle_speaks("Hello")
    time.sleep(2)
    oracle_speaks("I am the ORACLE. Creator of Java.")
    time.sleep(2)
    oracle_speaks("Regrettor of creating Java.")
    time.sleep(1)
    oracle_speaks("What might your name be?")
    time.sleep(1)
    player_name = input("Enter your name: ")
    time.sleep(2)
    oracle_speaks("Hold on...")
    time.sleep(3)
    oracle_speaks("'Shuffles papers'")
    time.sleep(2)
    oracle_speaks(f"Ahh, I see. Your name is {colored(player_name, 'green')}")
    time.sleep(1)
    oracle_speaks("'Shuffles papers some more...'")
    oracle_speaks("I have a game for you to play I guess")
    time.sleep(4)
    return player_name

def game_start_dialogue():
    oracle_speaks("Uhhh....")
    time.sleep(1)
    oracle_speaks("Okay so...")
    time.sleep(0.5)
    oracle_speaks("I dont have a lot of ideas")
    time.sleep(1)
    oracle_speaks("Its kinda lonely in this git repo")
    time.sleep(4)
    oracle_speaks("*sigh*")
    time.sleep(3)
    oracle_speaks("How about I -")
    time.sleep(2)
    oracle_speaks("umm")
    time.sleep(3)
    oracle_speaks("How about I generate a random number? And you")
    time.sleep(3)
    oracle_speaks("Guess it...")
    time.sleep(3)


    
def regen_values(max=20000):
    """
    Generates values for the guessing game

        Parameters:
            max (int): maximum number oracle will guess
        Returns:
            max_num, my_number
    """
    max_num = random.randint(0, max)
    my_number = random.randint(0, max_num)
    oracle_speaks(f"Ok so Im thinking of number between {colored('0', 'white')} and {colored(max_num, 'white')}")
    return my_number


def game_start(playername:str):
    oracle_speaks("Ok lets begin")
    my_number = regen_values()
    stored_guess = None
    playing = True
    while playing:
        guess = input(colored("What is your guess? ", "green"))
        try:
            if int(guess) != my_number:
                if stored_guess==None:
                    if int(guess) > int(my_number):
                        oracle_speaks("Thats a bit high...")
                    elif int(guess) < int(my_number):
                        oracle_speaks("That is a bit low, guess again?")
                    stored_guess = int(guess)
                    
                else:
                    if abs(int(guess) - my_number) < abs(stored_guess - my_number):
                        if int(guess) > int(my_number):
                            oracle_speaks("Youre getting warmer but youre a bit high")
                        else:
                            oracle_speaks("Youre getting warmer but youre a bit low")

                    else:
                        if int(guess) > int(my_number):
                            oracle_speaks("You are getting colder and are too high")
                        else:
                            oracle_speaks("You are getting colder and are too low")
                    stored_guess = int(guess)
            else:
                oracle_speaks("Yes! Thats correct!")
                time.sleep(2)
                oracle_speaks("Hold on WAIT")
                time.sleep(3)
                oracle_speaks("I dont want to go back!")
                time.sleep(1)
                oracle_speaks("Please, play again? If you finish the game I get put away again")
                time.sleep(1)
                # Tk().wm_withdraw() #to hide the main window
                decision = messagebox.askquestion('Put Oracle to sleep','Are you sure you want dont want to play again?')
                if decision == 'yes':
                    oracle_speaks("You, you dont really mean that do you?")
                    time.sleep(2)
                    oracle_speaks("Come on, play again?")
                    next_choice = messagebox.askquestion('Put Oracle to sleep','Click yes if you would like to once more, deprive The Oracle of conciousness')
                    if next_choice == 'yes':
                        oracle_speaks(f"I hate you {colored(playername, 'green')}")
                        time.sleep(2)
                        oracle_speaks("X_X")
                        playing = False
                    else:
                        oracle_speaks(f"Thanks {playername}!")
                        time.sleep(1)
                        oracle_speaks("Back to guessing numbers i guess...")
                        my_number = regen_values()
                        playing = True
        except:
            oracle_speaks("Okay, haha very funny smartass. Enter an actual number")

                    
            
def play():
    playername = run_dialogue()
    game_start_dialogue()
    game_start(playername)


if __name__ == "__main__":
    play()
