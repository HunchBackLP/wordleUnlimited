# lol
import string
import keyboard
import random
from selenium.webdriver.common.by import By
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get("https://www.wordleunlimited.com")

with open('words2.txt') as file:
    FULL_LIST = file.readlines()

class Solver:
    
    def __init__(self) -> None:
        self.wordlist = FULL_LIST
        self.word_vector = self.create_word_vector(5)

    def create_word_vector(self, WORD_LENGTH):
        """creates a vector of all possible char combinations
            inspired by: https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python
        """
        return[set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]

    def in_word_vector(self, word) -> bool:
        for letter, vector in zip(word, self.get_word_vector()):
            if letter not in vector:
                return False
        return True

    def test(self) -> None:
        keyboard.write(FULL_LIST[0])
        keyboard.press_and_release("enter")

    def get_wordlist(self) -> list:
        return self.wordlist

    def set_wordlist(self, liste) -> None:
        self.wordlist = liste

    def enter_word(self, word) -> None:
        print(f'DEBUG: {word}')
        keyboard.write(word)
        
    def press_key(self, key:str) -> None:
        keyboard.press_and_release(key)

    def solve(self) -> None:
        for i in range(6):
            if self.is_solved():#
                print('SOLVED!')
                break
            else:
                print(f'Guess {i + 1}')
                word = self.get_word()
                self.enter_word(word)
                keyboard.wait('ctrl')
                self.press_key('enter')
                self.filter_list()
                #print(self.get_word_vector())
        driver.quit()

    def get_current_row(self) -> list:
        """Returns the last row with filled characters"""
        return driver.find_elements(by=By.CLASS_NAME, value="RowL.RowL-locked-in")[-1]

    def get_letter_and_hints(self) -> list:
        divs = self.get_current_row().find_elements(by=By.TAG_NAME, value="div")
        letter = [div.text for div in divs]
        hints = [div.get_attribute('class') for div in divs]
        #print(f'DEBUG: Letters: {letter}, Hints: {hints}')
        return letter, hints


    def filter_list(self) -> None:
        letter, hints = self.get_letter_and_hints()
        index = 0
        for l, h in zip(letter, hints):
            # If letter is not in word filter wordx containing said letter
            if h == 'RowL-letter letter-absent':
                for vector in self.get_word_vector():
                    try:
                        vector.remove(str(l).lower())
                    # if char was already removed e.g. "marry" -> two 'r' skip this letter
                    except KeyError:
                        pass
                #print(f'{self.get_wordlist_length()}, Letter: {str(l).lower()}, Mode: {h}')
            # If letter is correct remove words not having said letter in correct position
            if h == 'RowL-letter letter-correct':
                self.set_word_vector(index, set(str(l).lower()))
                #print(f'{self.get_wordlist_length()}, Letter: {str(l).lower()}, Mode: {h}')
            if h == 'RowL-letter letter-elsewhere':
                try:
                    self.get_word_vector()[index].remove(str(l).lower())
                except KeyError:
                    pass
                #print(f'{self.get_wordlist_length()}, Letter: {str(l).lower()}, Mode: {h}')
            index = index + 1
        self.update_wordlist()
        print(f'Valid words: {self.get_wordlist_length()}')
        print('________________________________________________')

    def get_word_vector(self):
        return self.word_vector

    def set_word_vector(self, index, value):
        self.word_vector[index] = value

    def get_matching_words(self) -> list:
        """returns all words with valid char combinations"""
        return [word for word in self.get_wordlist() if self.in_word_vector(word)]

    def update_wordlist(self) -> None:
        self.set_wordlist(self.get_matching_words())

    def get_word(self):
        try:
            return random.choice(self.get_wordlist())
        except IndexError:
            driver.quit()

    def get_wordlist_length(self) -> int:
        return len(self.get_wordlist())

    def is_solved(self) -> bool:
        count = 0
        for vector in self.get_word_vector():
            if len(vector) == 1:
                count = count + 1
        return count == 5

