import os
import json
import time
import random
from word_grid import *
import argparse

def save_to_json(data, folder, filename):
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main(cheated=False, words_file=None, size=8, num_boards=50):
    # Create a folder to save JSON files
    folder_name = "WordFindBoards"
    os.makedirs(folder_name, exist_ok=True)

    for board_num in range(1, num_boards + 1):
        # generating words from file
        words = []
        file1 = open(words_file, 'r')
        lines = file1.readlines()
        file1.close()

        # appending words to array
        for _ in range(8):
            words.append(lines[random.randint(0, len(lines) - 1)].strip())

        # creating the word grid
        grid = WordGrid(size)

        print(f"Generating board {board_num}...")

        grid.cheated = cheated
        grid.generate_with_words(words)

        # Create a data structure to save grid and words
        data = {
            "grid": grid.grid,
            "words": words
        }

        # Adding row and column number with each letter
        rows, cols = grid.width, grid.width
        for i, letter in enumerate(data["grid"]):
            row = i // cols
            col = i % cols
            data["grid"][i] = {
                "letter": letter,
                "row": row,
                "col": col
            }

        # Generate filename with current timestamp
        timestamp = int(time.time())
        filename = f"word_search_{timestamp}_{board_num}.json"

        # Save data to JSON file
        save_to_json(data, folder_name, filename)

    print(f"{num_boards} boards generated and saved in '{folder_name}' folder.")


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(description="Generates word search puzzles")

    # Adding optional arguments
    parser.add_argument("-c", "--cheated", action="store_true", help="Highlight words")
    parser.add_argument("-f", "--file", type=str, default="newwords.txt", help="Path to a custom words file. One word per line.")
    parser.add_argument("-s", "--size", type=int, default=8, help="Sets a custom grid size (Default: 8)")
    parser.add_argument("-n", "--num_boards", type=int, default=50, help="Number of word search boards to generate (Default: 250)")

    # Read arguments from command line
    args = parser.parse_args()

    main(cheated=args.cheated, words_file=args.file, size=args.size, num_boards=args.num_boards)
