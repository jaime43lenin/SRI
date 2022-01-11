import nltk, string, operator
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


class query:

  def __init__(self, text):
    self.Text = text
    self.Words = {}
    self.Weight = {}
    self.Relevant = []
    self.Not_relevant = []
    self.Engine()

  def engine(self):
    tokens = word_tokenize(self.Text)
    sw = stopwords.words('english')
    clean_tokens = [token for token in tokens if token not in sw]
    stemmer = PorterStemmer()
    stem_tokens = [stemmer.stem(word) for word in clean_tokens if word not in string.punctuation]
    freq = nltk.FreqDist(stem_tokens)
    self._terms = freq

  