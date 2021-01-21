from wordnet.utils import whitespace_to_underscores


def bag_words(doc):
    return {word.lemma_ for word in doc if word.is_alpha and not word.is_stop}.union(
        whitespace_to_underscores(doc.noun_chunks))
