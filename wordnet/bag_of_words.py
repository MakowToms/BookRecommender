from nltk.corpus import stopwords
import re

stop_words = set(stopwords.words('english'))


def bag_words(text):
    text = re.sub(r'[^\w\'\s]', '', text)
    words = re.split(r'[\'\s]', text)
    return [word for word in words if word.lower() not in stop_words]
