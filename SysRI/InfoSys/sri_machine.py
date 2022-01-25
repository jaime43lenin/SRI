from re import L
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
    self.last_query = None
    self.last_ranking = []

  def get_documents(self): return self.documents
  def get_last_query(self): return self.last_query
  def get_last_ranking(self): return self.last_ranking

  def set_last_query(self, query): self.last_query = query
  def set_last_ranking(self, ranking): self.last_ranking = ranking

  def load_data(self):
    os.chdir('./corpus/')
    data = [element for element in os.listdir()]
    id = 0
    for d in data:
      id += 1
      file = open(d, 'r', errors='ignore')
      doc = parser.Newsgroup(file)
      self.documents.append(doc_handle.handler(doc[0], doc[1], id))
      
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
      if doc not in ranking: cs = self.framework.sim(doc, query, self.dict)
      if cs > 0.1:
        ranking[doc] = cs
    return sorted(ranking.items(), key=operator.itemgetter(1),reverse=True)

  def rocchio(self, old_q, a , b, c, relevants, not_relevants):
    new_q = self.create_query(old_q.get_text())
    self.query_weight(new_q)
    for t in new_q.get_weight().keys():
      new_q.set_weight(t, a * old_q.get_weight()[t])
        
    for d in relevants:
      for t in d.get_weight().keys():
        if t in new_q.get_weight().keys():
          new_q.set_weight(t, new_q.get_weight()[t] + d.get_weight()[t]*(b/len(relevants)))
        else:
           new_q.set_weight(t, d.get_weight()[t])
            
      for d in not_relevants:
        for t in d.get_weight().keys():
          if t in new_q.get_weight().keys():
            new_q.set_weight(t, new_q.get_weight()[t] - d.get_weight()[t]*(c/len(not_relevants)))
          else:
           new_q.set_weight(t, d.get_weight()[t])

    return new_q  