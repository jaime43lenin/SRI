import nltk, string, operator

from nltk import stem
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

class handler:
  def __init__(self, title, text, id):
    self.id = id
    self.Title = title
    self.Text = text
    self.terms = {}
    self.weight = {}
    self.engine()

  def get_id(self): return self.id
  def get_title(self): return self.Title
  def get_text(self): return self.Text
  def get_terms(self): return self.terms
  def get_weight(self): return self.weight


  def set_Title(self, title):
    self.Title = title

  def set_Text(self, text):
    self.Text = text
  
  def set_weight(self, term, weight):
    self.weight[term] = weight

  def engine(self):
    tokens = word_tokenize(self.Text)
    sw = stopwords.words('english')
    clean_tokens = [token for token in tokens if token not in sw]
    stem_tokens = [word.lower() for word in clean_tokens if word not in string.punctuation]
    freq = nltk.FreqDist(stem_tokens)
    self.terms = freq
