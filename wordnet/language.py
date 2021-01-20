from nltk.corpus import wordnet as wn


def _detect_language(word):
    # Cannot use natural_language.n.01, because one might want a book in esperanto
    # Excluding programming languages, though
    found = any([wn.synset('language.n.01') in synset.closure(lambda x: x.hypernyms(), depth=99) for synset in wn.synsets(word)]) and\
        not any([wn.synset('programming_language.n.01') in synset.closure(lambda x: x.hypernyms(), depth=99) for synset in wn.synsets(word)])
    return found, word


def detect_language(bag_of_words):
    languages = set()
    for word in bag_of_words:
        found, language = _detect_language(word)
        if found:
            languages.add(language)
    return languages
