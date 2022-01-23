import numpy as np 
import math as m 
from . import doc_handle, query
from nltk.stem import PorterStemmer
class vectorial:
  def tf(self, doc: doc_handle.handler, term):
    if term in doc.get_terms():
      freq = doc.get_terms()[term]
      freq_max = doc.get_terms().most_common(1)[0][1]
      return freq/freq_max

  def idf(self, n , N):
    return m.log(N/n)

  def weight_query(self, docs, terms, a, q, t):
    tf = self.tf(q, t)
    idf = self.idf(len(terms[t]), len(docs))
    return (a + (1-a)*(tf)) * idf
  
  def weight_doc(self, docs, terms, d, t):
    return self.idf(len(terms[t]), len(docs)) * self.tf(d, t)
  
  def sim(self, d: doc_handle.handler, q: query.query, dict):
    weight = 0
    sum_d, sum_q = 0, 0
    for t in q.get_weight().keys():
      w_q = q.get_weight()[t]
      if t in d.get_weight().keys():
        w_d = d.get_weight()[t]
        weight += w_d * w_q
      else:
        stemmer = PorterStemmer()
        for synonymous in dict[stemmer.stem(t)]:
          if synonymous in d.get_weight().keys():
            w_d = d.get_weight()[synonymous]
            weight += w_d * w_q * 0.50
    vec_d, vec_q = list(d.get_weight().values()), list(q.get_weight().values())
    sum_d = np.linalg.norm(vec_d)
    sum_q = np.linalg.norm(vec_q)
            
    return weight/(sum_d * sum_q)

