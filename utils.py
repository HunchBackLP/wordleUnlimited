from nltk.corpus import words
#import nltk
#nltk.download('words')

FULL_LIST = [word.lower() for word in words.words() if len(word) == 5]