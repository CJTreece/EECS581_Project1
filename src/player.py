"""
Name: player.py
Description: This file contains our player class, which holds the players name, board, and ships
             This also contains our functions to place ships, attack opponents, and check if the player is defeated
Authors: Carson Treece, Zachary Craig, Joshua Park
Other Sources: ...
Date Created: 9/9/2024
Last Modified: 9/12/2024
"""

from board import Board
from ship import Ship
import os
import re

class Player:
    def __init__(self, name, shipCount):
        self.name = name
        self.board = Board(shipCount)
        self.shipCount = shipCount

    # function to clear the screen
    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear') # makes a system call to clear the screen.
        print(f"Battleship - {self.name}\n") # print the title of the game every time the screen is cleared

    # check input against regex
    def regexCheck(self, userInput, inputType):
        if((not re.match("^[ABCDEFGHIJabcdefghij]([123456789]|10)$", userInput)) and inputType == "location"): # checks to see if first character is A-J or a-j and second character is 1-10
            return False
        if((not re.match("^[hv]$", userInput)) and inputType == "orientation"): # checks to see if input is h or v
            return False
        return True

    # Place the ships on the board
    def place_ships(self): 
        for ship in range(self.shipCount): # Loop through all ship sizes
            shipLocation = list()  # Initialize the ship location
            shipOrientation = ""  # Initialize the ship orientation
            
            # We need to get the input beefore calling addShip to avoid the error message
            inputValid = False  # Initialize the input variable
            while not inputValid:
                # clear the screen
                self.cls()
                # print the board
                self.board.printBoard()
                # clear location
                shipLocation.clear()

                # get the location of the ship
                print(f"Placing ship of size {ship+1} at location (ex: \"F4\"):", end=" ") # ask for input
                shipLocationString = input() # get the input

                if(self.regexCheck(shipLocationString, "location") is False): # check the input against the regex
                    print("Invalid ship location. Location should be [A-J][1-10].") # print error message
                    input("Please press enter to continue...") # wait for user to press enter
                    continue

                # Append the location to the list
                shipLocation.append(shipLocationString[0])  # add the letter to the location
                shipLocation.append(int(shipLocationString[1:]))  # add the number to the location

                # get the ship's orientation
                print("Placing ship horizontally or vertically (h/v):", end=" ") # ask for input
                shipOrientation = input().lower() # get the input

                if(self.regexCheck(shipOrientation, "orientation") is False): # check the input against the regex
                    print("Invalid ship orientation. Orientation should be h or v.") # print error message
                    input("Please press enter to continue...") # wait for user to press enter
                    continue # restart the loop to get the input again when invalid user input is provided

                # Attempt to place the ship after gathering input
                inputValid = self.board.addShip(ship + 1, shipOrientation, shipLocation)
                if(not inputValid):  # Only display the error if it exists
                    print(f"{self.board.getErr()}")
                    self.board.clearErr()
                    input("Please press enter to continue...")

    # function used to attack the opponent
    def attack_opponent(self, opponent):
        attackLocation = list() # Initialize the attack location
        inputValid = False # Initialize the input variable

        while not inputValid or opponent.board.attack(attackLocation) == False:
            
            self.cls() # clear the screen

            # print the attack board and player's board
            print("Attack board:")
            opponent.board.printAttackBoard() # print the attack board with all previously attacked locations
            print("\n\nYour board:")
            self.board.printBoard() # print the player's board with all ships placed

            attackLocation.clear() # clear location

            # check if there was an error
            if opponent.board.getErr() != "": # if there is an error, print it
                print(f"{opponent.board.getErr()}")
                opponent.board.clearErr() # clear the error after printing it

            # get the attack location
            print("Enter the location to attack (ex: \"F4\"): ", end=" ")
            attackLocationString = input().upper()

            # check input against regex
            if(self.regexCheck(attackLocationString, "location") is False):
                print("Invalid attack location. Location should be [A-J][1-10].")
                input("Please press enter to continue...")
                continue

            # Append the column (letter) to attackLocation
            attackLocation.append(attackLocationString[0])
            attackLocation.append(int(attackLocationString[1:]))

            self.cls() # clear the screen
            
            # If attack is successful, break out of loop
            if opponent.board.attack(attackLocation):
                inputValid = True # Attack is valid
                break
            else:
                inputValid = False # Attack failed, re-enter location

        # show updated attack board
        print("")
        opponent.board.printAttackBoard() # print the updated attack board
        print("Press enter to continue...", end="")
        input() # wait for user to press enter

            
    def is_defeated(self): # need to implement this
        return self.board.checkGameOver() # check if the player is defeated by checking if all ships are sunk