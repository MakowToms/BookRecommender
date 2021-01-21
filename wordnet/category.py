from statistics import mean

from nltk.corpus import wordnet as wn

from wordnet.utils import merge_synsets


def similarity(synset1, synset2):
    # used with lch_similarity
    # if synset1.pos() != synset2.pos():
    #     return 0
    res = synset1.wup_similarity(synset2)
    return res if res is not None else 0


class Category:
    categories = dict()

    def __init__(self, label, *args):
        self.label = label
        self.synsets = merge_synsets(args)
        Category.categories[label] = self

    def word_similarity(self, word):
        similarities = [similarity(synset1, synset2) for synset1 in wn.synsets(word) for synset2 in self.synsets]
        return max(similarities) if len(similarities) > 0 else 0

    def bag_similarity(self, bag_of_words):
        similarities = [self.word_similarity(word) for word in bag_of_words]
        return mean(similarities) if len(similarities) > 0 else 0


def rank_categories(bag_of_words):
    return sorted([(label, category.bag_similarity(bag_of_words)) for label, category in Category.categories.items()],
                  reverse=True)


Category('crime', wn.synsets('crime'))
Category('love', wn.synsets('love'))
Category('comedy', wn.synsets('comedy'), wn.synsets('fun'), wn.synsets('laugh'))
