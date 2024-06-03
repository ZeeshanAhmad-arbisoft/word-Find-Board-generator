import sys

def filter_words(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            words = file.read().split()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    except IOError:
        print(f"Error: Unable to read file '{input_file}'.")
        return

    eight_letter_words = [word for word in words if len(word) >= 3]

    try:
        with open(output_file, 'w') as file:
            file.write('\n'.join(eight_letter_words))
        print(f"Filtered words saved to '{output_file}'.")
    except IOError:
        print(f"Error: Unable to write to file '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file output_file")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        filter_words(input_file, output_file)
