import nltk, string, operator
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

class handler:
  def __init__(self, title, text):
    self.Title = title
    self.Text = text
    self._terms = {}
    self._weight = {}
    self.engine()

  def engine(self):
    tokens = word_tokenize(self.Text)
    sw = stopwords.words('english')
    clean_tokens = [token for token in tokens if token not in sw]
    stemmer = PorterStemmer()
    stem_tokens = [stemmer.stem(word) for word in clean_tokens if word not in string.punctuation]
    freq = nltk.FreqDist(stem_tokens)
    self._terms = freq