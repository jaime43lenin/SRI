from InfoSys import doc_handle, query, parser, vectorial_framework
import os, math, operator



class sri_machine:
  def __init__(self):
    self.documents = []
    self.querys = []

  def load_data(self):
    os.chdir('/Users/jaime_perez/Documents/School/SRI/SRI/SysRI/corpus/')
    data = [element for element in os.listdir()]
    for d in data:
      file = open(d, 'r', errors='ignore')
      doc = parser.Newsgroup(file)
      self.documents.append(doc_handle.handler(doc[0], doc[1]))
      file.close()
    os.chdir("..")
  def create_query(self, q):
    return query.query(str(q))

  def query_response(self, query):
    ranking = {}
    
    for doc in self.documents:
      cs = vectorial_framework.vectorial.sim(doc, query)
      if cs > 0.12:
        ranking[doc] = cs
    return sorted(ranking.items(), key=operator.itemgetter(1),reverse=True)