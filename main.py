import pyautogui
import time

with open('words.txt', 'r') as file:
    words = file.readlines()


words = []
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

print("You have 5 seconds to focus on the textbox")
time.sleep(5)

for word in filtered_words:
    pyautogui.write(word)  
    pyautogui.press('enter')  