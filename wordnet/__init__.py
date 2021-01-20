import nltk

from wordnet.category import rank_categories
from wordnet.language import detect_language
from wordnet.bag_of_words import bag_words

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
