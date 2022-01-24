import nltk, string, operator
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


class query:

  def __init__(self, text):
    self.Text = text
    self.terms = {}
    self.Weight = {}
    self.Relevant = []
    self.Not_relevant = []
    self.engine()

  def get_weight(self): return self.Weight
  def get_terms(self): return self.terms
  def get_text(self): return self.Text
  def set_weight(self, term, value):
    self.Weight[term] = value

  def engine(self):
    tokens = word_tokenize(self.Text)
    sw = stopwords.words('english')
    clean_tokens = [token for token in tokens if token not in sw]
    stem_tokens = [word for word in clean_tokens if word not in string.punctuation]
    freq = nltk.FreqDist(stem_tokens)
    self.terms = freq

  