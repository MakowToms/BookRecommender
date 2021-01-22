from math import sqrt
from statistics import mean

from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset

from wordnet.utils import merge_synsets


def synset_similarity(synset1: Synset, synset2: Synset):
    # used with lch_similarity
    # if synset1.pos() != synset2.pos():
    #     return 0
    res = synset1.wup_similarity(synset2)
    return res if res is not None else 0


def word_word_similarity(synset_list1: list, synset_list2: list):
    similarities = [synset_similarity(synset1, synset2) ** 2 for synset1 in synset_list1 for synset2 in synset_list2]
    return sqrt(mean(similarities)) if len(similarities) > 0 else 0


def bag_bag_similarity(bag1, bag2):
    similarities = [word_word_similarity(wn.synsets(word1), wn.synsets(word2)) for word1 in bag1 for word2 in bag2]
    return mean(similarities) if len(similarities) > 0 else 0


class Category:
    categories = dict()

    def __init__(self, labels, *args):
        self.labels = labels
        self.synsets = merge_synsets(args)
        Category.categories[labels[0]] = self

    def word_similarity(self, word: str):
        return word_word_similarity(wn.synsets(word), self.synsets)

    def bag_similarity(self, bag_of_words: set):
        similarities = [self.word_similarity(word) for word in bag_of_words]
        return mean(similarities) if len(similarities) > 0 else 0


def rank_categories(bag_of_words: set):
    return sorted([(category, category.bag_similarity(bag_of_words)) for category in Category.categories.values()],
                  key=lambda x: x[1],
                  reverse=True)


Category(['Science_fiction', 'Science_fantasy', 'Science_Fiction'],
         wn.synsets('science'), wn.synsets('technology'), wn.synsets('robot'), wn.synsets('science_fiction'))
Category(['Thriller_(genre)', 'Thriller_fiction'],
         wn.synsets('authority'), wn.synsets('spy'), wn.synsets('thriller'))
Category(['Horror_fiction', 'Horror_novel'],
         wn.synsets('scary'), wn.synsets('devil'), wn.synsets('undead'), wn.synsets('monster'), wn.synsets('horror'))
Category(['Comedy_(genre)', 'Humor', 'Comic_novel', 'Comedy'],
         wn.synsets('funny'), wn.synsets('laugh'), wn.synsets('comedy'))
Category(['Romance_novel', 'Romantic_suspense'],
         wn.synsets('romance'), wn.synsets('lover'))
Category(['Fantasy', 'Fantasy_novel', 'Fantasy_fiction'],
         wn.synsets('fantasy'), wn.synsets('otherworld'), wn.synsets('magic'), wn.synsets('imaginary'),
         wn.synsets('strange'))
Category(['Adventure_(genre)', 'Adventure_novel'],
         wn.synsets('adventure'), wn.synsets('riddle'))
Category(['Biography'],
         wn.synsets('biography'), wn.synsets('life_story'))
Category(['Crime_fiction', 'Mystery_novel', 'Mystery_fiction', 'Mystery_(fiction)', 'Detective_fiction', 'Crime', 'Crime_novel'],
         wn.synsets('crime'), wn.synsets('mystery'), wn.synsets('detective'), wn.synsets('murder'), wn.synsets('clue'))
Category(['War_novel'],
         wn.synsets('pony'), wn.synsets('war'), wn.synsets('tank'), wn.synsets('rifle'), wn.synsets('soldier'))
