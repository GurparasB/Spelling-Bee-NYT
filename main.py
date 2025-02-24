import pyautogui
import time
import random
import keyboard

def spelling_bee():
    with open('words.txt', 'r') as file:
        words = file.readlines()

    s = sorted(word.strip().lower() for word in words)

    main_letter_input = input('Enter main letter: ').lower()
    main_letter = [main_letter_input]

    letters = []
    for i in range(6):
        letter = input(f'Enter letter {i + 1}: ').lower()
        letters.append(letter)

    all_letters = set(letters)
    all_letters.add(main_letter[0])  

    def is_valid_word(word):
        return word.isalpha() and len(word) >= 4 and not word[0].isupper()

    filtered_words = [
        word for word in s
        if (main_letter[0] in word and
            is_valid_word(word) and     
            all(l in all_letters for l in word))  
    ]

    print(f'Filtered Words: {filtered_words}')
    print("You have 5 seconds to focus on the textbox. Press '1' to stop at any time.")
    
    time.sleep(5)

    for word in filtered_words:
        if keyboard.is_pressed('1'):  # Stop if '1' is pressed
            print("Stopping the script.")
            break
        pyautogui.write(word)  
        pyautogui.press('enter') 


def wordle():
    try:
        with open('wordle.txt', 'r') as file:
            word_list = [line.strip() for line in file.readlines()]
        print(f"Loaded {len(word_list)} words from wordle.txt")  
    except FileNotFoundError:
        print("Error: wordle.txt file not found.")
        return

    def filter_words(guess, feedback, word_list):
        possible_words = []
        excluded_letters = set()  # Letters that must not appear anywhere
        required_letters = {}  # Letters that must appear, but in a different position

        # Step 1: Identify excluded and required letters
        for i in range(len(guess)):
            letter = guess[i]
            if feedback[i] == 'x':  # Gray (letter must NOT be in the word at all)
                if letter not in required_letters:  # Only exclude if it's not yellow elsewhere
                    excluded_letters.add(letter)
            elif feedback[i] == 'y':  # Yellow (letter is present but in a different position)
                required_letters.setdefault(letter, []).append(i)
            elif feedback[i] == 'g':  # Green (letter must be in this exact position)
                required_letters.setdefault(letter, []).append(i)

        # Step 2: Filter words based on these rules
        for word in word_list:
            valid = True
            for i in range(len(guess)):
                letter = guess[i]
                if feedback[i] == 'g':  # Green - must be exactly here
                    if word[i] != letter:
                        valid = False
                        break
                elif feedback[i] == 'y':  # Yellow - must be present but NOT here
                    if letter not in word or word[i] == letter:
                        valid = False
                        break
                elif feedback[i] == 'x':  # Gray - must NOT be anywhere
                    if letter in word:
                        valid = False
                        break
        
            # Ensure all required letters are present (from yellow/green hints)
            for required_letter, positions in required_letters.items():
                if required_letter not in word:
                    valid = False
                    break
                if all(word[pos] == required_letter for pos in positions):  # Yellow rule violation
                    valid = False
                    break
        
            if valid:
                possible_words.append(word)

        return possible_words

    def wordle_guess():
        word_of_the_day = random.choice(word_list).strip()

        print("Welcome to Wordle helper!")
        print("You have to guess the 5-letter word.")
        
        while True:
            guess = input("Enter your guess word (5 letters): ").lower()

            if len(guess) != 5 or not guess.isalpha():
                print("Please enter a valid 5-letter word.")
                continue

            if guess == word_of_the_day:
                print("Congratulations! You guessed the correct word!")
                break

            feedback = input("Enter feedback (g = green, y = yellow, x = gray): ").lower()

            if len(feedback) != 5 or any(c not in 'gyx' for c in feedback):
                print("Invalid feedback. Please use 'g', 'y', and 'x' for the feedback.")
                continue

            possible_words = filter_words(guess, feedback, word_list)

            if possible_words:
                print("Possible next guesses: ")
                for word in possible_words:
                    print(word) 
            else:
                print("No valid words found, double-check your feedback.")

    wordle_guess()


def main():
    while True:
        que = input('Enter the game name (spelling bee(1) or wordle(2)): ').strip().lower()

        if que == 'spelling bee' or que == "1":
            spelling_bee()
            break  
        elif que == 'wordle' or que == "2":
            wordle()
            break  
        else:
            print("Invalid input. Please enter 'spelling bee' or 'wordle'.")


if __name__ == "__main__":
    main()
