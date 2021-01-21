import re


def merge_synsets(list_of_lists):
    res = set()
    res.update(*list_of_lists)
    return res


def whitespace_to_underscores(word_chunks):
    return {re.sub(r'\w+', r'_', chunk.lemma_) for chunk in word_chunks}
