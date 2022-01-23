from django.shortcuts import render
from . import sri_machine
from django.views.generic.base import TemplateView

class Home(TemplateView):
  template_name = 'home.html'
  machine = sri_machine.sri_machine()
  machine.load_data()
  def get(self,request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

  def post(self,request, *args, **kwargs):
    query = request.POST['query']
    q = self.machine.create_query(query)
    ranking = self.machine.query_response(q)
    data = [i[0].Title for i in ranking]
    return render(request, 'home.html',{'data': data})

