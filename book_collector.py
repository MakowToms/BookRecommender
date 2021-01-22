import spacy

from sparql.query import QueryExecutor
from wordnet import bag_words, rank_categories, detect_language
from wordnet.category import bag_bag_similarity
from wordnet.detect_hyponym import detect_person, detect_work_of_art

nlp = spacy.load('en_core_web_sm')


def compute_list_score(scores: list):
    result = 1
    for score in scores:
        result *= 1 - score
    return 1 - result


class BookScores:
    def __init__(self, book, score, bag_of_words):
        self.__scores = [score]
        self.book = book
        self.book_relevance = self.score_book_relevance(bag_of_words)
        self.final_score = 0

    def score_book_relevance(self, bag_of_words):
        book_abstract = str(self.book[2])
        abstract_doc = nlp(book_abstract)
        return bag_bag_similarity(bag_words(abstract_doc), bag_of_words)

    def add_score(self, score):
        self.__scores.append(score)

    def compute_score(self):
        """
        Collects scores into one number, where greater value means better score.

        :return: a number in range [0, 10]
        """
        self.final_score = round(10 * self.book_relevance * (compute_list_score(self.__scores)), 2)


class BookCollector:
    def __init__(self, query: str):
        self.doc = nlp(query)
        self.bag_of_words = bag_words(self.doc)
        self.book_scores = dict()

    def assign_score(self, book, score):
        if not self.book_scores.__contains__(str(book[0])):
            self.book_scores[str(book[0])] = BookScores(book, score, self.bag_of_words)
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
        language = languages[0] if len(languages) != 0 else None
        people = detect_person(self.doc)
        people = people if len(people) != 0 else None
        works_of_art = list(detect_work_of_art(self.doc))
        book_name = works_of_art[0] if len(works_of_art) != 0 else None

        category_ranking = rank_categories(self.bag_of_words)

        # find exactly written works of art
        if book_name is not None:
            for book in QueryExecutor.find_books_by_conditions(book_name=book_name):
                self.assign_score(book, 0.5)
            if people is not None:
                for book in QueryExecutor.find_books_by_conditions(people=people, book_name=book_name):
                    self.assign_score(book, 0.8)

        # find books made in language
        if language is not None:
            for book in QueryExecutor.find_books_by_conditions(language=language):
                self.assign_score(book, 0.3)
            if people is not None:
                for book in QueryExecutor.find_books_by_conditions(language=language, people=people):
                    self.assign_score(book, 0.7)

        # find peoples in books
        if people is not None:
            for book in QueryExecutor.find_books_by_conditions(people=people):
                self.assign_score(book, 0.6)

        # Select only top 3 categories
        for category, cat_score in category_ranking[:3]:
            for book in QueryExecutor.find_books_by_conditions(category.categories):
                self.assign_score(book, cat_score)

            if people is not None:
                for book in QueryExecutor.find_books_by_conditions(category.categories, people=people):
                    self.assign_score(book, compute_list_score([0.6,  cat_score]))

            if language is not None:
                for book in QueryExecutor.find_books_by_conditions(category.categories, language=language):
                    self.assign_score(book, compute_list_score([0.3,  cat_score]))
                if people is not None:
                    for book in QueryExecutor.find_books_by_conditions(category.categories, language=language, people=people):
                        self.assign_score(book, compute_list_score([0.7, cat_score]))

        self.compute_final_scores()
        return sorted(self.book_scores.values(), key=lambda v: v.final_score, reverse=True)
