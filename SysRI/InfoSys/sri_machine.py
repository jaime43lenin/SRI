from InfoSys import doc_handle, query, parser, vectorial_framework
import os, math, operator
from nltk.stem import PorterStemmer


class sri_machine:
  def __init__(self):
    self.framework = vectorial_framework.vectorial()
    self.documents = []
    self.querys = []
    self.terms = {}
    self.dict= {}

  def load_data(self):
    os.chdir('/Users/jaime_perez/Documents/School/SRI/SRI/SysRI/corpus/')
    data = [element for element in os.listdir()]
    for d in data:
      file = open(d, 'r', errors='ignore')
      doc = parser.Newsgroup(file)
      self.documents.append(doc_handle.handler(doc[0], doc[1]))
      
      file.close()
    os.chdir("..")
    self.index_inverted()
    self.global_weight()
    self.build_dict()
  def global_weight(self):
    for term in self.terms.keys():
      for doc in self.terms[term]:
        weight = self.framework.weight_doc(self.documents, self.terms, doc, term)
        doc.set_weight(term,weight)

  def index_inverted(self):
    for doc in self.documents:
      for term in doc.get_terms().keys():
        if term in self.terms.keys():
          self.terms[term].append(doc)
        else: self.terms[term] = [doc]
        
  def build_dict(self):
    stemmer = PorterStemmer()
    for term in self.terms.keys():
      stem_term = stemmer.stem(term)
      if stem_term not in self.dict.keys():
        self.dict[stem_term] = [term]
      else: 
        if term not in self.dict[stem_term]: 
          self.dict[stem_term].append(term)
    


  def create_query(self, q):
    return query.query(str(q))

  def query_weight(self, query):
    for term in query.get_terms().keys():
      if term in self.terms.keys():
        weight = self.framework.weight_query(self.documents, self.terms, 0.4, query, term)
        query.set_weight(term, weight)

  def query_response(self, query):
    self.query_weight(query)
    ranking = {}
    
    for doc in self.documents:
      cs = self.framework.sim(doc, query, self.dict)
      if cs > 0.12:
        ranking[doc] = cs
    return sorted(ranking.items(), key=operator.itemgetter(1),reverse=True)