from django.shortcuts import render
from . import sri_machine
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

machine = sri_machine.sri_machine()
machine.load_data()
class Home(TemplateView):
  template_name = 'home.html'
  def get(self,request, *args, **kwargs):
    return super().get(request, *args, **kwargs)

  def post(self,request, *args, **kwargs):
    if 'query' in request.POST:
      query = request.POST['query']
      q = machine.create_query(query)
      machine.set_last_query(q)
      ranking = machine.query_response(q)
      machine.set_last_ranking(ranking)
      data = [doc[0].get_title() + '  id: ' + str(doc[0].get_id()) for doc in ranking]
      
      return render(request, 'home.html',{'data': data})
    if 'id' in request.POST:
      id = request.POST['id']
      doc = 0
      for d in machine.get_documents():
        if d.get_id() == int(id):
          doc = d
          break
      relevants = [doc]
      not_relevants = [machine.get_last_ranking().pop()[0]]
      new_query = machine.rocchio(machine.get_last_query(), 1, 0.75, 0.15, relevants, not_relevants) 
      machine.set_last_query(new_query)
      ranking = machine.query_response(new_query)
      machine.set_last_ranking(ranking)
      data = [doc[0].get_title() + '  id: ' + str(doc[0].get_id()) for doc in ranking[1:6]]
      return render(request, 'selected.html', {'data': data, 'Title': doc.get_title(), 'Text': doc.get_text()})

class Selected(TemplateView):
  template_name = 'selected.html'
  def get(self,request, *args, **kwargs):
    return super().get(request, *args, **kwargs)

  def post(self,request, *args, **kwargs):
    data = {}
    return render(request, 'selected.html', data)