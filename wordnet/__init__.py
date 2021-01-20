import nltk

from wordnet.category import rank_categories
from wordnet.detect_hyponym import detect_language, detect_genre
from wordnet.bag_of_words import bag_words

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
