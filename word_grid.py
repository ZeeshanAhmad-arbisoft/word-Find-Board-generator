from math import sqrt
from alphabet import *
import random
import os

HORIZONTAL = 0
VERTICAL = 1
DIAGONAL_DOWN_RIGHT = 2
DIAGONAL_DOWN_LEFT = 3

class WordGrid:
    def __init__(self, width) -> None:
        self.grid = []
        self.width = width
        self.area = width**2
        self.cheated = False

        # creating the grid array
        for col in range(self.area):
            self.grid.append(get_random_letter())

        self.available_spots = []

        # all the available spots that a letter can be placed
        # True: can be placed
        # False: can not be placed
        for spot in range(self.area):
            self.available_spots.append(True)  # all spots are available at the beginning

    # generates the word grid with words
    # if this method is not called before printing the grid, 
    # it will print just some random letters
    def generate_with_words(self, words):
        # check if there are too many letters
        if self.can_generate(words):
            # Ensure at least one diagonal word
            if not self.place_mandatory_diagonal(words):
                print("Error: Could not place the mandatory diagonal word. Exiting.")
                return

            for word in words:
                finded_place_to_enter_word = False
                attempt = 0  # attempts to place word (because there is a chance that it can't find, and then it would be on an infinite loop)
                while not finded_place_to_enter_word and attempt <= 100:

                    # chooses a random direction
                    random_direction = random.choice([HORIZONTAL, VERTICAL, DIAGONAL_DOWN_RIGHT, DIAGONAL_DOWN_LEFT])

                    # random x and y positions of the first letter of the current word
                    random_x = random.randint(0, self.width - 1)
                    random_y = random.randint(0, self.width - 1)

                    # making sure the word won't go out of bounds
                    if random_direction in [HORIZONTAL, DIAGONAL_DOWN_RIGHT] and random_x + len(word) > self.width:
                        random_x -= (random_x + len(word)) - self.width
                    if random_direction in [VERTICAL, DIAGONAL_DOWN_RIGHT, DIAGONAL_DOWN_LEFT] and random_y + len(word) > self.width:
                        random_y -= (random_y + len(word)) - self.width
                    if random_direction == DIAGONAL_DOWN_LEFT and random_x - len(word) < -1:
                        random_x += (len(word) - random_x) - 1

                    # checking if the word can be placed before placing it
                    if self.is_placeable(word, random_x, random_y, random_direction):
                        self.place_word(word, random_x, random_y, random_direction)
                        finded_place_to_enter_word = True

                    # one more attempt...
                    attempt += 1

            # checks if the counter is bigger than the number of attempts
            # this means it could not find a place to place word
            # (this situation is more common when the grid size is smaller)
            if attempt >= 100:
                # asks user if he wants to print the puzzle without some of the words
                i = input("Error: Could not place some words (out of space), print the puzzle anyway? [y/n] ")
                # if the user wants, print the grid
                if i.casefold() == 'y':
                    self.print()
                # otherwise, exit the program
                else:
                    exit()
            # but if it could normally find a place to enter the word, print the grid without errors
            else:
                self.print()

    # sets a word in a position and with a particular direction
    def place_word(self, word, x, y, direction):
        # for every letter on the word
        for l in range(len(word)):
            if direction == HORIZONTAL:
                # place horizontally
                self.grid[x + l + y * self.width] = "\033[32m" + word[l] + "\033[0m" if self.cheated else word[l]
                self.available_spots[x + l + y * self.width] = False  # making the horizontal spot unavailable
            elif direction == VERTICAL:
                # place vertically
                self.grid[x + (y + l) * self.width] = "\033[32m" + word[l] + "\033[0m" if self.cheated else word[l]
                self.available_spots[x + (y + l) * self.width] = False  # making the vertical spot unavailable
            elif direction == DIAGONAL_DOWN_RIGHT:
                # place diagonally down-right
                self.grid[x + l + (y + l) * self.width] = "\033[32m" + word[l] + "\033[0m" if self.cheated else word[l]
                self.available_spots[x + l + (y + l) * self.width] = False  # making the diagonal down-right spot unavailable
            elif direction == DIAGONAL_DOWN_LEFT:
                # place diagonally down-left
                self.grid[x - l + (y + l) * self.width] = "\033[32m" + word[l] + "\033[0m" if self.cheated else word[l]
                self.available_spots[x - l + (y + l) * self.width] = False  # making the diagonal down-left spot unavailable

    # checks if a word can be placed in a position and with a particular direction
    def is_placeable(self, word, x, y, direction):
        # for every letter on the word
        for l in range(len(word)):

            # getting the current letter (cheated or not)
            letter = "\033[32m" + word[l] + "\033[0m" if self.cheated else word[l]

            # CHECKING FOR WORD CROSSING
            # checking if the letter is on the next spot, even if already with a letter from another word placed
            # that way we can make word crossings
            if direction == HORIZONTAL:
                if self.grid[x + l + y * self.width] == letter:
                    # marks the available spot true again (possibly being false before, because of a letter from another word occupying it)
                    # then the current letter on this loop will overlap the same letter from the other word
                    self.available_spots[x + l + y * self.width] = True
            elif direction == VERTICAL:
                if self.grid[x + (y + l) * self.width] == letter:
                    self.available_spots[x + (y + l) * self.width] = True
            elif direction == DIAGONAL_DOWN_RIGHT:
                if self.grid[x + l + (y + l) * self.width] == letter:
                    self.available_spots[x + l + (y + l) * self.width] = True
            elif direction == DIAGONAL_DOWN_LEFT:
                if self.grid[x - l + (y + l) * self.width] == letter:
                    self.available_spots[x - l + (y + l) * self.width] = True

            # at the end, check if the spot is available or not
            spot_available = False
            if direction == HORIZONTAL:
                spot_available = self.available_spots[x + l + y * self.width]
            elif direction == VERTICAL:
                spot_available = self.available_spots[x + (y + l) * self.width]
            elif direction == DIAGONAL_DOWN_RIGHT:
                spot_available = self.available_spots[x + l + (y + l) * self.width]
            elif direction == DIAGONAL_DOWN_LEFT:
                spot_available = self.available_spots[x - l + (y + l) * self.width]

            if spot_available:
                continue
            # if a spot is unavailable, then is not placeable, returns false 
            else:
                return False
        # if the loop finishes without returning false, it means that is placeable, returns true
        return True

    def can_generate(self, words):
        letter_count = 0
        for word in words:
            for letter in word:
                letter_count += 1
                # if there are much more letters than the grid area
                if letter_count > self.area:
                    print("\nToo many words for a little grid!")
                    return False
            if len(word) > self.width:
                print(f"\nYou entered a word too big for the grid size! (Grid size: {self.width})")
                return False
        return True

    # Ensures at least one word is placed diagonally
    def place_mandatory_diagonal(self, words):
        diagonal_directions = [DIAGONAL_DOWN_RIGHT, DIAGONAL_DOWN_LEFT]
        for word in words:
            for direction in diagonal_directions:
                for _ in range(100):  # Attempt 100 times to place the word diagonally
                    random_x = random.randint(0, self.width - 1)
                    random_y = random.randint(0, self.width - 1)

                    # making sure the word won't go out of bounds
                    if direction == DIAGONAL_DOWN_RIGHT and (random_x + len(word) > self.width or random_y + len(word) > self.width):
                        continue
                    if direction == DIAGONAL_DOWN_LEFT and (random_x - len(word) < -1 or random_y + len(word) > self.width):
                        continue

                    # checking if the word can be placed before placing it
                    if self.is_placeable(word, random_x, random_y, direction):
                        self.place_word(word, random_x, random_y, direction)
                        words.remove(word)  # Remove the word from the list once placed
                        return True
        return False  # Return False if no diagonal word could be placed

    # prints the grid on the terminal
    def print(self):
        print("\033[96m┌" + ("─" * (2 * (self.width) + 1)) + "┐\033[0m")  # just a nice little line
        for y in range(self.width):
            print("\033[96m│\033[0m", end=" ")
            for x in range(self.width):
                print(self.grid[x + y * self.width], end=" ")
            print("\033[96m│\033[0m")
        print("\033[96m└" + ("─" * (2 * (self.width) + 1)) + "┘\033[0m")
