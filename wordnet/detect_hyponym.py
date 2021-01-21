from nltk.corpus import wordnet as wn


def _detect_hyponym(word, condition_synset):
    # Cannot use natural_language.n.01, because one might want a book in esperanto
    # Excluding programming languages, though
    comparison_target = wn.synset(condition_synset)
    found = any([comparison_target in synset.closure(lambda x: x.hypernyms(), depth=99) for synset in wn.synsets(word)])
    return found, word


def detect_hyponym(bag_of_words, condition_synset):
    languages = set()
    for word in bag_of_words:
        found, language = _detect_hyponym(word, condition_synset)
        if found:
            languages.add(language)
    return languages


def detect_language(bag_of_words):
    return detect_hyponym(bag_of_words, 'language.n.01') - detect_hyponym(bag_of_words, 'programming_language.n.01')


def detect_genre(bag_of_words):
    return detect_hyponym(bag_of_words, 'literary_composition.n.01')


def detect_person(doc):
    return {ent.lemma_ for ent in doc.ents if ent.label_ == 'PERSON'}
