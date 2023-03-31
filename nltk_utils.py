import nltk
nltk.download('punkt')

import numpy as np


from nltk.stem.porter import PorterStemmer


stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    tokenized_sentence = ["hello", "how", "are", "you"]
    all_words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    
    """
    tokenized_sentence = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)

    for index, word in enumerate(all_words):
        if word in tokenized_sentence:
            bag[index] = 1.0

    return bag