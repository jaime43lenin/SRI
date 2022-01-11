import numpy as np 
import math as m 
import doc_handle
class vectorial:
  def tf(self, doc: doc_handle.handler, term):
    if term in doc._terms:
      freq = doc._terms[term]
      freq_max = doc._terms.most_common(1)[0][1]
      return freq/freq_max

  def idf(self, n , N):
    return m.log(N/n)

  def weight_query(self, docs, terms, a, q, t):
    freq = q._term(t)
    freq_m = q._terms.most_common(1)[0][1]
    return (a + (1-a)*(freq/freq_m)) * self.idf(len(terms[t][1]), len(docs))
  
  def weight_doc(self, docs, terms, d, t):
    return self.idf(len(terms[t][1]), len(docs)) * self.tf(d, t)
  
  def sim(self, d, q):
    weight = 0
    sum_d, sum_q = 0, 0
    for t in q.get_weights().keys():
      if t in d.get_weights().keys():
        w_d = d.get_weight(t)
        w_q = q.get_weight(t)
        weight += w_d * w_q
    vec_d, vec_q = list(d.get_weights().values()), list(q.get_weights().values())
    sum_d = np.linalg.norm(vec_d)
    sum_q = np.linalg.norm(vec_q)
            
    return weight/(sum_d * sum_q)

