import spacy

from sparql.query import QueryExecutor
from wordnet import bag_words, rank_categories
from wordnet.category import Category

nlp = spacy.load('en_core_web_sm')


def score_book_relevance(book):
    # TODO: make it a little bit better maybe?
    return 1


def find_by_category(category: Category):
    """
    Manages calling proper function to make query to DBpedia and computing relevance scores of results.

    :param category: possible genre properties of book ontology
    :return: a tuple of book ontology data and its score
    """
    books = QueryExecutor.find_books_for_genre(category.labels)
    return [(book, score_book_relevance(book)) for book in books]


class BookScores:
    def __init__(self, book, score):
        self.__scores = [score]
        self.book = book
        self.final_score = 0

    def add_score(self, score):
        self.__scores.append(score)

    def compute_score(self):
        """
        Collects scores into one number, where greater value means better score.

        :return: a number in range [0, 1]
        """
        self.final_score = 1
        for score in self.__scores:
            self.final_score *= 1 - score
        self.final_score = 1 - self.final_score


class BookCollector:
    def __init__(self, query: str):
        self.doc = nlp(query)
        self.bag_of_words = bag_words(self.doc)
        self.book_scores = dict()

    def assign_score(self, book, score):
        if not self.book_scores[str(book[0])]:
            self.book_scores[str(book[0])] = BookScores(score, book)
        else:
            self.book_scores[str(book[0])].add_score(score)

    def compute_final_scores(self):
        for book in self.book_scores.keys():
            self.book_scores[book] = self.book_scores[book].compute_score()

    def collect(self):
        """
        Takes care of all possible cases, depending on entities found in query.

        :return: list of book URIs and names sorted by some metric
        """
        category_ranking = rank_categories(self.bag_of_words)
        # Select only top 3 categories
        for category, cat_score in category_ranking[:3]:
            for book, book_score in find_by_category(category):
                self.assign_score(book, cat_score * book_score)
        self.compute_final_scores()
        return sorted(self.book_scores.values(), key=lambda v: v.final_score, reverse=True)
