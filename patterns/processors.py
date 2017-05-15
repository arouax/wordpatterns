import pickle
import os
from django.conf import settings

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

skeletondict_ru = pickle.load(
    open(os.path.join(settings.BASE_DIR,
                      'patterns/resources/skeletondict_ru_1.pickle'), 'rb'))

skeletondict_ru_extra = pickle.load(
    open(os.path.join(settings.BASE_DIR,
                      'patterns/resources/skeletondict_ru_2.pickle'), 'rb'))

skeletondict_ru.update(skeletondict_ru_extra)

skeletondict_en = pickle.load(
    open(os.path.join(settings.BASE_DIR,
                      'patterns/resources/skeletondict_en.pickle'), 'rb'))

def skeletonize(word):
    """
    Creates a skeleton of a given word: "dad" becomes "aba", "molecula" becomes
    "abcdefbg", "abba" stays "abba".
    """
    if not isinstance(word, str):
        return False
    worddict = {}
    n = 0
    skeleton = ''
    for letter in word.lower():
        if letter not in worddict:
            worddict[letter] = alphabet[n]
            n += 1
        skeleton += worddict[letter]
    return skeleton

def get_matches(word, lang='ru'):
    if not isinstance(word, str) or ' ' in word:
        return ['Bad input']
    if lang == 'en':
        skeletondict = skeletondict_en
    else:
        skeletondict = skeletondict_ru
    if skeletonize(word) in skeletondict:
        result = []
        for item in skeletondict[skeletonize(word)]:
            result.append(item)
    else:
        result = []
    return result


def mask_match(maskword, word):
    """ Returns true if word ("abba") matches mask ("*b**")"""
    print('Checking ' + word)
    for position, letter in enumerate(maskword):
        if letter != '*' and letter != word[position]:
            print('Returning false')
            return False
    return True
