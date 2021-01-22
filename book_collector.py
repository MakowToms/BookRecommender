import spacy

from sparql.query import QueryExecutor
from wordnet import bag_words, rank_categories, detect_language
from wordnet.category import Category
from wordnet.detect_hyponym import detect_person

nlp = spacy.load('en_core_web_sm')


def score_book_relevance(book):
    # TODO: make it a little bit better maybe?
    return 1


def find_by_conditions(category: Category, language: str, people: set):
    """
    Manages calling proper function to make query to DBpedia and computing relevance scores of results.

    :param category: possible genre properties of book ontology
    :param language: expected language of a book
    :param people: possible people (fictional or not) related to a book
    :return: a tuple of book ontology data and its score
    """
    books = QueryExecutor.find_books_by_conditions(category.labels, language=language, people=people)
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
        if not self.book_scores.__contains__(str(book[0])):
            self.book_scores[str(book[0])] = BookScores(book, score)
        else:
            self.book_scores[str(book[0])].add_score(score)

    def compute_final_scores(self):
        for key in self.book_scores.keys():
            self.book_scores[key].compute_score()

    def collect(self):
        """
        Takes care of all possible cases, depending on entities found in query.

        :return: list of book URIs and names sorted by some metric
        """
        languages = list(detect_language(self.bag_of_words))
        people = detect_person(self.doc)

        category_ranking = rank_categories(self.bag_of_words)
        # Select only top 3 categories
        for category, cat_score in category_ranking[:3]:
            for book, book_score in find_by_conditions(category,
                                                       languages[0] if len(languages) != 0 else None,
                                                       people if len(people) != 0 else None):
                self.assign_score(book, cat_score * book_score)
        self.compute_final_scores()
        return sorted(self.book_scores.values(), key=lambda v: v.final_score, reverse=True)
